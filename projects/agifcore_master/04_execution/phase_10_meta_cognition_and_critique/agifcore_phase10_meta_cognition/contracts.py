from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Any, Mapping

MAX_SELF_MODEL_RECORDS = 4
MAX_META_COGNITION_OBSERVATIONS = 8
MAX_ATTENTION_REDIRECTS = 2
MAX_SKEPTIC_BRANCHES = 3
MAX_STRATEGY_JOURNAL_ENTRIES = 2
MAX_THINKER_TISSUE_ITEMS = 6
MAX_SURPRISE_EVENTS = 4
MAX_THEORY_FRAGMENTS = 3
MAX_WEAK_ANSWER_DIAGNOSIS_ITEMS = 5
MAX_REASON_CODES = 12
MAX_TRACE_REFS = 24
MAX_PUBLIC_EXPLANATION_CHARACTERS = 2600


class Phase10MetaCognitionError(ValueError):
    """Raised when Phase 10 runtime state violates the governed contract."""


def clamp_score(value: float, *, digits: int = 6) -> float:
    return round(min(1.0, max(0.0, float(value))), digits)


def stable_hash_payload(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return len(encoded)


def make_trace_ref(prefix: str, payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    clean_prefix = require_non_empty_str(prefix, "prefix").replace(" ", "_")
    return f"{clean_prefix}::{stable_hash_payload(payload)[:12]}"


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase10MetaCognitionError(f"{field_name} must be a non-empty string")
    return value


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase10MetaCognitionError(f"{field_name} must be a mapping")
    return dict(value)


def require_schema(payload: Mapping[str, Any], expected_schema: str, field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    if payload_map.get("schema") != expected_schema:
        raise Phase10MetaCognitionError(f"{field_name} schema mismatch: expected {expected_schema}")
    return payload_map


def coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    if isinstance(value, (int, float)):
        return bool(value)
    return bool(value)


def bounded_unique(values: list[str], *, ceiling: int, field_name: str) -> tuple[str, ...]:
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
    if not result:
        raise Phase10MetaCognitionError(f"{field_name} must include at least one value")
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


class CritiqueOutcome(StrEnum):
    RECHECK_SUPPORT = "recheck_support"
    REFRAME_EXPLANATION = "reframe_explanation"
    CLARIFY = "clarify"
    ABSTAIN = "abstain"
    NO_REDIRECT = "no_redirect"


class ObservationKind(StrEnum):
    SUPPORT_GAP = "support_gap"
    REPEATED_UNCERTAINTY = "repeated_uncertainty"
    CONTRADICTION_SIGNAL = "contradiction_signal"
    WEAK_ANSWER_SIGNAL = "weak_answer_signal"
    MISSING_NEED = "missing_need"


class RedirectTargetKind(StrEnum):
    SUPPORT_STATE = "support_state"
    REASONING_SUMMARY = "reasoning_summary"
    RICH_EXPRESSION = "rich_expression"
    CLARIFICATION = "clarification"
    CONTRADICTION_PROBE = "contradiction_probe"


class SurpriseTrigger(StrEnum):
    RECHECK_SUPPORT = "recheck_support"
    THEORY_FRAGMENT_CANDIDATE = "theory_fragment_candidate"
    CONCEPT_REFINEMENT_CANDIDATE = "concept_refinement_candidate"
    CLARIFY = "clarify"
    HONEST_FALLBACK = "honest_fallback"
    NO_ACTION = "no_action"


class DiagnosisKind(StrEnum):
    WEAK_SUPPORT = "weak_support"
    CONTRADICTION_RISK = "contradiction_risk"
    MISSING_VARIABLE = "missing_variable"
    VAGUE_EXPLANATION = "vague_explanation"
    SUPPORT_THIN = "support_thin"


@dataclass(frozen=True, slots=True)
class SelfModelRecord:
    record_id: str
    knows: tuple[str, ...]
    infers: tuple[str, ...]
    unknowns: tuple[str, ...]
    answer_mode: str
    confidence_band: str
    confidence_reason: str
    what_would_verify: tuple[str, ...]
    anchor_refs: tuple[str, ...]
    record_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfModelSnapshot:
    schema: str
    turn_id: str
    record_count: int
    records: tuple[SelfModelRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class MetaCognitionObservation:
    observation_id: str
    kind: ObservationKind
    detail: str
    source_ref: str
    severity: float
    observation_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class MetaCognitionObserverSnapshot:
    schema: str
    turn_id: str
    observation_count: int
    observations: tuple[MetaCognitionObservation, ...]
    weak_answer_flags: tuple[str, ...]
    repeated_uncertainty_signals: tuple[str, ...]
    missing_needs: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class AttentionRedirect:
    redirect_id: str
    target_kind: RedirectTargetKind
    target_ref: str
    reason: str
    priority: int
    redirect_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class AttentionRedirectSnapshot:
    schema: str
    turn_id: str
    redirect_count: int
    redirects: tuple[AttentionRedirect, ...]
    stop_reason: str
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SkepticCounterexampleRecord:
    branch_id: str
    what_could_make_this_wrong: str
    what_variable_could_flip_the_answer: str
    what_counterexample_weakens_the_theory: str
    changed_answer_after_skeptic: bool
    forced_fallback: bool
    supporting_refs: tuple[str, ...]
    record_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SkepticCounterexampleSnapshot:
    schema: str
    turn_id: str
    branch_count: int
    branches: tuple[SkepticCounterexampleRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class StrategyJournalEntry:
    entry_id: str
    reasoning_path: str
    worked: tuple[str, ...]
    failed: tuple[str, ...]
    priors_used: tuple[str, ...]
    hidden_variables_seen: tuple[str, ...]
    question_types_that_still_break: tuple[str, ...]
    monitoring_note: str
    entry_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class StrategyJournalSnapshot:
    schema: str
    turn_id: str
    entry_count: int
    entries: tuple[StrategyJournalEntry, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ThinkerTissueRecord:
    record_id: str
    watched_failures: tuple[str, ...]
    watched_weak_answers: tuple[str, ...]
    watched_repeated_uncertainty: tuple[str, ...]
    asked_what_is_missing: tuple[str, ...]
    bounded_proposals: tuple[str, ...]
    governance_mode: str
    record_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ThinkerTissueSnapshot:
    schema: str
    turn_id: str
    item_count: int
    records: tuple[ThinkerTissueRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SurpriseEngineRecord:
    event_id: str
    detected_contradiction: bool
    detected_missing_variable: bool
    detected_boundary_failure: bool
    detected_wrong_prior_choice: bool
    detected_weak_causal_chain: bool
    triggered_action: SurpriseTrigger
    trigger_reason: str
    supporting_refs: tuple[str, ...]
    record_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SurpriseEngineSnapshot:
    schema: str
    turn_id: str
    event_count: int
    events: tuple[SurpriseEngineRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class TheoryFragmentRecord:
    fragment_id: str
    source_answer_id: str
    fragment_label: str
    fragment_statement: str
    falsifier: str
    next_verification_step: str
    record_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class TheoryFragmentsSnapshot:
    schema: str
    turn_id: str
    fragment_count: int
    fragments: tuple[TheoryFragmentRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class WeakAnswerDiagnosisItem:
    diagnosis_id: str
    kind: DiagnosisKind
    why_weak: str
    missing_support_or_signal: str
    next_step: str
    support_honesty_preserved: bool
    supporting_refs: tuple[str, ...]
    diagnosis_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class WeakAnswerDiagnosisSnapshot:
    schema: str
    turn_id: str
    item_count: int
    items: tuple[WeakAnswerDiagnosisItem, ...]
    summary: str
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class MetaCognitionLayerSnapshot:
    schema: str
    turn_id: str
    selected_outcome: CritiqueOutcome
    redirect_required: bool
    active_modules: tuple[str, ...]
    outcome_notes: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class Phase10OverlayContract:
    schema: str
    conversation_id: str
    turn_id: str
    selected_outcome: CritiqueOutcome
    phase7_interfaces: tuple[str, ...]
    phase8_interfaces: tuple[str, ...]
    phase9_interfaces: tuple[str, ...]
    support_state: str
    support_honesty_preserved: bool
    public_explanation: str
    self_model_ref: str
    observer_ref: str
    strategy_journal_ref: str
    skeptic_ref: str
    surprise_ref: str
    theory_fragment_refs: tuple[str, ...]
    diagnosis_ref: str
    redirect_refs: tuple[str, ...]
    upstream_revision_trace_ref: str | None
    upstream_consolidation_trace_ref: str | None
    upstream_reorganization_trace_ref: str | None
    evidence_refs: tuple[str, ...]
    contract_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class MetaCognitionTurnSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    support_resolution_hash: str
    self_knowledge_hash: str
    answer_contract_hash: str
    science_world_turn_hash: str
    rich_expression_turn_hash: str
    self_model: SelfModelSnapshot
    meta_cognition_layer: MetaCognitionLayerSnapshot
    attention_redirect: AttentionRedirectSnapshot
    meta_cognition_observer: MetaCognitionObserverSnapshot
    skeptic_counterexample: SkepticCounterexampleSnapshot
    strategy_journal: StrategyJournalSnapshot
    thinker_tissue: ThinkerTissueSnapshot
    surprise_engine: SurpriseEngineSnapshot
    theory_fragments: TheoryFragmentsSnapshot
    weak_answer_diagnosis: WeakAnswerDiagnosisSnapshot
    overlay_contract: Phase10OverlayContract
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)
