from __future__ import annotations

import sys
from copy import deepcopy
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
KERNEL_ROOT = PROJECT_ROOT / "04_execution" / "phase_02_fabric_kernel_and_workspace" / "agifcore_phase2_kernel"
EVIDENCE_ROOT = PROJECT_ROOT / "06_outputs" / "phase_02_fabric_kernel_and_workspace" / "phase_02_evidence"

if str(KERNEL_ROOT) not in sys.path:
    sys.path.insert(0, str(KERNEL_ROOT))

from cell_registry import CellRegistry
from event_bus import EventBus
from event_types import (
    AbstainOrAnswer,
    DiscourseMode,
    FinalAnswerMode,
    KnowledgeGapReason,
    KernelEventType,
    KernelResponseSurface,
    KernelTraceRefs,
    KernelTurnContext,
    NextAction,
    SupportState,
    new_kernel_event,
)
from lifecycle_engine import LifecycleEngine
from quarantine_controller import QuarantineController
from rollback_controller import RollbackController
from workspace_state import SharedWorkspaceState

REPORT_PATH = EVIDENCE_ROOT / "phase_02_rollback_quarantine_report.json"
MANIFEST_PATH = EVIDENCE_ROOT / "phase_02_evidence_manifest.json"

RUNTIME_FILES = [
    KERNEL_ROOT / "workspace_state.py",
    KERNEL_ROOT / "cell_registry.py",
    KERNEL_ROOT / "lifecycle_engine.py",
    KERNEL_ROOT / "scheduler.py",
    KERNEL_ROOT / "replay_ledger.py",
    KERNEL_ROOT / "rollback_controller.py",
    KERNEL_ROOT / "quarantine_controller.py",
]

