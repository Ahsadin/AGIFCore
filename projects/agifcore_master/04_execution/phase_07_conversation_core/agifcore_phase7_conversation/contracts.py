from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime, timezone
from enum import StrEnum
from hashlib import sha256
from typing import Any, Mapping

MAX_RAW_INPUT_CHARACTERS = 4000
MAX_PARSED_SIGNALS = 64
MAX_SUPPORT_CANDIDATES = 24
MAX_CLARIFICATION_QUESTIONS = 2
MAX_UTTERANCE_PLAN_BRANCHES = 6
MAX_RESPONSE_CHARACTERS = 3200
MAX_CONTRACT_FIELDS = 20


class Phase7ConversationError(ValueError):
    """Raised when Phase 7 runtime state violates the governed contract."""


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clamp_score(value: float, *, digits: int = 6) -> float:
    return round(min(1.0, max(0.0, float(value))), digits)


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


def stable_hash_payload(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase7ConversationError(f"{field_name} must be a non-empty string")
    return value


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase7ConversationError(f"{field_name} must be a mapping")
    return dict(value)


def require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise Phase7ConversationError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        normalized = require_non_empty_str(item, f"{field_name}[]")
        if normalized in seen:
            raise Phase7ConversationError(f"{field_name} contains duplicate entries")
        seen.add(normalized)
        result.append(normalized)
    return result


def require_schema(payload: Mapping[str, Any], expected_schema: str, field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    if payload_map.get("schema") != expected_schema:
        raise Phase7ConversationError(f"{field_name} schema mismatch: expected {expected_schema}")
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


class DiscourseMode(StrEnum):
    STATUS = "status"
    EXPLAIN = "explain"
    COMPARE = "compare"
    TEACH = "teach"
    ANALOGY = "analogy"
    PLAN = "plan"
    SYNTHESIZE = "synthesize"
    CRITIQUE_REWRITE = "critique_rewrite"
    CLARIFY = "clarify"
    SELF_KNOWLEDGE = "self_knowledge"
    ABSTAIN = "abstain"


class SupportState(StrEnum):
    GROUNDED = "grounded"
    INFERRED = "inferred"
    SEARCH_NEEDED = "search_needed"
    UNKNOWN = "unknown"


class KnowledgeGapReason(StrEnum):
    NONE = "none"
    AMBIGUOUS_REQUEST = "ambiguous_request"
    MISSING_LOCAL_EVIDENCE = "missing_local_evidence"
    CONFLICTING_STATE = "conflicting_state"
    BLOCKED_BY_POLICY = "blocked_by_policy"
    NEEDS_FRESH_INFORMATION = "needs_fresh_information"
    OUT_OF_SCOPE = "out_of_scope"


class NextAction(StrEnum):
    ANSWER = "answer"
    CLARIFY = "clarify"
    SEARCH_LOCAL = "search_local"
    SEARCH_EXTERNAL = "search_external"
    ABSTAIN = "abstain"


class FinalAnswerMode(StrEnum):
    GROUNDED_FACT = "grounded_fact"
    DERIVED_ESTIMATE = "derived_estimate"
    DERIVED_EXPLANATION = "derived_explanation"
    HYPOTHESIS = "hypothesis"
    CLARIFY = "clarify"
    SEARCH_NEEDED = "search_needed"
    UNKNOWN = "unknown"
    ABSTAIN = "abstain"


class QuestionCategory(StrEnum):
    ORDINARY = "ordinary"
    LIVE_CURRENT = "live_current"
    AMBIGUOUS = "ambiguous"
    SELF_KNOWLEDGE = "self_knowledge"
    LOCAL_ARTIFACT = "local_artifact"
    CORRECTION_HINT = "correction_hint"
    REPEATED_FACT_HINT = "repeated_fact_hint"


class GuardrailStatus(StrEnum):
    PASS = "pass"
    FALLBACK_APPLIED = "fallback_applied"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class RawTextIntakeRecord:
    conversation_id: str
    turn_id: str
    raw_text: str
    normalized_text: str
    active_context_refs: tuple[str, ...]
    token_count: int
    character_count: int
    contains_code_block: bool
    ends_with_question: bool
    intake_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class QuestionInterpretation:
    schema: str
    conversation_id: str
    turn_id: str
    raw_text_hash: str
    user_intent: str
    discourse_mode_hint: DiscourseMode
    question_category: QuestionCategory
    target_domain_hint: str | None
    live_current_requested: bool
    ambiguous_request: bool
    self_knowledge_requested: bool
    local_artifact_requested: bool
    correction_hint: bool
    repeated_fact_hint: bool
    comparison_requested: bool
    token_count: int
    extracted_terms: tuple[str, ...]
    signal_notes: tuple[str, ...]
    interpretation_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SupportStateResolution:
    schema: str
    conversation_id: str
    turn_id: str
    support_state: SupportState
    knowledge_gap_reason: KnowledgeGapReason
    next_action: NextAction
    evidence_refs: tuple[str, ...]
    blocked_refs: tuple[str, ...]
    selected_domain_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]
    memory_review_ref: str
    simulation_trace_ref: str
    critic_trace_ref: str
    governance_trace_ref: str
    resolution_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfKnowledgeStatement:
    statement_id: str
    statement_kind: str
    statement: str
    anchor_refs: tuple[str, ...]
    statement_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class SelfKnowledgeSnapshot:
    schema: str
    statement_count: int
    statements: tuple[SelfKnowledgeStatement, ...]
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ClarificationQuestion:
    question_id: str
    question_text: str
    missing_variables: tuple[str, ...]
    reason_code: str
    question_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ClarificationRequest:
    schema: str
    question_count: int
    questions: tuple[ClarificationQuestion, ...]
    request_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class UtterancePlan:
    schema: str
    plan_id: str
    discourse_mode: DiscourseMode
    response_sections: tuple[str, ...]
    sentence_obligations: tuple[str, ...]
    constraint_slots: tuple[str, ...]
    branch_count: int
    planner_trace_ref: str
    plan_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class RealizationDraft:
    draft_id: str
    response_text: str
    final_answer_mode: FinalAnswerMode
    cited_evidence_refs: tuple[str, ...]
    draft_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class ResponseSurface:
    response_id: str
    response_text: str
    final_answer_mode: FinalAnswerMode
    cited_evidence_refs: tuple[str, ...]
    response_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class GuardrailViolation:
    violation_id: str
    reason_code: str
    detail: str
    violation_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class GuardrailResult:
    schema: str
    status: GuardrailStatus
    fallback_action: NextAction
    output_text: str
    violations: tuple[GuardrailViolation, ...]
    guardrail_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)


