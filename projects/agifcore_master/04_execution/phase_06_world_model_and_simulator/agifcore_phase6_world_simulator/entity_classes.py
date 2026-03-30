from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import datetime, timezone
from enum import StrEnum
from hashlib import sha256
from typing import Any, Mapping

MAX_ENTITY_COUNT = 256
MAX_TARGET_DOMAIN_OBJECTS = 128
MAX_CANDIDATE_FUTURES = 24
MAX_BRANCH_DEPTH = 4
MAX_LANE_GROUPS = 32
MAX_INSTRUMENTATION_EVENTS = 160
MAX_USEFULNESS_INPUTS = 64
MAX_PROVENANCE_LINKS = 16
MINIMUM_QUALIFIED_DOMAINS = 4

ALLOWED_PROVENANCE_ROLES = {
    "source_memory",
    "review",
    "graph",
    "transfer",
    "support_selection",
    "working_memory",
    "world_model",
    "future",
    "simulation",
    "lane",
    "instrumentation",
    "rollback",
    "replay",
    "workspace",
    "source",
    "domain",
}


class Phase6EntityError(ValueError):
    """Raised when a Phase 6 contract or typed payload is malformed."""


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clamp_score(value: float, *, digits: int = 6) -> float:
    return round(min(1.0, max(0.0, float(value))), digits)


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


def stable_hash_payload(payload: Mapping[str, Any]) -> str:
    return sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase6EntityError(f"{field_name} must be a non-empty string")
    return value


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase6EntityError(f"{field_name} must be a mapping")
    return dict(value)


def require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise Phase6EntityError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        normalized = require_non_empty_str(item, f"{field_name}[]")
        if normalized in seen:
            raise Phase6EntityError(f"{field_name} contains duplicate entries")
        seen.add(normalized)
        result.append(normalized)
    return result


def require_schema(payload: Mapping[str, Any], expected_schema: str, field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    if payload_map.get("schema") != expected_schema:
        raise Phase6EntityError(f"{field_name} schema mismatch: expected {expected_schema}")
    return payload_map


def _serialize_value(value: Any) -> Any:
    if isinstance(value, StrEnum):
        return value.value
    if is_dataclass(value):
        return {field_info.name: _serialize_value(getattr(value, field_info.name)) for field_info in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): _serialize_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_serialize_value(item) for item in value]
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    return deepcopy(value)


def trust_band_confidence(trust_band: str) -> float:
    normalized = require_non_empty_str(trust_band, "trust_band").lower()
    table = {
        "policy": 0.92,
        "reviewed": 0.82,
        "bounded_local": 0.72,
        "experimental": 0.38,
        "unknown": 0.5,
    }
    return clamp_score(table.get(normalized, table["unknown"]))


@dataclass(frozen=True, slots=True)
class Phase6ProvenanceLink:
    role: str
    ref_id: str
    ref_kind: str
    source_path: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class Phase6ProvenanceBundle:
    entity_kind: str
    entity_id: str
    origin_kind: str
    links: tuple[Phase6ProvenanceLink, ...]
    inherited_from: tuple[str, ...]
    created_at: str
    provenance_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


def _normalize_provenance_link(value: Phase6ProvenanceLink | Mapping[str, Any]) -> Phase6ProvenanceLink:
    if isinstance(value, Phase6ProvenanceLink):
        link = value
    else:
        payload = require_mapping(value, "provenance_link")
        link = Phase6ProvenanceLink(
            role=require_non_empty_str(payload.get("role"), "role"),
            ref_id=require_non_empty_str(payload.get("ref_id"), "ref_id"),
            ref_kind=require_non_empty_str(payload.get("ref_kind"), "ref_kind"),
            source_path=require_non_empty_str(payload.get("source_path"), "source_path"),
            metadata=require_mapping(payload.get("metadata", {}), "metadata"),
        )
    if link.role not in ALLOWED_PROVENANCE_ROLES:
        raise Phase6EntityError(f"unsupported provenance role: {link.role}")
    return link


