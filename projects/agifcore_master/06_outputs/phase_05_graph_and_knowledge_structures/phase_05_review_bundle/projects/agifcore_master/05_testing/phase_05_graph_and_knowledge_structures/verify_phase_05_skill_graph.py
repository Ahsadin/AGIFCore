from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_05_graph_and_knowledge_structures"
VERIFICATION_NAME = "skill_graph"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase5_graph"
RUNTIME_IMPORTS = (f"{RUNTIME_PACKAGE}.skill_graph", f"{RUNTIME_PACKAGE}.provenance_links")
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md",
    "projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/__init__.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/skill_graph.py",
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
REPORT_PATH = EVIDENCE_DIR / "phase_05_skill_graph_report.json"


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
        "verifier": "verify_phase_05_skill_graph",
        "status": "blocked",
        "blocker": {"kind": "missing_runtime_dependencies", "missing_files": missing},
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "skill-runtime-present", "result": "blocked"},
            {"id": "skill-grounding-ready", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "notes": ["skill graph must stay procedural and governed", "no approval implied"],
    }


def build_pass_report() -> dict[str, Any]:
    from agifcore_phase5_graph.skill_graph import SkillGraphError, SkillGraphStore

    source_links = [
        {"role": "source_memory", "ref_id": "procedure-entry-1", "ref_kind": "procedure_entry", "source_path": "phase4/procedural"},
        {"role": "review", "ref_id": "memory-review-10", "ref_kind": "review", "source_path": "phase4/review"},
    ]
    edge_links = [{"role": "review", "ref_id": "memory-review-11", "ref_kind": "review", "source_path": "phase4/review"}]
    store = SkillGraphStore()
    store.add_skill(
        skill_id="skill-1",
        skill_name="Extract invoice fields",
        objective="Extract reviewed invoice fields from a bounded local document",
        descriptor_refs=["desc-1"],
        preconditions=["document available"],
        postconditions=["fields extracted"],
        constraints=["no external model", "reviewed support only"],
        allowed_target_domains=["finance_document_workflows"],
        trust_band="bounded_local",
        policy_requirements=["route"],
        provenance_links=source_links,
    )
    store.add_skill(
        skill_id="skill-2",
        skill_name="Normalize invoice fields",
        objective="Normalize extracted invoice fields",
        descriptor_refs=["desc-2"],
        preconditions=["fields extracted"],
        postconditions=["fields normalized"],
        constraints=["reviewed support only"],
        allowed_target_domains=["finance_document_workflows"],
        trust_band="reviewed",
        policy_requirements=["route"],
        provenance_links=source_links,
    )
    edge_id = store.add_grounding(
        edge_id="skill-edge-1",
        skill_id="skill-1",
        descriptor_id="desc-2",
        provenance_links=edge_links,
    )
    store.mark_superseded(skill_id="skill-1", successor_id="skill-2", review_ref="memory-review-12")

    exported = store.export_state()
    clone = SkillGraphStore()
    clone.load_state(exported)

    try:
        store.add_skill(
            skill_id="skill-bad",
            skill_name="Bad skill",
            objective="Should fail",
            descriptor_refs=[],
            preconditions=[],
            postconditions=[],
            constraints=[],
            allowed_target_domains=[],
            trust_band="unknown",
            policy_requirements=[],
            provenance_links=[source_links[0]],
        )
        missing_review_blocked = False
    except SkillGraphError:
        missing_review_blocked = True

    if clone.export_state() != exported:
        raise ValueError("skill graph export did not round-trip cleanly")
    if store.skill_state("skill-1")["status"] != "superseded":
        raise ValueError("skill supersession was not preserved")
    if "desc-2" not in store.skill_state("skill-1")["descriptor_refs"]:
        raise ValueError("skill grounding edge did not update descriptor refs")
    if not missing_review_blocked:
        raise ValueError("skill graph accepted missing review provenance")

    return {
        "phase": "5",
        "verifier": "verify_phase_05_skill_graph",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "skill-runtime-importable", "result": "pass"},
            {"id": "skill-grounding-edges-supported", "result": "pass"},
            {"id": "skill-supersession-supported", "result": "pass"},
            {"id": "skill-provenance-enforced", "result": "pass"},
            {"id": "skill-load-state-roundtrip-clean", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "anchors": {
            "active_skill_ids": store.active_skill_ids(),
            "superseded_skill": store.skill_state("skill-1"),
            "replacement_skill": store.skill_state("skill-2"),
            "grounding_edge_id": edge_id,
        },
        "notes": ["skill graph stays procedural and non-automatic", "no approval implied"],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_05 skill_graph verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_05 skill_graph verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
