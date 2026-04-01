from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from event_types import KernelContractError

DEFAULT_MAX_ROLLBACK_SNAPSHOTS = 8
DEFAULT_MAX_ROLLBACK_TOTAL_BYTES = 1024 * 1024 * 1024


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class RollbackControllerError(KernelContractError):
    """Raised when rollback snapshot operations fail."""


@dataclass(slots=True)
class RollbackSnapshot:
    rollback_ref: str
    state_hash: str
    state_payload: dict[str, Any]
    size_bytes: int
    label: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rollback_ref": self.rollback_ref,
            "state_hash": self.state_hash,
            "size_bytes": self.size_bytes,
            "label": self.label,
            "created_at": self.created_at,
        }


class RollbackController:
    """Bounded rollback snapshots with restore support."""

    def __init__(
        self,
        *,
        max_snapshots: int = DEFAULT_MAX_ROLLBACK_SNAPSHOTS,
        max_total_bytes: int = DEFAULT_MAX_ROLLBACK_TOTAL_BYTES,
    ) -> None:
        self._max_snapshots = max_snapshots
        self._max_total_bytes = max_total_bytes
        self._snapshot_counter = 0
        self._snapshots: list[RollbackSnapshot] = []

    def create_snapshot(self, *, state_export: dict[str, Any], label: str) -> dict[str, Any]:
        if not label:
            raise RollbackControllerError("snapshot label must be non-empty")
        encoded = json.dumps(
            state_export, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        snapshot = RollbackSnapshot(
            rollback_ref=f"rollback-{self._snapshot_counter + 1:08d}",
            state_hash=hashlib.sha256(encoded).hexdigest(),
            state_payload=deepcopy(state_export),
            size_bytes=len(encoded),
            label=label,
            created_at=utc_timestamp(),
        )
        self._snapshot_counter += 1
        self._snapshots.append(snapshot)
        evicted = self._trim_to_budget()
        return {
            "rollback_ref": snapshot.rollback_ref,
            "state_hash": snapshot.state_hash,
            "size_bytes": snapshot.size_bytes,
            "evicted_refs": evicted,
        }

    def restore_snapshot(self, *, rollback_ref: str) -> dict[str, Any]:
        snapshot = self._get_snapshot(rollback_ref)
        return {
            "rollback_ref": snapshot.rollback_ref,
            "state_hash": snapshot.state_hash,
            "state_export": deepcopy(snapshot.state_payload),
        }

    def snapshot_export(self) -> dict[str, Any]:
        return {
            "snapshot_count": len(self._snapshots),
            "max_snapshot_count": self._max_snapshots,
            "max_total_bytes": self._max_total_bytes,
            "total_bytes": self._total_bytes(),
            "snapshots": [snapshot.to_dict() for snapshot in self._snapshots],
        }

    def _trim_to_budget(self) -> list[str]:
        evicted: list[str] = []
        while len(self._snapshots) > self._max_snapshots:
            evicted.append(self._snapshots.pop(0).rollback_ref)
        while self._total_bytes() > self._max_total_bytes and self._snapshots:
            evicted.append(self._snapshots.pop(0).rollback_ref)
        if not self._snapshots:
            raise RollbackControllerError("rollback budget cannot retain any snapshot")
        return evicted

    def _total_bytes(self) -> int:
        return sum(snapshot.size_bytes for snapshot in self._snapshots)

    def _get_snapshot(self, rollback_ref: str) -> RollbackSnapshot:
        for snapshot in self._snapshots:
            if snapshot.rollback_ref == rollback_ref:
                return snapshot
        raise RollbackControllerError(f"rollback snapshot not found: {rollback_ref}")
