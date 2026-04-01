from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    AdoptionDecisionRecord,
    AdoptionOrRejectionPipelineSnapshot,
    DecisionState,
    MAX_DECISIONS,
    MAX_SUPPORTING_REFS,
    optional_bounded_unique,
    require_phase10_turn_state,
    require_schema,
    stable_hash_payload,
)


class AdoptionOrRejectionPipelineEngine:
    SCHEMA = "agifcore.phase_11.adoption_or_rejection_pipeline.v1"

    def build_snapshot(
        self,
        *,
        proposal_generation_state: Mapping[str, Any],
        before_after_measurement_state: Mapping[str, Any],
        phase10_turn_state: Mapping[str, Any],
    ) -> AdoptionOrRejectionPipelineSnapshot:
        proposals = require_schema(
            proposal_generation_state,
            "agifcore.phase_11.proposal_generation.v1",
            "proposal_generation_state",
        )
        measurements = require_schema(
            before_after_measurement_state,
            "agifcore.phase_11.before_after_measurement.v1",
            "before_after_measurement_state",
        )
        phase10_turn = require_phase10_turn_state(phase10_turn_state, "phase10_turn_state")
        overlay = phase10_turn["overlay_contract"]
        support_state = str(overlay.get("support_state", "unknown")).strip() or "unknown"
        measurement_by_proposal = {
            str(item.get("proposal_id", "")).strip(): dict(item)
            for item in list(measurements.get("measurements", ()))
            if isinstance(item, Mapping)
        }
        decisions: list[AdoptionDecisionRecord] = []
        adopted_once = False
        for proposal in list(proposals.get("proposals", ()))[:MAX_DECISIONS]:
            if not isinstance(proposal, Mapping):
                continue
            proposal_id = str(proposal.get("proposal_id", "")).strip()
            measurement = measurement_by_proposal.get(proposal_id, {})
            pass_threshold_met = bool(measurement.get("pass_threshold_met", False))
            if support_state == "inferred" and pass_threshold_met and not adopted_once:
                decision = DecisionState.ADOPTED
                reason = "candidate improved bounded metrics and rollback is available"
                adopted_once = True
            elif support_state == "search_needed":
                decision = DecisionState.HELD
                reason = "support remains unresolved, so the candidate stays governed but not adopted"
            else:
                decision = DecisionState.REJECTED
                reason = "candidate did not clear the bounded adoption gate"
            payload = {
                "proposal_id": proposal_id,
                "decision": decision.value,
                "reason": reason,
                "rollback_required": decision is DecisionState.ADOPTED,
            }
            decisions.append(
                AdoptionDecisionRecord(
                    decision_id=f"decision::{proposal_id}",
                    proposal_id=proposal_id,
                    decision=decision,
                    reason=reason,
                    rollback_required=decision is DecisionState.ADOPTED,
                    supporting_refs=optional_bounded_unique(
                        [
                            str(measurement.get("measurement_id", "")).strip(),
                            str(proposal.get("rollback_target", "")).strip(),
                            str(overlay.get("diagnosis_ref", "")).strip(),
                        ],
                        ceiling=MAX_SUPPORTING_REFS,
                    ),
                    decision_hash=stable_hash_payload(payload),
                )
            )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": str(proposals.get("conversation_id")),
            "turn_id": str(proposals.get("turn_id")),
            "decision_ids": [decision.decision_id for decision in decisions],
        }
        return AdoptionOrRejectionPipelineSnapshot(
            schema=self.SCHEMA,
            conversation_id=str(proposals.get("conversation_id")),
            turn_id=str(proposals.get("turn_id")),
            decision_count=len(decisions),
            decisions=tuple(decisions),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
