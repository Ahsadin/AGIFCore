from __future__ import annotations

from typing import Any, Mapping

from .entity_classes import (
    OverloadLaneEntry,
    OverloadLaneSnapshot,
    OverloadOutcome,
    OverloadResult,
    build_provenance_bundle,
    canonical_size_bytes,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

MAX_OVERLOAD_STATE_BYTES = 2 * 1024 * 1024
OVERLOADED_THRESHOLD = 0.72
UNSAFE_THRESHOLD = 0.9


class OverloadLanesError(ValueError):
    """Raised when overload-lane evaluation violates Phase 6 limits."""


class OverloadLaneEngine:
    """Evaluate bounded overload state from pressure and conflict lanes."""

    def __init__(self, *, max_state_bytes: int = MAX_OVERLOAD_STATE_BYTES) -> None:
        self.max_state_bytes = max_state_bytes

    def build_snapshot(
        self,
        *,
        pressure_lane_state: Mapping[str, Any],
        conflict_lane_state: Mapping[str, Any],
    ) -> OverloadLaneSnapshot:
        pressure_state = require_schema(pressure_lane_state, "agifcore.phase_06.pressure_lanes.v1", "pressure_lane_state")
        conflict_state = require_schema(conflict_lane_state, "agifcore.phase_06.conflict_lanes.v1", "conflict_lane_state")
        conflict_by_simulation = {
            require_non_empty_str(item.get("source_simulation_entry_id"), "source_simulation_entry_id"): require_mapping(
                item, "conflict_entry"
            )
            for item in conflict_state.get("entries", [])
        }
        entries: list[OverloadLaneEntry] = []
        for pressure_payload in pressure_state.get("entries", []):
            pressure_entry = require_mapping(pressure_payload, "pressure_entry")
            simulation_entry_id = require_non_empty_str(
                pressure_entry.get("source_simulation_entry_id"),
                "source_simulation_entry_id",
            )
            conflict_entry = conflict_by_simulation.get(simulation_entry_id)
            scenario_scores = [
                float(require_mapping(item, "pressure_scenario").get("pressure_score", 0.0))
                for item in pressure_entry.get("scenarios", [])
            ]
            load_score = clamp_score(
                max([float(pressure_entry.get("working_memory_utilization", 0.0)), *scenario_scores] or [0.0])
            )
            conflict_score = max(
                [
                    float(require_mapping(item, "conflict_result").get("conflict_score", 0.0))
                    for item in (conflict_entry.get("results", []) if conflict_entry is not None else [])
                ]
                or [0.0]
            )
            combined_score = clamp_score((0.65 * load_score) + (0.35 * conflict_score))
            if conflict_entry is not None and str(conflict_entry.get("outcome")) == "blocked":
                outcome = OverloadOutcome.UNSAFE
                threshold = UNSAFE_THRESHOLD
                reason_codes = ["blocked_conflict_escalates_overload"]
            elif combined_score >= UNSAFE_THRESHOLD:
                outcome = OverloadOutcome.UNSAFE
                threshold = UNSAFE_THRESHOLD
                reason_codes = ["load_score_above_unsafe_threshold"]
            elif combined_score >= OVERLOADED_THRESHOLD:
                outcome = OverloadOutcome.OVERLOADED
                threshold = OVERLOADED_THRESHOLD
                reason_codes = ["load_score_above_overload_threshold"]
            else:
                outcome = OverloadOutcome.CLEAR
                threshold = OVERLOADED_THRESHOLD
                reason_codes = ["load_score_within_bounds"]
            result_payload = {
                "simulation_entry_id": simulation_entry_id,
                "outcome": outcome.value,
                "load_score": combined_score,
            }
            result_id = f"overload_result::{stable_hash_payload(result_payload)[:12]}"
            result_provenance = build_provenance_bundle(
                entity_kind="overload_result",
                entity_id=result_id,
                origin_kind="constructed",
                links=[
                    {
                        "role": "lane",
                        "ref_id": require_non_empty_str(pressure_entry.get("pressure_entry_id"), "pressure_entry_id"),
                        "ref_kind": "pressure_lane_entry",
                        "source_path": "phase6/pressure_lanes",
                    },
                    {
                        "role": "lane",
                        "ref_id": result_id,
                        "ref_kind": "overload_result",
                        "source_path": "phase6/overload_lanes",
                    },
                ],
            )
            result = OverloadResult(
                overload_result_id=result_id,
                outcome=outcome,
                load_score=combined_score,
                conflict_score=conflict_score,
                threshold=threshold,
                reason_codes=tuple(reason_codes),
                provenance=result_provenance,
                result_hash=stable_hash_payload({**result_payload, "result_id": result_id}),
            )
            entry_id = f"overload_entry::{stable_hash_payload({'simulation_entry_id': simulation_entry_id})[:12]}"
            entry_provenance = build_provenance_bundle(
                entity_kind="overload_entry",
                entity_id=entry_id,
                origin_kind="constructed",
                links=[
                    {
                        "role": "lane",
                        "ref_id": require_non_empty_str(pressure_entry.get("pressure_entry_id"), "pressure_entry_id"),
                        "ref_kind": "pressure_lane_entry",
                        "source_path": "phase6/pressure_lanes",
                    },
                    {
                        "role": "lane",
                        "ref_id": entry_id,
                        "ref_kind": "overload_lane_entry",
                        "source_path": "phase6/overload_lanes",
                    },
                ],
            )
            entries.append(
                OverloadLaneEntry(
                    overload_entry_id=entry_id,
                    source_pressure_entry_id=require_non_empty_str(
                        pressure_entry.get("pressure_entry_id"),
                        "pressure_entry_id",
                    ),
                    source_conflict_entry_id=(
                        require_non_empty_str(conflict_entry.get("conflict_entry_id"), "conflict_entry_id")
                        if conflict_entry is not None
                        else None
                    ),
                    outcome=outcome,
                    results=(result,),
                    provenance=entry_provenance,
                    entry_hash=stable_hash_payload(
                        {
                            "overload_entry_id": entry_id,
                            "pressure_entry_id": pressure_entry.get("pressure_entry_id"),
                            "outcome": outcome.value,
                        }
                    ),
                )
            )

        snapshot = OverloadLaneSnapshot(
            schema="agifcore.phase_06.overload_lanes.v1",
            source_pressure_hash=require_non_empty_str(pressure_state.get("snapshot_hash"), "snapshot_hash"),
            source_conflict_hash=require_non_empty_str(conflict_state.get("snapshot_hash"), "snapshot_hash"),
            entries=tuple(entries),
            snapshot_hash=stable_hash_payload(
                {
                    "source_pressure_hash": pressure_state.get("snapshot_hash"),
                    "source_conflict_hash": conflict_state.get("snapshot_hash"),
                    "entries": [entry.to_dict() for entry in entries],
                }
            ),
        )
        if canonical_size_bytes(snapshot.to_dict()) > self.max_state_bytes:
            raise OverloadLanesError("overload-lane state exceeds Phase 6 byte ceiling")
        return snapshot
