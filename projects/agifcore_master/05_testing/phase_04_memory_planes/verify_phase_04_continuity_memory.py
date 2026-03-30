from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_04_memory_planes"
SLICE_ID = "slice_1"
VERIFICATION_NAME = "continuity_memory"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_IMPORTS = ("continuity_memory",)
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
OUTPUT_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = OUTPUT_DIR / "phase_04_evidence"
RUNTIME_DIR = PROJECT_ROOT / EXECUTION_ROOT_NAME / PHASE_NAME / "agifcore_phase4_memory"
REPORT_PATH = EVIDENCE_DIR / "phase_04_continuity_memory_report.json"


class ContinuityMemoryVerifierError(ValueError):
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
            "message": "Phase 4 continuity memory runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "continuity-memory-runtime-present", "result": "blocked"},
            {"id": "self-history-anchor-ready", "result": "blocked"},
            {"id": "supersession-marker-behavior-ready", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "notes": [
            "continuity memory must remain self-history only",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, object]:
    from continuity_memory import ContinuityMemoryError, ContinuityMemoryStore

    store = ContinuityMemoryStore(max_entries=4, max_state_bytes=8192)
    anchor_one = store.record_anchor(
        anchor_id="anchor-0001",
        subject="self",
        continuity_kind="self_history",
        statement="Phase 4 verifier has an explicit self-history anchor.",
        provenance_refs=["trace://phase4/continuity/turn-0001"],
        metadata={"source": "verifier", "level": "primary"},
    )
    anchor_two = store.record_anchor(
        anchor_id="anchor-0002",
        subject="self",
        continuity_kind="self_history",
        statement="Phase 4 verifier supersedes the earlier continuity statement.",
        provenance_refs=["trace://phase4/continuity/turn-0002"],
        metadata={"source": "verifier", "level": "replacement"},
    )
    store.mark_superseded(
        anchor_id=anchor_one,
        superseded_by=anchor_two,
        correction_ref="correction://phase4/continuity/0001",
    )

    duplicate_blocked = False
    try:
        store.record_anchor(
            anchor_id=anchor_one,
            subject="self",
            continuity_kind="self_history",
            statement="should be blocked",
            provenance_refs=["trace://phase4/continuity/turn-0003"],
        )
    except ContinuityMemoryError:
        duplicate_blocked = True

    exported = store.export_state()
    clone = ContinuityMemoryStore()
    clone.load_state(exported)
    active_ids = clone.active_anchor_ids()
    anchor_map = {item["anchor_id"]: item for item in exported["anchors"]}

    if not duplicate_blocked:
        raise ContinuityMemoryVerifierError("continuity memory did not block duplicate anchors")
    if active_ids != [anchor_two]:
        raise ContinuityMemoryVerifierError("continuity active anchor list did not reflect supersession")
    if anchor_map[anchor_one]["status"] != "superseded":
        raise ContinuityMemoryVerifierError("continuity superseded status was not preserved")
    if anchor_map[anchor_one]["superseded_by"] != anchor_two:
        raise ContinuityMemoryVerifierError("continuity supersession target was not preserved")
    if anchor_map[anchor_one]["correction_refs"] != ["correction://phase4/continuity/0001"]:
        raise ContinuityMemoryVerifierError("continuity correction ref was not preserved")
    if clone.export_state() != exported:
        raise ContinuityMemoryVerifierError("continuity memory did not roundtrip cleanly")

    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "continuity-memory-runtime-importable", "result": "pass"},
            {"id": "self-history-anchor-recorded", "result": "pass"},
            {"id": "supersession-marker-applied", "result": "pass"},
            {"id": "duplicate-anchor-blocked", "result": "pass"},
            {"id": "load-state-roundtrip-clean", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "runtime_symbols": {
            "continuity_memory": [
                "ContinuityMemoryStore",
                "ContinuityAnchor",
                "ContinuityMemoryError",
                "record_anchor",
                "mark_superseded",
                "active_anchor_ids",
                "load_state",
            ],
        },
        "anchors": {
            "anchor_ids": [anchor_one, anchor_two],
            "active_anchor_ids": active_ids,
            "exported_anchor_count": len(exported["anchors"]),
        },
        "notes": [
            "continuity memory preserves durable self-history anchors",
            "supersession remains explicit and reversible",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_04 slice_1 continuity_memory verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_04 slice_1 continuity_memory verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
