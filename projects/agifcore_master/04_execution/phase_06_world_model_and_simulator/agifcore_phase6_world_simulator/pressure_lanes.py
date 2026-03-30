from __future__ import annotations

from typing import Any, Mapping

from .entity_classes import (
    PressureLaneEntry,
    PressureLaneSnapshot,
    PressureOutcome,
    PressureScenario,
    build_provenance_bundle,
    canonical_size_bytes,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

MAX_PRESSURE_STATE_BYTES = 2 * 1024 * 1024


class PressureLanesError(ValueError):
    """Raised when pressure-lane computation violates Phase 6 boundaries."""


class PressureLaneEngine:
    """Project bounded pressure scenarios from simulation and fault overlays."""

    def __init__(self, *, max_state_bytes: int = MAX_PRESSURE_STATE_BYTES) -> None:
        self.max_state_bytes = max_state_bytes

    def build_snapshot(
        self,
        *,
        what_if_simulation_state: Mapping[str, Any],
        fault_lane_state: Mapping[str, Any],
        working_memory_state: Mapping[str, Any] | None = None,
    ) -> PressureLaneSnapshot:
        simulation_state = require_schema(
            what_if_simulation_state,
            "agifcore.phase_06.what_if_simulation.v1",
            "what_if_simulation_state",
        )
        fault_state = require_schema(fault_lane_state, "agifcore.phase_06.fault_lanes.v1", "fault_lane_state")
        pressure_payload = {"utilization": 0.0}
        if working_memory_state is not None:
            working_state = require_schema(working_memory_state, "agifcore.phase_04.working_memory.v1", "working_memory_state")
            pressure_payload = require_mapping(working_state.get("memory_pressure", {}), "memory_pressure")
        fault_by_simulation = {
            require_non_empty_str(entry.get("source_simulation_entry_id"), "source_simulation_entry_id"): require_mapping(
                entry, "fault_entry"
            )
            for entry in fault_state.get("entries", [])
        }
        entries: list[PressureLaneEntry] = []
        for simulation_payload in simulation_state.get("entries", []):
            simulation_entry = require_mapping(simulation_payload, "simulation_entry")
            simulation_entry_id = require_non_empty_str(
                simulation_entry.get("simulation_entry_id"),
                "simulation_entry_id",
            )
            fault_entry = fault_by_simulation.get(simulation_entry_id)
            fault_cases = fault_entry.get("fault_cases", []) if fault_entry is not None else []
            fault_severity = max(
                [float(require_mapping(item, "fault_case").get("severity", 0.0)) for item in fault_cases] or [0.0]
            )
            working_memory_utilization = float(pressure_payload.get("utilization", 0.0))
            pressure_score = clamp_score(
                max(working_memory_utilization, 1.0 - float(simulation_entry.get("confidence", 0.0)), fault_severity)
            )
            if bool(simulation_entry.get("fail_closed")) or (fault_entry is not None and bool(fault_entry.get("fail_closed"))):
                outcome = PressureOutcome.FAIL_CLOSED
                scenario_kind = "fail_closed_pressure"
                scenario_reason_codes = ["upstream_fail_closed"]
            elif pressure_score >= 0.55:
                outcome = PressureOutcome.STRESSED
                scenario_kind = "bounded_pressure_cascade"
                scenario_reason_codes = ["pressure_threshold_crossed"]
            else:
                outcome = PressureOutcome.CLEAR
                scenario_kind = "clear_pressure_lane"
                scenario_reason_codes = ["pressure_below_threshold"]
            scenarios: list[PressureScenario] = []
            if outcome != PressureOutcome.CLEAR or working_memory_utilization > 0.0:
                scenario_payload = {
                    "source_simulation_entry_id": simulation_entry_id,
                    "scenario_kind": scenario_kind,
                    "pressure_score": pressure_score,
                    "target_domain": simulation_entry.get("target_domain"),
                }
                scenario_id = f"pressure::{stable_hash_payload(scenario_payload)[:12]}"
                scenario_provenance = build_provenance_bundle(
                    entity_kind="pressure_scenario",
                    entity_id=scenario_id,
                    origin_kind="constructed",
                    links=[
                        {
                            "role": "simulation",
                            "ref_id": simulation_entry_id,
                            "ref_kind": "what_if_simulation_entry",
                            "source_path": "phase6/what_if_simulation",
                        },
                        {
                            "role": "working_memory",
                            "ref_id": "phase4-working-memory",
                            "ref_kind": "working_memory_state",
                            "source_path": "phase4/working_memory",
                        },
                        {
                            "role": "lane",
                            "ref_id": scenario_id,
                            "ref_kind": "pressure_scenario",
                            "source_path": "phase6/pressure_lanes",
                        },
                    ],
                )
                scenarios.append(
                    PressureScenario(
                        pressure_scenario_id=scenario_id,
                        scenario_kind=scenario_kind,
                        pressure_score=pressure_score,
                        target_domain=simulation_entry.get("target_domain"),
                        reason_codes=tuple(scenario_reason_codes),
                        provenance=scenario_provenance,
                        scenario_hash=stable_hash_payload({**scenario_payload, "scenario_id": scenario_id}),
                    )
                )
            entry_id = f"pressure_entry::{stable_hash_payload({'simulation_entry_id': simulation_entry_id})[:12]}"
            entry_provenance = build_provenance_bundle(
                entity_kind="pressure_entry",
                entity_id=entry_id,
                origin_kind="constructed",
                links=[
                    {
                        "role": "simulation",
                        "ref_id": simulation_entry_id,
                        "ref_kind": "what_if_simulation_entry",
                        "source_path": "phase6/what_if_simulation",
                    },
                    {
                        "role": "lane",
                        "ref_id": entry_id,
                        "ref_kind": "pressure_lane_entry",
                        "source_path": "phase6/pressure_lanes",
                    },
                ],
            )
            entries.append(
                PressureLaneEntry(
                    pressure_entry_id=entry_id,
                    source_simulation_entry_id=simulation_entry_id,
                    source_fault_entry_id=(
                        require_non_empty_str(fault_entry.get("fault_entry_id"), "fault_entry_id")
                        if fault_entry is not None
                        else None
                    ),
                    outcome=outcome,
                    scenarios=tuple(scenarios),
                    working_memory_utilization=clamp_score(working_memory_utilization),
                    provenance=entry_provenance,
                    entry_hash=stable_hash_payload(
                        {
                            "pressure_entry_id": entry_id,
                            "simulation_entry_id": simulation_entry_id,
                            "outcome": outcome.value,
                            "working_memory_utilization": working_memory_utilization,
                        }
                    ),
                )
            )

        snapshot = PressureLaneSnapshot(
            schema="agifcore.phase_06.pressure_lanes.v1",
            source_fault_hash=require_non_empty_str(fault_state.get("snapshot_hash"), "snapshot_hash"),
            entries=tuple(entries),
            snapshot_hash=stable_hash_payload(
                {
                    "source_fault_hash": fault_state.get("snapshot_hash"),
                    "entries": [entry.to_dict() for entry in entries],
                }
            ),
        )
        if canonical_size_bytes(snapshot.to_dict()) > self.max_state_bytes:
            raise PressureLanesError("pressure-lane state exceeds Phase 6 byte ceiling")
        return snapshot
