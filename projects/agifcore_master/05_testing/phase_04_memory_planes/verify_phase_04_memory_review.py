from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_04_memory_planes"
SLICE_ID = "slice_1"
VERIFICATION_NAME = "memory_review"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_IMPORTS = ("memory_review",)
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
REPORT_PATH = EVIDENCE_DIR / "phase_04_memory_review_report.json"


class MemoryReviewVerifierError(ValueError):
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
            "message": "Phase 4 memory review runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "memory-review-runtime-present", "result": "blocked"},
            {"id": "review-decision-state-changes-ready", "result": "blocked"},
            {"id": "tier-tracking-ready", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "notes": [
            "memory review must preserve explicit approval, rejection, and hold decisions",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, object]:
    from memory_review import MemoryReviewQueue, MemoryReviewError

    queue = MemoryReviewQueue(max_candidates=4)
    review_ref_one = queue.submit_candidate(
        candidate_id="candidate-0001",
        source_plane="working",
        target_plane="semantic",
        candidate_kind="summary",
        proposed_tier="hot",
        payload={"summary": "hot concept ready for promotion"},
        provenance_refs=["trace://phase4/review/candidate-0001"],
    )
    review_ref_two = queue.submit_candidate(
        candidate_id="candidate-0002",
        source_plane="working",
        target_plane="procedural",
        candidate_kind="procedure",
        proposed_tier="warm",
        payload={"summary": "procedure candidate"},
        provenance_refs=["trace://phase4/review/candidate-0002"],
    )
    review_ref_three = queue.submit_candidate(
        candidate_id="candidate-0003",
        source_plane="episodic",
        target_plane="continuity",
        candidate_kind="correction",
        proposed_tier="cold",
        payload={"summary": "correction candidate"},
        provenance_refs=["trace://phase4/review/candidate-0003"],
    )
    review_ref_four = queue.submit_candidate(
        candidate_id="candidate-0004",
        source_plane="continuity",
        target_plane="semantic",
        candidate_kind="retention",
        proposed_tier="ephemeral",
        payload={"summary": "ephemeral candidate"},
        provenance_refs=["trace://phase4/review/candidate-0004"],
    )

    approval = queue.decide(
        review_ref=review_ref_one,
        decision="approve",
        assigned_tier="hot",
        rationale="stable enough for reuse",
    )
    rejection = queue.decide(
        review_ref=review_ref_two,
        decision="reject",
        assigned_tier="warm",
        rationale="too procedural for current review",
    )
    hold = queue.decide(
        review_ref=review_ref_three,
        decision="hold",
        assigned_tier="cold",
        rationale="needs more evidence before promotion",
    )

    invalid_blocked = False
    try:
        queue.decide(
            review_ref=review_ref_four,
            decision="approve",
            assigned_tier="invalid-tier",
            rationale="should be blocked",
        )
    except MemoryReviewError:
        invalid_blocked = True

    exported = queue.export_state()
    clone = MemoryReviewQueue()
    clone.load_state(exported)
    approved = clone.approved_candidates(target_plane="semantic")
    tier_summary = clone.tier_summary()

    if approval["status"] != "approved" or approval["assigned_tier"] != "hot":
        raise MemoryReviewVerifierError("approval did not change candidate state correctly")
    if rejection["status"] != "rejected" or rejection["assigned_tier"] != "warm":
        raise MemoryReviewVerifierError("rejection did not change candidate state correctly")
    if hold["status"] != "held" or hold["assigned_tier"] != "cold":
        raise MemoryReviewVerifierError("hold did not change candidate state correctly")
    if not invalid_blocked:
        raise MemoryReviewVerifierError("invalid tier decision was not blocked")
    if tier_summary != {"hot": 1, "warm": 1, "cold": 1, "ephemeral": 1}:
        raise MemoryReviewVerifierError("tier summary did not track all submitted tiers")
    if len(approved) != 1 or approved[0]["candidate_id"] != "candidate-0001":
        raise MemoryReviewVerifierError("approved candidate filtering did not work")
    if clone.export_state() != exported:
        raise MemoryReviewVerifierError("memory review queue did not roundtrip cleanly")

    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "memory-review-runtime-importable", "result": "pass"},
            {"id": "approval-state-change-enforced", "result": "pass"},
            {"id": "rejection-state-change-enforced", "result": "pass"},
            {"id": "hold-state-change-enforced", "result": "pass"},
            {"id": "tier-summary-tracks-submissions", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
        },
        "runtime_symbols": {
            "memory_review": [
                "MemoryReviewQueue",
                "ReviewCandidate",
                "ReviewDecision",
                "MemoryReviewError",
                "submit_candidate",
                "decide",
                "approved_candidates",
                "tier_summary",
            ],
        },
        "anchors": {
            "review_refs": [review_ref_one, review_ref_two, review_ref_three, review_ref_four],
            "approval": approval,
            "rejection": rejection,
            "hold": hold,
            "tier_summary": tier_summary,
        },
        "notes": [
            "memory review state changes are explicit",
            "tier tracking stays visible in exported state",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(SUPPORTING_VERIFIER_FILES) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_04 slice_1 memory_review verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_04 slice_1 memory_review verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
