from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping

from .entity_classes import (
    InstrumentationMetric,
    InstrumentationRecord,
    InstrumentationRecordKind,
    InstrumentationSnapshot,
    InstrumentationSummary,
    InstrumentationSummaryKind,
    MAX_INSTRUMENTATION_EVENTS,
    MetricValueType,
    build_provenance_bundle,
    canonical_size_bytes,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

MAX_INSTRUMENTATION_STATE_BYTES = 2 * 1024 * 1024


class InstrumentationError(ValueError):
    """Raised when Phase 6 instrumentation exceeds bounded audit limits."""


def _record(
    *,
    record_kind: InstrumentationRecordKind,
    source_entry_id: str,
    status: str,
    reason_codes: list[str],
    numeric_score: float,
    links: list[dict[str, str]],
) -> InstrumentationRecord:
    payload = {
        "record_kind": record_kind.value,
        "source_entry_id": require_non_empty_str(source_entry_id, "source_entry_id"),
        "status": require_non_empty_str(status, "status"),
        "reason_codes": tuple(reason_codes),
        "numeric_score": clamp_score(numeric_score),
    }
    record_id = f"instrument_record::{stable_hash_payload(payload)[:12]}"
    provenance = build_provenance_bundle(
        entity_kind="instrumentation_record",
        entity_id=record_id,
        origin_kind="constructed",
        links=[
            *links,
            {
                "role": "instrumentation",
                "ref_id": record_id,
                "ref_kind": "instrumentation_record",
                "source_path": "phase6/instrumentation",
            },
        ],
    )
    return InstrumentationRecord(
        record_id=record_id,
        record_kind=record_kind,
        source_entry_id=payload["source_entry_id"],
        status=payload["status"],
        reason_codes=payload["reason_codes"],
        numeric_score=payload["numeric_score"],
        provenance=provenance,
        record_hash=stable_hash_payload({**payload, "record_id": record_id}),
    )


class InstrumentationEngine:
    """Build machine-readable audit records over the full Phase 6 simulator chain."""

    def __init__(self, *, max_events: int = MAX_INSTRUMENTATION_EVENTS, max_state_bytes: int = MAX_INSTRUMENTATION_STATE_BYTES) -> None:
        self.max_events = max_events
        self.max_state_bytes = max_state_bytes

    def build_snapshot(
        self,
        *,
        world_model_state: Mapping[str, Any],
        candidate_future_state: Mapping[str, Any],
        what_if_simulation_state: Mapping[str, Any],
        fault_lane_state: Mapping[str, Any],
        pressure_lane_state: Mapping[str, Any],
        conflict_lane_state: Mapping[str, Any],
        overload_lane_state: Mapping[str, Any],
    ) -> InstrumentationSnapshot:
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

        records: list[InstrumentationRecord] = []
        source_domain_by_entry: dict[str, str] = {}

        for entity in world_state.get("entities", [])[:12]:
            entity_map = require_mapping(entity, "world_entity")
            entity_id = require_non_empty_str(entity_map.get("entity_id"), "entity_id")
            source_domain_by_entry[entity_id] = str(entity_map.get("target_domain") or "")
            records.append(
                _record(
                    record_kind=InstrumentationRecordKind.WORLD_ENTITY,
                    source_entry_id=entity_id,
                    status=str(entity_map.get("status")),
                    reason_codes=["world_model_entity_recorded"],
                    numeric_score=float(entity_map.get("world_confidence", 0.0)),
                    links=[
                        {
                            "role": "world_model",
                            "ref_id": entity_id,
                            "ref_kind": "world_entity",
                            "source_path": "phase6/world_model",
                        }
                    ],
                )
            )
        for future in future_state.get("futures", []):
            future_map = require_mapping(future, "candidate_future")
            future_id = require_non_empty_str(future_map.get("future_id"), "future_id")
            source_domain_by_entry[future_id] = str(future_map.get("target_domain"))
            records.append(
                _record(
                    record_kind=InstrumentationRecordKind.FUTURE,
                    source_entry_id=future_id,
                    status=str(future_map.get("projected_outcome")),
                    reason_codes=list(str(item) for item in future_map.get("reason_codes", [])),
                    numeric_score=float(future_map.get("bounded_confidence", 0.0)),
                    links=[
                        {
                            "role": "future",
                            "ref_id": future_id,
                            "ref_kind": "candidate_future",
                            "source_path": "phase6/candidate_futures",
                        }
                    ],
                )
            )
        for entry in simulation_state.get("entries", []):
            entry_map = require_mapping(entry, "simulation_entry")
            entry_id = require_non_empty_str(entry_map.get("simulation_entry_id"), "simulation_entry_id")
            source_domain_by_entry[entry_id] = str(entry_map.get("target_domain"))
            records.append(
                _record(
                    record_kind=InstrumentationRecordKind.SIMULATION,
                    source_entry_id=entry_id,
                    status=str(entry_map.get("outcome")),
                    reason_codes=list(str(item) for item in entry_map.get("reason_codes", [])),
                    numeric_score=float(entry_map.get("confidence", 0.0)),
                    links=[
                        {
                            "role": "simulation",
                            "ref_id": entry_id,
                            "ref_kind": "what_if_simulation_entry",
                            "source_path": "phase6/what_if_simulation",
                        }
                    ],
                )
            )
        for lane_state, record_kind, id_field, status_field, score_field, source_path in (
            (fault_state, InstrumentationRecordKind.FAULT, "fault_entry_id", "outcome", None, "phase6/fault_lanes"),
            (pressure_state, InstrumentationRecordKind.PRESSURE, "pressure_entry_id", "outcome", "working_memory_utilization", "phase6/pressure_lanes"),
            (conflict_state, InstrumentationRecordKind.CONFLICT, "conflict_entry_id", "outcome", None, "phase6/conflict_lanes"),
            (overload_state, InstrumentationRecordKind.OVERLOAD, "overload_entry_id", "outcome", None, "phase6/overload_lanes"),
        ):
            for entry in lane_state.get("entries", []):
                entry_map = require_mapping(entry, "lane_entry")
                entry_id = require_non_empty_str(entry_map.get(id_field), id_field)
                source_domain_by_entry[entry_id] = source_domain_by_entry.get(
                    str(entry_map.get("source_simulation_entry_id", "")),
                    "",
                )
                if score_field is None and entry_map.get("results"):
                    first_result = require_mapping(entry_map["results"][0], "result")
                    numeric_score = float(
                        first_result.get("load_score")
                        or first_result.get("conflict_score")
                        or first_result.get("severity")
                        or 0.0
                    )
                else:
                    numeric_score = float(entry_map.get(score_field or "", 0.0))
                records.append(
                    _record(
                        record_kind=record_kind,
                        source_entry_id=entry_id,
                        status=str(entry_map.get(status_field)),
                        reason_codes=[f"{record_kind.value}_entry_recorded"],
                        numeric_score=numeric_score,
                        links=[
                            {
                                "role": "lane",
                                "ref_id": entry_id,
                                "ref_kind": f"{record_kind.value}_lane_entry",
                                "source_path": source_path,
                            }
                        ],
                    )
                )

        if len(records) > self.max_events:
            raise InstrumentationError("instrumentation record count exceeds Phase 6 ceiling")

        record_ids = [record.record_id for record in records]
        fail_closed_record_ids = [
            record.record_id for record in records if record.status in {"abstain", "fail_closed", "blocked"}
        ]
        domain_record_ids: defaultdict[str, list[str]] = defaultdict(list)
        for record in records:
            domain = source_domain_by_entry.get(record.source_entry_id)
            if domain:
                domain_record_ids[domain].append(record.record_id)

        metrics: list[InstrumentationMetric] = []
        metric_specs = [
            ("record_count", MetricValueType.COUNT, len(records)),
            ("fail_closed_count", MetricValueType.COUNT, len(fail_closed_record_ids)),
            ("world_entity_count", MetricValueType.COUNT, sum(1 for item in records if item.record_kind == InstrumentationRecordKind.WORLD_ENTITY)),
            ("future_count", MetricValueType.COUNT, sum(1 for item in records if item.record_kind == InstrumentationRecordKind.FUTURE)),
            ("simulation_count", MetricValueType.COUNT, sum(1 for item in records if item.record_kind == InstrumentationRecordKind.SIMULATION)),
            ("domain_count", MetricValueType.COUNT, len(domain_record_ids)),
        ]
        for metric_name, value_type, numeric_value in metric_specs:
            payload = {"metric_name": metric_name, "value_text": str(numeric_value), "numeric_value": numeric_value}
            metric_id = f"instrument_metric::{stable_hash_payload(payload)[:12]}"
            provenance = build_provenance_bundle(
                entity_kind="instrumentation_metric",
                entity_id=metric_id,
                origin_kind="constructed",
                links=[
                    {
                        "role": "instrumentation",
                        "ref_id": metric_id,
                        "ref_kind": "instrumentation_metric",
                        "source_path": "phase6/instrumentation",
                    }
                ],
            )
            metrics.append(
                InstrumentationMetric(
                    metric_id=metric_id,
                    metric_name=metric_name,
                    value_type=value_type,
                    value_text=str(numeric_value),
                    numeric_value=numeric_value,
                    provenance=provenance,
                    metric_hash=stable_hash_payload({**payload, "metric_id": metric_id}),
                )
            )

        summaries: list[InstrumentationSummary] = []
        summary_specs: list[tuple[InstrumentationSummaryKind, str, list[str], list[str]]] = [
            (InstrumentationSummaryKind.COVERAGE, "complete", record_ids, [metric.metric_id for metric in metrics]),
            (
                InstrumentationSummaryKind.FAIL_CLOSED,
                "observed" if fail_closed_record_ids else "clear",
                fail_closed_record_ids,
                [metric.metric_id for metric in metrics if metric.metric_name == "fail_closed_count"],
            ),
        ]
        for domain, ids in sorted(domain_record_ids.items()):
            summary_specs.append(
                (
                    InstrumentationSummaryKind.DOMAIN,
                    domain,
                    ids,
                    [metric.metric_id for metric in metrics if metric.metric_name in {"record_count", "domain_count"}],
                )
            )
        for summary_kind, status, covered_record_ids, metric_ids in summary_specs:
            payload = {
                "summary_kind": summary_kind.value,
                "status": status,
                "covered_record_ids": sorted(covered_record_ids),
                "metric_ids": sorted(metric_ids),
            }
            summary_id = f"instrument_summary::{stable_hash_payload(payload)[:12]}"
            provenance = build_provenance_bundle(
                entity_kind="instrumentation_summary",
                entity_id=summary_id,
                origin_kind="constructed",
                links=[
                    {
                        "role": "instrumentation",
                        "ref_id": summary_id,
                        "ref_kind": "instrumentation_summary",
                        "source_path": "phase6/instrumentation",
                    }
                ],
            )
            summaries.append(
                InstrumentationSummary(
                    summary_id=summary_id,
                    summary_kind=summary_kind,
                    status=status,
                    covered_record_ids=tuple(sorted(covered_record_ids)),
                    metric_ids=tuple(sorted(metric_ids)),
                    provenance=provenance,
                    summary_hash=stable_hash_payload({**payload, "summary_id": summary_id}),
                )
            )

        snapshot = InstrumentationSnapshot(
            schema="agifcore.phase_06.instrumentation.v1",
            records=tuple(records),
            summaries=tuple(summaries),
            metrics=tuple(metrics),
            snapshot_hash=stable_hash_payload(
                {
                    "records": [record.to_dict() for record in records],
                    "summaries": [summary.to_dict() for summary in summaries],
                    "metrics": [metric.to_dict() for metric in metrics],
                }
            ),
        )
        if canonical_size_bytes(snapshot.to_dict()) > self.max_state_bytes:
            raise InstrumentationError("instrumentation state exceeds Phase 6 byte ceiling")
        return snapshot