def build_provenance_bundle(
    *,
    entity_kind: str,
    entity_id: str,
    origin_kind: str,
    links: list[Phase6ProvenanceLink | Mapping[str, Any]],
    inherited_from: list[str] | None = None,
) -> Phase6ProvenanceBundle:
    normalized_links = tuple(_normalize_provenance_link(item) for item in links)
    if not normalized_links:
        raise Phase6EntityError("links must contain at least one provenance link")
    if len(normalized_links) > MAX_PROVENANCE_LINKS:
        raise Phase6EntityError("provenance link fanout exceeds Phase 6 ceiling")
    seen_pairs: set[tuple[str, str]] = set()
    for link in normalized_links:
        pair = (link.role, link.ref_id)
        if pair in seen_pairs:
            raise Phase6EntityError("duplicate provenance role/ref_id pair")
        seen_pairs.add(pair)
    normalized_inherited_from = tuple(require_unique_str_list(inherited_from or [], "inherited_from"))
    payload = {
        "entity_kind": require_non_empty_str(entity_kind, "entity_kind"),
        "entity_id": require_non_empty_str(entity_id, "entity_id"),
        "origin_kind": require_non_empty_str(origin_kind, "origin_kind"),
        "links": [link.to_dict() for link in normalized_links],
        "inherited_from": list(normalized_inherited_from),
    }
    return Phase6ProvenanceBundle(
        entity_kind=payload["entity_kind"],
        entity_id=payload["entity_id"],
        origin_kind=payload["origin_kind"],
        links=normalized_links,
        inherited_from=normalized_inherited_from,
        created_at=utc_timestamp(),
        provenance_hash=stable_hash_payload(payload),
    )


def bundle_from_dict(payload: Mapping[str, Any]) -> Phase6ProvenanceBundle:
    payload_map = require_mapping(payload, "provenance_bundle")
    links = [_normalize_provenance_link(item) for item in payload_map.get("links", [])]
    bundle = build_provenance_bundle(
        entity_kind=payload_map.get("entity_kind"),
        entity_id=payload_map.get("entity_id"),
        origin_kind=payload_map.get("origin_kind", "constructed"),
        links=links,
        inherited_from=list(payload_map.get("inherited_from", [])),
    )
    created_at = payload_map.get("created_at")
    if created_at is not None:
        bundle = Phase6ProvenanceBundle(
            entity_kind=bundle.entity_kind,
            entity_id=bundle.entity_id,
            origin_kind=bundle.origin_kind,
            links=bundle.links,
            inherited_from=bundle.inherited_from,
            created_at=require_non_empty_str(created_at, "created_at"),
            provenance_hash=bundle.provenance_hash,
        )
    provenance_hash = payload_map.get("provenance_hash")
    if provenance_hash is not None:
        normalized_hash = require_non_empty_str(provenance_hash, "provenance_hash")
        if normalized_hash != bundle.provenance_hash:
            raise Phase6EntityError("provenance_hash does not match canonical Phase 6 bundle payload")
        bundle = Phase6ProvenanceBundle(
            entity_kind=bundle.entity_kind,
            entity_id=bundle.entity_id,
            origin_kind=bundle.origin_kind,
            links=bundle.links,
            inherited_from=bundle.inherited_from,
            created_at=bundle.created_at,
            provenance_hash=normalized_hash,
        )
    return bundle


def require_roles(bundle: Phase6ProvenanceBundle, required_roles: tuple[str, ...]) -> None:
    present = {link.role for link in bundle.links}
    missing = [role for role in required_roles if role not in present]
    if missing:
        raise Phase6EntityError(f"missing required provenance roles: {missing}")


def provenance_score(bundle: Phase6ProvenanceBundle) -> float:
    roles = {link.role for link in bundle.links}
    score = 0.0
    if "source_memory" in roles:
        score += 0.25
    if "review" in roles:
        score += 0.25
    if "graph" in roles or "transfer" in roles:
        score += 0.2
    if "simulation" in roles or "lane" in roles:
        score += 0.15
    if "instrumentation" in roles:
        score += 0.1
    if bundle.inherited_from:
        score += 0.05
    return clamp_score(score)


