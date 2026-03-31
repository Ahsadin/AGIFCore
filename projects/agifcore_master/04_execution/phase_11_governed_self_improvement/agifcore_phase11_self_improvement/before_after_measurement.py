from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    BeforeAfterMeasurementRecord,
    BeforeAfterMeasurementSnapshot,
    MAX_MEASUREMENT_PAIRS,
    MAX_SUPPORTING_REFS,
    clamp_score,
    optional_bounded_unique,
    require_schema,
    stable_hash_payload,
)


class BeforeAfterMeasurementEngine:
    SCHEMA = "agifcore.phase_11.before_after_measurement.v1"

    def build_snapshot(self, *, shadow_evaluation_state: Mapping[str, Any]) -> BeforeAfterMeasurementSnapshot:
        evaluations = require_schema(
            shadow_evaluation_state,
            "agifcore.phase_11.shadow_evaluation.v1",
            "shadow_evaluation_state",
        )
        conversation_id = str(evaluations.get("conversation_id"))
        turn_id = str(evaluations.get("turn_id"))
        measurements: list[BeforeAfterMeasurementRecord] = []
        for evaluation in list(evaluations.get("evaluations", ()))[:MAX_MEASUREMENT_PAIRS]:
            if not isinstance(evaluation, Mapping):
                continue
            proposal_id = str(evaluation.get("proposal_id", "")).strip()
            baseline_metric = float(evaluation.get("baseline_score", 0.0))
            adopted_metric = float(evaluation.get("candidate_score", 0.0))
            rollback_metric = baseline_metric
            improvement = clamp_score(adopted_metric - baseline_metric)
            pass_threshold_met = bool(evaluation.get("ready_for_measurement", False)) and improvement >= 0.05
            payload = {
                "proposal_id": proposal_id,
                "baseline_metric": baseline_metric,
                "adopted_metric": adopted_metric,
                "rollback_metric": rollback_metric,
                "improvement": improvement,
                "pass_threshold_met": pass_threshold_met,
            }
            measurements.append(
                BeforeAfterMeasurementRecord(
                    measurement_id=f"measurement::{proposal_id}",
                    proposal_id=proposal_id,
                    baseline_metric=baseline_metric,
                    adopted_metric=adopted_metric,
                    rollback_metric=rollback_metric,
                    improvement=improvement,
                    pass_threshold_met=pass_threshold_met,
                    supporting_refs=optional_bounded_unique(
                        [
                            str(evaluation.get("evaluation_id", "")).strip(),
                            *list(evaluation.get("supporting_refs", ())),
                        ],
                        ceiling=MAX_SUPPORTING_REFS,
                    ),
                    measurement_hash=stable_hash_payload(payload),
                )
            )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "measurement_ids": [measurement.measurement_id for measurement in measurements],
        }
        return BeforeAfterMeasurementSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            pair_count=len(measurements),
            measurements=tuple(measurements),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
