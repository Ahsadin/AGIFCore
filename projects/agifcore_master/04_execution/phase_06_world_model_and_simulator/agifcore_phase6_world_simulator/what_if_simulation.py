from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping

from .entity_classes import (
    MAX_BRANCH_DEPTH,
    SimulationOutcome,
    SimulationTraceStep,
    WhatIfSimulationEntry,
    WhatIfSimulationSnapshot,
    WorldEntityStatus,
    WorldOperatorStatus,
    build_provenance_bundle,
    canonical_size_bytes,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

MAX_SIMULATION_STATE_BYTES = 2 * 1024 * 1024


class WhatIfSimulationError(ValueError):
    """Raised when what-if simulation violates Phase 6 constraints."""


def _trace_step(
    *,
    step_kind: str,
    detail: str,
    decision: str,
    supporting_refs: list[str],
) -> SimulationTraceStep:
    payload = {
        "step_kind": require_non_empty_str(step_kind, "step_kind"),
        "detail": require_non_empty_str(detail, "detail"),
        "decision": require_non_empty_str(decision, "decision"),
        "supporting_refs": [require_non_empty_str(item, "supporting_ref") for item in supporting_refs],
    }
    step_id = f"trace::{stable_hash_payload(payload)[:12]}"
    return SimulationTraceStep(
        step_id=step_id,
        step_kind=payload["step_kind"],
        detail=payload["detail"],
        decision=payload["decision"],
        supporting_refs=tuple(payload["supporting_refs"]),
        step_hash=stable_hash_payload({**payload, "step_id": step_id}),
    )


class WhatIfSimulationEngine:
    """Run a bounded, fail-closed simulation over candidate futures."""

    def __init__(self, *, max_branch_depth: int = MAX_BRANCH_DEPTH, max_state_bytes: int = MAX_SIMULATION_STATE_BYTES) -> None:
        self.max_branch_depth = max_branch_depth
        self.max_state_bytes = max_state_bytes

    def build_snapshot(
        self,
        *,
        world_model_state: Mapping[str, Any],
        candidate_future_state: Mapping[str, Any],
    ) -> WhatIfSimulationSnapshot:
        world_state = require_schema(world_model_state, "agifcore.phase_06.world_model.v1", "world_model_state")
        future_state = require_schema(
            candidate_future_state,
            "agifcore.phase_06.candidate_futures.v1",
            "candidate_future_state",
        )
        if future_state.get("source_world_model_hash") != world_state.get("snapshot_hash"):
            raise WhatIfSimulationError("candidate futures do not match the provided world-model snapshot")

        entity_by_id = {
            require_non_empty_str(item.get("entity_id"), "entity_id"): require_mapping(item, "world_entity")
            for item in world_state.get("entities", [])
        }
        relation_by_id = {
            require_non_empty_str(item.get("relation_id"), "relation_id"): require_mapping(item, "world_relation")
            for item in world_state.get("relations", [])
        }
        relations_by_source: defaultdict[str, list[str]] = defaultdict(list)
        for relation in relation_by_id.values():
            relations_by_source[str(relation.get("source_entity_id"))].append(str(relation.get("relation_id")))

        entries: list[WhatIfSimulationEntry] = []
        for future_payload in future_state.get("futures", []):
            future_map = require_mapping(future_payload, "candidate_future")
            future_id = require_non_empty_str(future_map.get("future_id"), "future_id")
            source_entity_id = require_non_empty_str(future_map.get("source_entity_id"), "source_entity_id")
            relation_id = require_non_empty_str(future_map.get("relation_id"), "relation_id")
            source_entity = entity_by_id.get(source_entity_id)
            relation = relation_by_id.get(relation_id)
            if source_entity is None or relation is None:
                raise WhatIfSimulationError("future refers to missing world-model entities or relations")
            operator = require_mapping(source_entity.get("operators", [{}])[0], "operator")
            projected_outcome = SimulationOutcome(str(future_map.get("projected_outcome")))
            fail_closed = (
                projected_outcome == SimulationOutcome.ABSTAIN
                or int(future_map.get("branch_depth")) > self.max_branch_depth
                or str(source_entity.get("status")) == WorldEntityStatus.BLOCKED.value
                or str(operator.get("status")) == WorldOperatorStatus.BLOCKED.value
            )
            considered_relation_ids = sorted(
                {relation_id, *relations_by_source.get(source_entity_id, [])}
            )
            outcome = SimulationOutcome.ABSTAIN if fail_closed else projected_outcome
            confidence = 0.0 if fail_closed else clamp_score(
                (0.5 * float(future_map.get("bounded_confidence", 0.0)))
                + (0.3 * float(relation.get("relation_strength", 0.0)))
                + (0.2 * float(source_entity.get("world_confidence", 0.0)))
            )
            trace_steps = (
                _trace_step(
                    step_kind="candidate_future_selected",
                    detail=f"Selected candidate future {future_id}",
                    decision="review_only_projection",
                    supporting_refs=[future_id, source_entity_id],
                ),
                _trace_step(
                    step_kind="relation_set_checked",
                    detail=f"Checked {len(considered_relation_ids)} relation(s) for {source_entity_id}",
                    decision="relation_grounded",
                    supporting_refs=considered_relation_ids[:4],
                ),
                _trace_step(
                    step_kind="simulation_decision",
                    detail=f"Simulation outcome {outcome.value}",
                    decision="fail_closed" if fail_closed else "projected_outcome_retained",
                    supporting_refs=[relation_id, str(future_map.get("target_domain"))],
                ),
            )
            reason_codes = list(str(item) for item in future_map.get("reason_codes", []))
            if fail_closed:
                reason_codes.append("fail_closed_guard")
            entry_id = f"simulation::{stable_hash_payload({'future_id': future_id, 'outcome': outcome.value})[:12]}"
            provenance = build_provenance_bundle(
                entity_kind="simulation_entry",
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
                        "role": "future",
                        "ref_id": future_id,
                        "ref_kind": "candidate_future",
                        "source_path": "phase6/candidate_futures",
                    },
                    {
                        "role": "simulation",
                        "ref_id": entry_id,
                        "ref_kind": "what_if_simulation_entry",
                        "source_path": "phase6/what_if_simulation",
                    },
                ],
            )
            entries.append(
                WhatIfSimulationEntry(
                    simulation_entry_id=entry_id,
                    future_id=future_id,
                    source_entity_id=source_entity_id,
                    target_domain=require_non_empty_str(future_map.get("target_domain"), "target_domain"),
                    branch_depth=int(future_map.get("branch_depth")),
                    outcome=outcome,
                    fail_closed=fail_closed,
                    confidence=confidence,
                    considered_relation_ids=tuple(considered_relation_ids),
                    trace_steps=trace_steps,
                    reason_codes=tuple(reason_codes),
                    provenance=provenance,
                    entry_hash=stable_hash_payload(
                        {
                            "simulation_entry_id": entry_id,
                            "future_id": future_id,
                            "outcome": outcome.value,
                            "fail_closed": fail_closed,
                            "confidence": confidence,
                        }
                    ),
                )
            )

        snapshot = WhatIfSimulationSnapshot(
            schema="agifcore.phase_06.what_if_simulation.v1",
            source_world_model_hash=require_non_empty_str(world_state.get("snapshot_hash"), "snapshot_hash"),
            source_future_hash=require_non_empty_str(future_state.get("snapshot_hash"), "snapshot_hash"),
            entries=tuple(entries),
            snapshot_hash=stable_hash_payload(
                {
                    "source_world_model_hash": world_state.get("snapshot_hash"),
                    "source_future_hash": future_state.get("snapshot_hash"),
                    "entries": [entry.to_dict() for entry in entries],
                }
            ),
        )
        if canonical_size_bytes(snapshot.to_dict()) > self.max_state_bytes:
            raise WhatIfSimulationError("what-if simulation state exceeds Phase 6 byte ceiling")
        return snapshot