@dataclass(frozen=True, slots=True)
class AnswerContractSnapshot:
    schema: str
    conversation_id: str
    turn_id: str
    user_intent: str
    active_context_refs: tuple[str, ...]
    planner_trace_ref: str
    simulation_trace_ref: str
    critic_trace_ref: str
    governance_trace_ref: str
    response_text: str
    abstain_or_answer: str
    memory_review_ref: str
    discourse_mode: DiscourseMode
    support_state: SupportState
    knowledge_gap_reason: KnowledgeGapReason
    next_action: NextAction
    final_answer_mode: FinalAnswerMode
    evidence_refs: tuple[str, ...]
    contract_hash: str

    def to_dict(self) -> dict[str, Any]:
        payload = _serialize_value(self)
        if len(payload) > MAX_CONTRACT_FIELDS:
            raise Phase7ConversationError("answer contract exceeds Phase 7 field ceiling")
        return payload


@dataclass(frozen=True, slots=True)
class ConversationTurnSnapshot:
    schema: str
    phase4_interfaces: tuple[str, ...]
    phase5_interfaces: tuple[str, ...]
    phase6_interfaces: tuple[str, ...]
    intake: RawTextIntakeRecord
    interpretation: QuestionInterpretation
    support_resolution: SupportStateResolution
    self_knowledge: SelfKnowledgeSnapshot
    clarification: ClarificationRequest
    utterance_plan: UtterancePlan
    response_surface: ResponseSurface
    guardrail_result: GuardrailResult
    answer_contract: AnswerContractSnapshot
    snapshot_hash: str

    def to_dict(self) -> dict[str, Any]:
        return _serialize_value(self)
