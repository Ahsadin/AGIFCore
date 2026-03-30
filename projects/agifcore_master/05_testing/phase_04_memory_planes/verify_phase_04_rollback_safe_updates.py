from __future__ import annotations

import importlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_04_memory_planes"
SLICE_ID = "slice_1"
VERIFICATION_NAME = "rollback_safe_updates"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_IMPORTS = ("rollback_safe_updates",)
SUPPORTING_VERIFIER_FILES = (
    "projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_workspace_state.py",
    "projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_replay.py",
    "projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_activation_and_trust.py",
    "projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py",
)
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/__init__.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/working_memory.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/episodic_memory.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/continuity_memory.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/memory_review.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/rollback_safe_updates.py",
)
PHASE2_KERNEL_FILES = (
    "projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/rollback_controller.py",
    "projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/replay_ledger.py",
    "projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_types.py",
)


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
OUTPUT_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = OUTPUT_DIR / "phase_04_evidence"
RUNTIME_DIR = PROJECT_ROOT / EXECUTION_ROOT_NAME / PHASE_NAME / "agifcore_phase4_memory"
PHASE2_KERNEL_DIR = PROJECT_ROOT / "04_execution" / "phase_02_fabric_kernel_and_workspace" / "agifcore_phase2_kernel"
REPORT_PATH = EVIDENCE_DIR / "phase_04_rollback_safe_updates_report.json"


class RollbackSafeUpdatesVerifierError(ValueError):
    pass


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_path() -> None:
    runtime_path = str(RUNTIME_DIR)
    if runtime_path not in sys.path:
        sys.path.insert(0, runtime_path)
    phase2_path = str(PHASE2_KERNEL_DIR)
    if phase2_path not in sys.path:
        sys.path.insert(0, phase2_path)


ensure_runtime_import_path()


def dump_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[str]) -> list[str]:
    return [path for path in paths if not (REPO_ROOT / path).exists()]


def load_runtime_module(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except Exception:
        return None


def runtime_modules_available() -> bool:
    return all(load_runtime_module(module_name) is not None for module_name in RUNTIME_IMPORTS)


def build_blocked_report(missing: list[str]) -> dict[str, object]:
    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "blocked",
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 4 rollback-safe update runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(PHASE2_KERNEL_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "rollback-safe-runtime-present", "result": "blocked"},
            {"id": "apply-batch-uses-rollback-substrate", "result": "blocked"},
            {"id": "restore-and-reject-paths-ready", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "notes": [
            "rollback-safe updates must stay tied to Phase 2 rollback and replay",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, object]:
    from rollback_safe_updates import RollbackSafeUpdateError, RollbackSafeUpdater

    updater = RollbackSafeUpdater()
    original_state = {
        "working": {
            "turn_ref": "turn://conv-phase4-slice1-rollback/turn-0001",
            "payload": {"draft": True, "summary": "initial"},
        },
        "episodic": {
            "event_ids": ["event-0001"],
            "correction_status": "original",
        },
    }

    def apply_mutator(state: dict[str, Any]) -> dict[str, Any]:
        state["working"]["payload"]["draft"] = False
        state["working"]["payload"]["summary"] = "applied"
        state["episodic"]["correction_status"] = "corrected"
        return state

    applied = updater.apply_batch(
        label="phase4-memory-apply",
        conversation_id="conv-phase4-slice1-rollback",
        turn_id="turn-0001",
        event_ids=["event-0001"],
        plane_exports=deepcopy(original_state),
        mutator=apply_mutator,
    )
    restored = updater.restore_batch(rollback_ref=applied.rollback_ref)

    def reject_mutator(_state: dict[str, Any]) -> dict[str, Any]:
        raise ValueError("reject this batch")

    rejected = updater.apply_batch(
        label="phase4-memory-reject",
        conversation_id="conv-phase4-slice1-rollback",
        turn_id="turn-0002",
        event_ids=["event-0002"],
        plane_exports=deepcopy(original_state),
        mutator=reject_mutator,
    )

    explicit_reject = updater.reject_batch(
        rollback_ref=applied.rollback_ref,
        reason="manual rollback after inspection",
    )

    rollback_snapshot = updater.rollback_snapshot_export()
    replay_export = updater.replay_export()

    if applied.status != "applied" or applied.replay_id is None:
        raise RollbackSafeUpdatesVerifierError("apply_batch did not report an applied batch")
    if applied.updated_state["working"]["payload"]["draft"] is not False:
        raise RollbackSafeUpdatesVerifierError("apply_batch did not mutate working state")
    if restored.status != "restored":
        raise RollbackSafeUpdatesVerifierError("restore_batch did not restore the snapshot")
    if restored.updated_state != original_state:
        raise RollbackSafeUpdatesVerifierError("restore_batch did not return the original state")
    if rejected.status != "rejected" or rejected.replay_id is not None:
        raise RollbackSafeUpdatesVerifierError("rejected batch did not stay rejected")
    if "reject this batch" not in (rejected.reason or ""):
        raise RollbackSafeUpdatesVerifierError("rejected batch did not preserve the rejection reason")
    if explicit_reject.status != "rejected":
        raise RollbackSafeUpdatesVerifierError("explicit reject_batch did not reject the batch")
    if explicit_reject.updated_state != original_state:
        raise RollbackSafeUpdatesVerifierError("explicit reject_batch did not restore the state")
    if rollback_snapshot["snapshot_count"] < 1:
        raise RollbackSafeUpdatesVerifierError("rollback snapshot export did not capture the snapshot")
    if replay_export["record_count"] < 3:
        raise RollbackSafeUpdatesVerifierError("replay export did not record apply/restore/reject actions")

    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(PHASE2_KERNEL_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "rollback-safe-runtime-importable", "result": "pass"},
            {"id": "apply-batch-records-replay-and-snapshot", "result": "pass"},
            {"id": "restore-batch-restores-original-state", "result": "pass"},
            {"id": "reject-batch-rejects-and-restores", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "runtime_symbols": {
            "rollback_safe_updates": [
                "RollbackSafeUpdater",
                "RollbackSafeUpdateError",
                "UpdateBatchResult",
                "apply_batch",
                "restore_batch",
                "reject_batch",
                "rollback_snapshot_export",
                "replay_export",
            ],
            "phase2_substrate": [
                "RollbackController",
                "ReplayLedger",
            ],
        },
        "anchors": {
            "applied": applied.to_dict(),
            "restored": restored.to_dict(),
            "rejected": rejected.to_dict(),
            "explicit_reject": explicit_reject.to_dict(),
            "rollback_snapshot": rollback_snapshot,
            "replay_export": replay_export,
        },
        "notes": [
            "rollback-safe updates must go through Phase 2 rollback and replay anchors",
            "apply, restore, and reject are all explicit runtime behaviors",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(PHASE2_KERNEL_FILES) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_04 slice_1 rollback_safe_updates verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_04 slice_1 rollback_safe_updates verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
