from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_04_memory_planes"
SLICE_ID = "slice_2"
VERIFICATION_NAME = "semantic_memory"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase4_memory"
RUNTIME_IMPORTS = (f"{RUNTIME_PACKAGE}.semantic_memory",)
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/__init__.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/semantic_memory.py",
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
REPORT_PATH = EVIDENCE_DIR / "phase_04_semantic_memory_report.json"


class SemanticVerifierError(ValueError):
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
            "message": "Phase 4 semantic memory runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "semantic-runtime-present", "result": "blocked"},
            {"id": "reviewed-abstraction-boundary-ready", "result": "blocked"},
            {"id": "supersession-ready", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "notes": ["semantic memory must stay abstraction-only", "no approval implied"],
    }


def build_pass_report() -> dict[str, object]:
    from agifcore_phase4_memory.semantic_memory import SemanticMemoryError, SemanticMemoryStore

    store = SemanticMemoryStore()
    entry_id = store.add_entry(
        entry_id="semantic-0001",
        concept_type="theory_fragment",
        abstraction="A reviewed abstraction about bounded memory pressure.",
        provenance_refs=["trace://phase4/semantic/0001"],
        review_ref="memory-review-00000011",
        source_candidate_id="candidate-0001",
        supporting_refs=["support://phase4/semantic/0001"],
        graph_refs=["concept-ref://memory/pressure"],
        metadata={"confidence": "high"},
    )
    store.mark_superseded(
        entry_id=entry_id,
        superseded_by="semantic-0002",
        correction_ref="corr-sem-0001",
    )
    exported = store.export_state()
    clone = SemanticMemoryStore()
    clone.load_state(exported)

    try:
        store.add_entry(
            entry_id="semantic-0003",
            concept_type="illegal_transcript",
            abstraction="this should fail",
            provenance_refs=["trace://phase4/semantic/0003"],
            review_ref="memory-review-00000012",
            source_candidate_id="candidate-0003",
            metadata={"raw_transcript": "full user turn text"},
        )
        raw_transcript_blocked = False
    except SemanticMemoryError:
        raw_transcript_blocked = True

    if clone.export_state() != exported:
        raise SemanticVerifierError("semantic memory export did not round-trip cleanly")
    if store.entry_state("semantic-0001")["status"] != "superseded":
        raise SemanticVerifierError("semantic supersession was not preserved")
    if not raw_transcript_blocked:
        raise SemanticVerifierError("semantic memory did not block raw transcript leakage")

    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "semantic-runtime-importable", "result": "pass"},
            {"id": "reviewed-abstraction-only", "result": "pass"},
            {"id": "supersession-supported", "result": "pass"},
            {"id": "raw-transcript-leakage-blocked", "result": "pass"},
            {"id": "load-state-roundtrip-clean", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "runtime_symbols": {
            "semantic_memory": [
                "SemanticMemoryStore",
                "SemanticMemoryEntry",
                "SemanticMemoryError",
                "add_entry",
                "mark_superseded",
                "active_entry_ids",
                "load_state",
            ]
        },
        "anchors": {
            "entry_id": entry_id,
            "active_entry_ids": store.active_entry_ids(),
            "superseded_entry": store.entry_state("semantic-0001"),
            "exported_entry_count": len(exported["entries"]),
        },
        "notes": [
            "semantic memory stores reviewed abstractions only",
            "graph refs remain plain references, not graph implementation",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_04 slice_2 semantic_memory verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_04 slice_2 semantic_memory verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
