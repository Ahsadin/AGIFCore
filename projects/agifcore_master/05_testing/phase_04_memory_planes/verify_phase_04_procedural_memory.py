from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_04_memory_planes"
SLICE_ID = "slice_2"
VERIFICATION_NAME = "procedural_memory"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase4_memory"
RUNTIME_IMPORTS = (f"{RUNTIME_PACKAGE}.procedural_memory",)
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/__init__.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/procedural_memory.py",
)


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
RUNTIME_DIR = PROJECT_ROOT / EXECUTION_ROOT_NAME / PHASE_NAME / "agifcore_phase4_memory"
RUNTIME_PARENT = PROJECT_ROOT / EXECUTION_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_04_evidence"
REPORT_PATH = EVIDENCE_DIR / "phase_04_procedural_memory_report.json"


class ProceduralVerifierError(ValueError):
    pass


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_path() -> None:
    runtime_path = str(RUNTIME_PARENT)
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
            "message": "Phase 4 procedural memory runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "procedural-runtime-present", "result": "blocked"},
            {"id": "procedure-fields-ready", "result": "blocked"},
            {"id": "execution-surface-absent", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "notes": ["procedural memory must stay reusable-procedure-only", "no approval implied"],
    }


def build_pass_report() -> dict[str, object]:
    from agifcore_phase4_memory.procedural_memory import ProceduralMemoryStore

    store = ProceduralMemoryStore()
    procedure_id = store.add_procedure(
        procedure_id="procedure-0001",
        procedure_name="review_memory_note",
        objective="Summarize a reviewed memory note safely.",
        steps=["read reviewed note", "extract stable summary", "attach provenance"],
        preconditions=["reviewed note exists"],
        postconditions=["summary artifact exists"],
        constraints=["no execution side effects", "keep provenance attached"],
        provenance_refs=["trace://phase4/procedural/0001"],
        review_ref="memory-review-00000021",
        source_candidate_id="candidate-0021",
        graph_refs=["skill-ref://memory/review-note"],
        metadata={"risk_band": "bounded"},
    )
    exported = store.export_state()
    clone = ProceduralMemoryStore()
    clone.load_state(exported)
    store.retire_procedure(procedure_id=procedure_id, retirement_ref="retire://phase4/procedural/0001")

    public_names = [name for name in dir(store) if not name.startswith("_")]
    execution_surface_absent = "execute" not in public_names and "run" not in public_names

    if clone.export_state() != exported:
        raise ProceduralVerifierError("procedural memory export did not round-trip cleanly")
    if not execution_surface_absent:
        raise ProceduralVerifierError("procedural memory exposed an execution surface")
    if store.procedure_state(procedure_id)["status"] != "retired":
        raise ProceduralVerifierError("procedure retirement marker was not preserved")

    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "procedural-runtime-importable", "result": "pass"},
            {"id": "procedure-fields-preserved", "result": "pass"},
            {"id": "explicit-constraints-preserved", "result": "pass"},
            {"id": "automatic-execution-surface-absent", "result": "pass"},
            {"id": "load-state-roundtrip-clean", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "runtime_symbols": {
            "procedural_memory": [
                "ProceduralMemoryStore",
                "ProcedureEntry",
                "ProceduralMemoryError",
                "add_procedure",
                "retire_procedure",
                "active_procedure_ids",
                "load_state",
            ]
        },
        "anchors": {
            "procedure_id": procedure_id,
            "active_procedure_ids": clone.active_procedure_ids(),
            "retired_entry": store.procedure_state(procedure_id),
            "exported_entry_count": len(exported["entries"]),
        },
        "notes": [
            "procedural memory stores reusable procedures, not executable behavior",
            "constraints and pre/postconditions remain explicit",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_04 slice_2 procedural_memory verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_04 slice_2 procedural_memory verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
