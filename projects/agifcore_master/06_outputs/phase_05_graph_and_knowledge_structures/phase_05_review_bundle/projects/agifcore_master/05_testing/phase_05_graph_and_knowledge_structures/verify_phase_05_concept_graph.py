from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_05_graph_and_knowledge_structures"
VERIFICATION_NAME = "concept_graph"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase5_graph"
RUNTIME_IMPORTS = (f"{RUNTIME_PACKAGE}.concept_graph", f"{RUNTIME_PACKAGE}.provenance_links")
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md",
    "projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/__init__.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/concept_graph.py",
)


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
RUNTIME_PARENT = PROJECT_ROOT / EXECUTION_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_05_evidence"
REPORT_PATH = EVIDENCE_DIR / "phase_05_concept_graph_report.json"


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


def runtime_modules_available() -> bool:
    try:
        for module_name in RUNTIME_IMPORTS:
            importlib.import_module(module_name)
    except Exception:
        return False
    return True


def build_blocked_report(missing: list[str]) -> dict[str, Any]:
    return {
        "phase": "5",
        "verifier": "verify_phase_05_concept_graph",
        "status": "blocked",
        "blocker": {"kind": "missing_runtime_dependencies", "missing_files": missing},
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "concept-runtime-present", "result": "blocked"},
            {"id": "concept-graph-relations-ready", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "notes": ["concept graph must hold reviewed abstractions only", "no approval implied"],
    }


def build_pass_report() -> dict[str, Any]:
    from agifcore_phase5_graph.concept_graph import ConceptGraphError, ConceptGraphStore

    source_links = [
        {"role": "source_memory", "ref_id": "semantic-entry-7", "ref_kind": "semantic_entry", "source_path": "phase4/semantic"},
        {"role": "review", "ref_id": "memory-review-21", "ref_kind": "review", "source_path": "phase4/review"},
    ]
    edge_links = [{"role": "review", "ref_id": "memory-review-22", "ref_kind": "review", "source_path": "phase4/review"}]
    store = ConceptGraphStore()
    store.add_concept(
        concept_id="concept-1",
        concept_type="theory_fragment",
        statement="Invoices share stable field structure",
        theory_fragments=["field stability"],
        descriptor_refs=["desc-1"],
        tags=["invoice", "structure"],
        trust_band="reviewed",
        policy_requirements=["route"],
        provenance_links=source_links,
    )
    store.add_concept(
        concept_id="concept-2",
        concept_type="abstraction",
        statement="Invoice workflows separate extraction from normalization",
        theory_fragments=["procedure layering"],
        descriptor_refs=["desc-2"],
        tags=["invoice", "normalization"],
        trust_band="bounded_local",
        policy_requirements=["route"],
        provenance_links=source_links,
    )
    store.add_concept(
        concept_id="concept-3",
        concept_type="abstraction",
        statement="Invoice workflows separate extraction and correction",
        theory_fragments=["correction layering"],
        descriptor_refs=["desc-3"],
        tags=["invoice", "correction"],
        trust_band="bounded_local",
        policy_requirements=["route"],
        provenance_links=source_links,
    )
    edge_id = store.relate(
        edge_id="concept-edge-1",
        source_concept_id="concept-1",
        target_concept_id="concept-2",
        relation="supports",
        provenance_links=edge_links,
    )
    store.mark_superseded(concept_id="concept-2", successor_id="concept-3", review_ref="memory-review-23")

    exported = store.export_state()
    clone = ConceptGraphStore()
    clone.load_state(exported)

    try:
        store.add_concept(
            concept_id="concept-bad",
            concept_type="theory_fragment",
            statement="Should fail",
            theory_fragments=[],
            descriptor_refs=[],
            tags=[],
            trust_band="unknown",
            policy_requirements=[],
            provenance_links=[source_links[0]],
        )
        missing_review_blocked = False
    except ConceptGraphError:
        missing_review_blocked = True

    if clone.export_state() != exported:
        raise ValueError("concept graph export did not round-trip cleanly")
    if store.concept_state("concept-2")["status"] != "superseded":
        raise ValueError("concept supersession was not preserved")
    if not missing_review_blocked:
        raise ValueError("concept graph accepted missing review provenance")

    return {
        "phase": "5",
        "verifier": "verify_phase_05_concept_graph",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "concept-runtime-importable", "result": "pass"},
            {"id": "concept-relations-supported", "result": "pass"},
            {"id": "concept-supersession-supported", "result": "pass"},
            {"id": "concept-provenance-enforced", "result": "pass"},
            {"id": "concept-load-state-roundtrip-clean", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "anchors": {
            "active_concept_ids": store.active_concept_ids(),
            "superseded_concept": store.concept_state("concept-2"),
            "replacement_concept": store.concept_state("concept-3"),
            "edge_id": edge_id,
        },
        "notes": ["concept graph stays abstraction-only and separate from procedural reuse", "no approval implied"],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_05 concept_graph verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_05 concept_graph verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
