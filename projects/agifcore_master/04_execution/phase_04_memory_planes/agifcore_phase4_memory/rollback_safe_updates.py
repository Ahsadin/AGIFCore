from __future__ import annotations

import json
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from rollback_safe_updates path")


def _ensure_phase2_imports() -> None:
    repo_root = _find_repo_root()
    kernel_dir = (
        repo_root
        / "projects"
        / "agifcore_master"
        / "04_execution"
        / "phase_02_fabric_kernel_and_workspace"
        / "agifcore_phase2_kernel"
    )
    kernel_path = str(kernel_dir)
    if kernel_path not in sys.path:
        sys.path.insert(0, kernel_path)


_ensure_phase2_imports()

from replay_ledger import ReplayLedger, ReplayLedgerError  # noqa: E402
from rollback_controller import RollbackController, RollbackControllerError  # noqa: E402


class RollbackSafeUpdateError(ValueError):
    """Raised when a Phase 4 memory update cannot remain replayable and reversible."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RollbackSafeUpdateError(f"{field_name} must be a non-empty string")
    return value


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise RollbackSafeUpdateError(f"{field_name} must be a mapping")
    return dict(value)


@dataclass(frozen=True, slots=True)
class UpdateBatchResult:
    label: str
    status: str
    rollback_ref: str
    replay_id: str | None
    state_hash: str
    updated_state: dict[str, Any]
    reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "status": self.status,
            "rollback_ref": self.rollback_ref,
            "replay_id": self.replay_id,
            "state_hash": self.state_hash,
            "updated_state": deepcopy(self.updated_state),
            "reason": self.reason,
        }


class RollbackSafeUpdater:
    """Batch memory updates through Phase 2 rollback snapshots and replay anchors."""

    def __init__(
        self,
        *,
        rollback_controller: RollbackController | None = None,
        replay_ledger: ReplayLedger | None = None,
    ) -> None:
        self.rollback_controller = rollback_controller or RollbackController()
        self.replay_ledger = replay_ledger or ReplayLedger()
        self._batch_counter = 0
        self._rollback_context: dict[str, dict[str, Any]] = {}
        self._decision_log: list[dict[str, Any]] = []

    def apply_batch(
        self,
        *,
        label: str,
        conversation_id: str,
        turn_id: str,
        event_ids: list[str],
        plane_exports: Mapping[str, Any],
        mutator: Callable[[dict[str, Any]], dict[str, Any] | None],
    ) -> UpdateBatchResult:
        normalized_label = _require_non_empty_str(label, "label")
        state_export = self._normalize_plane_exports(plane_exports)
        try:
            snapshot = self.rollback_controller.create_snapshot(
                state_export=state_export,
                label=normalized_label,
            )
        except RollbackControllerError as exc:
            raise RollbackSafeUpdateError(str(exc)) from exc

        rollback_ref = snapshot["rollback_ref"]
        self._rollback_context[rollback_ref] = {
            "label": normalized_label,
            "conversation_id": _require_non_empty_str(conversation_id, "conversation_id"),
            "turn_id": _require_non_empty_str(turn_id, "turn_id"),
            "event_ids": [_require_non_empty_str(item, "event_id") for item in event_ids],
        }
        candidate_state = deepcopy(state_export)
        try:
            mutated = mutator(candidate_state)
            if mutated is not None:
                candidate_state = self._normalize_plane_exports(mutated)
            replay_id = self._record_replay(
                rollback_ref=rollback_ref,
                conversation_id=conversation_id,
                turn_id=turn_id,
                event_ids=event_ids,
                label=normalized_label,
                action="apply",
                state_export=candidate_state,
            )
            result = UpdateBatchResult(
                label=normalized_label,
                status="applied",
                rollback_ref=rollback_ref,
                replay_id=replay_id,
                state_hash=snapshot["state_hash"],
                updated_state=candidate_state,
            )
            self._decision_log.append(result.to_dict())
            return result
        except Exception as exc:  # noqa: BLE001 - rejection is part of the runtime surface.
            restored = self._restore_export(rollback_ref)
            result = UpdateBatchResult(
                label=normalized_label,
                status="rejected",
                rollback_ref=rollback_ref,
                replay_id=None,
                state_hash=snapshot["state_hash"],
                updated_state=restored,
                reason=str(exc),
            )
            self._decision_log.append(result.to_dict())
            return result

    def reject_batch(self, *, rollback_ref: str, reason: str) -> UpdateBatchResult:
        context = self._get_context(rollback_ref)
        restored = self._restore_export(rollback_ref)
        replay_id = self._record_replay(
            rollback_ref=rollback_ref,
            conversation_id=context["conversation_id"],
            turn_id=context["turn_id"],
            event_ids=context["event_ids"],
            label=context["label"],
            action="reject",
            state_export=restored,
        )
        state_hash = self._snapshot_hash(rollback_ref)
        result = UpdateBatchResult(
            label=context["label"],
            status="rejected",
            rollback_ref=rollback_ref,
            replay_id=replay_id,
            state_hash=state_hash,
            updated_state=restored,
            reason=_require_non_empty_str(reason, "reason"),
        )
        self._decision_log.append(result.to_dict())
        return result

    def restore_batch(self, *, rollback_ref: str) -> UpdateBatchResult:
        context = self._get_context(rollback_ref)
        restored = self._restore_export(rollback_ref)
        replay_id = self._record_replay(
            rollback_ref=rollback_ref,
            conversation_id=context["conversation_id"],
            turn_id=context["turn_id"],
            event_ids=context["event_ids"],
            label=context["label"],
            action="restore",
            state_export=restored,
        )
        state_hash = self._snapshot_hash(rollback_ref)
        result = UpdateBatchResult(
            label=context["label"],
            status="restored",
            rollback_ref=rollback_ref,
            replay_id=replay_id,
            state_hash=state_hash,
            updated_state=restored,
        )
        self._decision_log.append(result.to_dict())
        return result

    def rollback_snapshot_export(self) -> dict[str, Any]:
        return self.rollback_controller.snapshot_export()

    def replay_export(self) -> dict[str, Any]:
        return self.replay_ledger.replay_export()

    def decision_log(self) -> list[dict[str, Any]]:
        return deepcopy(self._decision_log)

    def _normalize_plane_exports(self, plane_exports: Mapping[str, Any]) -> dict[str, Any]:
        normalized = _require_mapping(plane_exports, "plane_exports")
        if not normalized:
            raise RollbackSafeUpdateError("plane_exports must not be empty")
        for plane_name, payload in normalized.items():
            _require_non_empty_str(plane_name, "plane_name")
            _require_mapping(payload, f"{plane_name}_state")
        try:
            json.dumps(normalized, sort_keys=True)
        except TypeError as exc:
            raise RollbackSafeUpdateError("plane_exports must be JSON serializable") from exc
        return deepcopy(normalized)

    def _record_replay(
        self,
        *,
        rollback_ref: str,
        conversation_id: str,
        turn_id: str,
        event_ids: list[str],
        label: str,
        action: str,
        state_export: Mapping[str, Any],
    ) -> str:
        self._batch_counter += 1
        replay_id = f"phase4-memory-update-{self._batch_counter:08d}"
        try:
            self.replay_ledger.record_replay(
                replay_id=replay_id,
                conversation_id=_require_non_empty_str(conversation_id, "conversation_id"),
                turn_id=_require_non_empty_str(turn_id, "turn_id"),
                trace_export=[
                    {
                        "label": _require_non_empty_str(label, "label"),
                        "action": _require_non_empty_str(action, "action"),
                        "rollback_ref": _require_non_empty_str(rollback_ref, "rollback_ref"),
                        "planes": sorted(state_export.keys()),
                    }
                ],
                state_export=dict(state_export),
                event_ids=[_require_non_empty_str(item, "event_id") for item in event_ids],
            )
        except ReplayLedgerError as exc:
            raise RollbackSafeUpdateError(str(exc)) from exc
        return replay_id

    def _restore_export(self, rollback_ref: str) -> dict[str, Any]:
        try:
            restored = self.rollback_controller.restore_snapshot(
                rollback_ref=_require_non_empty_str(rollback_ref, "rollback_ref")
            )
        except RollbackControllerError as exc:
            raise RollbackSafeUpdateError(str(exc)) from exc
        return _require_mapping(restored.get("state_export"), "state_export")

    def _snapshot_hash(self, rollback_ref: str) -> str:
        snapshot_export = self.rollback_controller.snapshot_export()
        for snapshot in snapshot_export.get("snapshots", []):
            if snapshot.get("rollback_ref") == rollback_ref:
                return _require_non_empty_str(snapshot.get("state_hash"), "state_hash")
        raise RollbackSafeUpdateError(f"unknown rollback_ref: {rollback_ref}")

    def _get_context(self, rollback_ref: str) -> dict[str, Any]:
        normalized = _require_non_empty_str(rollback_ref, "rollback_ref")
        context = self._rollback_context.get(normalized)
        if context is None:
            raise RollbackSafeUpdateError(f"rollback context not found: {normalized}")
        return deepcopy(context)
