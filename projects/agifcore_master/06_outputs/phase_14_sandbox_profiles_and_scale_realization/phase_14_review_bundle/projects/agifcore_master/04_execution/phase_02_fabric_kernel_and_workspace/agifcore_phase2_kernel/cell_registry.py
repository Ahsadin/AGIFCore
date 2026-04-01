from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping
from uuid import uuid4

from event_types import KernelContractError, utc_timestamp

ALLOWED_LIFECYCLE_STATES = {
    "seed",
    "dormant",
    "active",
    "split_pending",
    "consolidating",
    "quarantined",
    "retired",
}


class CellRegistryError(KernelContractError):
    """Raised when the cell registry violates the Phase 2 runtime boundary."""


class CellRegistry:
    """Bounded logical cell registry for the Phase 2 kernel."""

    def __init__(self) -> None:
        self._records: dict[str, dict[str, Any]] = {}

    def register_cell(
        self,
        *,
        cell_id: str,
        role_family: str,
        lineage_id: str | None = None,
        lifecycle_state: str = "dormant",
        workspace_ref: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._validate_state(lifecycle_state)
        if cell_id in self._records:
            raise CellRegistryError(f"cell already registered: {cell_id}")
        if not role_family:
            raise CellRegistryError("role_family must be non-empty")
        record = {
            "cell_id": cell_id,
            "role_family": role_family,
            "lineage_id": lineage_id or f"lineage-{uuid4().hex[:12]}",
            "lifecycle_state": lifecycle_state,
            "workspace_ref": workspace_ref,
            "quarantine_ref": None,
            "rollback_ref": None,
            "metadata": dict(metadata or {}),
            "registered_at": utc_timestamp(),
            "updated_at": utc_timestamp(),
        }
        self._records[cell_id] = record
        return deepcopy(record)

    def update_cell(
        self,
        cell_id: str,
        *,
        lifecycle_state: str | None = None,
        workspace_ref: str | None = None,
        quarantine_ref: str | None = None,
        rollback_ref: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        record = self._require_record(cell_id)
        if lifecycle_state is not None:
            self._validate_state(lifecycle_state)
            record["lifecycle_state"] = lifecycle_state
        if workspace_ref is not None:
            record["workspace_ref"] = workspace_ref
        if quarantine_ref is not None:
            record["quarantine_ref"] = quarantine_ref
        if rollback_ref is not None:
            record["rollback_ref"] = rollback_ref
        if metadata:
            record["metadata"].update(dict(metadata))
        record["updated_at"] = utc_timestamp()
        return deepcopy(record)

    def set_quarantine(self, cell_id: str, *, quarantine_ref: str, reason_code: str) -> dict[str, Any]:
        return self.update_cell(
            cell_id,
            lifecycle_state="quarantined",
            quarantine_ref=quarantine_ref,
            metadata={"quarantine_reason_code": reason_code},
        )

    def get_cell_record(self, cell_id: str) -> dict[str, Any]:
        return deepcopy(self._require_record(cell_id))

    def list_cells(self) -> list[dict[str, Any]]:
        return [deepcopy(record) for record in self._records.values()]

    def active_cells(self) -> list[dict[str, Any]]:
        return [
            deepcopy(record)
            for record in self._records.values()
            if record["lifecycle_state"] == "active"
        ]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_02.cell_registry.v1",
            "records": self.list_cells(),
            "counts": {
                "total": len(self._records),
                "active": len(self.active_cells()),
                "quarantined": sum(
                    1
                    for record in self._records.values()
                    if record["lifecycle_state"] == "quarantined"
                ),
            },
        }

    def load_export(self, payload: dict[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_02.cell_registry.v1":
            raise CellRegistryError("cell registry export schema mismatch")
        records = payload.get("records")
        if not isinstance(records, list):
            raise CellRegistryError("cell registry export must contain a records list")
        self._records = {}
        for item in records:
            cell_id = str(item["cell_id"])
            lifecycle_state = str(item["lifecycle_state"])
            self._validate_state(lifecycle_state)
            self._records[cell_id] = deepcopy(item)

    def _require_record(self, cell_id: str) -> dict[str, Any]:
        record = self._records.get(cell_id)
        if record is None:
            raise CellRegistryError(f"unknown cell_id: {cell_id}")
        return record

    @staticmethod
    def _validate_state(lifecycle_state: str) -> None:
        if lifecycle_state not in ALLOWED_LIFECYCLE_STATES:
            raise CellRegistryError(f"unsupported lifecycle state: {lifecycle_state}")
