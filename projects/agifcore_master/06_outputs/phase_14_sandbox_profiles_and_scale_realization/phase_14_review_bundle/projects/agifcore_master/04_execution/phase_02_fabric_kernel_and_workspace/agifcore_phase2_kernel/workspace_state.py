from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from event_types import KernelContractError, KernelEvent, utc_timestamp

MAX_WORKSPACE_STATE_BYTES = 256 * 1024 * 1024
ALLOWED_OPERATOR_COMMANDS = (
    "inspect_state",
    "plan_governed_action",
    "verify_or_replay",
    "rollback_or_quarantine",
    "export_evidence",
)


class WorkspaceStateError(KernelContractError):
    """Raised when shared workspace state violates the governed Phase 2 boundary."""


def _canonical_size_bytes(payload: dict[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class SharedWorkspaceState:
    """Bounded shared workspace state with explicit replay and review anchors only."""

    def __init__(
        self,
        *,
        workspace_id: str = "phase-02-workspace",
        max_state_bytes: int = MAX_WORKSPACE_STATE_BYTES,
    ) -> None:
        self.workspace_id = workspace_id
        self.max_state_bytes = max_state_bytes
        self._turn_records: dict[str, dict[str, Any]] = {}
        self._cell_anchors: dict[str, dict[str, Any]] = {}
        self._replay_refs: list[str] = []
        self._rollback_refs: list[str] = []
        self._quarantine_refs: list[str] = []
        self._evidence_refs: list[str] = []
        self._memory_review_refs: list[dict[str, str | None]] = []
        self._operator_log: list[dict[str, str]] = []
        self._created_at = utc_timestamp()

    def bind_event(self, event: KernelEvent) -> str:
        event.validate()
        turn_key = self._turn_key(event.turn.conversation_id, event.turn.turn_id)
        turn_ref = self.turn_ref(event.turn.conversation_id, event.turn.turn_id)
        record = {
            "turn_ref": turn_ref,
            "conversation_id": event.turn.conversation_id,
            "turn_id": event.turn.turn_id,
            "user_intent": event.turn.user_intent,
            "active_context_refs": list(event.turn.active_context_refs),
            "discourse_mode": event.turn.discourse_mode.value,
            "support_state": event.turn.support_state.value,
            "knowledge_gap_reason": event.turn.knowledge_gap_reason.value,
            "next_action": event.turn.next_action.value,
            "planner_trace_ref": event.trace_refs.planner_trace_ref,
            "simulation_trace_ref": event.trace_refs.simulation_trace_ref,
            "critic_trace_ref": event.trace_refs.critic_trace_ref,
            "governance_trace_ref": event.trace_refs.governance_trace_ref,
            "last_event_type": event.event_type.value,
            "response_text": event.response.response_text if event.response else "",
            "abstain_or_answer": (
                event.response.abstain_or_answer.value if event.response else None
            ),
            "final_answer_mode": (
                event.response.final_answer_mode.value if event.response else None
            ),
            "memory_review_ref": (
                event.response.memory_review_ref if event.response else None
            ),
            "workspace_updated_at": utc_timestamp(),
        }
        self._turn_records[turn_key] = record
        self._operator_log.append(
            {
                "command_class": "inspect_state",
                "turn_ref": turn_ref,
                "occurred_at": utc_timestamp(),
            }
        )
        if event.response and event.response.memory_review_ref:
            self.attach_memory_review_ref(
                event.response.memory_review_ref,
                conversation_id=event.turn.conversation_id,
                turn_id=event.turn.turn_id,
            )
        self._ensure_size()
        return turn_ref

    def register_cell_anchor(
        self,
        *,
        cell_id: str,
        role_family: str,
        lifecycle_state: str = "dormant",
        workspace_ref: str | None = None,
    ) -> str:
        if not cell_id:
            raise WorkspaceStateError("cell_id must be non-empty")
        if not role_family:
            raise WorkspaceStateError("role_family must be non-empty")
        anchor_ref = self.cell_ref(cell_id)
        self._cell_anchors[cell_id] = {
            "cell_ref": anchor_ref,
            "cell_id": cell_id,
            "role_family": role_family,
            "lifecycle_state": lifecycle_state,
            "workspace_ref": workspace_ref or anchor_ref,
            "quarantine_ref": None,
            "rollback_ref": None,
            "updated_at": utc_timestamp(),
        }
        self._ensure_size()
        return anchor_ref

    def update_cell_anchor(
        self,
        cell_id: str,
        *,
        lifecycle_state: str | None = None,
        workspace_ref: str | None = None,
        quarantine_ref: str | None = None,
        rollback_ref: str | None = None,
    ) -> None:
        anchor = self._cell_anchors.get(cell_id)
        if anchor is None:
            raise WorkspaceStateError(f"unknown cell anchor: {cell_id}")
        if lifecycle_state is not None:
            anchor["lifecycle_state"] = lifecycle_state
        if workspace_ref is not None:
            anchor["workspace_ref"] = workspace_ref
        if quarantine_ref is not None:
            anchor["quarantine_ref"] = quarantine_ref
        if rollback_ref is not None:
            anchor["rollback_ref"] = rollback_ref
        anchor["updated_at"] = utc_timestamp()
        self._ensure_size()

    def attach_replay_ref(self, replay_ref: str) -> None:
        self._attach_unique_ref(self._replay_refs, replay_ref)

    def attach_rollback_ref(self, rollback_ref: str) -> None:
        self._attach_unique_ref(self._rollback_refs, rollback_ref)

    def attach_quarantine_ref(self, quarantine_ref: str) -> None:
        self._attach_unique_ref(self._quarantine_refs, quarantine_ref)

    def attach_evidence_ref(self, evidence_ref: str) -> None:
        self._attach_unique_ref(self._evidence_refs, evidence_ref)

    def attach_memory_review_ref(
        self,
        memory_review_ref: str,
        *,
        conversation_id: str | None = None,
        turn_id: str | None = None,
    ) -> None:
        if not memory_review_ref:
            raise WorkspaceStateError("memory_review_ref must be non-empty")
        candidate = {
            "memory_review_ref": memory_review_ref,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
        }
        if candidate not in self._memory_review_refs:
            self._memory_review_refs.append(candidate)
        self._ensure_size()

    def state_export(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_02.state_export.v1",
            "workspace_id": self.workspace_id,
            "created_at": self._created_at,
            "operator_commands": list(ALLOWED_OPERATOR_COMMANDS),
            "turns": [deepcopy(item) for item in self._turn_records.values()],
            "cells": [deepcopy(item) for item in self._cell_anchors.values()],
            "replay_refs": list(self._replay_refs),
            "rollback_refs": list(self._rollback_refs),
            "quarantine_refs": list(self._quarantine_refs),
            "evidence_refs": list(self._evidence_refs),
            "memory_hook_surface": self.memory_review_export(),
            "operator_log": list(self._operator_log),
        }

    def memory_review_export(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_02.memory_review_export.v1",
            "workspace_id": self.workspace_id,
            "memory_review_refs": [deepcopy(item) for item in self._memory_review_refs],
            "retention_candidate_refs": [],
            "notes": [
                "references only",
                "no semantic memory",
                "no procedural memory",
                "no graph persistence",
            ],
        }

    def load_export(self, payload: dict[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_02.state_export.v1":
            raise WorkspaceStateError("workspace export schema mismatch")
        turns = payload.get("turns")
        cells = payload.get("cells")
        if not isinstance(turns, list) or not isinstance(cells, list):
            raise WorkspaceStateError("workspace export turns and cells must be lists")
        self.workspace_id = str(payload.get("workspace_id", self.workspace_id))
        self._created_at = str(payload.get("created_at", self._created_at))
        self._turn_records = {
            self._turn_key(str(item["conversation_id"]), str(item["turn_id"])): deepcopy(item)
            for item in turns
        }
        self._cell_anchors = {str(item["cell_id"]): deepcopy(item) for item in cells}
        self._replay_refs = [str(item) for item in payload.get("replay_refs", [])]
        self._rollback_refs = [str(item) for item in payload.get("rollback_refs", [])]
        self._quarantine_refs = [str(item) for item in payload.get("quarantine_refs", [])]
        self._evidence_refs = [str(item) for item in payload.get("evidence_refs", [])]
        memory_surface = payload.get("memory_hook_surface", {})
        refs = memory_surface.get("memory_review_refs", [])
        self._memory_review_refs = [deepcopy(item) for item in refs]
        self._operator_log = [deepcopy(item) for item in payload.get("operator_log", [])]
        self._ensure_size()

    def turn_ref(self, conversation_id: str, turn_id: str) -> str:
        return f"workspace://{self.workspace_id}/turn/{conversation_id}/{turn_id}"

    def cell_ref(self, cell_id: str) -> str:
        return f"workspace://{self.workspace_id}/cell/{cell_id}"

    def estimated_size_bytes(self) -> int:
        return _canonical_size_bytes(self.state_export())

    def _attach_unique_ref(self, target: list[str], ref: str) -> None:
        if not ref:
            raise WorkspaceStateError("workspace reference must be non-empty")
        if ref not in target:
            target.append(ref)
        self._ensure_size()

    def _ensure_size(self) -> None:
        if self.estimated_size_bytes() > self.max_state_bytes:
            raise WorkspaceStateError(
                f"workspace state exceeds max size of {self.max_state_bytes} bytes"
            )

    @staticmethod
    def _turn_key(conversation_id: str, turn_id: str) -> str:
        return f"{conversation_id}:{turn_id}"
