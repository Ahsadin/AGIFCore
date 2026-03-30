from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_04_memory_planes"
SLICE_ID = "slice_2"
VERIFICATION_NAME = "corrections_and_promotion"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase4_memory"
RUNTIME_IMPORTS = (
    f"{RUNTIME_PACKAGE}.working_memory",
    f"{RUNTIME_PACKAGE}.memory_review",
    f"{RUNTIME_PACKAGE}.semantic_memory",
    f"{RUNTIME_PACKAGE}.procedural_memory",
    f"{RUNTIME_PACKAGE}.promotion_pipeline",
    f"{RUNTIME_PACKAGE}.correction_handling",
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
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/semantic_memory.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/procedural_memory.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/promotion_pipeline.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/correction_handling.py",
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
REPORT_PATH = EVIDENCE_DIR / "phase_04_corrections_and_promotion_report.json"


class CorrectionsPromotionVerifierError(ValueError):
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
            "message": "Phase 4 correction and promotion runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "promotion-runtime-present", "result": "blocked"},
            {"id": "review-gated-promotion-ready", "result": "blocked"},
            {"id": "rollback-safe-correction-ready", "result": "blocked"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "notes": ["promotion and correction must stay explicit", "no approval implied"],
    }


def build_pass_report() -> dict[str, object]:
    from agifcore_phase4_memory.correction_handling import CorrectionHandler
    from agifcore_phase4_memory.continuity_memory import ContinuityMemoryStore
    from agifcore_phase4_memory.episodic_memory import EpisodicMemoryStore
    from agifcore_phase4_memory.memory_review import MemoryReviewQueue
    from agifcore_phase4_memory.procedural_memory import ProceduralMemoryStore
    from agifcore_phase4_memory.promotion_pipeline import (
        PromotionPipeline,
        PromotionPipelineError,
    )
    from agifcore_phase4_memory.semantic_memory import SemanticMemoryStore
    from agifcore_phase4_memory.working_memory import WorkingMemoryStore

    working = WorkingMemoryStore()
    turn_ref = working.bind_turn(
        conversation_id="conv-phase4-slice2",
        turn_id="turn-0001",
        task_id="phase4-slice2",
        support_refs=["ctx://phase4/slice2"],
    )
    working.add_candidate(
        candidate_id="candidate-semantic",
        candidate_kind="theory_fragment",
        target_plane="semantic",
        payload={"summary": "semantic abstraction", "supporting_refs": ["support://phase4/semantic"]},
        provenance_refs=[turn_ref],
    )
    working.add_candidate(
        candidate_id="candidate-procedural",
        candidate_kind="procedure",
        target_plane="procedural",
        payload={
            "procedure_name": "memory_note_review",
            "objective": "review a memory note",
            "steps": ["open note", "extract abstraction", "attach provenance"],
            "preconditions": ["memory note exists"],
            "postconditions": ["review summary exists"],
            "constraints": ["no execution side effects"],
        },
        provenance_refs=[turn_ref],
    )

    review = MemoryReviewQueue()
    pending_review_ref = review.submit_candidate(
        candidate_id="candidate-semantic",
        source_plane="working",
        target_plane="semantic",
        candidate_kind="theory_fragment",
        proposed_tier="hot",
        payload={"summary": "semantic abstraction"},
        provenance_refs=[turn_ref],
    )
    semantic_review_ref = review.submit_candidate(
        candidate_id="candidate-semantic",
        source_plane="working",
        target_plane="semantic",
        candidate_kind="theory_fragment",
        proposed_tier="hot",
        payload={"summary": "semantic abstraction"},
        provenance_refs=[turn_ref],
    )
    procedural_review_ref = review.submit_candidate(
        candidate_id="candidate-procedural",
        source_plane="working",
        target_plane="procedural",
        candidate_kind="procedure",
        proposed_tier="warm",
        payload={"procedure_name": "memory_note_review"},
        provenance_refs=[turn_ref],
    )
    review.decide(
        review_ref=semantic_review_ref,
        decision="approve",
        assigned_tier="warm",
        rationale="stable abstraction",
    )
    review.decide(
        review_ref=procedural_review_ref,
        decision="approve",
        assigned_tier="warm",
        rationale="useful reusable procedure",
    )

    semantic = SemanticMemoryStore()
    procedural = ProceduralMemoryStore()
    continuity = ContinuityMemoryStore()
    promotion = PromotionPipeline()

    try:
        promotion.promote_review_candidate(
            review_candidate={
                "review_ref": pending_review_ref,
                "target_plane": "semantic",
                "status": "pending",
            },
            source_candidate=working.consume_candidate("candidate-semantic"),
            semantic_store=semantic,
        )
        pending_blocked = False
    except PromotionPipelineError:
        pending_blocked = True

    # Recreate the semantic candidate because the negative check consumed it.
    working.add_candidate(
        candidate_id="candidate-semantic-approved",
        candidate_kind="theory_fragment",
        target_plane="semantic",
        payload={"summary": "semantic abstraction", "supporting_refs": ["support://phase4/semantic"]},
        provenance_refs=[turn_ref],
    )
    semantic_promotion = promotion.promote_review_candidate(
        review_candidate=review.approved_candidates(target_plane="semantic")[0],
        source_candidate=working.consume_candidate("candidate-semantic-approved"),
        semantic_store=semantic,
    )
    procedural_promotion = promotion.promote_review_candidate(
        review_candidate=review.approved_candidates(target_plane="procedural")[0],
        source_candidate=working.consume_candidate("candidate-procedural"),
        procedural_store=procedural,
    )

    episodic = EpisodicMemoryStore()
    episodic.append_event(
        event_id="event-0001",
        conversation_id="conv-phase4-slice2",
        turn_id="turn-0001",
        event_type="semantic_candidate_promoted",
        event_summary="first semantic abstraction was promoted",
        provenance_refs=[turn_ref],
    )
    correction = CorrectionHandler()
    correction_result = correction.apply_correction(
        correction_id="correction-0001",
        conversation_id="conv-phase4-slice2",
        turn_id="turn-0001",
        event_id="event-0001",
        reason="refine semantic abstraction",
        target_plane="semantic",
        target_id=semantic_promotion["created_id"],
        corrected_payload={"abstraction": "refined semantic abstraction"},
        episodic_store=episodic,
        semantic_store=semantic,
    )

    if not pending_blocked:
        raise CorrectionsPromotionVerifierError("promotion accepted a pending review candidate")
    if semantic_promotion["target_plane"] != "semantic":
        raise CorrectionsPromotionVerifierError("semantic promotion did not target semantic memory")
    if procedural_promotion["target_plane"] != "procedural":
        raise CorrectionsPromotionVerifierError("procedural promotion did not target procedural memory")
    if correction_result["correction"]["rollback_ref"] == "":
        raise CorrectionsPromotionVerifierError("correction did not preserve rollback information")
    replacement_id = correction_result["correction"]["replacement_id"]
    if replacement_id not in semantic.active_entry_ids():
        raise CorrectionsPromotionVerifierError("correction did not create an active replacement semantic entry")
    if semantic.entry_state(semantic_promotion["created_id"])["status"] != "superseded":
        raise CorrectionsPromotionVerifierError("correction did not supersede the original semantic entry")
    if episodic.recent_window(limit=1)[0]["correction_status"] != "corrected":
        raise CorrectionsPromotionVerifierError("episodic correction marker was not applied")

    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "promotion-runtime-importable", "result": "pass"},
            {"id": "pending-review-promotion-blocked", "result": "pass"},
            {"id": "approved-review-promotion-routes-correctly", "result": "pass"},
            {"id": "semantic-correction-is-rollback-safe", "result": "pass"},
            {"id": "episodic-correction-marker-preserved", "result": "pass"},
        ],
        "outputs": {"report": rel(REPORT_PATH)},
        "runtime_symbols": {
            "promotion_pipeline": [
                "PromotionPipeline",
                "PromotionPipelineError",
                "promote_review_candidate",
            ],
            "correction_handling": [
                "CorrectionHandler",
                "CorrectionHandlingError",
                "apply_correction",
            ],
        },
        "anchors": {
            "semantic_promotion": semantic_promotion,
            "procedural_promotion": procedural_promotion,
            "correction_result": correction_result["correction"],
            "semantic_active_entry_ids": semantic.active_entry_ids(),
            "procedural_active_procedure_ids": procedural.active_procedure_ids(),
            "episodic_recent_window": episodic.recent_window(limit=1),
        },
        "notes": [
            "promotion remains review-gated",
            "correction remains explicit, rollback-safe, and semantic-state visible",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(list(PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        print("phase_04 slice_2 corrections_and_promotion verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    print("phase_04 slice_2 corrections_and_promotion verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