class StateValueType(StrEnum):
    LABEL = "label"
    SCORE = "score"
    FLAG = "flag"
    COUNT = "count"


class WorldEntityKind(StrEnum):
    DESCRIPTOR_SUPPORT = "descriptor_support"
    CONCEPT_SUPPORT = "concept_support"
    PROCEDURAL_SKILL = "procedural_skill"
    TRANSFER_PROJECTION = "transfer_projection"
    TARGET_DOMAIN_OBJECT = "target_domain_object"
    REVIEW_SIGNAL = "review_signal"


class WorldRelationKind(StrEnum):
    PROJECTS_TO_TARGET = "projects_to_target"
    SUPPORTED_BY_MEMORY = "supported_by_memory"
    ENABLES_FUTURE = "enables_future"
    CONFLICTS_WITH = "conflicts_with"
    FOCUSES_ON = "focuses_on"


class WorldEntityStatus(StrEnum):
    REVIEW_ONLY = "review_only"
    HELD = "held"
    BLOCKED = "blocked"
    EXECUTION_DISABLED = "execution_disabled"


class WorldOperatorKind(StrEnum):
    TARGET_PROJECTION = "target_projection"
    FUTURE_EVALUATION = "future_evaluation"
    FAULT_REVIEW = "fault_review"
    PRESSURE_REVIEW = "pressure_review"
    CONFLICT_REVIEW = "conflict_review"
    OVERLOAD_REVIEW = "overload_review"


class WorldOperatorStatus(StrEnum):
    READY_FOR_REVIEW = "ready_for_review"
    HOLD_REQUIRED = "hold_required"
    BLOCKED = "blocked"
    EXECUTION_DISABLED = "execution_disabled"


class SimulationOutcome(StrEnum):
    REVIEW_ONLY_PROJECTED = "review_only_projected"
    HOLD_PROJECTED = "hold_projected"
    ABSTAIN = "abstain"


class FaultOutcome(StrEnum):
    CLEAR = "clear"
    DEGRADED = "degraded"
    FAIL_CLOSED = "fail_closed"


class PressureOutcome(StrEnum):
    CLEAR = "clear"
    STRESSED = "stressed"
    FAIL_CLOSED = "fail_closed"


class ConflictOutcome(StrEnum):
    CLEAR = "clear"
    HOLD = "hold"
    BLOCKED = "blocked"
    ABSTAIN = "abstain"


class OverloadOutcome(StrEnum):
    CLEAR = "clear"
    OVERLOADED = "overloaded"
    UNSAFE = "unsafe"


class InstrumentationRecordKind(StrEnum):
    WORLD_ENTITY = "world_entity"
    FUTURE = "future"
    SIMULATION = "simulation"
    FAULT = "fault"
    PRESSURE = "pressure"
    CONFLICT = "conflict"
    OVERLOAD = "overload"


class InstrumentationSummaryKind(StrEnum):
    COVERAGE = "coverage"
    FAIL_CLOSED = "fail_closed"
    DOMAIN = "domain"


class MetricValueType(StrEnum):
    COUNT = "count"
    SCORE = "score"
    FLAG = "flag"
    TEXT = "text"


class UsefulnessOutcome(StrEnum):
    QUALIFIED = "qualified"
    INSUFFICIENT = "insufficient"


@dataclass(frozen=True, slots=True)
class StateValue:
    field_name: str
    value_type: StateValueType
    value_text: str
    numeric_value: float | int | None
    state_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


def build_state_value(
    *,
    field_name: str,
    value_type: StateValueType,
    value_text: str,
    numeric_value: float | int | None = None,
) -> StateValue:
    payload = {
        "field_name": require_non_empty_str(field_name, "field_name"),
        "value_type": value_type.value,
        "value_text": require_non_empty_str(value_text, "value_text"),
        "numeric_value": numeric_value,
    }
    return StateValue(
        field_name=payload["field_name"],
        value_type=value_type,
        value_text=payload["value_text"],
        numeric_value=numeric_value,
        state_hash=stable_hash_payload(payload),
    )


