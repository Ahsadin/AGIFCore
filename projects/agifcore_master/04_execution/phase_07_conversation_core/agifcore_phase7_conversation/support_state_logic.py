from __future__ import annotations

from .contracts import (
    KnowledgeGapReason,
    NextAction,
    Phase7ConversationError,
    SupportState,
    SupportStateResolution,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)


class SupportStateError(Phase7ConversationError):
    """Raised when support-state routing violates the Phase 7 contract."""


def _latest_memory_review_ref(memory_review_state: dict[str, object]) -> str:
    candidates = list(memory_review_state.get("candidates", []))
    approved = [require_mapping(item, "review_candidate") for item in candidates if item.get("status") == "approved"]
    if approved:
        return require_non_empty_str(approved[-1].get("review_ref"), "review_ref")
    return "memory-review:none"


def _selected_domain_ids(
    *,
    question_interpretation: dict[str, object],
    support_selection_result: dict[str, object],
    world_model_state: dict[str, object],
) -> list[str]:
    if question_interpretation.get("target_domain_hint"):
        return [str(question_interpretation["target_domain_hint"])]
    selected_candidate_ids = list(support_selection_result.get("selected_candidate_ids", []))
    if not selected_candidate_ids:
        return []
    domains: list[str] = []
    entities = [require_mapping(item, "world_entity") for item in world_model_state.get("entities", [])]
    for candidate_id in selected_candidate_ids:
        _, _, source_id = candidate_id.partition("::")
        for entity in entities:
            if entity.get("target_domain") and (
                str(entity.get("entity_id", "")).endswith(source_id)
                or source_id in list(entity.get("source_refs", []))
            ):
                domain = str(entity.get("target_domain"))
                if domain not in domains:
                    domains.append(domain)
    return domains


def _simulation_trace_ref(selected_domains: list[str], what_if_simulation_state: dict[str, object]) -> str:
    entries = [require_mapping(item, "simulation_entry") for item in what_if_simulation_state.get("entries", [])]
    for entry in entries:
        if selected_domains and str(entry.get("target_domain")) not in selected_domains:
            continue
        return require_non_empty_str(entry.get("simulation_entry_id"), "simulation_entry_id")
    return require_non_empty_str(what_if_simulation_state.get("snapshot_hash"), "snapshot_hash")


def _has_domain_conflict(selected_domains: list[str], conflict_lane_state: dict[str, object]) -> bool:
    if not selected_domains:
        return False
    entries = [require_mapping(item, "conflict_entry") for item in conflict_lane_state.get("entries", [])]
    for entry in entries:
        if bool(entry.get("fail_closed")):
            return True
        for result in entry.get("results", []):
            result_map = require_mapping(result, "conflict_result")
            if str(result_map.get("conflicting_domain")) in selected_domains and str(result_map.get("outcome")) != "clear":
                return True
    return False


