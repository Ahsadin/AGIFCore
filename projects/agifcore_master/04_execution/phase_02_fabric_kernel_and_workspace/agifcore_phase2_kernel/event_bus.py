from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Callable

from event_types import KernelContractError, KernelEvent, KernelEventType

DEFAULT_MAX_EVENT_QUEUE_DEPTH = 1024

EventHandler = Callable[[KernelEvent], None]


class EventBusCapacityError(KernelContractError):
    """Raised when the slice-1 queue would exceed the planning ceiling."""


@dataclass(frozen=True, slots=True)
class TraceRecord:
    sequence: int
    event_id: str
    event_type: str
    conversation_id: str
    turn_id: str
    producer: str
    discourse_mode: str
    support_state: str
    knowledge_gap_reason: str
    next_action: str
    planner_trace_ref: str
    simulation_trace_ref: str
    critic_trace_ref: str
    governance_trace_ref: str
    payload_size_bytes: int
    final_answer_mode: str | None
    occurred_at: str

    def to_dict(self) -> dict[str, object]:
        return {
            "sequence": self.sequence,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "conversation_id": self.conversation_id,
            "turn_id": self.turn_id,
            "producer": self.producer,
            "discourse_mode": self.discourse_mode,
            "support_state": self.support_state,
            "knowledge_gap_reason": self.knowledge_gap_reason,
            "next_action": self.next_action,
            "planner_trace_ref": self.planner_trace_ref,
            "simulation_trace_ref": self.simulation_trace_ref,
            "critic_trace_ref": self.critic_trace_ref,
            "governance_trace_ref": self.governance_trace_ref,
            "payload_size_bytes": self.payload_size_bytes,
            "final_answer_mode": self.final_answer_mode,
            "occurred_at": self.occurred_at,
        }


class EventBus:
    """Slice-1 governed synchronous event bus with trace-ready recording."""

    def __init__(self, *, max_queue_depth: int = DEFAULT_MAX_EVENT_QUEUE_DEPTH) -> None:
        self._max_queue_depth = max_queue_depth
        self._queue: deque[KernelEvent] = deque()
        self._subscribers: dict[KernelEventType, list[EventHandler]] = defaultdict(list)
        self._events: list[KernelEvent] = []
        self._trace: list[TraceRecord] = []

    def subscribe(self, event_type: KernelEventType, handler: EventHandler) -> None:
        self._subscribers[event_type].append(handler)

    def subscriber_count(self, event_type: KernelEventType) -> int:
        return len(self._subscribers[event_type])

    def publish(self, event: KernelEvent) -> None:
        event.validate()
        self._queue.append(event)
        if len(self._queue) > self._max_queue_depth:
            self._queue.pop()
            raise EventBusCapacityError(
                f"event queue depth would exceed {self._max_queue_depth}"
            )
        self._drain_queue()

    def event_export(self) -> list[dict[str, object]]:
        return [event.to_dict() for event in self._events]

    def trace_export(self) -> list[dict[str, object]]:
        return [record.to_dict() for record in self._trace]

    def _drain_queue(self) -> None:
        while self._queue:
            event = self._queue.popleft()
            self._events.append(event)
            self._trace.append(self._build_trace_record(event))
            for handler in self._subscribers[event.event_type]:
                handler(event)

    def _build_trace_record(self, event: KernelEvent) -> TraceRecord:
        final_answer_mode = None
        if event.response is not None:
            final_answer_mode = event.response.final_answer_mode.value
        return TraceRecord(
            sequence=len(self._trace) + 1,
            event_id=event.event_id,
            event_type=event.event_type.value,
            conversation_id=event.turn.conversation_id,
            turn_id=event.turn.turn_id,
            producer=event.producer,
            discourse_mode=event.turn.discourse_mode.value,
            support_state=event.turn.support_state.value,
            knowledge_gap_reason=event.turn.knowledge_gap_reason.value,
            next_action=event.turn.next_action.value,
            planner_trace_ref=event.trace_refs.planner_trace_ref,
            simulation_trace_ref=event.trace_refs.simulation_trace_ref,
            critic_trace_ref=event.trace_refs.critic_trace_ref,
            governance_trace_ref=event.trace_refs.governance_trace_ref,
            payload_size_bytes=event.serialized_size_bytes(),
            final_answer_mode=final_answer_mode,
            occurred_at=event.occurred_at,
        )
