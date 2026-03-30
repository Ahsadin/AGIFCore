from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_05_graph_and_knowledge_structures"
VERIFICATION_NAME = "descriptor_graph"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase5_graph"
RUNTIME_IMPORTS = (
    f"{RUNTIME_PACKAGE}.descriptor_graph",
    f"{RUNTIME_PACKAGE}.provenance_links",
    f"{RUNTIME_PACKAGE}.supersession_rules",
)
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/__init__.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/descriptor_graph.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/provenance_links.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/supersession_rules.py",
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
REPORT_PATH = EVIDENCE_DIR / "phase_05_descriptor_graph_report.json"


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
        "verifier": "verify_phase_05_descriptor_graph",
        "status": "blocked",
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 5 descriptor graph runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "descriptor-runtime-present", "result": "blocked"},
            {"id": "descriptor-supersession-supported", "result": "blocked"},
            {"id": "descriptor-provenance-enforced", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "notes": ["descriptor graph must stay distinct from skill, concept, and transfer graphs", "no approval implied"],
    }


def build_pass_report() -> dict[str, Any]:
    from agifcore_phase5_graph.descriptor_graph import DescriptorGraphError, DescriptorGraphStore

    source_links = [
        {"role": "source_memory", "ref_id": "semantic-entry-1", "ref_kind": "semantic_entry", "source_path": "phase4/semantic"},
        {"role": "review", "ref_id": "memory-review-1", "ref_kind": "review", "source_path": "phase4/review"},
    ]
    edge_links = [{"role": "review", "ref_id": "memory-review-2", "ref_kind": "review", "source_path": "phase4/review"}]
    store = DescriptorGraphStore()
    store.add_node(
        descriptor_id="desc-1",
        descriptor_type="workflow_pattern",
        label="Invoice extraction",
        alias_tags=["invoice", "extract"],
        domain_tags=["finance_document_workflows"],
        concept_tags=["extraction"],
        support_refs=["support://desc-1"],
        trust_band="policy",
        policy_requirements=["route"],
        provenance_links=source_links,
        origin_kind="inherited",
        inherited_from=["agif_fabric_v1"],
    )
    store.add_node(
        descriptor_id="desc-2",
        descriptor_type="workflow_pattern",
        label="Invoice normalization",
        alias_tags=["invoice", "normalize"],
        domain_tags=["finance_document_workflows"],
        concept_tags=["normalization"],
        support_refs=["support://desc-2"],
        trust_band="bounded_local",
        policy_requirements=["route"],
        provenance_links=source_links,
    )
    store.add_node(
        descriptor_id="desc-3",
        descriptor_type="workflow_pattern",
        label="Invoice structured extraction",
        alias_tags=["invoice", "structured"],
        domain_tags=["finance_document_workflows"],
        concept_tags=["extraction"],
        support_refs=["support://desc-3"],
        trust_band="bounded_local",
        policy_requirements=["route"],
        provenance_links=source_links,
    )
    edge_id = store.relate(
        edge_id="edge-1",
        source_descriptor_id="desc-1",
        target_descriptor_id="desc-2",
        relation="supports",
        weight=0.8,
        provenance_links=edge_links,
    )
    store.mark_retired(descriptor_id="desc-1", retirement_ref="retirement-1")
    store.mark_superseded(descriptor_id="desc-2", successor_id="desc-3", review_ref="memory-review-3")

    exported = store.export_state()
    clone = DescriptorGraphStore()
    clone.load_state(exported)

    try:
        store.add_node(
            descriptor_id="desc-bad",
            descriptor_type="workflow_pattern",
            label="Bad node",
            alias_tags=[],
            domain_tags=["finance_document_workflows"],
            concept_tags=[],
            support_refs=[],
            trust_band="unknown",
            policy_requirements=[],
            provenance_links=[source_links[0]],
        )
        missing_review_blocked = False
    except DescriptorGraphError:
        missing_review_blocked = True

    if clone.export_state() != exported:
        raise ValueError("descriptor graph export did not round-trip cleanly")
    if store.node_state("desc-2")["status"] != "superseded":
        raise ValueError("descriptor supersession state was not preserved")
    if store.node_state("desc-1")["status"] != "retired":
        raise ValueError("descriptor retirement state was not preserved")
    if not missing_review_blocked:
        raise ValueError("descriptor graph accepted missing review provenance")

    return {
        "phase": "5",
        "verifier": "verify_phase_05_descriptor_graph",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "descriptor-runtime-importable", "result": "pass"},
            {"id": "descriptor-edge-relations-supported", "result": "pass"},
            {"id": "descriptor-retirement-visible", "result": "pass"},
            {"id": "descriptor-supersession-visible", "result": "pass"},
            {"id": "descriptor-provenance-enforced", "result": "pass"},
            {"id": "descriptor-load-state-roundtrip-clean", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "anchors": {
            "active_descriptor_ids": store.active_node_ids(),
            "retired_descriptor": store.node_state("desc-1"),
            "superseded_descriptor": store.node_state("desc-2"),
            "edge": store.edge_state(edge_id),
        },
        "notes": ["descriptor graph stays distinct from transfer approval logic", "no approval implied"],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_05 descriptor_graph verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_05 descriptor_graph verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
