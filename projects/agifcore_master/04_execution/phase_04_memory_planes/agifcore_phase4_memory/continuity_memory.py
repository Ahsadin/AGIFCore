from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

MAX_CONTINUITY_ENTRIES = 256
MAX_CONTINUITY_BYTES = 1024 * 1024


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class ContinuityMemoryError(ValueError):
    """Raised when continuity anchors violate the bounded Phase 4 surface."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContinuityMemoryError(f"{field_name} must be a non-empty string")
    return value


def _require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ContinuityMemoryError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        text = _require_non_empty_str(item, f"{field_name}[]")
        if text in seen:
            raise ContinuityMemoryError(f"{field_name} contains duplicate entries")
        seen.add(text)
        result.append(text)
    return result


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContinuityMemoryError(f"{field_name} must be a mapping")
    return dict(value)


@dataclass(slots=True)
class ContinuityAnchor:
    anchor_id: str
    subject: str
    continuity_kind: str
    statement: str
    provenance_refs: list[str]
    created_at: str
    updated_at: str
    status: str = "active"
    superseded_by: str | None = None
    correction_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "anchor_id": self.anchor_id,
            "subject": self.subject,
            "continuity_kind": self.continuity_kind,
            "statement": self.statement,
            "provenance_refs": list(self.provenance_refs),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "superseded_by": self.superseded_by,
            "correction_refs": list(self.correction_refs),
            "metadata": deepcopy(self.metadata),
        }


class ContinuityMemoryStore:
    """Correction-aware self-history anchors that stay distinct from episodic history."""

    def __init__(
        self,
        *,
        store_id: str = "phase-04-continuity-memory",
        max_entries: int = MAX_CONTINUITY_ENTRIES,
        max_state_bytes: int = MAX_CONTINUITY_BYTES,
    ) -> None:
        self.store_id = store_id
        self.max_entries = max_entries
        self.max_state_bytes = max_state_bytes
        self._anchors: dict[str, ContinuityAnchor] = {}
        self._order: list[str] = []

    def record_anchor(
        self,
        *,
        anchor_id: str,
        subject: str,
        continuity_kind: str,
        statement: str,
        provenance_refs: list[str],
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        normalized_anchor_id = _require_non_empty_str(anchor_id, "anchor_id")
        if normalized_anchor_id in self._anchors:
            raise ContinuityMemoryError(f"duplicate anchor_id: {normalized_anchor_id}")
        timestamp = utc_timestamp()
        anchor = ContinuityAnchor(
            anchor_id=normalized_anchor_id,
            subject=_require_non_empty_str(subject, "subject"),
            continuity_kind=_require_non_empty_str(continuity_kind, "continuity_kind"),
            statement=_require_non_empty_str(statement, "statement"),
            provenance_refs=_require_unique_str_list(provenance_refs, "provenance_refs"),
            created_at=timestamp,
            updated_at=timestamp,
            metadata=_require_mapping(metadata or {}, "metadata"),
        )
        self._anchors[anchor.anchor_id] = anchor
        self._order.append(anchor.anchor_id)
        self._ensure_size()
        return anchor.anchor_id

    def mark_superseded(
        self,
        *,
        anchor_id: str,
        superseded_by: str,
        correction_ref: str | None = None,
    ) -> None:
        anchor = self._get_anchor(anchor_id)
        anchor.status = "superseded"
        anchor.superseded_by = _require_non_empty_str(superseded_by, "superseded_by")
        if correction_ref is not None:
            normalized = _require_non_empty_str(correction_ref, "correction_ref")
            if normalized not in anchor.correction_refs:
                anchor.correction_refs.append(normalized)
        anchor.updated_at = utc_timestamp()
        self._ensure_size()

    def active_anchor_ids(self) -> list[str]:
        return [anchor_id for anchor_id in self._order if self._anchors[anchor_id].status == "active"]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_04.continuity_memory.v1",
            "store_id": self.store_id,
            "max_entries": self.max_entries,
            "anchors": [self._anchors[anchor_id].to_dict() for anchor_id in self._order],
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_04.continuity_memory.v1":
            raise ContinuityMemoryError("continuity memory schema mismatch")
        self.store_id = _require_non_empty_str(payload.get("store_id"), "store_id")
        max_entries = payload.get("max_entries", self.max_entries)
        if not isinstance(max_entries, int) or max_entries <= 0:
            raise ContinuityMemoryError("max_entries must be a positive integer")
        self.max_entries = max_entries
        anchors = payload.get("anchors", [])
        if not isinstance(anchors, list):
            raise ContinuityMemoryError("anchors must be a list")
        self._anchors = {}
        self._order = []
        for anchor_payload in anchors:
            anchor_map = _require_mapping(anchor_payload, "anchor")
            anchor = ContinuityAnchor(
                anchor_id=_require_non_empty_str(anchor_map.get("anchor_id"), "anchor_id"),
                subject=_require_non_empty_str(anchor_map.get("subject"), "subject"),
                continuity_kind=_require_non_empty_str(anchor_map.get("continuity_kind"), "continuity_kind"),
                statement=_require_non_empty_str(anchor_map.get("statement"), "statement"),
                provenance_refs=_require_unique_str_list(anchor_map.get("provenance_refs", []), "provenance_refs"),
                created_at=_require_non_empty_str(anchor_map.get("created_at"), "created_at"),
                updated_at=_require_non_empty_str(anchor_map.get("updated_at"), "updated_at"),
                status=_require_non_empty_str(anchor_map.get("status", "active"), "status"),
                superseded_by=anchor_map.get("superseded_by"),
                correction_refs=_require_unique_str_list(anchor_map.get("correction_refs", []), "correction_refs"),
                metadata=_require_mapping(anchor_map.get("metadata", {}), "metadata"),
            )
            self._anchors[anchor.anchor_id] = anchor
            self._order.append(anchor.anchor_id)
        self._ensure_size()

    def _get_anchor(self, anchor_id: str) -> ContinuityAnchor:
        normalized = _require_non_empty_str(anchor_id, "anchor_id")
        anchor = self._anchors.get(normalized)
        if anchor is None:
            raise ContinuityMemoryError(f"unknown anchor_id: {normalized}")
        return anchor

    def _ensure_size(self) -> None:
        if len(self._order) > self.max_entries:
            raise ContinuityMemoryError("continuity memory exceeds max entry count")
        size_bytes = canonical_size_bytes(self.export_state())
        if size_bytes > self.max_state_bytes:
            raise ContinuityMemoryError("continuity memory exceeds max state bytes")
