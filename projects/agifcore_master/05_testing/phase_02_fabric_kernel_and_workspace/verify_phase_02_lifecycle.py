from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
KERNEL_ROOT = PROJECT_ROOT / "04_execution" / "phase_02_fabric_kernel_and_workspace" / "agifcore_phase2_kernel"
EVIDENCE_ROOT = PROJECT_ROOT / "06_outputs" / "phase_02_fabric_kernel_and_workspace" / "phase_02_evidence"

REPORT_PATH = EVIDENCE_ROOT / "phase_02_lifecycle_report.json"
MANIFEST_PATH = EVIDENCE_ROOT / "phase_02_evidence_manifest.json"

RUNTIME_FILES = [
    KERNEL_ROOT / "workspace_state.py",
    KERNEL_ROOT / "cell_registry.py",
    KERNEL_ROOT / "lifecycle_engine.py",
]

BASELINE_FILES = [
    KERNEL_ROOT / "event_types.py",
    KERNEL_ROOT / "event_bus.py",
    PROJECT_ROOT / "01_plan" / "PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md",
    PROJECT_ROOT / "03_design" / "WORKSPACE_MODEL.md",
    PROJECT_ROOT / "03_design" / "GOVERNANCE_MODEL.md",
]

sys.path.insert(0, str(KERNEL_ROOT))