@dataclass(frozen=True, slots=True)
class WorldOperator:
    operator_id: str
    operator_kind: WorldOperatorKind
    status: WorldOperatorStatus
    bounded_confidence: float
    execution_enabled: bool
    reason_codes: tuple[str, ...]
    operator_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


def build_world_operator(
    *,
    operator_kind: WorldOperatorKind,
    status: WorldOperatorStatus,
    bounded_confidence: float,
    reason_codes: list[str],
) -> WorldOperator:
    payload = {
        "operator_kind": operator_kind.value,
        "status": status.value,
        "bounded_confidence": clamp_score(bounded_confidence),
        "execution_enabled": False,
        "reason_codes": require_unique_str_list(reason_codes, "reason_codes"),
    }
    operator_id = f"phase6.operator.{stable_hash_payload(payload)[:12]}"
    return WorldOperator(
        operator_id=operator_id,
        operator_kind=operator_kind,
        status=status,
        bounded_confidence=payload["bounded_confidence"],
        execution_enabled=False,
        reason_codes=tuple(payload["reason_codes"]),
        operator_hash=stable_hash_payload({**payload, "operator_id": operator_id}),
    )


@dataclass(frozen=True, slots=True)
class WorldEntity:
    entity_id: str
    entity_kind: WorldEntityKind
    label: str
    target_domain: str | None
    status: WorldEntityStatus
    world_confidence: float
    source_refs: tuple[str, ...]
    state_values: tuple[StateValue, ...]
    operators: tuple[WorldOperator, ...]
    replay_safe: bool
    provenance: Phase6ProvenanceBundle
    entity_hash: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class WorldRelation:
    relation_id: str
    relation_kind: WorldRelationKind
    source_entity_id: str
    target_entity_id: str
    relation_strength: float
    reason_codes: tuple[str, ...]
    replay_safe: bool
    provenance: Phase6ProvenanceBundle
    relation_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class WorldModelSnapshot:
    schema: str
    entity_capacity: int
    relation_capacity: int
    phase4_interfaces: tuple[str, ...]
    phase5_interfaces: tuple[str, ...]
    entities: tuple[WorldEntity, ...]
    relations: tuple[WorldRelation, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class TargetDomainObject:
    object_id: str
    domain_id: str
    label: str
    category: str
    provenance: Phase6ProvenanceBundle
    object_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class TargetDomainStructure:
    domain_id: str
    domain_name: str
    prefixes: tuple[str, ...]
    descriptor_tokens: tuple[str, ...]
    minimum_signal_groups: int
    object_templates: tuple[str, ...]
    objects: tuple[TargetDomainObject, ...]
    requires_target_match: bool
    provenance: Phase6ProvenanceBundle
    structure_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class CandidateFuture:
    future_id: str
    source_entity_id: str
    target_domain: str
    relation_id: str
    branch_depth: int
    parent_future_id: str | None
    projected_outcome: SimulationOutcome
    bounded_confidence: float
    state_codes: tuple[str, ...]
    reason_codes: tuple[str, ...]
    provenance: Phase6ProvenanceBundle
    future_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class CandidateFutureSnapshot:
    schema: str
    max_futures: int
    max_branch_depth: int
    source_world_model_hash: str
    futures: tuple[CandidateFuture, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SimulationTraceStep:
    step_id: str
    step_kind: str
    detail: str
    decision: str
    supporting_refs: tuple[str, ...]
    step_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class WhatIfSimulationEntry:
    simulation_entry_id: str
    future_id: str
    source_entity_id: str
    target_domain: str
    branch_depth: int
    outcome: SimulationOutcome
    fail_closed: bool
    confidence: float
    considered_relation_ids: tuple[str, ...]
    trace_steps: tuple[SimulationTraceStep, ...]
    reason_codes: tuple[str, ...]
    provenance: Phase6ProvenanceBundle
    entry_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class WhatIfSimulationSnapshot:
    schema: str
    source_world_model_hash: str
    source_future_hash: str
    entries: tuple[WhatIfSimulationEntry, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class FaultCase:
    fault_case_id: str
    fault_kind: str
    severity: float
    description: str
    provenance: Phase6ProvenanceBundle
    case_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class FaultLaneEntry:
    fault_entry_id: str
    source_simulation_entry_id: str
    source_entity_id: str
    outcome: FaultOutcome
    fault_cases: tuple[FaultCase, ...]
    fail_closed: bool
    reason_codes: tuple[str, ...]
    provenance: Phase6ProvenanceBundle
    entry_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class FaultLaneSnapshot:
    schema: str
    source_simulation_hash: str
    entries: tuple[FaultLaneEntry, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class PressureScenario:
    pressure_scenario_id: str
    scenario_kind: str
    pressure_score: float
    target_domain: str | None
    reason_codes: tuple[str, ...]
    provenance: Phase6ProvenanceBundle
    scenario_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class PressureLaneEntry:
    pressure_entry_id: str
    source_simulation_entry_id: str
    source_fault_entry_id: str | None
    outcome: PressureOutcome
    scenarios: tuple[PressureScenario, ...]
    working_memory_utilization: float
    provenance: Phase6ProvenanceBundle
    entry_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class PressureLaneSnapshot:
    schema: str
    source_fault_hash: str
    entries: tuple[PressureLaneEntry, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ConflictResult:
    conflict_result_id: str
    conflict_kind: str
    outcome: ConflictOutcome
    source_transfer_id: str | None
    source_simulation_entry_id: str
    conflicting_domain: str | None
    conflict_score: float
    reason_codes: tuple[str, ...]
    provenance: Phase6ProvenanceBundle
    result_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ConflictLaneEntry:
    conflict_entry_id: str
    source_simulation_entry_id: str
    source_pressure_entry_id: str | None
    outcome: ConflictOutcome
    results: tuple[ConflictResult, ...]
    fail_closed: bool
    provenance: Phase6ProvenanceBundle
    entry_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ConflictLaneSnapshot:
    schema: str
    source_pressure_hash: str
    entries: tuple[ConflictLaneEntry, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class OverloadResult:
    overload_result_id: str
    outcome: OverloadOutcome
    load_score: float
    conflict_score: float
    threshold: float
    reason_codes: tuple[str, ...]
    provenance: Phase6ProvenanceBundle
    result_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class OverloadLaneEntry:
    overload_entry_id: str
    source_pressure_entry_id: str
    source_conflict_entry_id: str | None
    outcome: OverloadOutcome
    results: tuple[OverloadResult, ...]
    provenance: Phase6ProvenanceBundle
    entry_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class OverloadLaneSnapshot:
    schema: str
    source_pressure_hash: str
    source_conflict_hash: str
    entries: tuple[OverloadLaneEntry, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class InstrumentationRecord:
    record_id: str
    record_kind: InstrumentationRecordKind
    source_entry_id: str
    status: str
    reason_codes: tuple[str, ...]
    numeric_score: float
    provenance: Phase6ProvenanceBundle
    record_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class InstrumentationSummary:
    summary_id: str
    summary_kind: InstrumentationSummaryKind
    status: str
    covered_record_ids: tuple[str, ...]
    metric_ids: tuple[str, ...]
    provenance: Phase6ProvenanceBundle
    summary_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class InstrumentationMetric:
    metric_id: str
    metric_name: str
    value_type: MetricValueType
    value_text: str
    numeric_value: float | int | None
    provenance: Phase6ProvenanceBundle
    metric_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class InstrumentationSnapshot:
    schema: str
    records: tuple[InstrumentationRecord, ...]
    summaries: tuple[InstrumentationSummary, ...]
    metrics: tuple[InstrumentationMetric, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class UsefulnessDomainScore:
    domain_id: str
    domain_name: str
    weighted_score: float
    evidence_inputs: int
    outcome: UsefulnessOutcome
    reason_codes: tuple[str, ...]
    provenance: Phase6ProvenanceBundle
    score_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class UsefulnessEvaluationSnapshot:
    schema: str
    qualified_domain_count: int
    minimum_qualified_domains: int
    overall_outcome: UsefulnessOutcome
    domain_scores: tuple[UsefulnessDomainScore, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)
