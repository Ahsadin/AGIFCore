from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_04_memory_planes"
SLICE_ID = "slice_1"
VERIFICATION_NAME = "episodic_memory"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_IMPORTS = ("episodic_memory",)
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
REPORT_PATH = EVIDENCE_DIR / "phase_04_episodic_memory_report.json"


class EpisodicMemoryVerifierError(ValueError):
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
            "message": "Phase 4 episodic memory runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "episodic-memory-runtime-present", "result": "blocked"},
            {"id": "replayable-event-records-ready", "result": "blocked"},
            {"id": "correction-marker-behavior-ready", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "notes": [
            "episodic memory must preserve event order and correction markers",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, object]:
    from episodic_memory import EpisodicMemoryError, EpisodicMemoryStore

    store = EpisodicMemoryStore(max_records=4, max_state_bytes=8192)
    event_one = store.append_event(
        event_id="event-0001",
        conversation_id="conv-phase4-slice1-episodic",
        turn_id="turn-0001",
        event_type="turn_admitted",
        event_summary="turn entered bounded memory",
        content_refs=["trace://phase4/episodic/turn-0001"],
        provenance_refs=["support://phase4/episodic/turn-0001"],
    )
    event_two = store.append_event(
        event_id="event-0002",
        conversation_id="conv-phase4-slice1-episodic",
        turn_id="turn-0002",
        event_type="response_ready",
        event_summary="response anchored for replay",
        content_refs=["trace://phase4/episodic/turn-0002"],
        provenance_refs=["support://phase4/episodic/turn-0002"],
    )
    store.add_correction_marker(
        event_id=event_one,
        correction_id="correction-0001",
        reason="replace initial summary with reviewed summary",
        replacement_event_id=event_two,
    )

    duplicate_blocked = False
    try:
        store.append_event(
            event_id=event_one,
            conversation_id="conv-phase4-slice1-episodic",
            turn_id="turn-0003",
            event_type="duplicate",
            event_summary="should be rejected",
        )
    except EpisodicMemoryError:
        duplicate_blocked = True

    exported = store.export_state()
    clone = EpisodicMemoryStore()
    clone.load_state(exported)
    recent_window = clone.recent_window(limit=2)

    if len(exported["events"]) != 2:
        raise EpisodicMemoryVerifierError("episodic memory did not keep two replayable events")
    if not duplicate_blocked:
        raise EpisodicMemoryVerifierError("episodic memory did not block duplicate event ids")
    if recent_window[0]["event_id"] != "event-0001" or recent_window[1]["event_id"] != "event-0002":
        raise EpisodicMemoryVerifierError("episodic recent window did not preserve order")
    if recent_window[0]["correction_status"] != "corrected":
        raise EpisodicMemoryVerifierError("episodic correction status was not updated")
    if recent_window[0]["correction_markers"][0]["replacement_event_id"] != event_two:
        raise EpisodicMemoryVerifierError("episodic correction marker did not retain replacement id")
    if clone.export_state() != exported:
        raise EpisodicMemoryVerifierError("episodic memory did not roundtrip cleanly")

    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "episodic-memory-runtime-importable", "result": "pass"},
            {"id": "replayable-event-order-preserved", "result": "pass"},
            {"id": "correction-marker-attached", "result": "pass"},
            {"id": "duplicate-event-id-blocked", "result": "pass"},
            {"id": "load-state-roundtrip-clean", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "runtime_symbols": {
            "episodic_memory": [
                "EpisodicMemoryStore",
                "EpisodicEvent",
                "EpisodicMemoryError",
                "append_event",
                "add_correction_marker",
                "recent_window",
                "load_state",
            ],
        },
        "anchors": {
            "event_ids": [event_one, event_two],
            "recent_window": recent_window,
            "exported_event_count": len(exported["events"]),
        },
        "notes": [
            "episodic memory is replayable event history only",
            "correction markers stay explicit and auditable",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_04 slice_1 episodic_memory verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_04 slice_1 episodic_memory verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
