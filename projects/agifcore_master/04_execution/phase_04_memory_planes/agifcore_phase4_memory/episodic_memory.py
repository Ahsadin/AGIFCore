from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

MAX_EPISODIC_RECORDS = 512
MAX_EPISODIC_BYTES = 2 * 1024 * 1024


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class EpisodicMemoryError(ValueError):
    """Raised when replayable episodic memory behavior is violated."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EpisodicMemoryError(f"{field_name} must be a non-empty string")
    return value


def _require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise EpisodicMemoryError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        text = _require_non_empty_str(item, f"{field_name}[]")
        if text in seen:
            raise EpisodicMemoryError(f"{field_name} contains duplicate entries")
        seen.add(text)
        result.append(text)
    return result


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise EpisodicMemoryError(f"{field_name} must be a mapping")
    return dict(value)


@dataclass(slots=True)
class EpisodicCorrectionMarker:
    correction_id: str
    reason: str
    corrected_at: str
    replacement_event_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "correction_id": self.correction_id,
            "reason": self.reason,
            "corrected_at": self.corrected_at,
            "replacement_event_id": self.replacement_event_id,
        }


@dataclass(slots=True)
class EpisodicEvent:
    event_id: str
    conversation_id: str
    turn_id: str
    event_type: str
    event_summary: str
    content_refs: list[str]
    provenance_refs: list[str]
    created_at: str
    correction_markers: list[EpisodicCorrectionMarker] = field(default_factory=list)
    correction_status: str = "original"

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "conversation_id": self.conversation_id,
            "turn_id": self.turn_id,
            "event_type": self.event_type,
            "event_summary": self.event_summary,
            "content_refs": list(self.content_refs),
            "provenance_refs": list(self.provenance_refs),
            "created_at": self.created_at,
            "correction_markers": [item.to_dict() for item in self.correction_markers],
            "correction_status": self.correction_status,
        }


class EpisodicMemoryStore:
    """Replayable event-style history with explicit correction markers."""

    def __init__(
        self,
        *,
        store_id: str = "phase-04-episodic-memory",
        max_records: int = MAX_EPISODIC_RECORDS,
        max_state_bytes: int = MAX_EPISODIC_BYTES,
    ) -> None:
        self.store_id = store_id
        self.max_records = max_records
        self.max_state_bytes = max_state_bytes
        self._events: dict[str, EpisodicEvent] = {}
        self._order: list[str] = []

    def append_event(
        self,
        *,
        event_id: str,
        conversation_id: str,
        turn_id: str,
        event_type: str,
        event_summary: str,
        content_refs: list[str] | None = None,
        provenance_refs: list[str] | None = None,
    ) -> str:
        normalized_event_id = _require_non_empty_str(event_id, "event_id")
        if normalized_event_id in self._events:
            raise EpisodicMemoryError(f"duplicate event_id: {normalized_event_id}")
        event = EpisodicEvent(
            event_id=normalized_event_id,
            conversation_id=_require_non_empty_str(conversation_id, "conversation_id"),
            turn_id=_require_non_empty_str(turn_id, "turn_id"),
            event_type=_require_non_empty_str(event_type, "event_type"),
            event_summary=_require_non_empty_str(event_summary, "event_summary"),
            content_refs=_require_unique_str_list(content_refs or [], "content_refs"),
            provenance_refs=_require_unique_str_list(provenance_refs or [], "provenance_refs"),
            created_at=utc_timestamp(),
        )
        self._events[event.event_id] = event
        self._order.append(event.event_id)
        self._ensure_size()
        return event.event_id

    def add_correction_marker(
        self,
        *,
        event_id: str,
        correction_id: str,
        reason: str,
        replacement_event_id: str | None = None,
    ) -> None:
        event = self._get_event(event_id)
        event.correction_markers.append(
            EpisodicCorrectionMarker(
                correction_id=_require_non_empty_str(correction_id, "correction_id"),
                reason=_require_non_empty_str(reason, "reason"),
                corrected_at=utc_timestamp(),
                replacement_event_id=replacement_event_id,
            )
        )
        event.correction_status = "corrected"
        self._ensure_size()

    def recent_window(self, *, limit: int = 20) -> list[dict[str, Any]]:
        if limit <= 0:
            raise EpisodicMemoryError("limit must be positive")
        return [self._events[event_id].to_dict() for event_id in self._order[-limit:]]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_04.episodic_memory.v1",
            "store_id": self.store_id,
            "max_records": self.max_records,
            "events": [self._events[event_id].to_dict() for event_id in self._order],
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_04.episodic_memory.v1":
            raise EpisodicMemoryError("episodic memory schema mismatch")
        self.store_id = _require_non_empty_str(payload.get("store_id"), "store_id")
        max_records = payload.get("max_records", self.max_records)
        if not isinstance(max_records, int) or max_records <= 0:
            raise EpisodicMemoryError("max_records must be a positive integer")
        self.max_records = max_records
        events = payload.get("events", [])
        if not isinstance(events, list):
            raise EpisodicMemoryError("events must be a list")
        self._events = {}
        self._order = []
        for event_payload in events:
            event_map = _require_mapping(event_payload, "event")
            event = EpisodicEvent(
                event_id=_require_non_empty_str(event_map.get("event_id"), "event_id"),
                conversation_id=_require_non_empty_str(event_map.get("conversation_id"), "conversation_id"),
                turn_id=_require_non_empty_str(event_map.get("turn_id"), "turn_id"),
                event_type=_require_non_empty_str(event_map.get("event_type"), "event_type"),
                event_summary=_require_non_empty_str(event_map.get("event_summary"), "event_summary"),
                content_refs=_require_unique_str_list(event_map.get("content_refs", []), "content_refs"),
                provenance_refs=_require_unique_str_list(event_map.get("provenance_refs", []), "provenance_refs"),
                created_at=_require_non_empty_str(event_map.get("created_at"), "created_at"),
                correction_markers=[
                    EpisodicCorrectionMarker(
                        correction_id=_require_non_empty_str(marker.get("correction_id"), "correction_id"),
                        reason=_require_non_empty_str(marker.get("reason"), "reason"),
                        corrected_at=_require_non_empty_str(marker.get("corrected_at"), "corrected_at"),
                        replacement_event_id=marker.get("replacement_event_id"),
                    )
                    for marker in event_map.get("correction_markers", [])
                ],
                correction_status=_require_non_empty_str(
                    event_map.get("correction_status", "original"), "correction_status"
                ),
            )
            self._events[event.event_id] = event
            self._order.append(event.event_id)
        self._ensure_size()

    def _get_event(self, event_id: str) -> EpisodicEvent:
        normalized = _require_non_empty_str(event_id, "event_id")
        event = self._events.get(normalized)
        if event is None:
            raise EpisodicMemoryError(f"unknown event_id: {normalized}")
        return event

    def _ensure_size(self) -> None:
        if len(self._order) > self.max_records:
            raise EpisodicMemoryError("episodic memory exceeds max record count")
        size_bytes = canonical_size_bytes(self.export_state())
        if size_bytes > self.max_state_bytes:
            raise EpisodicMemoryError("episodic memory exceeds max state bytes")
