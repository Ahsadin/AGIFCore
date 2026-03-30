from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_05_graph_and_knowledge_structures"
VERIFICATION_NAME = "support_selection"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase5_graph"
RUNTIME_IMPORTS = (
    f"{RUNTIME_PACKAGE}.descriptor_graph",
    f"{RUNTIME_PACKAGE}.skill_graph",
    f"{RUNTIME_PACKAGE}.concept_graph",
    f"{RUNTIME_PACKAGE}.support_selection",
)
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md",
    "projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/descriptor_graph.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/skill_graph.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/concept_graph.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/support_selection.py",
)
REQUIRED_REPORT_FILES = (
    "phase_05_descriptor_graph_report.json",
    "phase_05_skill_graph_report.json",
    "phase_05_concept_graph_report.json",
    "phase_05_transfer_graph_report.json",
    "phase_05_provenance_links_report.json",
    "phase_05_conflict_and_supersession_report.json",
    "phase_05_support_selection_report.json",
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
REPORT_PATH = EVIDENCE_DIR / "phase_05_support_selection_report.json"
MANIFEST_PATH = EVIDENCE_DIR / "phase_05_evidence_manifest.json"


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
        "verifier": "verify_phase_05_support_selection",
        "status": "blocked",
        "blocker": {"kind": "missing_runtime_dependencies", "missing_files": missing},
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "support-selection-runtime-present", "result": "blocked"},
            {"id": "bounded-selection-ready", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH), "manifest": rel(MANIFEST_PATH)},
        "notes": ["support selection must stay graph-grounded and bounded", "no approval implied"],
    }


def build_pass_report() -> dict[str, Any]:
    from agifcore_phase5_graph.concept_graph import ConceptGraphStore
    from agifcore_phase5_graph.descriptor_graph import DescriptorGraphStore
    from agifcore_phase5_graph.skill_graph import SkillGraphStore
    from agifcore_phase5_graph.support_selection import SupportSelectionEngine

    links = [
        {"role": "source_memory", "ref_id": "entry-1", "ref_kind": "semantic_entry", "source_path": "phase4/semantic"},
        {"role": "review", "ref_id": "review-1", "ref_kind": "review", "source_path": "phase4/review"},
    ]
    dg = DescriptorGraphStore()
    sg = SkillGraphStore()
    cg = ConceptGraphStore()
    dg.add_node(descriptor_id="desc-1", descriptor_type="pattern", label="Invoice extraction", alias_tags=["invoice", "extract"], domain_tags=["finance_document_workflows"], concept_tags=["extraction"], support_refs=["support://1"], trust_band="policy", policy_requirements=["route"], provenance_links=links)
    sg.add_skill(skill_id="skill-1", skill_name="Extract invoice fields", objective="Extract invoice fields", descriptor_refs=["desc-1"], preconditions=["document available"], postconditions=["fields extracted"], constraints=["reviewed only"], allowed_target_domains=["finance_document_workflows"], trust_band="bounded_local", policy_requirements=["route"], provenance_links=links)
    cg.add_concept(concept_id="concept-1", concept_type="theory_fragment", statement="Invoices share stable field structure", theory_fragments=["field stability"], descriptor_refs=["desc-1"], tags=["invoice", "structure"], trust_band="reviewed", policy_requirements=["route"], provenance_links=links)

    selector = SupportSelectionEngine()
    selected = selector.select_from_graphs(
        query_id="query-1",
        query_text="invoice extraction structure",
        target_domain="finance_document_workflows",
        required_policy_requirements=["route"],
        descriptor_graph=dg,
        skill_graph=sg,
        concept_graph=cg,
    )

    oversized_dg = DescriptorGraphStore()
    for index in range(25):
        oversized_dg.add_node(
            descriptor_id=f"oversized-{index:02d}",
            descriptor_type="pattern",
            label=f"Invoice support {index}",
            alias_tags=["invoice"],
            domain_tags=["finance_document_workflows"],
            concept_tags=["extraction"],
            support_refs=[f"support://oversized/{index}"],
            trust_band="bounded_local",
            policy_requirements=["route"],
            provenance_links=links,
        )
    blocked = selector.select_from_graphs(
        query_id="query-2",
        query_text="invoice support",
        target_domain="finance_document_workflows",
        required_policy_requirements=["route"],
        descriptor_graph=oversized_dg,
        skill_graph=sg,
        concept_graph=cg,
    )

    missing_policy = selector.select_from_graphs(
        query_id="query-3",
        query_text="invoice extraction structure",
        target_domain="finance_document_workflows",
        required_policy_requirements=[],
        descriptor_graph=dg,
        skill_graph=sg,
        concept_graph=cg,
    )

    if selected.status != "selected" or not selected.selected_candidate_ids:
        raise ValueError("support selection did not select governed graph-backed candidates")
    if blocked.status != "blocked":
        raise ValueError("support selection did not enforce the candidate ceiling")
    if missing_policy.status != "abstained":
        raise ValueError("support selection did not block candidates that fail policy requirements")

    return {
        "phase": "5",
        "verifier": "verify_phase_05_support_selection",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "graph-grounded-selection-supported", "result": "pass"},
            {"id": "trust-and-provenance-bounded-selection-supported", "result": "pass"},
            {"id": "candidate-ceiling-enforced", "result": "pass"},
            {"id": "policy-filtering-enforced", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH), "manifest": rel(MANIFEST_PATH)},
        "anchors": {
            "selected_result": selected.to_dict(),
            "blocked_result": blocked.to_dict(),
            "missing_policy_result": missing_policy.to_dict(),
        },
        "notes": ["selection stays graph-grounded, bounded, and honest", "no approval implied"],
    }


def refresh_evidence_manifest() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    missing_reports: list[str] = []
    invalid_reports: list[str] = []
    for filename in REQUIRED_REPORT_FILES:
        report_path = EVIDENCE_DIR / filename
        if not report_path.exists():
            missing_reports.append(filename)
            continue
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        status = str(payload.get("status", "unknown"))
        if status not in {"pass", "blocked"}:
            invalid_reports.append(filename)
        reports.append(
            {
                "report_id": filename.removeprefix("phase_05_").removesuffix("_report.json"),
                "path": rel(report_path),
                "status": status,
            }
        )

    overall_pass = not missing_reports and not invalid_reports and all(report["status"] == "pass" for report in reports)
    manifest = {
        "phase": "5",
        "phase_remains_open": True,
        "required_report_count": len(REQUIRED_REPORT_FILES),
        "available_report_count": len(reports),
        "missing_reports": missing_reports,
        "invalid_reports": invalid_reports,
        "reports": reports,
        "status": "phase_5_verifier_family_pass" if overall_pass else "phase_5_verifier_family_incomplete",
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 5 remains open",
            "manifest is rebuilt from actual report files on disk",
            "no approval implied",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        refresh_evidence_manifest()
        print("phase_05 support_selection verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    refresh_evidence_manifest()
    print("phase_05 support_selection verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
