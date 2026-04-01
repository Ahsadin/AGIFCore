from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Sequence
from uuid import uuid4

from cell_registry import CellRegistry, CellRegistryError
from event_types import KernelContractError, utc_timestamp


class LifecycleEngineError(KernelContractError):
    """Raised when a lifecycle transition would violate the governed state model."""


class LifecycleEngine:
    """Explicit Phase 2 lifecycle transitions with audit-ready history."""

    def __init__(self, *, registry: CellRegistry) -> None:
        self.registry = registry
        self._history: list[dict[str, Any]] = []

    def bootstrap_cell(
        self,
        *,
        cell_id: str,
        role_family: str,
        workspace_ref: str | None = None,
        lineage_id: str | None = None,
        reason: str,
        actor: str = "kernel",
    ) -> dict[str, Any]:
        record = self.registry.register_cell(
            cell_id=cell_id,
            role_family=role_family,
            lineage_id=lineage_id,
            lifecycle_state="dormant",
            workspace_ref=workspace_ref,
        )
        event = self._record_event(
            action="bootstrap",
            transition="seed_to_dormant",
            cell_id=cell_id,
            from_state="seed",
            to_state="dormant",
            reason=reason,
            actor=actor,
        )
        return {"record": record, "event": event}

    def activate(self, cell_id: str, *, reason: str, actor: str = "kernel") -> dict[str, Any]:
        return self._transition(
            cell_id=cell_id,
            from_states={"dormant"},
            to_state="active",
            action="activate",
            transition="dormant_to_active",
            reason=reason,
            actor=actor,
        )

    def hibernate(self, cell_id: str, *, reason: str, actor: str = "kernel") -> dict[str, Any]:
        return self._transition(
            cell_id=cell_id,
            from_states={"active"},
            to_state="dormant",
            action="hibernate",
            transition="active_to_dormant",
            reason=reason,
            actor=actor,
        )

    def reactivate(self, cell_id: str, *, reason: str, actor: str = "kernel") -> dict[str, Any]:
        return self.activate(cell_id, reason=reason, actor=actor)

    def quarantine(
        self,
        cell_id: str,
        *,
        reason: str,
        actor: str = "kernel",
        quarantine_ref: str | None = None,
        rollback_ref: str | None = None,
    ) -> dict[str, Any]:
        result = self._transition(
            cell_id=cell_id,
            from_states={"active", "dormant"},
            to_state="quarantined",
            action="quarantine",
            transition="active_or_dormant_to_quarantined",
            reason=reason,
            actor=actor,
        )
        self.registry.update_cell(
            cell_id,
            quarantine_ref=quarantine_ref,
            rollback_ref=rollback_ref,
        )
        event = result["event"]
        event["quarantine_ref"] = quarantine_ref
        event["rollback_ref"] = rollback_ref
        return result

    def clear_quarantine(self, cell_id: str, *, reason: str, actor: str = "kernel") -> dict[str, Any]:
        return self._transition(
            cell_id=cell_id,
            from_states={"quarantined"},
            to_state="dormant",
            action="clear_quarantine",
            transition="quarantined_to_dormant",
            reason=reason,
            actor=actor,
        )

    def retire(self, cell_id: str, *, reason: str, actor: str = "kernel") -> dict[str, Any]:
        return self._transition(
            cell_id=cell_id,
            from_states={"dormant", "quarantined"},
            to_state="retired",
            action="retire",
            transition="dormant_or_quarantined_to_retired",
            reason=reason,
            actor=actor,
        )

    def split(
        self,
        *,
        parent_cell_id: str,
        child_specs: Sequence[dict[str, str]],
        reason: str,
        actor: str = "kernel",
    ) -> dict[str, Any]:
        parent = self.registry.get_cell_record(parent_cell_id)
        if parent["lifecycle_state"] != "active":
            raise LifecycleEngineError("split requires the parent cell to be active")
        if len(child_specs) < 2:
            raise LifecycleEngineError("split requires at least two child specs")
        self.registry.update_cell(parent_cell_id, lifecycle_state="split_pending")
        child_ids: list[str] = []
        for item in child_specs:
            child_id = str(item["cell_id"])
            child_role_family = str(item.get("role_family", parent["role_family"]))
            record = self.registry.register_cell(
                cell_id=child_id,
                role_family=child_role_family,
                lineage_id=str(parent["lineage_id"]),
                lifecycle_state="active",
                workspace_ref=parent.get("workspace_ref"),
                metadata={"split_parent_cell_id": parent_cell_id},
            )
            child_ids.append(record["cell_id"])
        self.registry.update_cell(parent_cell_id, lifecycle_state="dormant")
        event = self._record_event(
            action="split",
            transition="active_to_split_pending_to_active_children",
            cell_id=parent_cell_id,
            from_state="active",
            to_state="dormant",
            reason=reason,
            actor=actor,
            related_cell_ids=child_ids,
        )
        return {"parent_cell_id": parent_cell_id, "child_ids": child_ids, "event": event}

    def merge(
        self,
        *,
        survivor_cell_id: str,
        merged_cell_id: str,
        reason: str,
        actor: str = "kernel",
    ) -> dict[str, Any]:
        survivor = self.registry.get_cell_record(survivor_cell_id)
        merged = self.registry.get_cell_record(merged_cell_id)
        if survivor["role_family"] != merged["role_family"]:
            raise LifecycleEngineError("merge requires matching role_family")
        if survivor["lineage_id"] != merged["lineage_id"]:
            raise LifecycleEngineError("merge requires matching lineage_id")
        if merged["lifecycle_state"] == "retired":
            raise LifecycleEngineError("cannot merge an already retired cell")
        self.registry.update_cell(survivor_cell_id, lifecycle_state="consolidating")
        self.registry.update_cell(merged_cell_id, lifecycle_state="retired")
        self.registry.update_cell(survivor_cell_id, lifecycle_state="dormant")
        event = self._record_event(
            action="merge",
            transition="active_or_dormant_to_consolidating_to_dormant",
            cell_id=survivor_cell_id,
            from_state=survivor["lifecycle_state"],
            to_state="dormant",
            reason=reason,
            actor=actor,
            related_cell_ids=[merged_cell_id],
        )
        return {
            "survivor_cell_id": survivor_cell_id,
            "retired_cell_id": merged_cell_id,
            "event": event,
        }

    def history_export(self) -> list[dict[str, Any]]:
        return [deepcopy(entry) for entry in self._history]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_02.lifecycle_engine.v1",
            "history": self.history_export(),
            "summary": self.summary(),
        }

    def load_export(self, payload: dict[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_02.lifecycle_engine.v1":
            raise LifecycleEngineError("lifecycle export schema mismatch")
        history = payload.get("history")
        if not isinstance(history, list):
            raise LifecycleEngineError("lifecycle export history must be a list")
        self._history = [deepcopy(entry) for entry in history]

    def summary(self) -> dict[str, Any]:
        records = self.registry.list_cells()
        counts: dict[str, int] = {}
        for record in records:
            state = str(record["lifecycle_state"])
            counts[state] = counts.get(state, 0) + 1
        return {
            "cell_count": len(records),
            "active_count": counts.get("active", 0),
            "dormant_count": counts.get("dormant", 0),
            "quarantined_count": counts.get("quarantined", 0),
            "retired_count": counts.get("retired", 0),
            "history_count": len(self._history),
            "state_digest": self.state_digest(),
        }

    def state_digest(self) -> str:
        payload = {
            "registry": self.registry.export_state(),
            "history": self._history,
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return encoded.hex()[:32]

    def _transition(
        self,
        *,
        cell_id: str,
        from_states: set[str],
        to_state: str,
        action: str,
        transition: str,
        reason: str,
        actor: str,
    ) -> dict[str, Any]:
        try:
            record = self.registry.get_cell_record(cell_id)
        except CellRegistryError as exc:
            raise LifecycleEngineError(str(exc)) from exc
        current_state = str(record["lifecycle_state"])
        if current_state not in from_states:
            raise LifecycleEngineError(
                f"{action} requires state in {sorted(from_states)}, got {current_state}"
            )
        updated = self.registry.update_cell(cell_id, lifecycle_state=to_state)
        event = self._record_event(
            action=action,
            transition=transition,
            cell_id=cell_id,
            from_state=current_state,
            to_state=to_state,
            reason=reason,
            actor=actor,
        )
        return {"record": updated, "event": event}

    def _record_event(
        self,
        *,
        action: str,
        transition: str,
        cell_id: str,
        from_state: str,
        to_state: str,
        reason: str,
        actor: str,
        related_cell_ids: Sequence[str] | None = None,
    ) -> dict[str, Any]:
        event = {
            "event_id": f"lifecycle-{uuid4().hex}",
            "action": action,
            "transition": transition,
            "cell_id": cell_id,
            "related_cell_ids": list(related_cell_ids or []),
            "from_state": from_state,
            "to_state": to_state,
            "reason": reason,
            "actor": actor,
            "occurred_at": utc_timestamp(),
            "rollback_ref": None,
            "quarantine_ref": None,
        }
        self._history.append(event)
        return event
