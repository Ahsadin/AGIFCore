from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

MAX_SEMANTIC_ENTRIES = 2048
MAX_SEMANTIC_BYTES = 8 * 1024 * 1024
FORBIDDEN_METADATA_KEYS = {"raw_transcript", "conversation_text", "utterance_text"}


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class SemanticMemoryError(ValueError):
    """Raised when semantic memory violates the Phase 4 abstraction boundary."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SemanticMemoryError(f"{field_name} must be a non-empty string")
    return value


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise SemanticMemoryError(f"{field_name} must be a mapping")
    return dict(value)


def _require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise SemanticMemoryError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        text = _require_non_empty_str(item, f"{field_name}[]")
        if text in seen:
            raise SemanticMemoryError(f"{field_name} contains duplicate entries")
        seen.add(text)
        result.append(text)
    return result


@dataclass(slots=True)
class SemanticMemoryEntry:
    entry_id: str
    concept_type: str
    abstraction: str
    provenance_refs: list[str]
    review_ref: str
    source_candidate_id: str
    supporting_refs: list[str]
    graph_refs: list[str]
    created_at: str
    updated_at: str
    status: str = "active"
    superseded_by: str | None = None
    correction_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "concept_type": self.concept_type,
            "abstraction": self.abstraction,
            "provenance_refs": list(self.provenance_refs),
            "review_ref": self.review_ref,
            "source_candidate_id": self.source_candidate_id,
            "supporting_refs": list(self.supporting_refs),
            "graph_refs": list(self.graph_refs),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "superseded_by": self.superseded_by,
            "correction_refs": list(self.correction_refs),
            "metadata": deepcopy(self.metadata),
        }


class SemanticMemoryStore:
    """Reviewed abstraction memory with explicit provenance and supersession."""

    def __init__(
        self,
        *,
        store_id: str = "phase-04-semantic-memory",
        max_entries: int = MAX_SEMANTIC_ENTRIES,
        max_state_bytes: int = MAX_SEMANTIC_BYTES,
    ) -> None:
        self.store_id = store_id
        self.max_entries = max_entries
        self.max_state_bytes = max_state_bytes
        self._entries: dict[str, SemanticMemoryEntry] = {}
        self._order: list[str] = []

    def add_entry(
        self,
        *,
        entry_id: str,
        concept_type: str,
        abstraction: str,
        provenance_refs: list[str],
        review_ref: str,
        source_candidate_id: str,
        supporting_refs: list[str] | None = None,
        graph_refs: list[str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        normalized_entry_id = _require_non_empty_str(entry_id, "entry_id")
        if normalized_entry_id in self._entries:
            raise SemanticMemoryError(f"duplicate entry_id: {normalized_entry_id}")
        metadata_map = _require_mapping(metadata or {}, "metadata")
        if FORBIDDEN_METADATA_KEYS & set(metadata_map.keys()):
            raise SemanticMemoryError("semantic memory metadata may not contain transcript fields")
        timestamp = utc_timestamp()
        entry = SemanticMemoryEntry(
            entry_id=normalized_entry_id,
            concept_type=_require_non_empty_str(concept_type, "concept_type"),
            abstraction=_require_non_empty_str(abstraction, "abstraction"),
            provenance_refs=_require_unique_str_list(provenance_refs, "provenance_refs"),
            review_ref=_require_non_empty_str(review_ref, "review_ref"),
            source_candidate_id=_require_non_empty_str(source_candidate_id, "source_candidate_id"),
            supporting_refs=_require_unique_str_list(supporting_refs or [], "supporting_refs"),
            graph_refs=_require_unique_str_list(graph_refs or [], "graph_refs"),
            created_at=timestamp,
            updated_at=timestamp,
            metadata=metadata_map,
        )
        self._entries[entry.entry_id] = entry
        self._order.append(entry.entry_id)
        self._ensure_size()
        return entry.entry_id

    def mark_superseded(
        self,
        *,
        entry_id: str,
        superseded_by: str,
        correction_ref: str | None = None,
    ) -> None:
        entry = self._get_entry(entry_id)
        entry.status = "superseded"
        entry.superseded_by = _require_non_empty_str(superseded_by, "superseded_by")
        if correction_ref is not None:
            normalized = _require_non_empty_str(correction_ref, "correction_ref")
            if normalized not in entry.correction_refs:
                entry.correction_refs.append(normalized)
        entry.updated_at = utc_timestamp()
        self._ensure_size()

    def entry_state(self, entry_id: str) -> dict[str, Any]:
        return self._get_entry(entry_id).to_dict()

    def active_entry_ids(self) -> list[str]:
        return [entry_id for entry_id in self._order if self._entries[entry_id].status == "active"]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_04.semantic_memory.v1",
            "store_id": self.store_id,
            "max_entries": self.max_entries,
            "entries": [self._entries[entry_id].to_dict() for entry_id in self._order],
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_04.semantic_memory.v1":
            raise SemanticMemoryError("semantic memory schema mismatch")
        self.store_id = _require_non_empty_str(payload.get("store_id"), "store_id")
        max_entries = payload.get("max_entries", self.max_entries)
        if not isinstance(max_entries, int) or max_entries <= 0:
            raise SemanticMemoryError("max_entries must be a positive integer")
        self.max_entries = max_entries
        entries = payload.get("entries", [])
        if not isinstance(entries, list):
            raise SemanticMemoryError("entries must be a list")
        self._entries = {}
        self._order = []
        for entry_payload in entries:
            entry_map = _require_mapping(entry_payload, "entry")
            metadata_map = _require_mapping(entry_map.get("metadata", {}), "metadata")
            if FORBIDDEN_METADATA_KEYS & set(metadata_map.keys()):
                raise SemanticMemoryError("semantic memory metadata may not contain transcript fields")
            entry = SemanticMemoryEntry(
                entry_id=_require_non_empty_str(entry_map.get("entry_id"), "entry_id"),
                concept_type=_require_non_empty_str(entry_map.get("concept_type"), "concept_type"),
                abstraction=_require_non_empty_str(entry_map.get("abstraction"), "abstraction"),
                provenance_refs=_require_unique_str_list(entry_map.get("provenance_refs", []), "provenance_refs"),
                review_ref=_require_non_empty_str(entry_map.get("review_ref"), "review_ref"),
                source_candidate_id=_require_non_empty_str(entry_map.get("source_candidate_id"), "source_candidate_id"),
                supporting_refs=_require_unique_str_list(entry_map.get("supporting_refs", []), "supporting_refs"),
                graph_refs=_require_unique_str_list(entry_map.get("graph_refs", []), "graph_refs"),
                created_at=_require_non_empty_str(entry_map.get("created_at"), "created_at"),
                updated_at=_require_non_empty_str(entry_map.get("updated_at"), "updated_at"),
                status=_require_non_empty_str(entry_map.get("status", "active"), "status"),
                superseded_by=entry_map.get("superseded_by"),
                correction_refs=_require_unique_str_list(entry_map.get("correction_refs", []), "correction_refs"),
                metadata=metadata_map,
            )
            self._entries[entry.entry_id] = entry
            self._order.append(entry.entry_id)
        self._ensure_size()

    def _get_entry(self, entry_id: str) -> SemanticMemoryEntry:
        normalized = _require_non_empty_str(entry_id, "entry_id")
        entry = self._entries.get(normalized)
        if entry is None:
            raise SemanticMemoryError(f"unknown entry_id: {normalized}")
        return entry

    def _ensure_size(self) -> None:
        if len(self._order) > self.max_entries:
            raise SemanticMemoryError("semantic memory exceeds max entry count")
        size_bytes = canonical_size_bytes(self.export_state())
        if size_bytes > self.max_state_bytes:
            raise SemanticMemoryError("semantic memory exceeds max state bytes")