class SupportStateEngine:
    """Route interpreted questions to governed support-state outcomes."""

    def build_resolution(
        self,
        *,
        question_interpretation_state: dict[str, object],
        continuity_memory_state: dict[str, object],
        memory_review_state: dict[str, object],
        support_selection_result: dict[str, object],
        world_model_state: dict[str, object],
        what_if_simulation_state: dict[str, object],
        conflict_lane_state: dict[str, object],
        usefulness_state: dict[str, object],
    ) -> SupportStateResolution:
        interpretation = require_schema(
            question_interpretation_state,
            "agifcore.phase_07.question_interpretation.v1",
            "question_interpretation_state",
        )
        continuity = require_schema(
            continuity_memory_state,
            "agifcore.phase_04.continuity_memory.v1",
            "continuity_memory_state",
        )
        memory_review = require_schema(
            memory_review_state,
            "agifcore.phase_04.memory_review.v1",
            "memory_review_state",
        )
        world_model = require_schema(world_model_state, "agifcore.phase_06.world_model.v1", "world_model_state")
        simulation = require_schema(
            what_if_simulation_state,
            "agifcore.phase_06.what_if_simulation.v1",
            "what_if_simulation_state",
        )
        conflict_state = require_schema(
            conflict_lane_state,
            "agifcore.phase_06.conflict_lanes.v1",
            "conflict_lane_state",
        )
        usefulness = require_schema(
            usefulness_state,
            "agifcore.phase_06.usefulness_scoring.v1",
            "usefulness_state",
        )
        support_result = require_mapping(support_selection_result, "support_selection_result")

        memory_review_ref = _latest_memory_review_ref(memory_review)
        selected_domains = _selected_domain_ids(
            question_interpretation=interpretation,
            support_selection_result=support_result,
            world_model_state=world_model,
        )
        simulation_trace_ref = _simulation_trace_ref(selected_domains, simulation)
        evidence_refs: list[str] = [memory_review_ref]
        evidence_refs.extend(str(item) for item in support_result.get("selected_candidate_ids", []))
        if selected_domains:
            evidence_refs.extend(selected_domains)
        evidence_refs.append(simulation_trace_ref)

        blocked_refs = [str(item) for item in support_result.get("blocked_candidate_ids", [])[:5]]
        reason_codes: list[str] = []
        usefulness_outcome = str(usefulness.get("overall_outcome"))
        self_knowledge_anchor_count = len(
            [
                item
                for item in continuity.get("anchors", [])
                if "agifcore" in str(item.get("subject", "")).lower() or "self" in str(item.get("continuity_kind", "")).lower()
            ]
        )

        if bool(interpretation.get("self_knowledge_requested")):
            if self_knowledge_anchor_count:
                support_state = SupportState.GROUNDED
                gap_reason = KnowledgeGapReason.NONE
                next_action = NextAction.ANSWER
                reason_codes.append("self_knowledge_supported_by_continuity")
            else:
                support_state = SupportState.UNKNOWN
                gap_reason = KnowledgeGapReason.MISSING_LOCAL_EVIDENCE
                next_action = NextAction.ABSTAIN
                reason_codes.append("self_knowledge_missing_continuity_support")
        elif bool(interpretation.get("live_current_requested")):
            support_state = SupportState.SEARCH_NEEDED
            gap_reason = KnowledgeGapReason.NEEDS_FRESH_INFORMATION
            next_action = NextAction.SEARCH_EXTERNAL
            reason_codes.append("fresh_external_information_required")
        elif bool(interpretation.get("ambiguous_request")):
            support_state = SupportState.UNKNOWN
            gap_reason = KnowledgeGapReason.AMBIGUOUS_REQUEST
            next_action = NextAction.CLARIFY
            reason_codes.append("clarification_required")
        elif _has_domain_conflict(selected_domains, conflict_state):
            support_state = SupportState.UNKNOWN
            gap_reason = KnowledgeGapReason.CONFLICTING_STATE
            next_action = NextAction.ABSTAIN
            reason_codes.append("phase6_conflict_detected")
        elif support_result.get("status") == "blocked":
            support_state = SupportState.UNKNOWN
            gap_reason = KnowledgeGapReason.BLOCKED_BY_POLICY
            next_action = NextAction.ABSTAIN
            reason_codes.append("support_selection_blocked")
        elif support_result.get("status") == "selected" and support_result.get("selected_candidate_ids"):
            any_fail_closed = any(bool(item.get("fail_closed")) for item in simulation.get("entries", []))
            if usefulness_outcome == "qualified" and not any_fail_closed:
                support_state = SupportState.GROUNDED
                gap_reason = KnowledgeGapReason.NONE
                next_action = NextAction.ANSWER
                reason_codes.append("qualified_phase6_usefulness")
            else:
                support_state = SupportState.INFERRED
                gap_reason = KnowledgeGapReason.NONE
                next_action = NextAction.ANSWER
                reason_codes.append("bounded_inference_only")
        elif bool(interpretation.get("local_artifact_requested")):
            support_state = SupportState.SEARCH_NEEDED
            gap_reason = KnowledgeGapReason.MISSING_LOCAL_EVIDENCE
            next_action = NextAction.SEARCH_LOCAL
            reason_codes.append("local_search_path_required")
        else:
            support_state = SupportState.UNKNOWN
            gap_reason = KnowledgeGapReason.MISSING_LOCAL_EVIDENCE
            next_action = NextAction.ABSTAIN
            reason_codes.append("no_grounded_local_support")

        critic_trace_ref = f"critic::{stable_hash_payload({'support_state': support_state.value, 'reason_codes': reason_codes})[:12]}"
        governance_trace_ref = f"governance::{stable_hash_payload({'gap_reason': gap_reason.value, 'next_action': next_action.value})[:12]}"
        payload = {
            "conversation_id": interpretation.get("conversation_id"),
            "turn_id": interpretation.get("turn_id"),
            "support_state": support_state.value,
            "knowledge_gap_reason": gap_reason.value,
            "next_action": next_action.value,
            "selected_domains": selected_domains,
            "evidence_refs": evidence_refs,
        }
        return SupportStateResolution(
            schema="agifcore.phase_07.support_state_logic.v1",
            conversation_id=require_non_empty_str(interpretation.get("conversation_id"), "conversation_id"),
            turn_id=require_non_empty_str(interpretation.get("turn_id"), "turn_id"),
            support_state=support_state,
            knowledge_gap_reason=gap_reason,
            next_action=next_action,
            evidence_refs=tuple(sorted(set(evidence_refs))),
            blocked_refs=tuple(blocked_refs),
            selected_domain_ids=tuple(selected_domains),
            reason_codes=tuple(reason_codes),
            memory_review_ref=memory_review_ref,
            simulation_trace_ref=simulation_trace_ref,
            critic_trace_ref=critic_trace_ref,
            governance_trace_ref=governance_trace_ref,
            resolution_hash=stable_hash_payload(payload),
        )
