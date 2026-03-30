from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from heapq import heappop, heappush
from typing import Any

from event_types import KernelContractError

DEFAULT_MAX_EVENT_QUEUE_DEPTH = 1024
DEFAULT_SCHEDULER_LATENCY_TARGET_MS = 50
DEFAULT_MAX_EVENT_SIZE_BYTES = 256 * 1024


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class SchedulerCapacityError(KernelContractError):
    """Raised when scheduler queue limits are violated."""


class SchedulerTaskError(KernelContractError):
    """Raised when task payload or shape is invalid."""


@dataclass(order=True, slots=True)
class _ScheduledItem:
    sort_key: tuple[int, int]
    task_id: str = field(compare=False)


@dataclass(slots=True)
class ScheduledTask:
    task_id: str
    cell_id: str
    priority: int
    need_score: float
    estimated_cost: float
    payload: dict[str, Any]
    enqueued_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "cell_id": self.cell_id,
            "priority": self.priority,
            "need_score": self.need_score,
            "estimated_cost": self.estimated_cost,
            "payload": dict(self.payload),
            "enqueued_at": self.enqueued_at,
        }


class Scheduler:
    """Bounded scheduler queue with inspectable dispatch metrics."""

    def __init__(
        self,
        *,
        max_queue_depth: int = DEFAULT_MAX_EVENT_QUEUE_DEPTH,
        latency_target_ms: int = DEFAULT_SCHEDULER_LATENCY_TARGET_MS,
    ) -> None:
        self._max_queue_depth = max_queue_depth
        self._latency_target_ms = latency_target_ms
        self._queue: list[_ScheduledItem] = []
        self._tasks: dict[str, ScheduledTask] = {}
        self._sequence_counter = 0
        self._max_observed_depth = 0
        self._enqueue_count = 0
        self._dispatch_count = 0
        self._last_dispatch_latency_ms: float | None = None

    def enqueue_task(
        self,
        *,
        task_id: str,
        cell_id: str,
        priority: int,
        need_score: float,
        estimated_cost: float,
        payload: dict[str, Any] | None = None,
    ) -> ScheduledTask:
        if not task_id:
            raise SchedulerTaskError("task_id must be non-empty")
        if not cell_id:
            raise SchedulerTaskError("cell_id must be non-empty")
        if task_id in self._tasks:
            raise SchedulerTaskError(f"duplicate task_id: {task_id}")
        if len(self._tasks) >= self._max_queue_depth:
            raise SchedulerCapacityError(
                f"scheduler queue would exceed {self._max_queue_depth}"
            )
        task_payload = payload or {}
        self._validate_payload(task_payload)

        self._sequence_counter += 1
        task = ScheduledTask(
            task_id=task_id,
            cell_id=cell_id,
            priority=priority,
            need_score=float(need_score),
            estimated_cost=float(estimated_cost),
            payload=dict(task_payload),
            enqueued_at=utc_timestamp(),
        )
        # Higher priority and higher need_score should come first.
        sort_key = (-priority, -int(task.need_score * 100000), self._sequence_counter)
        heappush(self._queue, _ScheduledItem(sort_key=sort_key, task_id=task_id))
        self._tasks[task_id] = task
        self._enqueue_count += 1
        self._max_observed_depth = max(self._max_observed_depth, len(self._tasks))
        return task

    def dispatch_next(self) -> ScheduledTask | None:
        while self._queue:
            scheduled = heappop(self._queue)
            task = self._tasks.pop(scheduled.task_id, None)
            if task is None:
                continue
            self._dispatch_count += 1
            self._last_dispatch_latency_ms = self._elapsed_ms(task.enqueued_at)
            return task
        return None

    def queue_depth(self) -> int:
        return len(self._tasks)

    def scheduler_metrics(self) -> dict[str, Any]:
        latency = self._last_dispatch_latency_ms
        over_target = latency is not None and latency > self._latency_target_ms
        return {
            "queue_depth": self.queue_depth(),
            "max_queue_depth": self._max_queue_depth,
            "enqueue_count": self._enqueue_count,
            "dispatch_count": self._dispatch_count,
            "max_observed_depth": self._max_observed_depth,
            "latency_target_ms": self._latency_target_ms,
            "last_dispatch_latency_ms": latency,
            "latency_over_target": over_target,
        }

    def queue_export(self) -> list[dict[str, Any]]:
        tasks = sorted(
            self._tasks.values(),
            key=lambda task: (-task.priority, -task.need_score, task.enqueued_at, task.task_id),
        )
        return [task.to_dict() for task in tasks]

    def _validate_payload(self, payload: dict[str, Any]) -> None:
        try:
            encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        except TypeError as exc:
            raise SchedulerTaskError(
                f"scheduler payload is not JSON-serializable: {exc}"
            ) from exc
        if len(encoded) > DEFAULT_MAX_EVENT_SIZE_BYTES:
            raise SchedulerTaskError(
                f"scheduler payload exceeds {DEFAULT_MAX_EVENT_SIZE_BYTES} bytes"
            )

    def _elapsed_ms(self, iso_timestamp: str) -> float:
        enqueued = datetime.fromisoformat(iso_timestamp)
        if enqueued.tzinfo is None:
            enqueued = enqueued.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return (now - enqueued).total_seconds() * 1000.0
