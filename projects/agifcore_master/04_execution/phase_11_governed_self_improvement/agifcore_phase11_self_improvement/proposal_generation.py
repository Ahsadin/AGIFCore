from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_PROPOSALS,
    MAX_SUPPORTING_REFS,
    ProposalGenerationSnapshot,
    ProposalRecord,
    make_trace_ref,
    optional_bounded_unique,
    require_non_empty_str,
    require_phase10_turn_state,
    require_schema,
    stable_hash_payload,
)


def _proposal_kind(source_kind: str, problem_statement: str) -> str:
    text = f"{source_kind} {problem_statement}".lower()
    if "contradiction" in text:
        return "contradiction_probe"
    if "missing_variable" in text or "missing_need" in text or "clarify" in text:
        return "clarify_missing_variable"
    if "weak_support" in text or "support" in text:
        return "support_recheck"
    return "explanation_reframe"


def _target_module(proposal_kind: str) -> str:
    if proposal_kind == "contradiction_probe":
        return "shadow_evaluation"
    if proposal_kind == "clarify_missing_variable":
        return "self_experiment_lab"
    if proposal_kind == "support_recheck":
        return "offline_reflection_and_consolidation"
    return "proposal_generation"


class ProposalGenerationEngine:
    SCHEMA = "agifcore.phase_11.proposal_generation.v1"

    def build_snapshot(
        self,
        *,
        offline_reflection_and_consolidation_state: Mapping[str, Any],
        idle_reflection_state: Mapping[str, Any],
        phase10_turn_state: Mapping[str, Any],
    ) -> ProposalGenerationSnapshot:
        reflection = require_schema(
            offline_reflection_and_consolidation_state,
            "agifcore.phase_11.offline_reflection_and_consolidation.v1",
            "offline_reflection_and_consolidation_state",
        )
        require_schema(idle_reflection_state, "agifcore.phase_11.idle_reflection.v1", "idle_reflection_state")
        phase10_turn = require_phase10_turn_state(phase10_turn_state, "phase10_turn_state")
        overlay = phase10_turn["overlay_contract"]
        conversation_id = require_non_empty_str(reflection.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(reflection.get("turn_id"), "turn_id")
        theory_fragments = phase10_turn.get("theory_fragments", {})
        fragment_map = {
            str(item.get("fragment_id", "")).strip(): dict(item)
            for item in list(theory_fragments.get("fragments", ()))
            if isinstance(item, Mapping)
        }

        proposals: list[ProposalRecord] = []
        for item in list(reflection.get("items", ())):
            if not isinstance(item, Mapping) or len(proposals) >= MAX_PROPOSALS:
                continue
            source_kind = str(item.get("source_kind", "weak_signal")).strip()
            problem_statement = " ".join(str(item.get("problem_statement", "")).split()).strip()
            proposal_kind = _proposal_kind(source_kind, problem_statement)
            proposal_id = make_trace_ref(
                "phase11_proposal",
                {
                    "conversation_id": conversation_id,
                    "turn_id": turn_id,
                    "source_kind": source_kind,
                    "proposal_kind": proposal_kind,
                    "problem_statement": problem_statement,
                },
            )
            fragment = next(iter(fragment_map.values()), {})
            falsifier = " ".join(
                str(fragment.get("falsifier") or item.get("problem_statement") or "the candidate does not improve the bounded outcome").split()
            ).strip()
            evidence_needed = " ".join(str(item.get("bounded_next_step", "")).split()).strip() or "collect bounded evidence before adoption"
            rationale = f"Use {source_kind} as a bounded improvement target without mutating Phase 10 truth."
            expected_gain = (
                "improve contradiction handling while preserving support honesty"
                if proposal_kind == "contradiction_probe"
                else "reduce uncertainty by checking the missing variable"
                if proposal_kind == "clarify_missing_variable"
                else "tighten support-state handling before confidence changes"
                if proposal_kind == "support_recheck"
                else "reshape the explanation without pretending stronger support"
            )
            supporting_refs = optional_bounded_unique(
                [
                    *list(item.get("supporting_refs", ())),
                    str(item.get("source_ref", "")).strip(),
                    str(fragment.get("fragment_id", "")).strip(),
                    str(overlay.get("diagnosis_ref", "")).strip(),
                ],
                ceiling=MAX_SUPPORTING_REFS,
            )
            payload = {
                "proposal_id": proposal_id,
                "proposal_kind": proposal_kind,
                "target_module": _target_module(proposal_kind),
                "rationale": rationale,
                "expected_gain": expected_gain,
                "falsifier": falsifier,
                "evidence_needed": evidence_needed,
                "rollback_target": f"rollback::{proposal_id}",
                "supporting_refs": list(supporting_refs),
            }
            proposals.append(
                ProposalRecord(
                    proposal_id=proposal_id,
                    proposal_kind=proposal_kind,
                    target_module=_target_module(proposal_kind),
                    rationale=rationale,
                    expected_gain=expected_gain,
                    falsifier=falsifier,
                    evidence_needed=evidence_needed,
                    rollback_target=f"rollback::{proposal_id}",
                    supporting_refs=supporting_refs,
                    proposal_hash=stable_hash_payload(payload),
                )
            )

        stop_reason = "proposal_budget_reached" if len(list(reflection.get("items", ()))) > len(proposals) else "bounded_proposal_set_ready"
        if not proposals:
            stop_reason = "no_bounded_proposals"
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "proposal_ids": [proposal.proposal_id for proposal in proposals],
            "stop_reason": stop_reason,
        }
        return ProposalGenerationSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            proposal_count=len(proposals),
            proposals=tuple(proposals),
            stop_reason=stop_reason,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
