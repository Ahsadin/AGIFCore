from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_04_memory_planes"
SLICE_ID = "slice_3"
VERIFICATION_NAME = "forgetting_and_compression"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_PACKAGE = "agifcore_phase4_memory"
RUNTIME_IMPORTS = (
    f"{RUNTIME_PACKAGE}.compression_pipeline",
    f"{RUNTIME_PACKAGE}.forgetting_retirement",
    f"{RUNTIME_PACKAGE}.semantic_memory",
    f"{RUNTIME_PACKAGE}.procedural_memory",
    f"{RUNTIME_PACKAGE}.episodic_memory",
    f"{RUNTIME_PACKAGE}.memory_review",
    f"{RUNTIME_PACKAGE}.rollback_safe_updates",
)
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/__init__.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/compression_pipeline.py",
    "projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/forgetting_retirement.py",
)
REQUIRED_REPORTS = (
    "phase_04_working_memory_report.json",
    "phase_04_episodic_memory_report.json",
    "phase_04_continuity_memory_report.json",
    "phase_04_memory_review_report.json",
    "phase_04_rollback_safe_updates_report.json",
    "phase_04_semantic_memory_report.json",
    "phase_04_procedural_memory_report.json",
    "phase_04_corrections_and_promotion_report.json",
    "phase_04_forgetting_and_compression_report.json",
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
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_04_evidence"
REPORT_PATH = EVIDENCE_DIR / "phase_04_forgetting_and_compression_report.json"
MANIFEST_PATH = EVIDENCE_DIR / "phase_04_evidence_manifest.json"


class ForgettingCompressionVerifierError(ValueError):
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
            "message": "Phase 4 compression and forgetting or retirement runtime files are not ready yet.",
            "missing_files": missing,
        },
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "compression-runtime-present", "result": "blocked"},
            {"id": "forgetting-runtime-present", "result": "blocked"},
            {"id": "retirement-runtime-present", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "compression, forgetting, and retirement must stay explicit lifecycle effects",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, object]:
    from agifcore_phase4_memory.compression_pipeline import (
        CompressionPipeline,
        CompressionPipelineError,
    )
    from agifcore_phase4_memory.episodic_memory import EpisodicMemoryStore
    from agifcore_phase4_memory.forgetting_retirement import (
        ForgettingRetirementError,
        ForgettingRetirementManager,
    )
    from agifcore_phase4_memory.memory_review import MemoryReviewQueue
    from agifcore_phase4_memory.procedural_memory import ProceduralMemoryStore
    from agifcore_phase4_memory.semantic_memory import SemanticMemoryStore

    review = MemoryReviewQueue()

    semantic = SemanticMemoryStore()
    semantic.add_entry(
        entry_id="semantic-0001",
        concept_type="theory_fragment",
        abstraction="Long semantic explanation about bounded memory pressure and trace discipline.",
        provenance_refs=["trace://phase4/semantic/a"],
        review_ref="memory-review-prev-0001",
        source_candidate_id="candidate-prev-0001",
        supporting_refs=["support://phase4/semantic/a"],
        graph_refs=["concept-ref://memory/pressure"],
        metadata={"confidence": "high"},
    )
    semantic.add_entry(
        entry_id="semantic-0002",
        concept_type="theory_fragment",
        abstraction="Second reviewed abstraction about retention policy and evidence honesty.",
        provenance_refs=["trace://phase4/semantic/b"],
        review_ref="memory-review-prev-0002",
        source_candidate_id="candidate-prev-0002",
        supporting_refs=["support://phase4/semantic/b"],
        graph_refs=["concept-ref://memory/review"],
        metadata={"confidence": "medium"},
    )

    pending_compression_review = review.submit_candidate(
        candidate_id="compression-pending-0001",
        source_plane="semantic",
        target_plane="semantic",
        candidate_kind="semantic_compression",
        proposed_tier="cold",
        payload={"entry_ids": ["semantic-0001", "semantic-0002"]},
        provenance_refs=["trace://phase4/review/compression/pending"],
    )
    compression_review = review.submit_candidate(
        candidate_id="compression-approved-0001",
        source_plane="semantic",
        target_plane="semantic",
        candidate_kind="semantic_compression",
        proposed_tier="cold",
        payload={"entry_ids": ["semantic-0001", "semantic-0002"]},
        provenance_refs=["trace://phase4/review/compression/approved"],
    )
    review.decide(
        review_ref=compression_review,
        decision="approve",
        assigned_tier="cold",
        rationale="compress two reviewed abstractions into one retained summary",
    )

    compression = CompressionPipeline()
    try:
        compression.compress_semantic_entries(
            review_ref=pending_compression_review,
            review_queue=review,
            semantic_store=semantic,
            entry_ids=["semantic-0001", "semantic-0002"],
            summary_abstraction="This should not succeed.",
        )
        pending_compression_blocked = False
    except CompressionPipelineError:
        pending_compression_blocked = True

    compression_result = compression.compress_semantic_entries(
        review_ref=compression_review,
        review_queue=review,
        semantic_store=semantic,
        entry_ids=["semantic-0001", "semantic-0002"],
        summary_abstraction="Compressed semantic summary for bounded retention review.",
        supporting_refs=["support://phase4/semantic/compression-summary"],
        graph_refs=["concept-ref://memory/compression"],
    )
    semantic_state = semantic.export_state()
    semantic_entries = {entry["entry_id"]: entry for entry in semantic_state["entries"]}
    compressed_summary_id = compression_result["compression"]["created_id"]
    compressed_summary = semantic_entries[compressed_summary_id]

    episodic = EpisodicMemoryStore()
    episodic.append_event(
        event_id="event-0001",
        conversation_id="conv-phase4-slice3",
        turn_id="turn-0001",
        event_type="memory_observation",
        event_summary="Older episodic note about memory pressure.",
        provenance_refs=["trace://phase4/episodic/1"],
    )
    episodic.append_event(
        event_id="event-0002",
        conversation_id="conv-phase4-slice3",
        turn_id="turn-0002",
        event_type="memory_observation",
        event_summary="Older episodic note about review queue decisions.",
        provenance_refs=["trace://phase4/episodic/2"],
    )
    episodic.append_event(
        event_id="event-0003",
        conversation_id="conv-phase4-slice3",
        turn_id="turn-0003",
        event_type="memory_observation",
        event_summary="Recent episodic note that remains active.",
        provenance_refs=["trace://phase4/episodic/3"],
    )
    forgetting_review = review.submit_candidate(
        candidate_id="forgetting-approved-0001",
        source_plane="episodic",
        target_plane="episodic",
        candidate_kind="episodic_forgetting",
        proposed_tier="cold",
        payload={"event_ids": ["event-0001", "event-0002"]},
        provenance_refs=["trace://phase4/review/forgetting/approved"],
    )
    review.decide(
        review_ref=forgetting_review,
        decision="approve",
        assigned_tier="cold",
        rationale="retain one explicit forgetting summary instead of two older events",
    )

    procedural = ProceduralMemoryStore()
    procedural.add_procedure(
        procedure_id="procedure-0001",
        procedure_name="review_memory_note",
        objective="Summarize a reviewed memory note safely.",
        steps=["read reviewed note", "extract stable summary", "attach provenance"],
        preconditions=["reviewed note exists"],
        postconditions=["summary artifact exists"],
        constraints=["no execution side effects", "keep provenance attached"],
        provenance_refs=["trace://phase4/procedural/0001"],
        review_ref="memory-review-prev-0003",
        source_candidate_id="candidate-prev-0003",
        graph_refs=["skill-ref://memory/review-note"],
        metadata={"risk_band": "bounded"},
    )
    retirement_review = review.submit_candidate(
        candidate_id="retirement-approved-0001",
        source_plane="procedural",
        target_plane="procedural",
        candidate_kind="procedural_retirement",
        proposed_tier="cold",
        payload={"procedure_id": "procedure-0001"},
        provenance_refs=["trace://phase4/review/retirement/approved"],
    )
    review.decide(
        review_ref=retirement_review,
        decision="approve",
        assigned_tier="cold",
        rationale="retire the older procedure from the active set",
    )

    manager = ForgettingRetirementManager()
    forgetting_result = manager.forget_episodic_events(
        review_ref=forgetting_review,
        review_queue=review,
        episodic_store=episodic,
        event_ids=["event-0001", "event-0002"],
        summary_event_id="event-summary-0001",
        summary="Two older episodic observations were compressed into one retained summary anchor.",
        conversation_id="conv-phase4-slice3",
        turn_id="turn-0004",
        provenance_refs=["trace://phase4/episodic/summary"],
    )
    retirement_result = manager.retire_procedure(
        review_ref=retirement_review,
        review_queue=review,
        procedural_store=procedural,
        procedure_id="procedure-0001",
    )

    recent_window = episodic.recent_window(limit=3)
    remaining_event_ids = [event["event_id"] for event in recent_window]
    active_semantic_ids = semantic.active_entry_ids()
    active_procedure_ids = procedural.active_procedure_ids()

    if not pending_compression_blocked:
        raise ForgettingCompressionVerifierError("pending compression review unexpectedly succeeded")
    if active_semantic_ids != [compressed_summary_id]:
        raise ForgettingCompressionVerifierError("semantic compression did not reduce the active semantic set to one summary")
    if {"event-0001", "event-0002"} & set(remaining_event_ids):
        raise ForgettingCompressionVerifierError("forgotten episodic events still remain in the active recent window")
    if "event-summary-0001" not in remaining_event_ids:
        raise ForgettingCompressionVerifierError("forgetting summary anchor is missing")
    if active_procedure_ids:
        raise ForgettingCompressionVerifierError("retired procedure still remains active")

    return {
        "phase": "4",
        "slice": SLICE_ID,
        "verifier": f"verify_phase_04_{VERIFICATION_NAME}",
        "status": "pass",
        "checked_files": list(PLAN_REFS) + list(RUNTIME_FILES),
        "assertions": [
            {"id": "compression-runtime-importable", "result": "pass"},
            {"id": "pending-compression-review-blocked", "result": "pass"},
            {"id": "semantic-compression-retains-one-summary-anchor", "result": "pass"},
            {"id": "episodic-forgetting-uses-rollback-safe-update", "result": "pass"},
            {"id": "procedural-retirement-removes-active-entry", "result": "pass"},
        ],
        "anchors": {
            "compression_result": compression_result["compression"],
            "compressed_summary": compressed_summary,
            "semantic_active_entry_ids": active_semantic_ids,
            "forgetting_result": forgetting_result["forgetting"],
            "episodic_recent_window": recent_window,
            "retirement_result": retirement_result["retirement"],
            "procedural_state": retirement_result["procedure_state"],
        },
        "runtime_symbols": {
            "compression_pipeline": [
                "CompressionPipeline",
                "CompressionPipelineError",
                "compress_semantic_entries",
            ],
            "forgetting_retirement": [
                "ForgettingRetirementManager",
                "ForgettingRetirementError",
                "forget_episodic_events",
                "retire_procedure",
            ],
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "compression leaves one retained semantic summary anchor and supersedes the source entries",
            "forgetting removes selected episodic events only through a rollback-safe batch with a retained summary event",
            "retirement explicitly removes the reviewed procedure from the active set",
            "no approval implied",
        ],
    }