BASELINE_FILES = [
    KERNEL_ROOT / "event_types.py",
    KERNEL_ROOT / "event_bus.py",
    PROJECT_ROOT / "01_plan" / "PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md",
    PROJECT_ROOT / "01_plan" / "TRACE_CONTRACT.md",
    PROJECT_ROOT / "03_design" / "GOVERNANCE_MODEL.md",
    PROJECT_ROOT / "03_design" / "WORKSPACE_MODEL.md",
]


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def build_pass_report() -> dict[str, object]:
    workspace = SharedWorkspaceState()
    registry = CellRegistry()
    lifecycle = LifecycleEngine(registry=registry)
    rollback = RollbackController()
    quarantine = QuarantineController()

    cell_id = "cell-recovery-001"
    workspace_ref = workspace.register_cell_anchor(
        cell_id=cell_id,
        role_family="recovery_verifier",
        lifecycle_state="active",
    )
    lifecycle.bootstrap_cell(
        cell_id=cell_id,
        role_family="recovery_verifier",
        workspace_ref=workspace_ref,
        reason="seed recovery verifier cell",
    )
    lifecycle.activate(cell_id, reason="activate recovery verifier cell")
    registry.update_cell(cell_id, workspace_ref=workspace_ref, lifecycle_state="active")
    workspace.update_cell_anchor(
        cell_id,
        lifecycle_state="active",
        workspace_ref=workspace_ref,
    )

    known_good_snapshot_payload = {
        "workspace": workspace.state_export(),
        "registry": registry.export_state(),
        "lifecycle": lifecycle.export_state(),
    }
    snapshot = rollback.create_snapshot(
        state_export=deepcopy(known_good_snapshot_payload),
        label="known-good-before-quarantine",
    )
    workspace.attach_rollback_ref(snapshot["rollback_ref"])
    workspace.attach_evidence_ref("evidence://phase2/recovery")

    quarantine_record = quarantine.quarantine_cell(
        cell_id=cell_id,
        reason_code="POLICY_BLOCKED",
        reason_text="quarantine before restore",
        rollback_ref=snapshot["rollback_ref"],
    )
    lifecycle.quarantine(
        cell_id,
        reason="quarantine before restore",
        quarantine_ref=quarantine_record.quarantine_ref,
        rollback_ref=snapshot["rollback_ref"],
    )
    registry.set_quarantine(
        cell_id,
        quarantine_ref=quarantine_record.quarantine_ref,
        reason_code=quarantine_record.reason_code,
    )
    workspace.attach_quarantine_ref(quarantine_record.quarantine_ref)
    workspace.update_cell_anchor(
        cell_id,
        lifecycle_state="quarantined",
        quarantine_ref=quarantine_record.quarantine_ref,
        rollback_ref=snapshot["rollback_ref"],
    )

    quarantined_state = {
        "workspace": workspace.state_export(),
        "registry": registry.export_state(),
        "lifecycle": lifecycle.export_state(),
    }
    restored_snapshot = rollback.restore_snapshot(rollback_ref=snapshot["rollback_ref"])
    restored_state = deepcopy(restored_snapshot["state_export"])
    workspace.load_export(restored_state["workspace"])
    registry.load_export(restored_state["registry"])
    lifecycle.load_export(restored_state["lifecycle"])

    restored_cell = registry.get_cell_record(cell_id)
    release_record = quarantine.release_quarantine(
        quarantine_ref=quarantine_record.quarantine_ref,
        release_reason="known-good snapshot restored",
    )

    if restored_cell["lifecycle_state"] != "active":
        raise AssertionError("restored cell did not return to active state")
    if quarantine.active_for_cell(cell_id) is not None:
        raise AssertionError("quarantine release path did not clear the active record")
    if release_record.status != "released":
        raise AssertionError("quarantine release did not mark the record as released")
    if workspace.state_export() != known_good_snapshot_payload["workspace"]:
        raise AssertionError("workspace restore did not round-trip the known-good snapshot")
    if registry.export_state() != known_good_snapshot_payload["registry"]:
        raise AssertionError("registry restore did not round-trip the known-good snapshot")
    if lifecycle.export_state() != known_good_snapshot_payload["lifecycle"]:
        raise AssertionError("lifecycle restore did not round-trip the known-good snapshot")
    if registry.export_state()["counts"]["quarantined"] != 0:
        raise AssertionError("registry retained quarantined state after restore")

    return {
        "phase": "2",
        "slice": "4",
        "verifier": "verify_phase_02_rollback_quarantine",
        "status": "pass",
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "rollback-snapshot-created", "result": "pass"},
            {"id": "quarantine-cell-created", "result": "pass"},
            {"id": "known-good-restore-roundtrip", "result": "pass"},
            {"id": "quarantine-release-path-cleared", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "runtime_symbols": {
            "workspace_state": [
                "state_export",
                "load_export",
                "attach_rollback_ref",
                "attach_quarantine_ref",
            ],
            "cell_registry": [
                "register_cell",
                "update_cell",
                "set_quarantine",
                "export_state",
            ],
            "lifecycle_engine": [
                "bootstrap_cell",
                "activate",
                "quarantine",
                "export_state",
            ],
            "rollback_controller": [
                "create_snapshot",
                "restore_snapshot",
                "snapshot_export",
            ],
            "quarantine_controller": [
                "quarantine_cell",
                "release_quarantine",
                "active_for_cell",
            ],
        },
        "snapshot": {
            "rollback_ref": snapshot["rollback_ref"],
            "state_hash": snapshot["state_hash"],
            "release_reason": release_record.release_reason,
            "quarantine_ref": quarantine_record.quarantine_ref,
            "quarantined_state_counts": quarantined_state["registry"]["counts"],
            "restored_state_counts": registry.export_state()["counts"],
        },
        "notes": [
            "recovery must stay bounded and explicit",
            "no approval implied",
        ],
    }


def build_blocked_report(missing: list[str]) -> dict[str, object]:
    return {
        "phase": "2",
        "slice": "4",
        "verifier": "verify_phase_02_rollback_quarantine",
        "status": "blocked",
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 2 slice 4 recovery-control runtime files are not on disk yet.",
            "missing_files": missing,
        },
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "rollback-runtime-present", "result": "blocked"},
            {"id": "quarantine-runtime-present", "result": "blocked"},
            {"id": "recovery-path-bounded", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "rollback and quarantine are part of slice 4",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(BASELINE_FILES + RUNTIME_FILES)
    if missing:
        report = build_blocked_report(missing)
        write_json(REPORT_PATH, report)
        print("phase_02 slice_4 rollback/quarantine verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    write_json(REPORT_PATH, report)
    print("phase_02 slice_4 rollback/quarantine verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
