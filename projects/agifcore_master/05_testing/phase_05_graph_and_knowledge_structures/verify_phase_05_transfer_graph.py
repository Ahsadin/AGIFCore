from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_05_graph_and_knowledge_structures"
VERIFICATION_NAME = "transfer_graph"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase5_graph"
RUNTIME_IMPORTS = (
    f"{RUNTIME_PACKAGE}.transfer_graph",
    f"{RUNTIME_PACKAGE}.conflict_rules",
    f"{RUNTIME_PACKAGE}.provenance_links",
)
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md",
    "projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/__init__.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/transfer_graph.py",
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/conflict_rules.py",
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
REPORT_PATH = EVIDENCE_DIR / "phase_05_transfer_graph_report.json"


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
        "verifier": "verify_phase_05_transfer_graph",
        "status": "blocked",
        "blocker": {"kind": "missing_runtime_dependencies", "missing_files": missing},
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "transfer-runtime-present", "result": "blocked"},
            {"id": "transfer-governance-ready", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "notes": ["transfer must stay governed and below Phase 6", "no approval implied"],
    }


def build_pass_report() -> dict[str, Any]:
    from agifcore_phase5_graph.transfer_graph import TransferGraphStore

    strong_links = [
        {"role": "source_memory", "ref_id": "semantic-entry-9", "ref_kind": "semantic_entry", "source_path": "phase4/semantic"},
        {"role": "review", "ref_id": "memory-review-30", "ref_kind": "review", "source_path": "phase4/review"},
        {"role": "rollback", "ref_id": "rollback-1", "ref_kind": "rollback_ref", "source_path": "phase2/rollback"},
    ]
    weak_links = [
        {"role": "source_memory", "ref_id": "semantic-entry-10", "ref_kind": "semantic_entry", "source_path": "phase4/semantic"},
        {"role": "review", "ref_id": "memory-review-31", "ref_kind": "review", "source_path": "phase4/review"},
    ]
    store = TransferGraphStore()
    approved_id = store.record_transfer(
        transfer_id="transfer-1",
        source_graph="descriptor",
        source_id="desc-1",
        source_domain="finance_document_workflows",
        target_graph="descriptor",
        target_id="desc-target-1",
        target_domain="finance_document_workflows",
        source_status="active",
        trust_band="policy",
        source_policy_requirements=["route"],
        requested_policy_requirements=["route"],
        allowed_target_domains=["finance_document_workflows"],
        explicit_transfer_approval=False,
        provenance_links=strong_links,
        baseline_support_score=0.82,
        target_support_score=0.76,
    )
    denied_id = store.record_transfer(
        transfer_id="transfer-2",
        source_graph="descriptor",
        source_id="desc-2",
        source_domain="finance_document_workflows",
        target_graph="descriptor",
        target_id="desc-target-2",
        target_domain="claims_case_handling",
        source_status="active",
        trust_band="bounded_local",
        source_policy_requirements=["route"],
        requested_policy_requirements=["route"],
        allowed_target_domains=["claims_case_handling"],
        explicit_transfer_approval=False,
        provenance_links=strong_links,
        baseline_support_score=0.8,
        target_support_score=0.75,
    )
    abstained_id = store.record_transfer(
        transfer_id="transfer-3",
        source_graph="descriptor",
        source_id="desc-3",
        source_domain="finance_document_workflows",
        target_graph="descriptor",
        target_id="desc-target-3",
        target_domain="finance_document_workflows",
        source_status="active",
        trust_band="experimental",
        source_policy_requirements=["route"],
        requested_policy_requirements=["route"],
        allowed_target_domains=["finance_document_workflows"],
        explicit_transfer_approval=False,
        provenance_links=weak_links,
        baseline_support_score=0.2,
        target_support_score=0.1,
    )
    blocked_id = store.record_transfer(
        transfer_id="transfer-4",
        source_graph="descriptor",
        source_id="desc-4",
        source_domain="finance_document_workflows",
        target_graph="descriptor",
        target_id="desc-target-4",
        target_domain="finance_document_workflows",
        source_status="retired",
        trust_band="bounded_local",
        source_policy_requirements=["route"],
        requested_policy_requirements=["route"],
        allowed_target_domains=["finance_document_workflows"],
        explicit_transfer_approval=False,
        provenance_links=strong_links,
        baseline_support_score=0.7,
        target_support_score=0.6,
    )
    cross_domain_approved_id = store.record_transfer(
        transfer_id="transfer-5",
        source_graph="descriptor",
        source_id="desc-5",
        source_domain="finance_document_workflows",
        target_graph="descriptor",
        target_id="desc-target-5",
        target_domain="claims_case_handling",
        source_status="active",
        trust_band="policy",
        source_policy_requirements=["route"],
        requested_policy_requirements=["route"],
        allowed_target_domains=["claims_case_handling"],
        explicit_transfer_approval=True,
        provenance_links=strong_links,
        baseline_support_score=0.9,
        target_support_score=0.84,
        authority_review_ref="authority-review-5",
    )
    missing_authority_ref_id = store.record_transfer(
        transfer_id="transfer-6",
        source_graph="descriptor",
        source_id="desc-6",
        source_domain="finance_document_workflows",
        target_graph="descriptor",
        target_id="desc-target-6",
        target_domain="claims_case_handling",
        source_status="active",
        trust_band="policy",
        source_policy_requirements=["route"],
        requested_policy_requirements=["route"],
        allowed_target_domains=["claims_case_handling"],
        explicit_transfer_approval=True,
        provenance_links=strong_links,
        baseline_support_score=0.88,
        target_support_score=0.83,
    )

    exported = store.export_state()
    clone = TransferGraphStore()
    clone.load_state(exported)
    if clone.export_state() != exported:
        raise ValueError("transfer graph export did not round-trip cleanly")

    if store.transfer_state(approved_id)["decision"] != "approved":
        raise ValueError("same-domain transfer was not approved")
    if store.transfer_state(denied_id)["decision"] != "denied":
        raise ValueError("cross-domain transfer without approval was not denied")
    if store.transfer_state(abstained_id)["decision"] != "abstained":
        raise ValueError("low-quality transfer was not abstained")
    if store.transfer_state(blocked_id)["decision"] != "blocked":
        raise ValueError("retired-source transfer was not blocked")
    if store.transfer_state(cross_domain_approved_id)["decision"] != "approved":
        raise ValueError("explicitly approved cross-domain transfer was not approved")
    if store.transfer_state(cross_domain_approved_id)["authority_review_ref"] != "authority-review-5":
        raise ValueError("cross-domain approval did not retain authority review reference")
    if store.transfer_state(missing_authority_ref_id)["decision"] != "denied":
        raise ValueError("cross-domain transfer without authority review ref was not denied")

    return {
        "phase": "5",
        "verifier": "verify_phase_05_transfer_graph",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "transfer-runtime-importable", "result": "pass"},
            {"id": "same-domain-transfer-approval-supported", "result": "pass"},
            {"id": "cross-domain-explicit-approval-enforced", "result": "pass"},
            {"id": "cross-domain-authority-review-ref-enforced", "result": "pass"},
            {"id": "low-quality-transfer-abstains", "result": "pass"},
            {"id": "retired-source-transfer-blocked", "result": "pass"},
            {"id": "transfer-load-state-roundtrip-clean", "result": "pass"},
            {"id": "cross-domain-authority-review-retained", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "anchors": {
            "active_transfer_ids": store.active_link_ids(),
            "approved_transfer": store.transfer_state(approved_id),
            "denied_transfer": store.transfer_state(denied_id),
            "abstained_transfer": store.transfer_state(abstained_id),
            "blocked_transfer": store.transfer_state(blocked_id),
            "cross_domain_approved_transfer": store.transfer_state(cross_domain_approved_id),
            "missing_authority_ref_transfer": store.transfer_state(missing_authority_ref_id),
        },
        "notes": ["transfer stays governed and read-only", "no approval implied"],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_05 transfer_graph verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_05 transfer_graph verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
