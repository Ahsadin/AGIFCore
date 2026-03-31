from __future__ import annotations

from .contracts import (
    AnswerContractSnapshot,
    DiscourseMode,
    KnowledgeGapReason,
    NextAction,
    Phase7ConversationError,
    ResponseSurface,
    SupportState,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)


class AnswerContractError(Phase7ConversationError):
    """Raised when the Phase 7 answer contract is malformed."""


class AnswerContractBuilder:
    """Build the machine-checkable Phase 7 answer envelope."""

    def build(
        self,
        *,
        intake_state: dict[str, object],
        question_interpretation_state: dict[str, object],
        support_state_resolution_state: dict[str, object],
        utterance_plan_state: dict[str, object],
        response_surface: ResponseSurface,
    ) -> AnswerContractSnapshot:
        interpretation = require_schema(
            question_interpretation_state,
            "agifcore.phase_07.question_interpretation.v1",
            "question_interpretation_state",
        )
        support_state = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )
        plan = require_schema(
            utterance_plan_state,
            "agifcore.phase_07.utterance_plan.v1",
            "utterance_plan_state",
        )
        evidence_refs = sorted(
            {
                *[str(item) for item in support_state.get("evidence_refs", [])],
                *list(response_surface.cited_evidence_refs),
            }
        )
        abstain_or_answer = (
            "answer"
            if response_surface.final_answer_mode.value
            in {"grounded_fact", "derived_estimate", "derived_explanation", "hypothesis"}
            else "abstain"
        )
        payload = {
            "conversation_id": intake_state["conversation_id"],
            "turn_id": intake_state["turn_id"],
            "user_intent": interpretation["user_intent"],
            "planner_trace_ref": plan["planner_trace_ref"],
            "simulation_trace_ref": support_state["simulation_trace_ref"],
            "critic_trace_ref": support_state["critic_trace_ref"],
            "governance_trace_ref": support_state["governance_trace_ref"],
            "response_text": response_surface.response_text,
            "abstain_or_answer": abstain_or_answer,
            "memory_review_ref": support_state["memory_review_ref"],
            "discourse_mode": plan["discourse_mode"],
            "support_state": support_state["support_state"],
            "knowledge_gap_reason": support_state["knowledge_gap_reason"],
            "next_action": support_state["next_action"],
            "final_answer_mode": response_surface.final_answer_mode.value,
            "evidence_refs": evidence_refs,
        }
        return AnswerContractSnapshot(
            schema="agifcore.phase_07.answer_contract.v1",
            conversation_id=require_non_empty_str(intake_state["conversation_id"], "conversation_id"),
            turn_id=require_non_empty_str(intake_state["turn_id"], "turn_id"),
            user_intent=require_non_empty_str(interpretation["user_intent"], "user_intent"),
            active_context_refs=tuple(str(item) for item in intake_state.get("active_context_refs", [])),
            planner_trace_ref=require_non_empty_str(plan["planner_trace_ref"], "planner_trace_ref"),
            simulation_trace_ref=require_non_empty_str(support_state["simulation_trace_ref"], "simulation_trace_ref"),
            critic_trace_ref=require_non_empty_str(support_state["critic_trace_ref"], "critic_trace_ref"),
            governance_trace_ref=require_non_empty_str(support_state["governance_trace_ref"], "governance_trace_ref"),
            response_text=response_surface.response_text,
            abstain_or_answer=abstain_or_answer,
            memory_review_ref=require_non_empty_str(support_state["memory_review_ref"], "memory_review_ref"),
            discourse_mode=DiscourseMode(str(plan["discourse_mode"])),
            support_state=SupportState(str(support_state["support_state"])),
            knowledge_gap_reason=KnowledgeGapReason(str(support_state["knowledge_gap_reason"])),
            next_action=NextAction(str(support_state["next_action"])),
            final_answer_mode=response_surface.final_answer_mode,
            evidence_refs=tuple(evidence_refs),
            contract_hash=stable_hash_payload(payload),
        )
