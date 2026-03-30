from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_05_graph_and_knowledge_structures"
VERIFICATION_NAME = "conflict_and_supersession"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase5_graph"
RUNTIME_IMPORTS = (f"{RUNTIME_PACKAGE}.conflict_rules", f"{RUNTIME_PACKAGE}.supersession_rules")
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/conflict_rules.py",
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
REPORT_PATH = EVIDENCE_DIR / "phase_05_conflict_and_supersession_report.json"


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
        "verifier": "verify_phase_05_conflict_and_supersession",
        "status": "blocked",
        "blocker": {"kind": "missing_runtime_dependencies", "missing_files": missing},
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "conflict-runtime-present", "result": "blocked"},
            {"id": "supersession-runtime-present", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "notes": ["conflict and supersession must be real runtime rules", "no approval implied"],
    }


def build_pass_report() -> dict[str, Any]:
    from agifcore_phase5_graph.conflict_rules import ConflictCandidate, ConflictRuleEngine
    from agifcore_phase5_graph.supersession_rules import SupersessionLedger, SupersessionRulesError

    engine = ConflictRuleEngine()
    clear = engine.evaluate_candidates(
        candidates=[
            ConflictCandidate(candidate_id="cand-a", active=True, trust_band="policy", provenance_score=0.9, utility_score=0.9, policy_requirements_met=True),
            ConflictCandidate(candidate_id="cand-b", active=True, trust_band="bounded_local", provenance_score=0.7, utility_score=0.6, policy_requirements_met=True),
        ],
        requested_domain=None,
    )
    defer = engine.evaluate_candidates(
        candidates=[
            ConflictCandidate(candidate_id="cand-c", active=True, trust_band="bounded_local", provenance_score=0.7, utility_score=0.61, policy_requirements_met=True),
            ConflictCandidate(candidate_id="cand-d", active=True, trust_band="bounded_local", provenance_score=0.71, utility_score=0.6, policy_requirements_met=True),
        ],
        requested_domain=None,
    )
    blocked = engine.evaluate_candidates(
        candidates=[
            ConflictCandidate(candidate_id="cand-e", active=False, trust_band="unknown", provenance_score=0.5, utility_score=0.5, policy_requirements_met=False, retired=True),
        ],
        requested_domain="finance_document_workflows",
    )

    ledger = SupersessionLedger()
    ledger.register(entity_kind="descriptor", predecessor_id="desc-1", successor_id="desc-2", review_ref="review-1")
    ledger.register(entity_kind="descriptor", predecessor_id="desc-2", successor_id="desc-3", review_ref="review-2")
    ledger.register(entity_kind="descriptor", predecessor_id="desc-3", successor_id="desc-4", review_ref="review-3")
    ledger.register(entity_kind="descriptor", predecessor_id="desc-4", successor_id="desc-5", review_ref="review-4")
    try:
        ledger.register(entity_kind="descriptor", predecessor_id="desc-5", successor_id="desc-6", review_ref="review-5")
        chain_limit_enforced = False
    except SupersessionRulesError:
        chain_limit_enforced = True

    if clear.status != "clear" or clear.chosen_candidate_id != "cand-a":
        raise ValueError("conflict clear path failed")
    if defer.status != "defer":
        raise ValueError("conflict defer path failed")
    if blocked.status != "blocked":
        raise ValueError("conflict blocked path failed")
    if ledger.active_id("desc-1") != "desc-5":
        raise ValueError("supersession active resolution failed")
    if not chain_limit_enforced:
        raise ValueError("supersession chain-length ceiling was not enforced")

    return {
        "phase": "5",
        "verifier": "verify_phase_05_conflict_and_supersession",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "conflict-clear-path-supported", "result": "pass"},
            {"id": "conflict-defer-path-supported", "result": "pass"},
            {"id": "conflict-blocked-path-supported", "result": "pass"},
            {"id": "supersession-active-resolution-supported", "result": "pass"},
            {"id": "supersession-chain-ceiling-enforced", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "anchors": {
            "clear_decision": clear.to_dict(),
            "defer_decision": defer.to_dict(),
            "blocked_decision": blocked.to_dict(),
            "supersession_chain": ledger.predecessor_chain("desc-1"),
        },
        "notes": ["conflict and supersession are runtime behavior, not prose", "no approval implied"],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_05 conflict_and_supersession verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_05 conflict_and_supersession verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