def load_report_status(filename: str) -> dict[str, str]:
    path = EVIDENCE_DIR / filename
    if not path.exists():
        return {"status": "missing", "path": rel(path)}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"status": "invalid_json", "path": rel(path)}
    status = payload.get("status")
    return {
        "status": status if isinstance(status, str) else "unknown",
        "path": rel(path),
    }


def build_evidence_manifest() -> dict[str, object]:
    reports = {filename: load_report_status(filename) for filename in REQUIRED_REPORTS}
    missing = [name for name, info in reports.items() if info["status"] == "missing"]
    invalid = [name for name, info in reports.items() if info["status"] == "invalid_json"]
    statuses = [info["status"] for info in reports.values()]
    full_pass = not missing and not invalid and all(status == "pass" for status in statuses)
    return {
        "phase": "4",
        "status": "phase_4_verifier_family_pass" if full_pass else "phase_4_verifier_family_partial",
        "reports": reports,
        "required_report_count": len(REQUIRED_REPORTS),
        "available_report_count": len(REQUIRED_REPORTS) - len(missing),
        "missing_reports": missing,
        "invalid_reports": invalid,
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "final integrated rerun and final package audit are still required before user review",
            "no approval implied",
        ],
    }


def main() -> int:
    required_paths = list(PLAN_REFS) + list(RUNTIME_FILES)
    missing = missing_files(required_paths)
    if missing or not runtime_modules_available():
        report = build_blocked_report(missing)
        dump_json(REPORT_PATH, report)
        dump_json(MANIFEST_PATH, build_evidence_manifest())
        print(f"phase_04 {SLICE_ID} {VERIFICATION_NAME} verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    manifest = build_evidence_manifest()
    dump_json(MANIFEST_PATH, manifest)
    print(f"phase_04 {SLICE_ID} {VERIFICATION_NAME} verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
