from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, Sequence
from uuid import uuid4

DEFAULT_MAX_EVENT_SIZE_BYTES = 256 * 1024


class StringEnum(str, Enum):
    """String-backed enum for stable event serialization."""


class KernelContractError(ValueError):
    """Raised when a slice-1 event breaks the governed contract."""


class KernelEventType(StringEnum):
    TURN_ADMITTED = "turn_admitted"
    TRACE_ANNOTATED = "trace_annotated"
    GOVERNANCE_DECIDED = "governance_decided"
    RESPONSE_READY = "response_ready"
    TURN_ABORTED = "turn_aborted"


class DiscourseMode(StringEnum):
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


class SupportState(StringEnum):
    GROUNDED = "grounded"
    INFERRED = "inferred"
    SEARCH_NEEDED = "search_needed"
    UNKNOWN = "unknown"


class KnowledgeGapReason(StringEnum):
    NONE = "none"
    AMBIGUOUS_REQUEST = "ambiguous_request"
    MISSING_LOCAL_EVIDENCE = "missing_local_evidence"
    CONFLICTING_STATE = "conflicting_state"
    BLOCKED_BY_POLICY = "blocked_by_policy"
    NEEDS_FRESH_INFORMATION = "needs_fresh_information"
    OUT_OF_SCOPE = "out_of_scope"


class NextAction(StringEnum):
    ANSWER = "answer"
    CLARIFY = "clarify"
    SEARCH_LOCAL = "search_local"
    SEARCH_EXTERNAL = "search_external"
    ABSTAIN = "abstain"


class FinalAnswerMode(StringEnum):
    GROUNDED_FACT = "grounded_fact"
    DERIVED_ESTIMATE = "derived_estimate"
    DERIVED_EXPLANATION = "derived_explanation"
    HYPOTHESIS = "hypothesis"
    CLARIFY = "clarify"
    SEARCH_NEEDED = "search_needed"
    UNKNOWN = "unknown"
    ABSTAIN = "abstain"


class AbstainOrAnswer(StringEnum):
    ANSWER = "answer"
    ABSTAIN = "abstain"


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True, slots=True)
class KernelTraceRefs:
    planner_trace_ref: str
    simulation_trace_ref: str
    critic_trace_ref: str
    governance_trace_ref: str

    def to_dict(self) -> dict[str, str]:
        return {
            "planner_trace_ref": self.planner_trace_ref,
            "simulation_trace_ref": self.simulation_trace_ref,
            "critic_trace_ref": self.critic_trace_ref,
            "governance_trace_ref": self.governance_trace_ref,
        }


@dataclass(frozen=True, slots=True)
class KernelTurnContext:
    conversation_id: str
    turn_id: str
    user_intent: str
    discourse_mode: DiscourseMode
    support_state: SupportState
    knowledge_gap_reason: KnowledgeGapReason
    next_action: NextAction
    active_context_refs: Sequence[str] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "turn_id": self.turn_id,
            "user_intent": self.user_intent,
            "discourse_mode": self.discourse_mode.value,
            "support_state": self.support_state.value,
            "knowledge_gap_reason": self.knowledge_gap_reason.value,
            "next_action": self.next_action.value,
            "active_context_refs": list(self.active_context_refs),
        }


@dataclass(frozen=True, slots=True)
class KernelResponseSurface:
    response_text: str
    abstain_or_answer: AbstainOrAnswer
    final_answer_mode: FinalAnswerMode
    memory_review_ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "response_text": self.response_text,
            "abstain_or_answer": self.abstain_or_answer.value,
            "final_answer_mode": self.final_answer_mode.value,
            "memory_review_ref": self.memory_review_ref,
        }


@dataclass(frozen=True, slots=True)
class KernelEvent:
    event_id: str
    event_type: KernelEventType
    turn: KernelTurnContext
    trace_refs: KernelTraceRefs
    producer: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    response: KernelResponseSurface | None = None
    occurred_at: str = field(default_factory=utc_timestamp)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "turn": self.turn.to_dict(),
            "trace_refs": self.trace_refs.to_dict(),
            "producer": self.producer,
            "payload": dict(self.payload),
            "response": self.response.to_dict() if self.response else None,
            "occurred_at": self.occurred_at,
        }

    def serialized_size_bytes(self) -> int:
        try:
            encoded = json.dumps(self.to_dict(), sort_keys=True).encode("utf-8")
        except TypeError as exc:
            raise KernelContractError(
                f"event payload is not JSON-serializable: {exc}"
            ) from exc
        return len(encoded)

    def validate(self) -> None:
        if not self.event_id:
            raise KernelContractError("event_id must be non-empty")
        if not self.producer:
            raise KernelContractError("producer must be non-empty")
        if not self.turn.conversation_id:
            raise KernelContractError("conversation_id must be non-empty")
        if not self.turn.turn_id:
            raise KernelContractError("turn_id must be non-empty")
        if not self.turn.user_intent:
            raise KernelContractError("user_intent must be non-empty")
        if self.event_type is KernelEventType.RESPONSE_READY and self.response is None:
            raise KernelContractError("response_ready events require a response surface")
        if self.response and not self.response.response_text:
            raise KernelContractError("response_text must be non-empty when response exists")
        if self.serialized_size_bytes() > DEFAULT_MAX_EVENT_SIZE_BYTES:
            raise KernelContractError(
                f"event exceeds max size of {DEFAULT_MAX_EVENT_SIZE_BYTES} bytes"
            )


def new_kernel_event(
    *,
    event_type: KernelEventType,
    turn: KernelTurnContext,
    trace_refs: KernelTraceRefs,
    producer: str,
    payload: Mapping[str, Any] | None = None,
    response: KernelResponseSurface | None = None,
) -> KernelEvent:
    event = KernelEvent(
        event_id=f"evt-{uuid4().hex}",
        event_type=event_type,
        turn=turn,
        trace_refs=trace_refs,
        producer=producer,
        payload=payload or {},
        response=response,
    )
    event.validate()
    return event
