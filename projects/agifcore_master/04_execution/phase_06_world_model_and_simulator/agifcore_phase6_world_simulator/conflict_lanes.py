from __future__ import annotations

from typing import Any, Mapping

from .entity_classes import (
    ConflictLaneEntry,
    ConflictLaneSnapshot,
    ConflictOutcome,
    ConflictResult,
    build_provenance_bundle,
    canonical_size_bytes,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

MAX_CONFLICT_STATE_BYTES = 2 * 1024 * 1024


class ConflictLanesError(ValueError):
    """Raised when conflict-lane evaluation violates Phase 6 boundaries."""


class ConflictLaneEngine:
    """Project governed conflict results from simulation, pressure, and transfer state."""

    def __init__(self, *, max_state_bytes: int = MAX_CONFLICT_STATE_BYTES) -> None:
        self.max_state_bytes = max_state_bytes

    def build_snapshot(
        self,
        *,
        what_if_simulation_state: Mapping[str, Any],
        pressure_lane_state: Mapping[str, Any],
        transfer_graph_state: Mapping[str, Any],
    ) -> ConflictLaneSnapshot:
        simulation_state = require_schema(
            what_if_simulation_state,
            "agifcore.phase_06.what_if_simulation.v1",
            "what_if_simulation_state",
        )
        pressure_state = require_schema(pressure_lane_state, "agifcore.phase_06.pressure_lanes.v1", "pressure_lane_state")
        transfer_state = require_schema(transfer_graph_state, "agifcore.phase_05.transfer_graph.v1", "transfer_graph_state")

        pressure_by_simulation = {
            require_non_empty_str(item.get("source_simulation_entry_id"), "source_simulation_entry_id"): require_mapping(
                item, "pressure_entry"
            )
            for item in pressure_state.get("entries", [])
        }
        transfer_records = [require_mapping(item, "transfer_record") for item in transfer_state.get("records", [])]
        entries: list[ConflictLaneEntry] = []
        for simulation_payload in simulation_state.get("entries", []):
            simulation_entry = require_mapping(simulation_payload, "simulation_entry")
            simulation_entry_id = require_non_empty_str(
                simulation_entry.get("simulation_entry_id"),
                "simulation_entry_id",
            )
            pressure_entry = pressure_by_simulation.get(simulation_entry_id)
            target_domain = require_non_empty_str(simulation_entry.get("target_domain"), "target_domain")
            matching_records = [item for item in transfer_records if item.get("target_domain") == target_domain]
            results: list[ConflictResult] = []
            entry_outcome = ConflictOutcome.CLEAR
            fail_closed = bool(simulation_entry.get("fail_closed"))
            if fail_closed:
                entry_outcome = ConflictOutcome.ABSTAIN
            for record in matching_records[:2]:
                decision = str(record.get("decision"))
                conflict_status = str(record.get("conflict_status", "clear"))
                pressure_outcome = str(pressure_entry.get("outcome")) if pressure_entry is not None else "clear"
                if decision in {"blocked", "denied"} or conflict_status in {"blocked", "conflict"}:
                    outcome = ConflictOutcome.BLOCKED
                    conflict_score = 1.0
                    reason_codes = ["transfer_blocked", "governed_conflict"]
                elif decision == "abstained" or pressure_outcome in {"stressed", "fail_closed"}:
                    outcome = ConflictOutcome.HOLD
                    conflict_score = clamp_score(0.65 + (0.15 if pressure_outcome == "fail_closed" else 0.0))
                    reason_codes = ["pressure_or_transfer_hold", "review_hold_required"]
                else:
                    outcome = ConflictOutcome.CLEAR
                    conflict_score = clamp_score(float(record.get("quality_score", 0.0)))
                    reason_codes = ["no_conflict_detected"]
                if outcome == ConflictOutcome.BLOCKED:
                    entry_outcome = ConflictOutcome.BLOCKED
                elif outcome == ConflictOutcome.HOLD and entry_outcome == ConflictOutcome.CLEAR:
                    entry_outcome = ConflictOutcome.HOLD
                result_payload = {
                    "simulation_entry_id": simulation_entry_id,
                    "transfer_id": record.get("transfer_id"),
                    "outcome": outcome.value,
                }
                result_id = f"conflict_result::{stable_hash_payload(result_payload)[:12]}"
                result_provenance = build_provenance_bundle(
                    entity_kind="conflict_result",
                    entity_id=result_id,
                    origin_kind="constructed",
                    links=[
                        {
                            "role": "transfer",
                            "ref_id": require_non_empty_str(record.get("transfer_id"), "transfer_id"),
                            "ref_kind": "transfer_record",
                            "source_path": "phase5/transfer_graph",
                        },
                        {
                            "role": "simulation",
                            "ref_id": simulation_entry_id,
                            "ref_kind": "what_if_simulation_entry",
                            "source_path": "phase6/what_if_simulation",
                        },
                        {
                            "role": "lane",
                            "ref_id": result_id,
                            "ref_kind": "conflict_result",
                            "source_path": "phase6/conflict_lanes",
                        },
                    ],
                )
                results.append(
                    ConflictResult(
                        conflict_result_id=result_id,
                        conflict_kind="governed_transfer_world_conflict",
                        outcome=outcome,
                        source_transfer_id=require_non_empty_str(record.get("transfer_id"), "transfer_id"),
                        source_simulation_entry_id=simulation_entry_id,
                        conflicting_domain=target_domain,
                        conflict_score=conflict_score,
                        reason_codes=tuple(reason_codes),
                        provenance=result_provenance,
                        result_hash=stable_hash_payload({**result_payload, "result_id": result_id}),
                    )
                )
            if fail_closed and not results:
                result_id = f"conflict_result::{stable_hash_payload({'simulation_entry_id': simulation_entry_id, 'outcome': 'abstain'})[:12]}"
                result_provenance = build_provenance_bundle(
                    entity_kind="conflict_result",
                    entity_id=result_id,
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
                            "ref_id": result_id,
                            "ref_kind": "conflict_result",
                            "source_path": "phase6/conflict_lanes",
                        },
                    ],
                )
                results.append(
                    ConflictResult(
                        conflict_result_id=result_id,
                        conflict_kind="fail_closed_conflict_guard",
                        outcome=ConflictOutcome.ABSTAIN,
                        source_transfer_id=None,
                        source_simulation_entry_id=simulation_entry_id,
                        conflicting_domain=target_domain,
                        conflict_score=1.0,
                        reason_codes=("simulation_fail_closed",),
                        provenance=result_provenance,
                        result_hash=stable_hash_payload(
                            {"simulation_entry_id": simulation_entry_id, "result_id": result_id, "outcome": "abstain"}
                        ),
                    )
                )
            entry_id = f"conflict_entry::{stable_hash_payload({'simulation_entry_id': simulation_entry_id})[:12]}"
            entry_provenance = build_provenance_bundle(
                entity_kind="conflict_entry",
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
                        "ref_kind": "conflict_lane_entry",
                        "source_path": "phase6/conflict_lanes",
                    },
                ],
            )
            entries.append(
                ConflictLaneEntry(
                    conflict_entry_id=entry_id,
                    source_simulation_entry_id=simulation_entry_id,
                    source_pressure_entry_id=(
                        require_non_empty_str(pressure_entry.get("pressure_entry_id"), "pressure_entry_id")
                        if pressure_entry is not None
                        else None
                    ),
                    outcome=entry_outcome,
                    results=tuple(results),
                    fail_closed=fail_closed,
                    provenance=entry_provenance,
                    entry_hash=stable_hash_payload(
                        {
                            "conflict_entry_id": entry_id,
                            "simulation_entry_id": simulation_entry_id,
                            "outcome": entry_outcome.value,
                        }
                    ),
                )
            )

        snapshot = ConflictLaneSnapshot(
            schema="agifcore.phase_06.conflict_lanes.v1",
            source_pressure_hash=require_non_empty_str(pressure_state.get("snapshot_hash"), "snapshot_hash"),
            entries=tuple(entries),
            snapshot_hash=stable_hash_payload(
                {
                    "source_pressure_hash": pressure_state.get("snapshot_hash"),
                    "entries": [entry.to_dict() for entry in entries],
                }
            ),
        )
        if canonical_size_bytes(snapshot.to_dict()) > self.max_state_bytes:
            raise ConflictLanesError("conflict-lane state exceeds Phase 6 byte ceiling")
        return snapshot
