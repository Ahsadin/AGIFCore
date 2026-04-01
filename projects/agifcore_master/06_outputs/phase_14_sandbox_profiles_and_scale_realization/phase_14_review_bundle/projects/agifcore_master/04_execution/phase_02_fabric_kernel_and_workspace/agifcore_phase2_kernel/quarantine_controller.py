from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from event_types import KernelContractError

DEFAULT_MAX_QUARANTINE_HISTORY = 4096


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class QuarantineControllerError(KernelContractError):
    """Raised when quarantine operations are invalid."""


@dataclass(slots=True)
class QuarantineRecord:
    quarantine_ref: str
    cell_id: str
    reason_code: str
    reason_text: str
    rollback_ref: str | None
    status: str
    created_at: str
    released_at: str | None = None
    release_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "quarantine_ref": self.quarantine_ref,
            "cell_id": self.cell_id,
            "reason_code": self.reason_code,
            "reason_text": self.reason_text,
            "rollback_ref": self.rollback_ref,
            "status": self.status,
            "created_at": self.created_at,
            "released_at": self.released_at,
            "release_reason": self.release_reason,
        }


class QuarantineController:
    """Explicit quarantine control with active and historical records."""

    def __init__(self, *, max_history: int = DEFAULT_MAX_QUARANTINE_HISTORY) -> None:
        self._max_history = max_history
        self._counter = 0
        self._active: dict[str, QuarantineRecord] = {}
        self._history: list[QuarantineRecord] = []

    def quarantine_cell(
        self,
        *,
        cell_id: str,
        reason_code: str,
        reason_text: str,
        rollback_ref: str | None = None,
    ) -> QuarantineRecord:
        if not cell_id:
            raise QuarantineControllerError("cell_id must be non-empty")
        if not reason_code:
            raise QuarantineControllerError("reason_code must be non-empty")
        if not reason_text:
            raise QuarantineControllerError("reason_text must be non-empty")
        if self.active_for_cell(cell_id) is not None:
            raise QuarantineControllerError(f"cell already quarantined: {cell_id}")
        self._counter += 1
        record = QuarantineRecord(
            quarantine_ref=f"quarantine-{self._counter:08d}",
            cell_id=cell_id,
            reason_code=reason_code,
            reason_text=reason_text,
            rollback_ref=rollback_ref,
            status="active",
            created_at=utc_timestamp(),
        )
        self._active[record.quarantine_ref] = record
        self._history.append(record)
        self._trim_history()
        return record

    def release_quarantine(
        self, *, quarantine_ref: str, release_reason: str
    ) -> QuarantineRecord:
        if not release_reason:
            raise QuarantineControllerError("release_reason must be non-empty")
        record = self._active.pop(quarantine_ref, None)
        if record is None:
            raise QuarantineControllerError(f"quarantine record not active: {quarantine_ref}")
        record.status = "released"
        record.released_at = utc_timestamp()
        record.release_reason = release_reason
        return record

    def active_for_cell(self, cell_id: str) -> QuarantineRecord | None:
        for record in self._active.values():
            if record.cell_id == cell_id and record.status == "active":
                return record
        return None

    def active_export(self) -> list[dict[str, Any]]:
        records = sorted(self._active.values(), key=lambda item: item.quarantine_ref)
        return [record.to_dict() for record in records]

    def history_export(self) -> list[dict[str, Any]]:
        return [record.to_dict() for record in self._history]

    def _trim_history(self) -> None:
        if len(self._history) <= self._max_history:
            return
        self._history = self._history[-self._max_history :]
