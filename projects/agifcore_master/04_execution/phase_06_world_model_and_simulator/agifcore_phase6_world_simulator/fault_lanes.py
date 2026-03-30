from __future__ import annotations

from typing import Any, Mapping

from .entity_classes import (
    FaultCase,
    FaultLaneEntry,
    FaultLaneSnapshot,
    FaultOutcome,
    build_provenance_bundle,
    canonical_size_bytes,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

MAX_FAULT_STATE_BYTES = 2 * 1024 * 1024


class FaultLanesError(ValueError):
    """Raised when fault-lane overlays violate Phase 6 boundaries."""


class FaultLaneEngine:
    """Apply explicit, read-only fault overlays to simulation entries."""

    def __init__(self, *, max_state_bytes: int = MAX_FAULT_STATE_BYTES) -> None:
        self.max_state_bytes = max_state_bytes

    def build_snapshot(
        self,
        *,
        world_model_state: Mapping[str, Any],
        what_if_simulation_state: Mapping[str, Any],
    ) -> FaultLaneSnapshot:
        world_state = require_schema(world_model_state, "agifcore.phase_06.world_model.v1", "world_model_state")
        simulation_state = require_schema(
            what_if_simulation_state,
            "agifcore.phase_06.what_if_simulation.v1",
            "what_if_simulation_state",
        )
        if simulation_state.get("source_world_model_hash") != world_state.get("snapshot_hash"):
            raise FaultLanesError("fault lanes require a matching world-model snapshot")

        entity_by_id = {
            require_non_empty_str(item.get("entity_id"), "entity_id"): require_mapping(item, "world_entity")
            for item in world_state.get("entities", [])
        }
        entries: list[FaultLaneEntry] = []
        for simulation_payload in simulation_state.get("entries", []):
            simulation_entry = require_mapping(simulation_payload, "simulation_entry")
            source_entity_id = require_non_empty_str(simulation_entry.get("source_entity_id"), "source_entity_id")
            entity = entity_by_id.get(source_entity_id)
            if entity is None:
                raise FaultLanesError("simulation entry refers to missing world entity")
            fail_closed = bool(simulation_entry.get("fail_closed"))
            confidence = float(simulation_entry.get("confidence", 0.0))
            fault_cases: list[FaultCase] = []
            reason_codes: list[str] = []
            if fail_closed:
                severity = 1.0
                fault_kind = "simulation_fail_closed"
                outcome = FaultOutcome.FAIL_CLOSED
                reason_codes.append("simulation_guard_triggered")
            elif confidence < 0.65 or str(entity.get("status")) == "held":
                severity = clamp_score(max(0.25, 1.0 - confidence))
                fault_kind = "bounded_confidence_drop"
                outcome = FaultOutcome.DEGRADED
                reason_codes.append("confidence_below_fault_gate")
            else:
                severity = 0.0
                fault_kind = "no_fault_overlay_needed"
                outcome = FaultOutcome.CLEAR
                reason_codes.append("no_fault_overlay_needed")
            if outcome != FaultOutcome.CLEAR:
                case_payload = {
                    "source_simulation_entry_id": simulation_entry["simulation_entry_id"],
                    "fault_kind": fault_kind,
                    "severity": severity,
                }
                case_id = f"fault_case::{stable_hash_payload(case_payload)[:12]}"
                case_provenance = build_provenance_bundle(
                    entity_kind="fault_case",
                    entity_id=case_id,
                    origin_kind="constructed",
                    links=[
                        {
                            "role": "simulation",
                            "ref_id": simulation_entry["simulation_entry_id"],
                            "ref_kind": "what_if_simulation_entry",
                            "source_path": "phase6/what_if_simulation",
                        },
                        {
                            "role": "lane",
                            "ref_id": case_id,
                            "ref_kind": "fault_case",
                            "source_path": "phase6/fault_lanes",
                        },
                    ],
                )
                fault_cases.append(
                    FaultCase(
                        fault_case_id=case_id,
                        fault_kind=fault_kind,
                        severity=severity,
                        description=f"Fault overlay for {simulation_entry['simulation_entry_id']}",
                        provenance=case_provenance,
                        case_hash=stable_hash_payload({**case_payload, "case_id": case_id}),
                    )
                )
            entry_payload = {
                "source_simulation_entry_id": simulation_entry["simulation_entry_id"],
                "source_entity_id": source_entity_id,
                "outcome": outcome.value,
            }
            entry_id = f"fault::{stable_hash_payload(entry_payload)[:12]}"
            provenance = build_provenance_bundle(
                entity_kind="fault_entry",
                entity_id=entry_id,
                origin_kind="constructed",
                links=[
                    {
                        "role": "world_model",
                        "ref_id": source_entity_id,
                        "ref_kind": "world_entity",
                        "source_path": "phase6/world_model",
                    },
                    {
                        "role": "simulation",
                        "ref_id": simulation_entry["simulation_entry_id"],
                        "ref_kind": "what_if_simulation_entry",
                        "source_path": "phase6/what_if_simulation",
                    },
                    {
                        "role": "lane",
                        "ref_id": entry_id,
                        "ref_kind": "fault_lane_entry",
                        "source_path": "phase6/fault_lanes",
                    },
                ],
            )
            entries.append(
                FaultLaneEntry(
                    fault_entry_id=entry_id,
                    source_simulation_entry_id=simulation_entry["simulation_entry_id"],
                    source_entity_id=source_entity_id,
                    outcome=outcome,
                    fault_cases=tuple(fault_cases),
                    fail_closed=fail_closed,
                    reason_codes=tuple(reason_codes),
                    provenance=provenance,
                    entry_hash=stable_hash_payload(
                        {
                            **entry_payload,
                            "fault_cases": [item.to_dict() for item in fault_cases],
                            "reason_codes": reason_codes,
                        }
                    ),
                )
            )

        snapshot = FaultLaneSnapshot(
            schema="agifcore.phase_06.fault_lanes.v1",
            source_simulation_hash=require_non_empty_str(simulation_state.get("snapshot_hash"), "snapshot_hash"),
            entries=tuple(entries),
            snapshot_hash=stable_hash_payload(
                {
                    "source_simulation_hash": simulation_state.get("snapshot_hash"),
                    "entries": [entry.to_dict() for entry in entries],
                }
            ),
        )
        if canonical_size_bytes(snapshot.to_dict()) > self.max_state_bytes:
            raise FaultLanesError("fault-lane state exceeds Phase 6 byte ceiling")
        return snapshot
