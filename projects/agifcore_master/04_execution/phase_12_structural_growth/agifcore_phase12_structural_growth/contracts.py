from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Any, Mapping

MAX_SELF_MODEL_FEEDBACK_ITEMS = 6
MAX_REFLECTION_CONTROL_ACTIONS = 3
MAX_SELF_REORGANIZATION_ACTIONS = 1
MAX_DOMAIN_GENESIS_ITEMS = 1
MAX_THEORY_FORMATION_CANDIDATES = 2
MAX_PROCEDURE_TOOL_INVENTION_CANDIDATES = 1
MAX_CURIOSITY_GAP_SELECTION_ITEMS = 2
MAX_SUPPORTING_REFS = 8
MAX_EVIDENCE_REFS = 40


class Phase12StructuralGrowthError(ValueError):
    """Raised when Phase 12 runtime state violates the governed contract."""


def clamp_score(value: float, *, digits: int = 6) -> float:
    return round(min(1.0, max(0.0, float(value))), digits)


def stable_hash_payload(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return len(encoded)


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase12StructuralGrowthError(f"{field_name} must be a non-empty string")
    return value.strip()


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase12StructuralGrowthError(f"{field_name} must be a mapping")
    return dict(value)


def require_schema(payload: Mapping[str, Any], expected_schema: str, field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    if payload_map.get("schema") != expected_schema:
        raise Phase12StructuralGrowthError(f"{field_name} schema mismatch: expected {expected_schema}")
    return payload_map


def require_phase11_cycle(payload: Mapping[str, Any], field_name: str) -> dict[str, Any]:
    cycle = require_schema(payload, "agifcore.phase_11.self_improvement_cycle.v1", field_name)
    require_schema(cycle.get("overlay_contract", {}), "agifcore.phase_11.overlay_contract.v1", f"{field_name}.overlay_contract")
    return cycle


def optional_bounded_unique(values: list[Any], *, ceiling: int) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in values:
        cleaned = " ".join(str(raw).split()).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
        if len(result) >= ceiling:
            break
    return tuple(result)


def bounded_unique(values: list[Any], *, ceiling: int, field_name: str) -> tuple[str, ...]:
    result = optional_bounded_unique(values, ceiling=ceiling)
    if not result:
        raise Phase12StructuralGrowthError(f"{field_name} must include at least one value")
    return result


def make_trace_ref(prefix: str, payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    return f"{require_non_empty_str(prefix, 'prefix').replace(' ', '_')}::{stable_hash_payload(payload)[:12]}"


def infer_phase12_scenario(phase11_cycle: Mapping[str, Any]) -> str:
    cycle = require_phase11_cycle(phase11_cycle, "phase11_cycle")
    overlay = require_schema(cycle.get("overlay_contract", {}), "agifcore.phase_11.overlay_contract.v1", "phase11_cycle.overlay_contract")
    if str(overlay.get("support_state", "")).strip() == "search_needed":
        return "weak"
    if list(overlay.get("adopted_proposal_ids", ())):
        return "contradiction"
    return "weak"


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


class ReflectionDecision(StrEnum):
    ADVANCE = "advance"
    HOLD = "hold"
    HALT = "halt"


class GapKind(StrEnum):
    STRUCTURAL_GAP = "structural_gap"
    THEORY_GAP = "theory_gap"
    PROCEDURE_GAP = "procedure_gap"
    DOMAIN_GAP = "domain_gap"


class TheoryGrowthStatus(StrEnum):
    NEW_CANDIDATE = "new_candidate"
    REFINE_EXISTING = "refine_existing"
    HOLD = "hold"


class CandidateState(StrEnum):
    CANDIDATE = "candidate"
    HELD = "held"
    DEFERRED = "deferred"


class ReorganizationActionKind(StrEnum):
    ROUTE_TUNING = "route_tuning"
    SPLIT_MERGE = "split_merge"
    TRANSFER_RESHAPE = "transfer_reshape"


class ProcedureToolKind(StrEnum):
    TRIAGE_CHECKLIST = "triage_checklist"
    REVIEW_PROTOCOL = "review_protocol"


@dataclass(frozen=True, slots=True)
class SelfModelFeedbackItem:
    feedback_id: str
    pressure_kind: str
    problem_statement: str
    recommended_lane: str
    bounded_next_step: str
    supporting_refs: tuple[str, ...]
    feedback_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfModelFeedbackSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    item_count: int
    items: tuple[SelfModelFeedbackItem, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ReflectionControlAction:
    action_id: str
    target_lane: str
    decision: ReflectionDecision
    reason: str
    supporting_feedback_ids: tuple[str, ...]
    stop_reason: str
    action_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ReflectionControlSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    action_count: int
    actions: tuple[ReflectionControlAction, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class CuriosityGapRecord:
    gap_id: str
    gap_kind: GapKind
    ranked_priority: int
    chosen_target_lane: str
    why_selected: str
    deferred_alternatives: tuple[str, ...]
    stop_condition: str
    supporting_refs: tuple[str, ...]
    gap_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class CuriosityGapSelectionSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    gap_count: int
    gaps: tuple[CuriosityGapRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class TheoryFormationCandidate:
    candidate_id: str
    growth_status: TheoryGrowthStatus
    source_fragment_ref: str
    theory_label: str
    theory_statement: str
    assumption_refs: tuple[str, ...]
    mechanism_step_refs: tuple[str, ...]
    predicted_observable_refs: tuple[str, ...]
    falsifier_refs: tuple[str, ...]
    theory_confidence_band: str
    verification_next_step: str
    candidate_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class TheoryFormationSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    candidate_count: int
    candidates: tuple[TheoryFormationCandidate, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ProcedureToolInventionCandidate:
    candidate_id: str
    invention_kind: ProcedureToolKind
    skill_anchor_ref: str
    procedure_statement: str
    preconditions: tuple[str, ...]
    limits: tuple[str, ...]
    sandbox_compatibility_note: str
    non_auto_execute: bool
    candidate_state: CandidateState
    supporting_refs: tuple[str, ...]
    candidate_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ProcedureToolInventionSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    candidate_count: int
    candidates: tuple[ProcedureToolInventionCandidate, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfReorganizationCandidate:
    candidate_id: str
    action_kind: ReorganizationActionKind
    target_structure_ref: str
    before_state_ref: str
    after_state_ref: str
    rollback_target: str
    rejected_alternative_ref: str
    rationale: str
    pressure_score_delta: float
    candidate_state: CandidateState
    candidate_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfReorganizationSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    candidate_count: int
    candidates: tuple[SelfReorganizationCandidate, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class DomainGenesisCandidate:
    candidate_id: str
    domain_label: str
    parent_domain_ref: str
    peer_domain_refs: tuple[str, ...]
    boundary_statement: str
    activation_signals: tuple[str, ...]
    rejection_path: str
    candidate_state: CandidateState
    supporting_refs: tuple[str, ...]
    candidate_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class DomainGenesisSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    candidate_count: int
    candidates: tuple[DomainGenesisCandidate, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class Phase12OverlayContract:
    schema: str
    conversation_id: str
    turn_id: str
    phase11_interfaces: tuple[str, ...]
    support_state: str
    selected_gap_ids: tuple[str, ...]
    candidate_theory_ids: tuple[str, ...]
    candidate_domain_ids: tuple[str, ...]
    candidate_procedure_ids: tuple[str, ...]
    reorganization_refs: tuple[str, ...]
    read_only_phase11_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    contract_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class StructuralGrowthCycleSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    phase11_cycle_hash: str
    self_model_feedback: SelfModelFeedbackSnapshot
    reflection_control: ReflectionControlSnapshot
    curiosity_gap_selection: CuriosityGapSelectionSnapshot
    theory_formation: TheoryFormationSnapshot
    procedure_tool_invention: ProcedureToolInventionSnapshot
    self_reorganization: SelfReorganizationSnapshot
    domain_genesis: DomainGenesisSnapshot
    overlay_contract: Phase12OverlayContract
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)
