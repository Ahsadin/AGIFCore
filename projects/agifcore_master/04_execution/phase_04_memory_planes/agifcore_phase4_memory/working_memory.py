from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

MAX_WORKING_MEMORY_BYTES = 512 * 1024
MAX_PROMOTABLE_CANDIDATES = 64
ALLOWED_TARGET_PLANES = ("semantic", "procedural", "continuity")


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class WorkingMemoryError(ValueError):
    """Raised when bounded working-memory behavior is violated."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkingMemoryError(f"{field_name} must be a non-empty string")
    return value


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise WorkingMemoryError(f"{field_name} must be a mapping")
    return dict(value)


def _require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise WorkingMemoryError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        text = _require_non_empty_str(item, f"{field_name}[]")
        if text in seen:
            raise WorkingMemoryError(f"{field_name} contains duplicate entries")
        seen.add(text)
        result.append(text)
    return result


@dataclass(slots=True)
class WorkingCandidate:
    candidate_id: str
    source_turn_ref: str
    candidate_kind: str
    target_plane: str
    payload: dict[str, Any]
    provenance_refs: list[str]
    created_at: str
    review_ref: str | None = None
    status: str = "pending_review"

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "source_turn_ref": self.source_turn_ref,
            "candidate_kind": self.candidate_kind,
            "target_plane": self.target_plane,
            "payload": deepcopy(self.payload),
            "provenance_refs": list(self.provenance_refs),
            "created_at": self.created_at,
            "review_ref": self.review_ref,
            "status": self.status,
        }


@dataclass(slots=True)
class WorkingTurnState:
    conversation_id: str
    turn_id: str
    task_id: str
    support_refs: list[str] = field(default_factory=list)
    scratchpad: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_timestamp)
    updated_at: str = field(default_factory=utc_timestamp)

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "turn_id": self.turn_id,
            "task_id": self.task_id,
            "support_refs": list(self.support_refs),
            "scratchpad": deepcopy(self.scratchpad),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class WorkingMemoryStore:
    """Bounded current-turn memory with explicit promotable candidates."""

    def __init__(
        self,
        *,
        workspace_id: str = "phase-04-working-memory",
        max_state_bytes: int = MAX_WORKING_MEMORY_BYTES,
        max_candidates: int = MAX_PROMOTABLE_CANDIDATES,
    ) -> None:
        self.workspace_id = workspace_id
        self.max_state_bytes = max_state_bytes
        self.max_candidates = max_candidates
        self._turn_state: WorkingTurnState | None = None
        self._promotable_candidates: dict[str, WorkingCandidate] = {}

    def turn_ref(self, conversation_id: str, turn_id: str) -> str:
        return f"turn://{conversation_id}/{turn_id}"

    def bind_turn(
        self,
        *,
        conversation_id: str,
        turn_id: str,
        task_id: str,
        support_refs: list[str] | None = None,
        scratchpad: Mapping[str, Any] | None = None,
    ) -> str:
        state = WorkingTurnState(
            conversation_id=_require_non_empty_str(conversation_id, "conversation_id"),
            turn_id=_require_non_empty_str(turn_id, "turn_id"),
            task_id=_require_non_empty_str(task_id, "task_id"),
            support_refs=_require_unique_str_list(support_refs or [], "support_refs"),
            scratchpad=_require_mapping(scratchpad or {}, "scratchpad"),
        )
        self._turn_state = state
        self._ensure_size()
        return self.turn_ref(conversation_id, turn_id)

    def set_scratch_value(self, key: str, value: Any) -> None:
        state = self._require_turn_state()
        state.scratchpad[_require_non_empty_str(key, "key")] = deepcopy(value)
        state.updated_at = utc_timestamp()
        self._ensure_size()

    def add_support_ref(self, support_ref: str) -> None:
        state = self._require_turn_state()
        normalized = _require_non_empty_str(support_ref, "support_ref")
        if normalized not in state.support_refs:
            state.support_refs.append(normalized)
            state.updated_at = utc_timestamp()
            self._ensure_size()

    def add_candidate(
        self,
        *,
        candidate_id: str,
        candidate_kind: str,
        target_plane: str,
        payload: Mapping[str, Any],
        provenance_refs: list[str],
    ) -> str:
        if len(self._promotable_candidates) >= self.max_candidates:
            raise WorkingMemoryError("working memory candidate budget exceeded")
        if candidate_id in self._promotable_candidates:
            raise WorkingMemoryError(f"duplicate candidate_id: {candidate_id}")
        state = self._require_turn_state()
        normalized_target = _require_non_empty_str(target_plane, "target_plane")
        if normalized_target not in ALLOWED_TARGET_PLANES:
            raise WorkingMemoryError(f"target_plane must be one of {ALLOWED_TARGET_PLANES}")
        candidate = WorkingCandidate(
            candidate_id=_require_non_empty_str(candidate_id, "candidate_id"),
            source_turn_ref=self.turn_ref(state.conversation_id, state.turn_id),
            candidate_kind=_require_non_empty_str(candidate_kind, "candidate_kind"),
            target_plane=normalized_target,
            payload=_require_mapping(payload, "payload"),
            provenance_refs=_require_unique_str_list(provenance_refs, "provenance_refs"),
            created_at=utc_timestamp(),
        )
        self._promotable_candidates[candidate.candidate_id] = candidate
        self._ensure_size()
        return candidate.candidate_id

    def mark_candidate_reviewed(self, *, candidate_id: str, review_ref: str, status: str) -> None:
        candidate = self._get_candidate(candidate_id)
        candidate.review_ref = _require_non_empty_str(review_ref, "review_ref")
        normalized = _require_non_empty_str(status, "status")
        if normalized not in {"pending_review", "approved", "rejected", "held"}:
            raise WorkingMemoryError("status must be pending_review, approved, rejected, or held")
        candidate.status = normalized
        self._ensure_size()

    def consume_candidate(self, candidate_id: str) -> dict[str, Any]:
        candidate = self._get_candidate(candidate_id)
        return self._promotable_candidates.pop(candidate_id).to_dict()

    def candidate_ids(self, *, status: str | None = None) -> list[str]:
        candidates = self._promotable_candidates.values()
        if status is not None:
            candidates = [item for item in candidates if item.status == status]
        return [item.candidate_id for item in candidates]

    def memory_pressure(self) -> dict[str, Any]:
        exported = self.export_state()
        size_bytes = canonical_size_bytes(exported)
        return {
            "current_state_bytes": size_bytes,
            "max_state_bytes": self.max_state_bytes,
            "utilization": round(size_bytes / self.max_state_bytes, 4),
            "candidate_count": len(self._promotable_candidates),
            "max_candidate_count": self.max_candidates,
        }

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_04.working_memory.v1",
            "workspace_id": self.workspace_id,
            "turn_state": self._turn_state.to_dict() if self._turn_state else None,
            "promotable_candidates": [
                candidate.to_dict() for candidate in self._promotable_candidates.values()
            ],
            "memory_pressure": self.memory_pressure_summary(),
        }

    def memory_pressure_summary(self) -> dict[str, Any]:
        payload = {
            "candidate_count": len(self._promotable_candidates),
            "max_candidate_count": self.max_candidates,
        }
        base = {
            "schema": "agifcore.phase_04.working_memory.v1",
            "workspace_id": self.workspace_id,
            "turn_state": self._turn_state.to_dict() if self._turn_state else None,
            "promotable_candidates": [
                candidate.to_dict() for candidate in self._promotable_candidates.values()
            ],
        }
        size_bytes = canonical_size_bytes({**base, "memory_pressure": payload})
        payload.update(
            {
                "current_state_bytes": size_bytes,
                "max_state_bytes": self.max_state_bytes,
                "utilization": round(size_bytes / self.max_state_bytes, 4),
            }
        )
        return payload

    def load_state(self, payload: Mapping[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_04.working_memory.v1":
            raise WorkingMemoryError("working memory schema mismatch")
        self.workspace_id = _require_non_empty_str(payload.get("workspace_id"), "workspace_id")
        turn_state = payload.get("turn_state")
        if turn_state is None:
            self._turn_state = None
        else:
            turn_map = _require_mapping(turn_state, "turn_state")
            self._turn_state = WorkingTurnState(
                conversation_id=_require_non_empty_str(turn_map.get("conversation_id"), "conversation_id"),
                turn_id=_require_non_empty_str(turn_map.get("turn_id"), "turn_id"),
                task_id=_require_non_empty_str(turn_map.get("task_id"), "task_id"),
                support_refs=_require_unique_str_list(turn_map.get("support_refs", []), "support_refs"),
                scratchpad=_require_mapping(turn_map.get("scratchpad", {}), "scratchpad"),
                created_at=_require_non_empty_str(turn_map.get("created_at"), "created_at"),
                updated_at=_require_non_empty_str(turn_map.get("updated_at"), "updated_at"),
            )
        candidates = payload.get("promotable_candidates", [])
        if not isinstance(candidates, list):
            raise WorkingMemoryError("promotable_candidates must be a list")
        self._promotable_candidates = {}
        for candidate_payload in candidates:
            candidate_map = _require_mapping(candidate_payload, "promotable_candidate")
            candidate = WorkingCandidate(
                candidate_id=_require_non_empty_str(candidate_map.get("candidate_id"), "candidate_id"),
                source_turn_ref=_require_non_empty_str(candidate_map.get("source_turn_ref"), "source_turn_ref"),
                candidate_kind=_require_non_empty_str(candidate_map.get("candidate_kind"), "candidate_kind"),
                target_plane=_require_non_empty_str(candidate_map.get("target_plane"), "target_plane"),
                payload=_require_mapping(candidate_map.get("payload", {}), "payload"),
                provenance_refs=_require_unique_str_list(candidate_map.get("provenance_refs", []), "provenance_refs"),
                created_at=_require_non_empty_str(candidate_map.get("created_at"), "created_at"),
                review_ref=candidate_map.get("review_ref"),
                status=_require_non_empty_str(candidate_map.get("status"), "status"),
            )
            self._promotable_candidates[candidate.candidate_id] = candidate
        self._ensure_size()

    def _require_turn_state(self) -> WorkingTurnState:
        if self._turn_state is None:
            raise WorkingMemoryError("no working turn state is bound")
        return self._turn_state

    def _get_candidate(self, candidate_id: str) -> WorkingCandidate:
        normalized = _require_non_empty_str(candidate_id, "candidate_id")
        candidate = self._promotable_candidates.get(normalized)
        if candidate is None:
            raise WorkingMemoryError(f"unknown candidate_id: {normalized}")
        return candidate

    def _ensure_size(self) -> None:
        size_bytes = canonical_size_bytes(self.export_state())
        if size_bytes > self.max_state_bytes:
            raise WorkingMemoryError("working memory exceeds max state bytes")
