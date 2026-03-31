from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    DecisionState,
    MAX_MONITORING_ITEMS,
    MAX_SUPPORTING_REFS,
    MonitoringStatus,
    PostAdoptionMonitoringRecord,
    PostAdoptionMonitoringSnapshot,
    optional_bounded_unique,
    require_schema,
    stable_hash_payload,
)


class PostAdoptionMonitoringEngine:
    SCHEMA = "agifcore.phase_11.post_adoption_monitoring.v1"

    def build_snapshot(
        self,
        *,
        adoption_or_rejection_pipeline_state: Mapping[str, Any],
        before_after_measurement_state: Mapping[str, Any],
    ) -> PostAdoptionMonitoringSnapshot:
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
        monitoring_items: list[PostAdoptionMonitoringRecord] = []
        for decision in list(adoption.get("decisions", ()))[:MAX_MONITORING_ITEMS]:
            if not isinstance(decision, Mapping):
                continue
            if str(decision.get("decision", "")).strip() != DecisionState.ADOPTED.value:
                continue
            proposal_id = str(decision.get("proposal_id", "")).strip()
            measurement = measurement_by_proposal.get(proposal_id, {})
            payload = {
                "proposal_id": proposal_id,
                "monitoring_window": "3 governed cycles",
                "trigger_threshold": "drop below baseline or lose rollback fidelity",
                "current_status": MonitoringStatus.ACTIVE.value,
            }
            monitoring_items.append(
                PostAdoptionMonitoringRecord(
                    monitoring_id=f"monitoring::{proposal_id}",
                    proposal_id=proposal_id,
                    monitoring_window="3 governed cycles",
                    trigger_threshold="drop below baseline or lose rollback fidelity",
                    current_status=MonitoringStatus.ACTIVE,
                    escalation_action="rollback if the adopted metric falls back to baseline or lower",
                    supporting_refs=optional_bounded_unique(
                        [
                            str(decision.get("decision_id", "")).strip(),
                            str(measurement.get("measurement_id", "")).strip(),
                        ],
                        ceiling=MAX_SUPPORTING_REFS,
                    ),
                    monitoring_hash=stable_hash_payload(payload),
                )
            )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": str(adoption.get("conversation_id")),
            "turn_id": str(adoption.get("turn_id")),
            "monitoring_ids": [item.monitoring_id for item in monitoring_items],
        }
        return PostAdoptionMonitoringSnapshot(
            schema=self.SCHEMA,
            conversation_id=str(adoption.get("conversation_id")),
            turn_id=str(adoption.get("turn_id")),
            monitoring_count=len(monitoring_items),
            items=tuple(monitoring_items),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
