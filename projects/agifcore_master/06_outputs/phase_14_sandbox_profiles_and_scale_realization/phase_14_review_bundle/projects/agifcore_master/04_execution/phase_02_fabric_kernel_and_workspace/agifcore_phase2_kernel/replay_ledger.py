from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from event_types import KernelContractError

DEFAULT_MAX_REPLAY_LEDGER_BYTES = 512 * 1024 * 1024


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class ReplayLedgerError(KernelContractError):
    """Raised when replay ledger operations are invalid."""


@dataclass(frozen=True, slots=True)
class ReplayRecord:
    replay_id: str
    conversation_id: str
    turn_id: str
    trace_anchor_hash: str
    state_anchor_hash: str
    event_ids: tuple[str, ...]
    recorded_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "replay_id": self.replay_id,
            "conversation_id": self.conversation_id,
            "turn_id": self.turn_id,
            "trace_anchor_hash": self.trace_anchor_hash,
            "state_anchor_hash": self.state_anchor_hash,
            "event_ids": list(self.event_ids),
            "recorded_at": self.recorded_at,
        }


class ReplayLedger:
    """Deterministic replay anchor ledger for Phase 2."""

    def __init__(self, *, max_ledger_bytes: int = DEFAULT_MAX_REPLAY_LEDGER_BYTES) -> None:
        self._max_ledger_bytes = max_ledger_bytes
        self._records: dict[str, ReplayRecord] = {}
        self._order: list[str] = []

    def record_replay(
        self,
        *,
        replay_id: str,
        conversation_id: str,
        turn_id: str,
        trace_export: list[dict[str, Any]],
        state_export: dict[str, Any],
        event_ids: list[str],
    ) -> ReplayRecord:
        if not replay_id:
            raise ReplayLedgerError("replay_id must be non-empty")
        if not conversation_id:
            raise ReplayLedgerError("conversation_id must be non-empty")
        if not turn_id:
            raise ReplayLedgerError("turn_id must be non-empty")
        if replay_id in self._records:
            raise ReplayLedgerError(f"duplicate replay_id: {replay_id}")

        trace_anchor_hash = self._deterministic_hash(
            {"conversation_id": conversation_id, "turn_id": turn_id, "trace_export": trace_export}
        )
        state_anchor_hash = self._deterministic_hash(state_export)
        record = ReplayRecord(
            replay_id=replay_id,
            conversation_id=conversation_id,
            turn_id=turn_id,
            trace_anchor_hash=trace_anchor_hash,
            state_anchor_hash=state_anchor_hash,
            event_ids=tuple(event_ids),
            recorded_at=utc_timestamp(),
        )
        self._records[replay_id] = record
        self._order.append(replay_id)
        self._enforce_budget()
        return record

    def verify_replay(
        self,
        *,
        replay_id: str,
        trace_export: list[dict[str, Any]],
        state_export: dict[str, Any],
    ) -> dict[str, Any]:
        record = self._records.get(replay_id)
        if record is None:
            raise ReplayLedgerError(f"replay record not found: {replay_id}")
        trace_hash = self._deterministic_hash(
            {
                "conversation_id": record.conversation_id,
                "turn_id": record.turn_id,
                "trace_export": trace_export,
            }
        )
        state_hash = self._deterministic_hash(state_export)
        return {
            "replay_id": replay_id,
            "conversation_id": record.conversation_id,
            "turn_id": record.turn_id,
            "trace_match": trace_hash == record.trace_anchor_hash,
            "state_match": state_hash == record.state_anchor_hash,
            "trace_anchor_hash": record.trace_anchor_hash,
            "state_anchor_hash": record.state_anchor_hash,
            "replay_match": trace_hash == record.trace_anchor_hash
            and state_hash == record.state_anchor_hash,
        }

    def replay_export(self) -> dict[str, Any]:
        records = [self._records[replay_id].to_dict() for replay_id in self._order]
        return {
            "record_count": len(records),
            "max_ledger_bytes": self._max_ledger_bytes,
            "records": records,
        }

    def _deterministic_hash(self, payload: Any) -> str:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _enforce_budget(self) -> None:
        encoded = json.dumps(
            self.replay_export(), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        if len(encoded) > self._max_ledger_bytes:
            last = self._order.pop()
            self._records.pop(last, None)
            raise ReplayLedgerError(
                f"replay ledger exceeds max size of {self._max_ledger_bytes} bytes"
            )
