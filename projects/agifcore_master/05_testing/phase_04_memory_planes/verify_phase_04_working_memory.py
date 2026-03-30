from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_04_memory_planes"
PHASE_LABEL = "Phase 4"
SLICE_ID = "slice_1"
VERIFICATION_NAME = "working_memory"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_IMPORTS = ("working_memory",)
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


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
TESTING_DIR = PROJECT_ROOT / TEST_ROOT_NAME / PHASE_NAME
OUTPUT_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = OUTPUT_DIR / "phase_04_evidence"
RUNTIME_DIR = PROJECT_ROOT / EXECUTION_ROOT_NAME / PHASE_NAME / "agifcore_phase4_memory"
REPORT_PATH = EVIDENCE_DIR / "phase_04_working_memory_report.json"


class WorkingMemoryVerifierError(ValueError):
    pass


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_path() -> None:
    runtime_path = str(RUNTIME_DIR)
    if runtime_path not in sys.path:
        sys.path.insert(0, runtime_path)


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
            "message": "Phase 4 working memory runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "working-memory-runtime-present", "result": "blocked"},
            {"id": "bounded-turn-state-ready", "result": "blocked"},
            {"id": "promotable-candidate-handling-ready", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "notes": [
            "working memory must stay bounded and candidate-driven",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, object]:
    from working_memory import WorkingMemoryError, WorkingMemoryStore

    store = WorkingMemoryStore(max_state_bytes=4096, max_candidates=1)
    turn_ref = store.bind_turn(
        conversation_id="conv-phase4-slice1-working",
        turn_id="turn-0001",
        task_id="task-phase4-working-001",
        support_refs=["ctx://phase4/working/primary"],
        scratchpad={"focus": "working memory", "step": 1},
    )
    store.set_scratch_value("status", "draft")
    store.add_support_ref("ctx://phase4/working/secondary")
    candidate_id = store.add_candidate(
        candidate_id="candidate-001",
        candidate_kind="promotable_summary",
        target_plane="semantic",
        payload={"summary": "ready for review", "confidence": 0.94},
        provenance_refs=[turn_ref, "trace://phase4/working/turn-0001"],
    )

    candidate_budget_blocked = False
    try:
        store.add_candidate(
            candidate_id="candidate-002",
            candidate_kind="promotable_summary",
            target_plane="procedural",
            payload={"summary": "should be blocked"},
            provenance_refs=[turn_ref],
        )
    except WorkingMemoryError:
        candidate_budget_blocked = True

    store.mark_candidate_reviewed(
        candidate_id=candidate_id,
        review_ref="memory-review://phase4/working/turn-0001",
        status="approved",
    )

    exported = store.export_state()
    pressure = store.memory_pressure()
    clone = WorkingMemoryStore()
    clone.load_state(exported)
    consumed = store.consume_candidate(candidate_id)

    if pressure["current_state_bytes"] > pressure["max_state_bytes"]:
        raise WorkingMemoryVerifierError("working memory exceeded its max state bytes")
    if pressure["candidate_count"] != 1:
        raise WorkingMemoryVerifierError("working memory did not track one promotable candidate")
    if pressure["max_candidate_count"] != 1:
        raise WorkingMemoryVerifierError("working memory did not preserve the candidate budget")
    if not candidate_budget_blocked:
        raise WorkingMemoryVerifierError("working memory did not block candidate budget overflow")
    if clone.candidate_ids(status="approved") != [candidate_id]:
        raise WorkingMemoryVerifierError("approved candidate did not survive load_state roundtrip")
    if clone.export_state()["turn_state"]["turn_id"] != "turn-0001":
        raise WorkingMemoryVerifierError("turn state turn_id was not preserved")
    if clone.export_state()["turn_state"]["support_refs"] != [
        "ctx://phase4/working/primary",
        "ctx://phase4/working/secondary",
    ]:
        raise WorkingMemoryVerifierError("support refs were not bounded and deduplicated")
    if consumed["status"] != "approved":
        raise WorkingMemoryVerifierError("consumed candidate did not preserve approval status")
    if store.candidate_ids():
        raise WorkingMemoryVerifierError("consuming the candidate did not empty working memory")

    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "working-memory-runtime-importable", "result": "pass"},
            {"id": "bounded-turn-state-enforced", "result": "pass"},
            {"id": "promotable-candidate-budget-enforced", "result": "pass"},
            {"id": "candidate-review-status-roundtrip", "result": "pass"},
            {"id": "candidate-consume-clears-working-state", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "runtime_symbols": {
            "working_memory": [
                "WorkingMemoryStore",
                "WorkingCandidate",
                "WorkingMemoryError",
                "bind_turn",
                "add_candidate",
                "mark_candidate_reviewed",
                "consume_candidate",
                "memory_pressure",
            ],
        },
        "anchors": {
            "turn_ref": turn_ref,
            "candidate_id": candidate_id,
            "approved_candidate_ids": clone.candidate_ids(status="approved"),
            "memory_pressure": pressure,
            "consumed_candidate": consumed,
        },
        "notes": [
            "working memory is bounded current-turn state only",
            "promotable candidates stay explicit until consumed",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_04 slice_1 working_memory verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_04 slice_1 working_memory verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
