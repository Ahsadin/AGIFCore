from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from event_types import (
    KnowledgeGapReason,
    KernelContractError,
    NextAction,
    SupportState,
    utc_timestamp,
)


class FailClosedReasonCode(str, Enum):
    INVALID_EVENT = "INVALID_EVENT"
    TRACE_ANCHOR_MISSING = "TRACE_ANCHOR_MISSING"
    SUPPORT_STATE_BLOCK = "SUPPORT_STATE_BLOCK"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    WORKSPACE_BUDGET_EXCEEDED = "WORKSPACE_BUDGET_EXCEEDED"
    SCHEDULER_QUEUE_EXCEEDED = "SCHEDULER_QUEUE_EXCEEDED"
    REPLAY_MISMATCH = "REPLAY_MISMATCH"
    ROLLBACK_REFERENCE_MISSING = "ROLLBACK_REFERENCE_MISSING"
    QUARANTINE_REQUIRED = "QUARANTINE_REQUIRED"
    INTEGRITY_VIOLATION = "INTEGRITY_VIOLATION"


class FailClosedAction(str, Enum):
    HALT_TURN = "halt_turn"
    HALT_KERNEL = "halt_kernel"
    QUARANTINE_CELL = "quarantine_cell"
    ESCALATE_GOVERNOR = "escalate_governor"


@dataclass(frozen=True, slots=True)
class FailClosedDecision:
    blocked: bool
    reason_code: str | None
    action: str
    message: str
    occurred_at: str
    context: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "blocked": self.blocked,
            "reason_code": self.reason_code,
            "action": self.action,
            "message": self.message,
            "occurred_at": self.occurred_at,
            "context": dict(self.context),
        }


class KernelFailClosedError(KernelContractError):
    """Raised when fail-closed reasoning or actions are invalid."""


class KernelFailClosed:
    """Fail-closed decision helper with explicit reason codes."""

    def __init__(self) -> None:
        self._decisions: list[FailClosedDecision] = []

    def allow(
        self, *, message: str = "allowed", context: dict[str, Any] | None = None
    ) -> FailClosedDecision:
        decision = FailClosedDecision(
            blocked=False,
            reason_code=None,
            action=FailClosedAction.HALT_TURN.value,
            message=message,
            occurred_at=utc_timestamp(),
            context=dict(context or {}),
        )
        self._decisions.append(decision)
        return decision

    def block(
        self,
        *,
        reason_code: FailClosedReasonCode,
        action: FailClosedAction,
        message: str,
        context: dict[str, Any] | None = None,
    ) -> FailClosedDecision:
        if not message:
            raise KernelFailClosedError("fail-closed message must be non-empty")
        decision = FailClosedDecision(
            blocked=True,
            reason_code=reason_code.value,
            action=action.value,
            message=message,
            occurred_at=utc_timestamp(),
            context=dict(context or {}),
        )
        self._decisions.append(decision)
        return decision

    def enforce_condition(
        self,
        *,
        condition: bool,
        reason_code: FailClosedReasonCode,
        action: FailClosedAction,
        message: str,
        context: dict[str, Any] | None = None,
    ) -> FailClosedDecision:
        if condition:
            return self.allow(message="condition satisfied", context=context)
        return self.block(
            reason_code=reason_code,
            action=action,
            message=message,
            context=context,
        )

    def evaluate_support_state(
        self,
        *,
        support_state: SupportState,
        knowledge_gap_reason: KnowledgeGapReason,
        next_action: NextAction,
        context: dict[str, Any] | None = None,
    ) -> FailClosedDecision:
        payload = dict(context or {})
        payload["support_state"] = support_state.value
        payload["knowledge_gap_reason"] = knowledge_gap_reason.value
        payload["next_action"] = next_action.value

        blocked_support = {
            SupportState.UNKNOWN,
            SupportState.SEARCH_NEEDED,
        }
        if support_state in blocked_support and next_action is NextAction.ANSWER:
            return self.block(
                reason_code=FailClosedReasonCode.SUPPORT_STATE_BLOCK,
                action=FailClosedAction.HALT_TURN,
                message="blocked answer because support_state requires caution",
                context=payload,
            )
        if knowledge_gap_reason is KnowledgeGapReason.BLOCKED_BY_POLICY:
            return self.block(
                reason_code=FailClosedReasonCode.POLICY_BLOCKED,
                action=FailClosedAction.ESCALATE_GOVERNOR,
                message="blocked by policy and escalated",
                context=payload,
            )
        return self.allow(message="support-state check passed", context=payload)

    def decisions_export(self) -> list[dict[str, Any]]:
        return [decision.to_dict() for decision in self._decisions]
