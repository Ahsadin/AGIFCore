from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Any, Mapping

MAX_TEACHING_SECTIONS = 6
MAX_COMPARISON_AXES = 5
MAX_PLANNING_STEPS = 10
MAX_SYNTHESIS_INPUTS = 12
MAX_ANALOGIES_PER_RESPONSE = 2
MAX_CONCEPT_COMPOSITION_ELEMENTS = 6
MAX_CROSS_DOMAIN_COMPOSITION_ELEMENTS = 4
MAX_AUDIENCE_PROFILE_BRANCHES = 4
MAX_REASON_CODES = 12
MAX_TRACE_REFS = 24
MAX_LANE_NOTES = 8
MAX_KEY_POINTS_PER_SECTION = 4
MAX_UNCERTAINTY_ITEMS = 4
MAX_PUBLIC_RESPONSE_CHARACTERS = 2600


class Phase9RichExpressionError(ValueError):
    """Raised when Phase 9 rich-expression runtime state violates the contract."""


def clamp_score(value: float, *, digits: int = 6) -> float:
    return round(min(1.0, max(0.0, float(value))), digits)


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return len(encoded)


def stable_hash_payload(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


def make_trace_ref(prefix: str, payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    clean_prefix = require_non_empty_str(prefix, "prefix").replace(" ", "_")
    return f"{clean_prefix}::{stable_hash_payload(payload)[:12]}"


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase9RichExpressionError(f"{field_name} must be a non-empty string")
    return value


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase9RichExpressionError(f"{field_name} must be a mapping")
    return dict(value)


def require_unique_str_list(
    value: Any,
    field_name: str,
    *,
    max_length: int | None = None,
) -> list[str]:
    if not isinstance(value, list):
        raise Phase9RichExpressionError(f"{field_name} must be a list")
    result: list[str] = []
    seen: set[str] = set()
    for item in value:
        normalized = require_non_empty_str(item, f"{field_name}[]")
        if normalized in seen:
            raise Phase9RichExpressionError(f"{field_name} contains duplicate entries")
        seen.add(normalized)
        result.append(normalized)
        if max_length is not None and len(result) > max_length:
            raise Phase9RichExpressionError(f"{field_name} exceeds the Phase 9 ceiling of {max_length}")
    return result


def require_schema(payload: Mapping[str, Any], expected_schema: str, field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    if payload_map.get("schema") != expected_schema:
        raise Phase9RichExpressionError(f"{field_name} schema mismatch: expected {expected_schema}")
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
            raise Phase9RichExpressionError(f"{field_name} missing required field: {key}")
    require_non_empty_str(payload_map["conversation_id"], f"{field_name}.conversation_id")
    require_non_empty_str(payload_map["turn_id"], f"{field_name}.turn_id")
    require_non_empty_str(payload_map["raw_text"], f"{field_name}.raw_text")
    require_non_empty_str(payload_map["normalized_text"], f"{field_name}.normalized_text")
    require_non_empty_str(payload_map["intake_hash"], f"{field_name}.intake_hash")
    if not isinstance(payload_map["active_context_refs"], (list, tuple)):
        raise Phase9RichExpressionError(f"{field_name}.active_context_refs must be a list or tuple")
    if not isinstance(payload_map["token_count"], int) or payload_map["token_count"] < 0:
        raise Phase9RichExpressionError(f"{field_name}.token_count must be a non-negative integer")
    if not isinstance(payload_map["character_count"], int) or payload_map["character_count"] < 0:
        raise Phase9RichExpressionError(f"{field_name}.character_count must be a non-negative integer")
    return payload_map


def coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    if isinstance(value, (int, float)):
        return bool(value)
    return bool(value)


def bounded_unique(
    values: list[str],
    *,
    ceiling: int,
    field_name: str,
) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        normalized = str(item).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
        if len(result) >= ceiling:
            break
    if not result:
        raise Phase9RichExpressionError(f"{field_name} must include at least one value")
    return tuple(result)


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


class ExpressionLane(StrEnum):
    TEACHING = "teaching"
    COMPARISON = "comparison"
    PLANNING = "planning"
    SYNTHESIS = "synthesis"
    ANALOGY = "analogy"
    CONCEPT_COMPOSITION = "concept_composition"
    CROSS_DOMAIN_COMPOSITION = "cross_domain_composition"


class AudienceProfile(StrEnum):
    NOVICE = "novice"
    PRACTITIONER = "practitioner"
    TECHNICAL = "technical"
    EXECUTIVE = "executive"


class TerminologyDensity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class BrevityLevel(StrEnum):
    BRIEF = "brief"
    BALANCED = "balanced"
    DETAILED = "detailed"


class UncertaintyLevel(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class AnalogyMode(StrEnum):
    STRUCTURAL = "structural"
    EXPLANATORY = "explanatory"
    BOUNDED_BRIDGE = "bounded_bridge"


@dataclass(frozen=True, slots=True)
class TeachingSection:
    section_id: str
    title: str
    objective: str
    key_points: tuple[str, ...]
    misconception_hint: str | None
    verify_prompt: str | None
    supporting_refs: tuple[str, ...]
    section_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class TeachingSnapshot:
    schema: str
    turn_id: str
    section_count: int
    sections: tuple[TeachingSection, ...]
    prerequisite_notes: tuple[str, ...]
    lane_notes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ComparisonAxis:
    axis_id: str
    axis_label: str
    left_value: str
    right_value: str
    asymmetry_note: str
    supporting_refs: tuple[str, ...]
    confidence: float
    axis_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ComparisonSnapshot:
    schema: str
    turn_id: str
    axis_count: int
    axes: tuple[ComparisonAxis, ...]
    lane_notes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class PlanningStep:
    step_id: str
    step_index: int
    action: str
    dependency_refs: tuple[str, ...]
    verification_hint: str
    caution_note: str | None
    supporting_refs: tuple[str, ...]
    stop_if_unsure: bool
    step_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class PlanningSnapshot:
    schema: str
    turn_id: str
    step_count: int
    steps: tuple[PlanningStep, ...]
    lane_notes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SynthesisInput:
    input_id: str
    input_kind: str
    summary: str
    support_ref: str
    uncertainty_note: str | None
    input_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SynthesisSnapshot:
    schema: str
    turn_id: str
    input_count: int
    inputs: tuple[SynthesisInput, ...]
    merged_summary: str
    unresolved_conflicts: tuple[str, ...]
    missing_support: tuple[str, ...]
    uncertainty_level: UncertaintyLevel
    preserves_support_honesty: bool
    lane_notes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class AnalogyMapping:
    mapping_id: str
    source_point: str
    target_point: str
    why_it_helps: str
    break_limit: str
    supporting_refs: tuple[str, ...]
    confidence: float
    mapping_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class AnalogySnapshot:
    schema: str
    turn_id: str
    analogy_mode: AnalogyMode
    source_domain_ref: str
    target_domain_ref: str
    analogy_count: int
    mappings: tuple[AnalogyMapping, ...]
    analogy_trace_ref: str
    support_refs: tuple[str, ...]
    lane_notes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ConceptCompositionElement:
    element_id: str
    concept_label: str
    role_in_composition: str
    supporting_refs: tuple[str, ...]
    confidence: float
    element_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ConceptCompositionSnapshot:
    schema: str
    turn_id: str
    element_count: int
    elements: tuple[ConceptCompositionElement, ...]
    composed_view: str
    concept_composition_ref: str
    fail_closed: bool
    lane_notes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class CrossDomainPatternElement:
    element_id: str
    label: str
    source_domain: str
    target_domain: str
    note: str
    confidence: float
    element_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class CrossDomainCompositionSnapshot:
    schema: str
    turn_id: str
    composition_kind: str
    concept_composition_ref: str
    domain_refs: tuple[str, str]
    element_count: int
    elements: tuple[CrossDomainPatternElement, ...]
    shared_pattern: str
    boundary_notes: tuple[str, ...]
    fail_closed: bool
    reason_codes: tuple[str, ...]
    lane_notes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class AudienceAwareExplanationQualitySnapshot:
    schema: str
    turn_id: str
    audience_profile: AudienceProfile
    terminology_density: TerminologyDensity
    brevity_level: BrevityLevel
    section_order: tuple[str, ...]
    anti_filler_checks: tuple[str, ...]
    uncertainty_preserved: bool
    caution_preserved: bool
    rewrite_applied: bool
    quality_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class Phase9OverlayContract:
    schema: str
    conversation_id: str
    turn_id: str
    selected_lane: ExpressionLane
    phase7_interfaces: tuple[str, ...]
    phase8_interfaces: tuple[str, ...]
    support_state: str
    support_honesty_preserved: bool
    response_sections: tuple[str, ...]
    public_response_text: str
    uncertainty_statements: tuple[str, ...]
    analogy_trace_ref: str | None
    concept_composition_ref: str | None
    revision_trace_ref: str | None
    consolidation_trace_ref: str | None
    reorganization_trace_ref: str | None
    evidence_refs: tuple[str, ...]
    contract_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class RichExpressionTurnSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    selected_lane: ExpressionLane
    active_lanes: tuple[ExpressionLane, ...]
    intake_hash: str
    interpretation_hash: str
    support_resolution_hash: str
    utterance_plan_hash: str
    answer_contract_hash: str
    science_world_turn_hash: str
    teaching: TeachingSnapshot | None
    comparison: ComparisonSnapshot | None
    planning: PlanningSnapshot | None
    synthesis: SynthesisSnapshot | None
    analogy: AnalogySnapshot | None
    concept_composition: ConceptCompositionSnapshot | None
    cross_domain_composition: CrossDomainCompositionSnapshot | None
    audience_aware_quality: AudienceAwareExplanationQualitySnapshot
    overlay_contract: Phase9OverlayContract
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)
