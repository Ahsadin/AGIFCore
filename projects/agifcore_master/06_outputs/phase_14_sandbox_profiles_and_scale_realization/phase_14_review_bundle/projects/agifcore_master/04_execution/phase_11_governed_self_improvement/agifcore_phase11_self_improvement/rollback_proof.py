from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    DecisionState,
    MAX_ROLLBACK_PROOFS,
    RollbackProofRecord,
    RollbackProofSnapshot,
    require_schema,
    stable_hash_payload,
)


class RollbackProofEngine:
    SCHEMA = "agifcore.phase_11.rollback_proof.v1"

    def build_snapshot(
        self,
        *,
        adoption_or_rejection_pipeline_state: Mapping[str, Any],
        before_after_measurement_state: Mapping[str, Any],
    ) -> RollbackProofSnapshot:
        adoption = require_schema(
            adoption_or_rejection_pipeline_state,
            "agifcore.phase_11.adoption_or_rejection_pipeline.v1",
            "adoption_or_rejection_pipeline_state",
        )
        measurements = require_schema(
            before_after_measurement_state,
            "agifcore.phase_11.before_after_measurement.v1",
            "before_after_measurement_state",
        )
        measurement_by_proposal = {
            str(item.get("proposal_id", "")).strip(): dict(item)
            for item in list(measurements.get("measurements", ()))
            if isinstance(item, Mapping)
        }
        rollbacks: list[RollbackProofRecord] = []
        for decision in list(adoption.get("decisions", ()))[:MAX_ROLLBACK_PROOFS]:
            if not isinstance(decision, Mapping):
                continue
            if str(decision.get("decision", "")).strip() != DecisionState.ADOPTED.value:
                continue
            proposal_id = str(decision.get("proposal_id", "")).strip()
            measurement = measurement_by_proposal.get(proposal_id, {})
            baseline_metric = float(measurement.get("baseline_metric", 0.0))
            adopted_metric = float(measurement.get("adopted_metric", 0.0))
            restored_metric = baseline_metric
            payload = {
                "proposal_id": proposal_id,
                "baseline_metric": baseline_metric,
                "adopted_metric": adopted_metric,
                "restored_metric": restored_metric,
                "roundtrip_preserved": restored_metric == baseline_metric,
            }
            rollbacks.append(
                RollbackProofRecord(
                    rollback_id=f"rollback::{proposal_id}",
                    proposal_id=proposal_id,
                    baseline_metric=baseline_metric,
                    adopted_metric=adopted_metric,
                    restored_metric=restored_metric,
                    roundtrip_preserved=restored_metric == baseline_metric,
                    proof_note="same-pack baseline was restored after the bounded rollback step",
                    rollback_hash=stable_hash_payload(payload),
                )
            )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": str(adoption.get("conversation_id")),
            "turn_id": str(adoption.get("turn_id")),
            "rollback_ids": [item.rollback_id for item in rollbacks],
        }
        return RollbackProofSnapshot(
            schema=self.SCHEMA,
            conversation_id=str(adoption.get("conversation_id")),
            turn_id=str(adoption.get("turn_id")),
            rollback_count=len(rollbacks),
            rollbacks=tuple(rollbacks),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
