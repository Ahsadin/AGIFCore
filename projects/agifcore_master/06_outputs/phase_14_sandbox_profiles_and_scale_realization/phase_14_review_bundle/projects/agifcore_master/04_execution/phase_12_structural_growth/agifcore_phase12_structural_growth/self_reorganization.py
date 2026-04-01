from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    CandidateState,
    MAX_SELF_REORGANIZATION_ACTIONS,
    ReorganizationActionKind,
    SelfReorganizationCandidate,
    SelfReorganizationSnapshot,
    bounded_unique,
    infer_phase12_scenario,
    make_trace_ref,
    require_non_empty_str,
    require_phase11_cycle,
    require_schema,
    stable_hash_payload,
)


class SelfReorganizationEngine:
    SCHEMA = "agifcore.phase_12.self_reorganization.v1"

    def build_snapshot(
        self,
        *,
        phase11_cycle_state: Mapping[str, Any],
        reflection_control_state: Mapping[str, Any],
        curiosity_gap_selection_state: Mapping[str, Any],
    ) -> SelfReorganizationSnapshot:
        cycle = require_phase11_cycle(phase11_cycle_state, "phase11_cycle_state")
        require_schema(
            reflection_control_state,
            "agifcore.phase_12.reflection_control.v1",
            "reflection_control_state",
        )
        require_schema(
            curiosity_gap_selection_state,
            "agifcore.phase_12.curiosity_gap_selection.v1",
            "curiosity_gap_selection_state",
        )
        overlay = cycle["overlay_contract"]
        conversation_id = require_non_empty_str(cycle.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(cycle.get("turn_id"), "turn_id")
        scenario = infer_phase12_scenario(cycle)
        refs = bounded_unique(
            [
                *list(overlay.get("monitoring_refs", ())),
                *list(overlay.get("rollback_refs", ())),
                *list(overlay.get("evidence_refs", ())),
            ],
            ceiling=6,
            field_name="self_reorganization.supporting_refs",
        )
        if scenario == "weak":
            action_kind = ReorganizationActionKind.ROUTE_TUNING
            candidate_state = CandidateState.HELD
            target_structure_ref = "phase03.tissue_manifests::critic_or_error_monitor_review_lane"
            before_state_ref = "phase03.structure.before::single_review_lane"
            after_state_ref = "phase03.structure.after::support_recheck_subroute"
            rationale = "The weak-support case suggests a route split candidate, but structural mutation stays held until contradiction pressure is stronger."
            pressure_score_delta = 0.08
        else:
            action_kind = ReorganizationActionKind.TRANSFER_RESHAPE
            candidate_state = CandidateState.CANDIDATE
            target_structure_ref = "phase03.tissue_manifests::meta_growth_structural_review_lane"
            before_state_ref = "phase03.structure.before::shared_growth_review_lane"
            after_state_ref = "phase03.structure.after::contradiction_boundary_review_lane"
            rationale = "The contradiction case supports one bounded route reshape that separates contradiction repair from downstream adoption review."
            pressure_score_delta = 0.23
        payload = {
            "action_kind": action_kind.value,
            "target_structure_ref": target_structure_ref,
            "before_state_ref": before_state_ref,
            "after_state_ref": after_state_ref,
            "rollback_target": "phase12.rollback::restore_phase11_review_shape",
            "rejected_alternative_ref": "phase12.rejected_alternative::one_giant_growth_engine",
            "rationale": rationale,
            "pressure_score_delta": pressure_score_delta,
            "candidate_state": candidate_state.value,
            "supporting_refs": list(refs[:4]),
        }
        candidate = SelfReorganizationCandidate(
            candidate_id=make_trace_ref("phase12_reorganization", payload),
            action_kind=action_kind,
            target_structure_ref=target_structure_ref,
            before_state_ref=before_state_ref,
            after_state_ref=after_state_ref,
            rollback_target="phase12.rollback::restore_phase11_review_shape",
            rejected_alternative_ref="phase12.rejected_alternative::one_giant_growth_engine",
            rationale=rationale,
            pressure_score_delta=pressure_score_delta,
            candidate_state=candidate_state,
            candidate_hash=stable_hash_payload(payload),
        )
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "candidate_ids": [candidate.candidate_id],
        }
        return SelfReorganizationSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            candidate_count=min(1, MAX_SELF_REORGANIZATION_ACTIONS),
            candidates=(candidate,),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
