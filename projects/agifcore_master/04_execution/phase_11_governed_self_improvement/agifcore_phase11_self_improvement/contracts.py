from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Any, Mapping

MAX_OFFLINE_REFLECTION_ITEMS = 12
MAX_IDLE_REFLECTION_ITEMS = 6
MAX_PROPOSALS = 3
MAX_SELF_EXPERIMENTS = 2
MAX_SHADOW_EVALUATIONS = 3
MAX_MEASUREMENT_PAIRS = 3
MAX_DECISIONS = 2
MAX_MONITORING_ITEMS = 4
MAX_ROLLBACK_PROOFS = 2
MAX_THOUGHT_EPISODES = 6
MAX_SELF_INITIATED_INQUIRIES = 1
MAX_SUPPORTING_REFS = 8
MAX_EVIDENCE_REFS = 32
MAX_ALLOWED_LOCAL_INPUTS = 6


class Phase11GovernedSelfImprovementError(ValueError):
    """Raised when the Phase 11 governed self-improvement contract is violated."""


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
        raise Phase11GovernedSelfImprovementError(f"{field_name} must be a non-empty string")
    return value.strip()


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase11GovernedSelfImprovementError(f"{field_name} must be a mapping")
    return dict(value)


def require_schema(payload: Mapping[str, Any], expected_schema: str, field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    if payload_map.get("schema") != expected_schema:
        raise Phase11GovernedSelfImprovementError(f"{field_name} schema mismatch: expected {expected_schema}")
    return payload_map


def require_phase10_turn_state(payload: Mapping[str, Any], field_name: str) -> dict[str, Any]:
    turn = require_schema(payload, "agifcore.phase_10.meta_cognition_turn.v1", field_name)
    require_schema(turn.get("overlay_contract", {}), "agifcore.phase_10.overlay_contract.v1", f"{field_name}.overlay_contract")
    return turn


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
        raise Phase11GovernedSelfImprovementError(f"{field_name} must include at least one value")
    return result


def make_trace_ref(prefix: str, payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    return f"{require_non_empty_str(prefix, 'prefix').replace(' ', '_')}::{stable_hash_payload(payload)[:12]}"


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


class ExperimentVerdict(StrEnum):
    IMPROVES = "improves"
    MIXED = "mixed"
    BLOCKED = "blocked"


class DecisionState(StrEnum):
    ADOPTED = "adopted"
    REJECTED = "rejected"
    HELD = "held"
    ROLLED_BACK = "rolled_back"


class MonitoringStatus(StrEnum):
    ACTIVE = "active"
    WATCH_ONLY = "watch_only"
    ESCALATE = "escalate"


class InquiryTriggerKind(StrEnum):
    MISSING_NEED = "missing_need"
    CONTRADICTION_SIGNAL = "contradiction_signal"
    MONITORING_REGRESSION = "monitoring_regression"


@dataclass(frozen=True, slots=True)
class OfflineReflectionItem:
    item_id: str
    source_kind: str
    source_ref: str
    problem_statement: str
    proposed_focus: str
    bounded_next_step: str
    supporting_refs: tuple[str, ...]
    item_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class OfflineReflectionAndConsolidationSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    item_count: int
    items: tuple[OfflineReflectionItem, ...]
    consolidated_focuses: tuple[str, ...]
    deferred_items: tuple[str, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class IdleReflectionSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    ran: bool
    processed_item_ids: tuple[str, ...]
    deferred_item_ids: tuple[str, ...]
    stop_reason: str
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ProposalRecord:
    proposal_id: str
    proposal_kind: str
    target_module: str
    rationale: str
    expected_gain: str
    falsifier: str
    evidence_needed: str
    rollback_target: str
    supporting_refs: tuple[str, ...]
    proposal_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ProposalGenerationSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    proposal_count: int
    proposals: tuple[ProposalRecord, ...]
    stop_reason: str
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfExperimentRecord:
    experiment_id: str
    proposal_id: str
    baseline_score: float
    candidate_score: float
    delta: float
    held_out_pack_ref: str
    regressions: tuple[str, ...]
    verdict: ExperimentVerdict
    safe_to_continue: bool
    experiment_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfExperimentLabSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    experiment_count: int
    experiments: tuple[SelfExperimentRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ShadowEvaluationRecord:
    evaluation_id: str
    proposal_id: str
    baseline_score: float
    candidate_score: float
    delta: float
    regressions: tuple[str, ...]
    uncertainty_notes: tuple[str, ...]
    ready_for_measurement: bool
    supporting_refs: tuple[str, ...]
    evaluation_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ShadowEvaluationSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    evaluation_count: int
    evaluations: tuple[ShadowEvaluationRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class BeforeAfterMeasurementRecord:
    measurement_id: str
    proposal_id: str
    baseline_metric: float
    adopted_metric: float
    rollback_metric: float
    improvement: float
    pass_threshold_met: bool
    supporting_refs: tuple[str, ...]
    measurement_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class BeforeAfterMeasurementSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    pair_count: int
    measurements: tuple[BeforeAfterMeasurementRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class AdoptionDecisionRecord:
    decision_id: str
    proposal_id: str
    decision: DecisionState
    reason: str
    rollback_required: bool
    supporting_refs: tuple[str, ...]
    decision_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class AdoptionOrRejectionPipelineSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    decision_count: int
    decisions: tuple[AdoptionDecisionRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class PostAdoptionMonitoringRecord:
    monitoring_id: str
    proposal_id: str
    monitoring_window: str
    trigger_threshold: str
    current_status: MonitoringStatus
    escalation_action: str
    supporting_refs: tuple[str, ...]
    monitoring_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class PostAdoptionMonitoringSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    monitoring_count: int
    items: tuple[PostAdoptionMonitoringRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class RollbackProofRecord:
    rollback_id: str
    proposal_id: str
    baseline_metric: float
    adopted_metric: float
    restored_metric: float
    roundtrip_preserved: bool
    proof_note: str
    rollback_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class RollbackProofSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    rollback_count: int
    rollbacks: tuple[RollbackProofRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ThoughtEpisodeRecord:
    episode_id: str
    proposal_id: str
    episode_note: str
    falsifier: str
    trace_refs: tuple[str, ...]
    episode_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ThoughtEpisodesSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    episode_count: int
    episodes: tuple[ThoughtEpisodeRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfInitiatedInquiryRecord:
    inquiry_id: str
    trigger_kind: InquiryTriggerKind
    goal: str
    budget_limit: str
    allowed_local_inputs: tuple[str, ...]
    stop_condition: str
    inquiry_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfInitiatedInquirySnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    inquiry_count: int
    inquiries: tuple[SelfInitiatedInquiryRecord, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class Phase11OverlayContract:
    schema: str
    conversation_id: str
    turn_id: str
    phase10_interfaces: tuple[str, ...]
    support_state: str
    adopted_proposal_ids: tuple[str, ...]
    held_proposal_ids: tuple[str, ...]
    rejected_proposal_ids: tuple[str, ...]
    monitoring_refs: tuple[str, ...]
    rollback_refs: tuple[str, ...]
    inquiry_refs: tuple[str, ...]
    read_only_phase10_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    contract_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfImprovementCycleSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    phase10_turn_hash: str
    offline_reflection_and_consolidation: OfflineReflectionAndConsolidationSnapshot
    idle_reflection: IdleReflectionSnapshot
    proposal_generation: ProposalGenerationSnapshot
    self_experiment_lab: SelfExperimentLabSnapshot
    shadow_evaluation: ShadowEvaluationSnapshot
    before_after_measurement: BeforeAfterMeasurementSnapshot
    adoption_or_rejection_pipeline: AdoptionOrRejectionPipelineSnapshot
    post_adoption_monitoring: PostAdoptionMonitoringSnapshot
    rollback_proof: RollbackProofSnapshot
    thought_episodes: ThoughtEpisodesSnapshot
    self_initiated_inquiry_engine: SelfInitiatedInquirySnapshot
    overlay_contract: Phase11OverlayContract
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)
