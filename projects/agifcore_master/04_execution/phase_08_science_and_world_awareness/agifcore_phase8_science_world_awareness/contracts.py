from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Any, Mapping

MAX_SELECTED_PRIORS = 12
MAX_INFERENCE_CANDIDATES = 16
MAX_REGION_CANDIDATES = 8
MAX_CAUSAL_CHAIN_STEPS = 10
MAX_CURRENT_WORLD_EVIDENCE_INPUTS = 24
MAX_VISIBLE_REASONING_CHARACTERS = 1200
MAX_REFLECTION_RECORDS = 6
MAX_REASON_CODES = 12
MAX_MATCHED_TERMS = 12
MAX_SUMMARY_ITEMS_PER_FIELD = 4


class Phase8ScienceWorldAwarenessError(ValueError):
    """Raised when Phase 8 science/world runtime state violates the contract."""


def clamp_score(value: float, *, digits: int = 6) -> float:
    return round(min(1.0, max(0.0, float(value))), digits)


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8"))


def stable_hash_payload(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase8ScienceWorldAwarenessError(f"{field_name} must be a non-empty string")
    return value


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase8ScienceWorldAwarenessError(f"{field_name} must be a mapping")
    return dict(value)


def require_unique_str_list(
    value: Any,
    field_name: str,
    *,
    max_length: int | None = None,
) -> list[str]:
    if not isinstance(value, list):
        raise Phase8ScienceWorldAwarenessError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        normalized = require_non_empty_str(item, f"{field_name}[]")
        if normalized in seen:
            raise Phase8ScienceWorldAwarenessError(f"{field_name} contains duplicate entries")
        seen.add(normalized)
        result.append(normalized)
        if max_length is not None and len(result) > max_length:
            raise Phase8ScienceWorldAwarenessError(f"{field_name} exceeds the Phase 8 ceiling of {max_length}")
    return result


def require_schema(payload: Mapping[str, Any], expected_schema: str, field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    if payload_map.get("schema") != expected_schema:
        raise Phase8ScienceWorldAwarenessError(
            f"{field_name} schema mismatch: expected {expected_schema}"
        )
    return payload_map


def require_phase7_intake_state(payload: Mapping[str, Any], field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    required = (
        "conversation_id",
        "turn_id",
        "raw_text",
        "normalized_text",
        "active_context_refs",
        "token_count",
        "character_count",
        "contains_code_block",
        "ends_with_question",
        "intake_hash",
    )
    for key in required:
        if key not in payload_map:
            raise Phase8ScienceWorldAwarenessError(f"{field_name} missing required field: {key}")
    require_non_empty_str(payload_map["conversation_id"], f"{field_name}.conversation_id")
    require_non_empty_str(payload_map["turn_id"], f"{field_name}.turn_id")
    require_non_empty_str(payload_map["raw_text"], f"{field_name}.raw_text")
    require_non_empty_str(payload_map["normalized_text"], f"{field_name}.normalized_text")
    require_non_empty_str(payload_map["intake_hash"], f"{field_name}.intake_hash")
    if not isinstance(payload_map["active_context_refs"], (list, tuple)):
        raise Phase8ScienceWorldAwarenessError(f"{field_name}.active_context_refs must be a list or tuple")
    if not isinstance(payload_map["token_count"], int) or payload_map["token_count"] < 0:
        raise Phase8ScienceWorldAwarenessError(f"{field_name}.token_count must be a non-negative integer")
    return payload_map


def require_support_selection_result(payload: Mapping[str, Any], field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    required = (
        "query_id",
        "status",
        "reason",
        "selected_candidate_ids",
        "ranked_candidates",
        "blocked_candidate_ids",
        "evaluated_candidate_count",
        "generated_at",
    )
    for key in required:
        if key not in payload_map:
            raise Phase8ScienceWorldAwarenessError(f"{field_name} missing required field: {key}")
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


class RequestType(StrEnum):
    CAUSAL_EXPLANATION = "causal_explanation"
    DERIVED_ESTIMATE = "derived_estimate"
    STATUS_CHECK = "status_check"
    DEFINITION = "definition"
    COMPARISON = "comparison"
    CLASSIFICATION = "classification"
    SCIENCE_EXPLANATION = "science_explanation"
    UNKNOWN = "unknown"


class EntityClass(StrEnum):
    PLACE = "place"
    PHYSICAL_SYSTEM = "physical_system"
    MATERIAL = "material"
    ORGANISM = "organism"
    PROCESS = "process"
    MEASUREMENT = "measurement"
    ARTIFACT = "artifact"
    UNKNOWN = "unknown"


class RegionKind(StrEnum):
    TARGET_DOMAIN = "target_domain"
    WORLD_ENTITY = "world_entity"
    ACTIVE_CONTEXT = "active_context"
    INFERRED_CONTEXT = "inferred_context"


class ChainStepKind(StrEnum):
    REQUEST_FRAME = "request_frame"
    REGION_CONTEXT = "region_context"
    PRIOR_APPLICATION = "prior_application"
    WORLD_SUPPORT = "world_support"
    SIMULATION_CHECK = "simulation_check"
    USEFULNESS_CHECK = "usefulness_check"
    MISSING_VARIABLE = "missing_variable"


class CurrentWorldDecision(StrEnum):
    NOT_CURRENT_WORLD_REQUEST = "not_current_world_request"
    BOUNDED_LOCAL_SUPPORT = "bounded_local_support"
    NEEDS_FRESH_INFORMATION = "needs_fresh_information"
    LIVE_MEASUREMENT_REQUIRED = "live_measurement_required"
    INSUFFICIENT_LOCAL_EVIDENCE = "insufficient_local_evidence"


class UncertaintyBand(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class ReflectionKind(StrEnum):
    WEAK_PRIOR_CHOICE = "weak_prior_choice"
    MISSING_VARIABLE = "missing_variable"
    FALSIFIER = "falsifier"
    NEXT_VERIFICATION_STEP = "next_verification_step"
    UNCERTAINTY_INCREASE = "uncertainty_increase"


@dataclass(frozen=True, slots=True)
class ScientificPriorCell:
    cell_id: str
    family_name: str
    principle_id: str
    seed_topic: str
    plain_language_law: str
    variables: tuple[str, ...]
    causal_mechanism: str
    scope_limits: str
    failure_case: str
    worked_example: str
    transfer_hint: str
    cue_terms: tuple[str, ...]
    hidden_variable_hints: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    cell_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelectedScientificPrior:
    selection_id: str
    cell_id: str
    principle_id: str
    matched_cue_terms: tuple[str, ...]
    matched_hidden_variables: tuple[str, ...]
    relevance_score: float
    reason_codes: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    selection_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ScientificPriorsSnapshot:
    schema: str
    request_id: str
    available_prior_count: int
    selected_prior_count: int
    selected_prior_ids: tuple[str, ...]
    selected_priors: tuple[SelectedScientificPrior, ...]
    selected_cells: tuple[ScientificPriorCell, ...]
    selection_notes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class EntityRequestCandidate:
    candidate_id: str
    entity_label: str
    entity_class: EntityClass
    request_type: RequestType
    science_topic_cues: tuple[str, ...]
    matched_terms: tuple[str, ...]
    hidden_variable_cues: tuple[str, ...]
    target_domain_hint: str | None
    region_hint: str | None
    live_current_requested: bool
    ambiguous_request: bool
    confidence: float
    reason_codes: tuple[str, ...]
    candidate_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class EntityRequestInferenceSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    raw_text_hash: str
    normalized_text: str
    extracted_terms: tuple[str, ...]
    candidate_count: int
    selected_candidate_id: str | None
    candidates: tuple[EntityRequestCandidate, ...]
    science_topic_cues: tuple[str, ...]
    hidden_variable_cues: tuple[str, ...]
    support_state_hint: str
    knowledge_gap_reason_hint: str
    inference_notes: tuple[str, ...]
    inference_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class WorldRegionCandidate:
    region_id: str
    region_label: str
    region_kind: RegionKind
    target_domain: str | None
    supporting_refs: tuple[str, ...]
    matched_terms: tuple[str, ...]
    reason_codes: tuple[str, ...]
    confidence: float
    candidate_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class WorldRegionSelectionSnapshot:
    schema: str
    request_id: str
    candidate_count: int
    selected_region_id: str | None
    candidates: tuple[WorldRegionCandidate, ...]
    unresolved: bool
    reason_codes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class CausalChainStep:
    step_id: str
    step_index: int
    step_kind: ChainStepKind
    statement: str
    principle_ref: str | None
    region_ref: str | None
    world_entity_ref: str | None
    simulation_ref: str | None
    usefulness_ref: str | None
    evidence_refs: tuple[str, ...]
    missing_variables: tuple[str, ...]
    fail_closed: bool
    reason_codes: tuple[str, ...]
    step_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class CausalChainSnapshot:
    schema: str
    request_id: str
    chain_id: str
    step_count: int
    steps: tuple[CausalChainStep, ...]
    principle_refs: tuple[str, ...]
    region_ref: str | None
    world_entity_refs: tuple[str, ...]
    simulation_refs: tuple[str, ...]
    usefulness_ref: str | None
    missing_variables: tuple[str, ...]
    fail_closed: bool
    weakest_link_reason: str
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class BoundedCurrentWorldSnapshot:
    schema: str
    request_id: str
    decision: CurrentWorldDecision
    live_current_requested: bool
    needs_fresh_information: bool
    live_measurement_required: bool
    exact_current_fact_allowed: bool
    bounded_local_support_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    evidence_input_count: int
    reason_codes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class VisibleReasoningSummary:
    schema: str
    request_id: str
    what_is_known: tuple[str, ...]
    what_is_inferred: tuple[str, ...]
    uncertainty: tuple[str, ...]
    what_would_verify: tuple[str, ...]
    principle_refs: tuple[str, ...]
    causal_chain_ref: str
    uncertainty_band: UncertaintyBand
    live_measurement_required: bool
    character_count: int
    evidence_refs: tuple[str, ...]
    summary_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ScienceReflectionRecord:
    record_id: str
    kind: ReflectionKind
    note: str
    source_ref: str
    next_verification_step: str | None
    increases_uncertainty: bool
    record_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ScienceReflectionSnapshot:
    schema: str
    request_id: str
    record_count: int
    records: tuple[ScienceReflectionRecord, ...]
    uncertainty_should_increase: bool
    reflection_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ScienceWorldTurnSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    phase4_interfaces: tuple[str, ...]
    phase5_interfaces: tuple[str, ...]
    phase6_interfaces: tuple[str, ...]
    phase7_interfaces: tuple[str, ...]
    entity_request_inference: EntityRequestInferenceSnapshot
    scientific_priors: ScientificPriorsSnapshot
    world_region_selection: WorldRegionSelectionSnapshot
    causal_chain: CausalChainSnapshot
    bounded_current_world_reasoning: BoundedCurrentWorldSnapshot
    visible_reasoning_summary: VisibleReasoningSummary
    science_reflection: ScienceReflectionSnapshot
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)