from cell_registry import CellRegistry  # noqa: E402
from lifecycle_engine import LifecycleEngine  # noqa: E402
from workspace_state import SharedWorkspaceState  # noqa: E402


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def build_blocked_report(missing: list[str]) -> dict[str, object]:
    return {
        "phase": "2",
        "slice": "3",
        "verifier": "verify_phase_02_lifecycle",
        "status": "blocked",
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 2 slice 3 runtime files are not on disk yet.",
            "missing_files": missing,
        },
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "lifecycle-runtime-present", "result": "blocked"},
            {"id": "lifecycle-history-backed", "result": "blocked"},
            {"id": "lifecycle-scheduler-boundary-ready", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "lifecycle is a later slice-3 target",
            "scheduler follows lifecycle in this slice",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, object]:
    workspace = SharedWorkspaceState(workspace_id="phase-02-lifecycle-workspace")
    registry = CellRegistry()
    lifecycle = LifecycleEngine(registry=registry)

    bootstrap = lifecycle.bootstrap_cell(
        cell_id="cell-lifecycle-parent",
        role_family="kernel",
        workspace_ref=workspace.cell_ref("cell-lifecycle-parent"),
        reason="bootstrap lifecycle test cell",
    )
    if registry.get_cell_record("cell-lifecycle-parent")["lifecycle_state"] != "dormant":
        raise AssertionError("bootstrap did not seed a dormant record")

    activated = lifecycle.activate("cell-lifecycle-parent", reason="activate lifecycle test cell")
    if activated["record"]["lifecycle_state"] != "active":
        raise AssertionError("activate did not move the cell to active")

    hibernated = lifecycle.hibernate("cell-lifecycle-parent", reason="hibernate lifecycle test cell")
    if hibernated["record"]["lifecycle_state"] != "dormant":
        raise AssertionError("hibernate did not move the cell to dormant")

    reactivated = lifecycle.reactivate(
        "cell-lifecycle-parent",
        reason="reactivate lifecycle test cell",
    )
    if reactivated["record"]["lifecycle_state"] != "active":
        raise AssertionError("reactivate did not return the cell to active")

    split_seed = lifecycle.bootstrap_cell(
        cell_id="cell-split-parent",
        role_family="kernel",
        workspace_ref=workspace.cell_ref("cell-split-parent"),
        reason="seed split lifecycle test cell",
    )
    lifecycle.activate("cell-split-parent", reason="activate split lifecycle test cell")
    split = lifecycle.split(
        parent_cell_id="cell-split-parent",
        child_specs=[
            {"cell_id": "cell-child-a", "role_family": "kernel"},
            {"cell_id": "cell-child-b", "role_family": "kernel"},
        ],
        reason="split lifecycle test cell",
    )
    if sorted(split["child_ids"]) != ["cell-child-a", "cell-child-b"]:
        raise AssertionError("split did not produce the expected child cells")
    if registry.get_cell_record("cell-child-a")["lifecycle_state"] != "active":
        raise AssertionError("split child A was not activated")
    if registry.get_cell_record("cell-child-b")["lifecycle_state"] != "active":
        raise AssertionError("split child B was not activated")
    if registry.get_cell_record("cell-split-parent")["lifecycle_state"] != "dormant":
        raise AssertionError("split parent did not settle back to dormant")

    merge = lifecycle.merge(
        survivor_cell_id="cell-child-a",
        merged_cell_id="cell-child-b",
        reason="merge lifecycle test cells",
    )
    if registry.get_cell_record("cell-child-a")["lifecycle_state"] != "dormant":
        raise AssertionError("merge survivor did not settle back to dormant")
    if registry.get_cell_record("cell-child-b")["lifecycle_state"] != "retired":
        raise AssertionError("merge target was not retired")

    quarantined = lifecycle.quarantine(
        "cell-lifecycle-parent",
        reason="quarantine lifecycle test cell",
        quarantine_ref="quarantine://phase2/lifecycle/0001",
        rollback_ref="rollback://phase2/lifecycle/0001",
    )
    if quarantined["record"]["lifecycle_state"] != "quarantined":
        raise AssertionError("quarantine did not move the cell to quarantined")
    if registry.get_cell_record("cell-lifecycle-parent")["quarantine_ref"] != "quarantine://phase2/lifecycle/0001":
        raise AssertionError("quarantine ref was not recorded")

    cleared = lifecycle.clear_quarantine(
        "cell-lifecycle-parent",
        reason="clear quarantine lifecycle test cell",
    )
    if cleared["record"]["lifecycle_state"] != "dormant":
        raise AssertionError("clear_quarantine did not move the cell back to dormant")

    retired = lifecycle.retire("cell-lifecycle-parent", reason="retire lifecycle test cell")
    if retired["record"]["lifecycle_state"] != "retired":
        raise AssertionError("retire did not move the cell to retired")

    history = lifecycle.history_export()
    summary = lifecycle.summary()
    export_state = lifecycle.export_state()
    lifecycle_clone = LifecycleEngine(registry=registry)
    lifecycle_clone.load_export(export_state)

    if len(history) < 8:
        raise AssertionError("lifecycle history did not capture all transitions")
    if summary["history_count"] != len(history):
        raise AssertionError("summary history count mismatch")
    if summary["active_count"] != 0:
        raise AssertionError("summary active count should be zero after retirements")
    if summary["retired_count"] < 2:
        raise AssertionError("summary retired count should include retired cells")
    if export_state["summary"]["state_digest"] != lifecycle.state_digest():
        raise AssertionError("state digest was not preserved in export")
    if lifecycle_clone.history_export() != history:
        raise AssertionError("lifecycle export did not round-trip cleanly")

    return {
        "phase": "2",
        "slice": "3",
        "verifier": "verify_phase_02_lifecycle",
        "status": "pass",
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "lifecycle-runtime-importable", "result": "pass"},
            {"id": "lifecycle-bootstrap-activate-hibernate-reactivate", "result": "pass"},
            {"id": "lifecycle-split-merge-quarantine-clear-retire", "result": "pass"},
            {"id": "lifecycle-history-summary-roundtrip", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "runtime_symbols": {
            "lifecycle_engine": [name for name in dir(LifecycleEngine) if not name.startswith("_")],
            "cell_registry": [name for name in dir(CellRegistry) if not name.startswith("_")],
        },
        "notes": [
            "lifecycle must stay replay-safe, history-backed, and bounded",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(BASELINE_FILES + RUNTIME_FILES)
    if missing:
        report = build_blocked_report(missing)
        write_json(REPORT_PATH, report)
        print("phase_02 slice_3 lifecycle verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    write_json(REPORT_PATH, report)
    print("phase_02 slice_3 lifecycle verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
