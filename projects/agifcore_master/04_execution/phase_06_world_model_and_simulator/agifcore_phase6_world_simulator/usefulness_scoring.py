from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping

from .entity_classes import (
    MAX_USEFULNESS_INPUTS,
    MINIMUM_QUALIFIED_DOMAINS,
    UsefulnessDomainScore,
    UsefulnessEvaluationSnapshot,
    UsefulnessOutcome,
    build_provenance_bundle,
    canonical_size_bytes,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

MAX_USEFULNESS_STATE_BYTES = 2 * 1024 * 1024


class UsefulnessScoringError(ValueError):
    """Raised when usefulness scoring bypasses evidence or Phase 6 limits."""


def _domain_score(
    *,
    domain_id: str,
    domain_name: str,
    minimum_signal_groups: int,
    evidence_inputs: int,
    weighted_score: float,
    links: list[dict[str, str]],
) -> UsefulnessDomainScore:
    outcome = (
        UsefulnessOutcome.QUALIFIED
        if evidence_inputs >= minimum_signal_groups and weighted_score >= 0.6
        else UsefulnessOutcome.INSUFFICIENT
    )
    payload = {
        "domain_id": domain_id,
        "weighted_score": weighted_score,
        "evidence_inputs": evidence_inputs,
        "outcome": outcome.value,
    }
    score_id = f"usefulness::{stable_hash_payload(payload)[:12]}"
    provenance = build_provenance_bundle(
        entity_kind="usefulness_domain_score",
        entity_id=score_id,
        origin_kind="constructed",
        links=[
            *links,
            {
                "role": "instrumentation",
                "ref_id": score_id,
                "ref_kind": "usefulness_domain_score",
                "source_path": "phase6/usefulness_scoring",
            },
        ],
    )
    return UsefulnessDomainScore(
        domain_id=domain_id,
        domain_name=domain_name,
        weighted_score=weighted_score,
        evidence_inputs=evidence_inputs,
        outcome=outcome,
        reason_codes=(
            "minimum_signal_groups_met" if evidence_inputs >= minimum_signal_groups else "insufficient_signal_groups",
            "weighted_score_qualified" if weighted_score >= 0.6 else "weighted_score_below_threshold",
        ),
        provenance=provenance,
        score_hash=stable_hash_payload({**payload, "score_id": score_id}),
    )


class UsefulnessScoringEngine:
    """Evaluate domain usefulness from evidence-linked world-model and simulator outputs."""

    def __init__(
        self,
        *,
        minimum_qualified_domains: int = MINIMUM_QUALIFIED_DOMAINS,
        max_inputs: int = MAX_USEFULNESS_INPUTS,
        max_state_bytes: int = MAX_USEFULNESS_STATE_BYTES,
    ) -> None:
        self.minimum_qualified_domains = minimum_qualified_domains
        self.max_inputs = max_inputs
        self.max_state_bytes = max_state_bytes

    def build_snapshot(
        self,
        *,
        target_domain_registry_state: Mapping[str, Any],
        world_model_state: Mapping[str, Any],
        candidate_future_state: Mapping[str, Any],
        what_if_simulation_state: Mapping[str, Any],
        fault_lane_state: Mapping[str, Any],
        pressure_lane_state: Mapping[str, Any],
        conflict_lane_state: Mapping[str, Any],
        overload_lane_state: Mapping[str, Any],
        instrumentation_state: Mapping[str, Any],
    ) -> UsefulnessEvaluationSnapshot:
        target_domain_state = require_schema(
            target_domain_registry_state,
            "agifcore.phase_06.target_domains.v1",
            "target_domain_registry_state",
        )
        world_state = require_schema(world_model_state, "agifcore.phase_06.world_model.v1", "world_model_state")
        future_state = require_schema(candidate_future_state, "agifcore.phase_06.candidate_futures.v1", "candidate_future_state")
        simulation_state = require_schema(
            what_if_simulation_state,
            "agifcore.phase_06.what_if_simulation.v1",
            "what_if_simulation_state",
        )
        fault_state = require_schema(fault_lane_state, "agifcore.phase_06.fault_lanes.v1", "fault_lane_state")
        pressure_state = require_schema(pressure_lane_state, "agifcore.phase_06.pressure_lanes.v1", "pressure_lane_state")
        conflict_state = require_schema(conflict_lane_state, "agifcore.phase_06.conflict_lanes.v1", "conflict_lane_state")
        overload_state = require_schema(overload_lane_state, "agifcore.phase_06.overload_lanes.v1", "overload_lane_state")
        instrumentation = require_schema(instrumentation_state, "agifcore.phase_06.instrumentation.v1", "instrumentation_state")

        simulation_by_id = {
            require_non_empty_str(item.get("simulation_entry_id"), "simulation_entry_id"): require_mapping(item, "simulation_entry")
            for item in simulation_state.get("entries", [])
        }
        domain_counts: defaultdict[str, dict[str, int]] = defaultdict(
            lambda: {"world": 0, "future": 0, "simulation": 0, "fault": 0, "pressure": 0, "conflict": 0, "overload": 0, "instrumentation": 0}
        )

        for entity in world_state.get("entities", []):
            entity_map = require_mapping(entity, "world_entity")
            domain = entity_map.get("target_domain")
            if domain:
                domain_counts[str(domain)]["world"] += 1
        for future in future_state.get("futures", []):
            future_map = require_mapping(future, "future")
            domain_counts[require_non_empty_str(future_map.get("target_domain"), "target_domain")]["future"] += 1
        for entry in simulation_state.get("entries", []):
            entry_map = require_mapping(entry, "simulation_entry")
            domain_counts[require_non_empty_str(entry_map.get("target_domain"), "target_domain")]["simulation"] += 1
        for fault_entry in fault_state.get("entries", []):
            entry_map = require_mapping(fault_entry, "fault_entry")
            simulation_entry = simulation_by_id.get(str(entry_map.get("source_simulation_entry_id")))
            if simulation_entry is not None:
                domain_counts[str(simulation_entry.get("target_domain"))]["fault"] += max(1, len(entry_map.get("fault_cases", [])))
        for pressure_entry in pressure_state.get("entries", []):
            entry_map = require_mapping(pressure_entry, "pressure_entry")
            simulation_entry = simulation_by_id.get(str(entry_map.get("source_simulation_entry_id")))
            if simulation_entry is not None:
                domain_counts[str(simulation_entry.get("target_domain"))]["pressure"] += max(1, len(entry_map.get("scenarios", [])))
        for conflict_entry in conflict_state.get("entries", []):
            entry_map = require_mapping(conflict_entry, "conflict_entry")
            results = [require_mapping(item, "conflict_result") for item in entry_map.get("results", [])]
            for result in results:
                domain = result.get("conflicting_domain")
                if domain:
                    domain_counts[str(domain)]["conflict"] += 1
        for overload_entry in overload_state.get("entries", []):
            entry_map = require_mapping(overload_entry, "overload_entry")
            pressure_entry_id = require_non_empty_str(entry_map.get("source_pressure_entry_id"), "source_pressure_entry_id")
            matching_pressure = next(
                (
                    require_mapping(item, "pressure_entry")
                    for item in pressure_state.get("entries", [])
                    if item.get("pressure_entry_id") == pressure_entry_id
                ),
                None,
            )
            if matching_pressure is not None:
                simulation_entry = simulation_by_id.get(str(matching_pressure.get("source_simulation_entry_id")))
                if simulation_entry is not None:
                    domain_counts[str(simulation_entry.get("target_domain"))]["overload"] += max(
                        1,
                        len(entry_map.get("results", [])),
                    )

        for record in instrumentation.get("records", []):
            record_map = require_mapping(record, "instrumentation_record")
            source_entry_id = str(record_map.get("source_entry_id"))
            domain = None
            if source_entry_id in simulation_by_id:
                domain = simulation_by_id[source_entry_id].get("target_domain")
            else:
                for future in future_state.get("futures", []):
                    future_map = require_mapping(future, "future")
                    if future_map.get("future_id") == source_entry_id:
                        domain = future_map.get("target_domain")
                        break
            if domain:
                domain_counts[str(domain)]["instrumentation"] += 1

        domain_scores: list[UsefulnessDomainScore] = []
        for structure in target_domain_state.get("structures", []):
            structure_map = require_mapping(structure, "target_domain_structure")
            domain_id = require_non_empty_str(structure_map.get("domain_id"), "domain_id")
            counts = domain_counts[domain_id]
            evidence_inputs = min(sum(1 for value in counts.values() if value > 0), self.max_inputs)
            weighted_score = clamp_score(
                (0.15 * min(counts["world"] / 3.0, 1.0))
                + (0.15 * min(counts["future"] / 2.0, 1.0))
                + (0.15 * min(counts["simulation"] / 2.0, 1.0))
                + (0.10 * min(counts["fault"] / 2.0, 1.0))
                + (0.10 * min(counts["pressure"] / 2.0, 1.0))
                + (0.10 * min(counts["conflict"] / 2.0, 1.0))
                + (0.10 * min(counts["overload"] / 2.0, 1.0))
                + (0.15 * min(counts["instrumentation"] / 4.0, 1.0))
            )
            domain_scores.append(
                _domain_score(
                    domain_id=domain_id,
                    domain_name=require_non_empty_str(structure_map.get("domain_name"), "domain_name"),
                    minimum_signal_groups=int(structure_map.get("minimum_signal_groups")),
                    evidence_inputs=evidence_inputs,
                    weighted_score=weighted_score,
                    links=[
                        {
                            "role": "domain",
                            "ref_id": domain_id,
                            "ref_kind": "target_domain_structure",
                            "source_path": "phase6/target_domains",
                        },
                        {
                            "role": "world_model",
                            "ref_id": require_non_empty_str(world_state.get("snapshot_hash"), "snapshot_hash"),
                            "ref_kind": "world_model_snapshot",
                            "source_path": "phase6/world_model",
                        },
                        {
                            "role": "future",
                            "ref_id": require_non_empty_str(future_state.get("snapshot_hash"), "snapshot_hash"),
                            "ref_kind": "candidate_future_snapshot",
                            "source_path": "phase6/candidate_futures",
                        },
                        {
                            "role": "simulation",
                            "ref_id": require_non_empty_str(simulation_state.get("snapshot_hash"), "snapshot_hash"),
                            "ref_kind": "what_if_simulation_snapshot",
                            "source_path": "phase6/what_if_simulation",
                        },
                        {
                            "role": "lane",
                            "ref_id": require_non_empty_str(overload_state.get("snapshot_hash"), "snapshot_hash"),
                            "ref_kind": "overload_lane_snapshot",
                            "source_path": "phase6/overload_lanes",
                        },
                    ],
                )
            )

        qualified_domain_count = sum(1 for item in domain_scores if item.outcome == UsefulnessOutcome.QUALIFIED)
        overall_outcome = (
            UsefulnessOutcome.QUALIFIED
            if qualified_domain_count >= self.minimum_qualified_domains
            else UsefulnessOutcome.INSUFFICIENT
        )
        snapshot = UsefulnessEvaluationSnapshot(
            schema="agifcore.phase_06.usefulness_scoring.v1",
            qualified_domain_count=qualified_domain_count,
            minimum_qualified_domains=self.minimum_qualified_domains,
            overall_outcome=overall_outcome,
            domain_scores=tuple(domain_scores),
            snapshot_hash=stable_hash_payload(
                {
                    "qualified_domain_count": qualified_domain_count,
                    "minimum_qualified_domains": self.minimum_qualified_domains,
                    "overall_outcome": overall_outcome.value,
                    "domain_scores": [score.to_dict() for score in domain_scores],
                }
            ),
        )
        if canonical_size_bytes(snapshot.to_dict()) > self.max_state_bytes:
            raise UsefulnessScoringError("usefulness state exceeds Phase 6 byte ceiling")
        return snapshot
