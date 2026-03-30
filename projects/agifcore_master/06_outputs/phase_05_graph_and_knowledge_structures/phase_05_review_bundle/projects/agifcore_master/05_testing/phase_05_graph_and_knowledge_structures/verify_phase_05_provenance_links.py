from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_05_graph_and_knowledge_structures"
VERIFICATION_NAME = "provenance_links"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase5_graph"
RUNTIME_IMPORTS = (f"{RUNTIME_PACKAGE}.provenance_links",)
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/__init__.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/provenance_links.py",
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
REPORT_PATH = EVIDENCE_DIR / "phase_05_provenance_links_report.json"


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
        "verifier": "verify_phase_05_provenance_links",
        "status": "blocked",
        "blocker": {"kind": "missing_runtime_dependencies", "missing_files": missing},
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "provenance-runtime-present", "result": "blocked"},
            {"id": "provenance-enforcement-ready", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "notes": ["provenance must be machine-checkable", "no approval implied"],
    }


def build_pass_report() -> dict[str, Any]:
    from agifcore_phase5_graph.provenance_links import (
        MAX_PROVENANCE_LINKS,
        ProvenanceLinksError,
        build_provenance_bundle,
        bundle_from_dict,
        provenance_score,
        require_roles,
    )

    links = [
        {"role": "source_memory", "ref_id": "semantic-entry-12", "ref_kind": "semantic_entry", "source_path": "phase4/semantic"},
        {"role": "review", "ref_id": "memory-review-40", "ref_kind": "review", "source_path": "phase4/review"},
        {"role": "rollback", "ref_id": "rollback-40", "ref_kind": "rollback_ref", "source_path": "phase2/rollback"},
        {"role": "workspace", "ref_id": "workspace-40", "ref_kind": "workspace_ref", "source_path": "phase2/workspace"},
    ]
    bundle = build_provenance_bundle(
        entity_kind="descriptor",
        entity_id="desc-1",
        origin_kind="inherited",
        links=links,
        inherited_from=["agif_fabric_v1"],
    )
    cloned = bundle_from_dict(bundle.to_dict())
    require_roles(bundle, ("source_memory", "review"))
    tampered_payload = bundle.to_dict()
    tampered_payload["provenance_hash"] = "tampered"

    try:
        require_roles(bundle_from_dict({"entity_kind": "descriptor", "entity_id": "bad-1", "origin_kind": "constructed", "links": [links[0]], "inherited_from": []}), ("source_memory", "review"))
        missing_role_blocked = False
    except ProvenanceLinksError:
        missing_role_blocked = True

    try:
        bundle_from_dict(tampered_payload)
        tampered_hash_blocked = False
    except ProvenanceLinksError:
        tampered_hash_blocked = True

    too_many_links = [
        {"role": "artifact" if i % 2 else "source", "ref_id": f"ref-{i}", "ref_kind": "artifact_ref", "source_path": "phaseX"}
        for i in range(MAX_PROVENANCE_LINKS + 1)
    ]
    too_many_links[0] = links[0]
    too_many_links[1] = links[1]
    try:
        build_provenance_bundle(
            entity_kind="descriptor",
            entity_id="bad-2",
            origin_kind="constructed",
            links=too_many_links,
        )
        fanout_blocked = False
    except ProvenanceLinksError:
        fanout_blocked = True

    if cloned.to_dict() != bundle.to_dict():
        raise ValueError("provenance bundle did not round-trip cleanly")
    if provenance_score(bundle) < 0.8:
        raise ValueError("provenance scoring did not reflect review and rollback anchors")
    if not missing_role_blocked:
        raise ValueError("missing review role was not blocked")
    if not tampered_hash_blocked:
        raise ValueError("tampered provenance hash was not blocked")
    if not fanout_blocked:
        raise ValueError("provenance fanout ceiling was not enforced")

    return {
        "phase": "5",
        "verifier": "verify_phase_05_provenance_links",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "provenance-runtime-importable", "result": "pass"},
            {"id": "required-roles-enforced", "result": "pass"},
            {"id": "provenance-score-reflects-review-and-rollback", "result": "pass"},
            {"id": "provenance-fanout-ceiling-enforced", "result": "pass"},
            {"id": "provenance-hash-tampering-blocked", "result": "pass"},
            {"id": "provenance-roundtrip-clean", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "anchors": {
            "provenance_hash": bundle.provenance_hash,
            "score": provenance_score(bundle),
            "link_count": len(bundle.links),
        },
        "notes": ["provenance links are enforced structures, not labels", "no approval implied"],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_05 provenance_links verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_05 provenance_links verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
