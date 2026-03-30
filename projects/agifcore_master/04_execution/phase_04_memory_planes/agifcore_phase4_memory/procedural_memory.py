from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

MAX_PROCEDURAL_ENTRIES = 512
MAX_PROCEDURAL_BYTES = 2 * 1024 * 1024


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class ProceduralMemoryError(ValueError):
    """Raised when procedural memory violates the Phase 4 procedure boundary."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProceduralMemoryError(f"{field_name} must be a non-empty string")
    return value


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ProceduralMemoryError(f"{field_name} must be a mapping")
    return dict(value)


def _require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ProceduralMemoryError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        text = _require_non_empty_str(item, f"{field_name}[]")
        if text in seen:
            raise ProceduralMemoryError(f"{field_name} contains duplicate entries")
        seen.add(text)
        result.append(text)
    return result


@dataclass(slots=True)
class ProcedureEntry:
    procedure_id: str
    procedure_name: str
    objective: str
    steps: list[str]
    preconditions: list[str]
    postconditions: list[str]
    constraints: list[str]
    provenance_refs: list[str]
    review_ref: str
    source_candidate_id: str
    graph_refs: list[str]
    created_at: str
    updated_at: str
    status: str = "active"
    retirement_ref: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "procedure_id": self.procedure_id,
            "procedure_name": self.procedure_name,
            "objective": self.objective,
            "steps": list(self.steps),
            "preconditions": list(self.preconditions),
            "postconditions": list(self.postconditions),
            "constraints": list(self.constraints),
            "provenance_refs": list(self.provenance_refs),
            "review_ref": self.review_ref,
            "source_candidate_id": self.source_candidate_id,
            "graph_refs": list(self.graph_refs),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "retirement_ref": self.retirement_ref,
            "metadata": deepcopy(self.metadata),
        }


class ProceduralMemoryStore:
    """Reusable procedures with explicit constraints and no automatic execution path."""

    def __init__(
        self,
        *,
        store_id: str = "phase-04-procedural-memory",
        max_entries: int = MAX_PROCEDURAL_ENTRIES,
        max_state_bytes: int = MAX_PROCEDURAL_BYTES,
    ) -> None:
        self.store_id = store_id
        self.max_entries = max_entries
        self.max_state_bytes = max_state_bytes
        self._entries: dict[str, ProcedureEntry] = {}
        self._order: list[str] = []

    def add_procedure(
        self,
        *,
        procedure_id: str,
        procedure_name: str,
        objective: str,
        steps: list[str],
        preconditions: list[str],
        postconditions: list[str],
        constraints: list[str],
        provenance_refs: list[str],
        review_ref: str,
        source_candidate_id: str,
        graph_refs: list[str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        normalized_id = _require_non_empty_str(procedure_id, "procedure_id")
        if normalized_id in self._entries:
            raise ProceduralMemoryError(f"duplicate procedure_id: {normalized_id}")
        timestamp = utc_timestamp()
        entry = ProcedureEntry(
            procedure_id=normalized_id,
            procedure_name=_require_non_empty_str(procedure_name, "procedure_name"),
            objective=_require_non_empty_str(objective, "objective"),
            steps=_require_unique_str_list(steps, "steps"),
            preconditions=_require_unique_str_list(preconditions, "preconditions"),
            postconditions=_require_unique_str_list(postconditions, "postconditions"),
            constraints=_require_unique_str_list(constraints, "constraints"),
            provenance_refs=_require_unique_str_list(provenance_refs, "provenance_refs"),
            review_ref=_require_non_empty_str(review_ref, "review_ref"),
            source_candidate_id=_require_non_empty_str(source_candidate_id, "source_candidate_id"),
            graph_refs=_require_unique_str_list(graph_refs or [], "graph_refs"),
            created_at=timestamp,
            updated_at=timestamp,
            metadata=_require_mapping(metadata or {}, "metadata"),
        )
        self._entries[entry.procedure_id] = entry
        self._order.append(entry.procedure_id)
        self._ensure_size()
        return entry.procedure_id

    def retire_procedure(self, *, procedure_id: str, retirement_ref: str) -> None:
        entry = self._get_entry(procedure_id)
        entry.status = "retired"
        entry.retirement_ref = _require_non_empty_str(retirement_ref, "retirement_ref")
        entry.updated_at = utc_timestamp()
        self._ensure_size()

    def procedure_state(self, procedure_id: str) -> dict[str, Any]:
        return self._get_entry(procedure_id).to_dict()

    def active_procedure_ids(self) -> list[str]:
        return [
            procedure_id
            for procedure_id in self._order
            if self._entries[procedure_id].status == "active"
        ]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_04.procedural_memory.v1",
            "store_id": self.store_id,
            "max_entries": self.max_entries,
            "entries": [self._entries[entry_id].to_dict() for entry_id in self._order],
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_04.procedural_memory.v1":
            raise ProceduralMemoryError("procedural memory schema mismatch")
        self.store_id = _require_non_empty_str(payload.get("store_id"), "store_id")
        max_entries = payload.get("max_entries", self.max_entries)
        if not isinstance(max_entries, int) or max_entries <= 0:
            raise ProceduralMemoryError("max_entries must be a positive integer")
        self.max_entries = max_entries
        entries = payload.get("entries", [])
        if not isinstance(entries, list):
            raise ProceduralMemoryError("entries must be a list")
        self._entries = {}
        self._order = []
        for entry_payload in entries:
            entry_map = _require_mapping(entry_payload, "entry")
            entry = ProcedureEntry(
                procedure_id=_require_non_empty_str(entry_map.get("procedure_id"), "procedure_id"),
                procedure_name=_require_non_empty_str(entry_map.get("procedure_name"), "procedure_name"),
                objective=_require_non_empty_str(entry_map.get("objective"), "objective"),
                steps=_require_unique_str_list(entry_map.get("steps", []), "steps"),
                preconditions=_require_unique_str_list(entry_map.get("preconditions", []), "preconditions"),
                postconditions=_require_unique_str_list(entry_map.get("postconditions", []), "postconditions"),
                constraints=_require_unique_str_list(entry_map.get("constraints", []), "constraints"),
                provenance_refs=_require_unique_str_list(entry_map.get("provenance_refs", []), "provenance_refs"),
                review_ref=_require_non_empty_str(entry_map.get("review_ref"), "review_ref"),
                source_candidate_id=_require_non_empty_str(entry_map.get("source_candidate_id"), "source_candidate_id"),
                graph_refs=_require_unique_str_list(entry_map.get("graph_refs", []), "graph_refs"),
                created_at=_require_non_empty_str(entry_map.get("created_at"), "created_at"),
                updated_at=_require_non_empty_str(entry_map.get("updated_at"), "updated_at"),
                status=_require_non_empty_str(entry_map.get("status", "active"), "status"),
                retirement_ref=entry_map.get("retirement_ref"),
                metadata=_require_mapping(entry_map.get("metadata", {}), "metadata"),
            )
            self._entries[entry.procedure_id] = entry
            self._order.append(entry.procedure_id)
        self._ensure_size()

    def _get_entry(self, procedure_id: str) -> ProcedureEntry:
        normalized = _require_non_empty_str(procedure_id, "procedure_id")
        entry = self._entries.get(normalized)
        if entry is None:
            raise ProceduralMemoryError(f"unknown procedure_id: {normalized}")
        return entry

    def _ensure_size(self) -> None:
        if len(self._order) > self.max_entries:
            raise ProceduralMemoryError("procedural memory exceeds max entry count")
        size_bytes = canonical_size_bytes(self.export_state())
        if size_bytes > self.max_state_bytes:
            raise ProceduralMemoryError("procedural memory exceeds max state bytes")
