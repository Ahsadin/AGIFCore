from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE = "7"
PHASE_NAME = "phase_07_conversation_core"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
TEST_ROOT_NAME = "05_testing"
RUNTIME_PACKAGE = "agifcore_phase7_conversation"
PHASE_04_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_04_memory_planes"
PHASE_05_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures"
PHASE_06_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator"
PHASE_07_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_07_conversation_core"
PHASE_06_TEST_COMMON = "projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/_phase_06_verifier_common.py"
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/01_plan/DEMO_PROTOCOL.md",
    "projects/agifcore_master/03_design/CONVERSATION_MODEL.md",
    "projects/agifcore_master/03_design/GOVERNANCE_MODEL.md",
    "projects/agifcore_master/03_design/MEMORY_MODEL.md",
    "projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md",
    "projects/agifcore_master/03_design/SIMULATOR_MODEL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/__init__.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/raw_text_intake.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/question_interpretation.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/support_state_logic.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/self_knowledge_surface.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/clarification.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/utterance_planner.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/surface_realizer.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/answer_contract.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/anti_generic_filler.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/conversation_turn.py",
)
REQUIRED_REPORT_FILES = (
    "phase_07_raw_text_intake_report.json",
    "phase_07_question_interpretation_report.json",
    "phase_07_support_state_logic_report.json",
    "phase_07_self_knowledge_surface_report.json",
    "phase_07_clarification_report.json",
    "phase_07_utterance_planner_and_surface_realizer_report.json",
    "phase_07_answer_contract_report.json",
    "phase_07_anti_generic_filler_report.json",
)
EXPECTED_REPORT_VERIFIERS = {
    "phase_07_raw_text_intake_report.json": "verify_phase_07_raw_text_intake",
    "phase_07_question_interpretation_report.json": "verify_phase_07_question_interpretation",
    "phase_07_support_state_logic_report.json": "verify_phase_07_support_state_logic",
    "phase_07_self_knowledge_surface_report.json": "verify_phase_07_self_knowledge_surface",
    "phase_07_clarification_report.json": "verify_phase_07_clarification",
    "phase_07_utterance_planner_and_surface_realizer_report.json": "verify_phase_07_utterance_planner_and_surface_realizer",
    "phase_07_answer_contract_report.json": "verify_phase_07_answer_contract",
    "phase_07_anti_generic_filler_report.json": "verify_phase_07_anti_generic_filler",
}


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
TEST_ROOT = PROJECT_ROOT / TEST_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_07_evidence"
DEMO_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_07_demo_bundle"
MANIFEST_PATH = EVIDENCE_DIR / "phase_07_evidence_manifest.json"


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_path() -> None:
    runtime_roots = (
        REPO_ROOT / PHASE_04_RUNTIME_PARENT,
        REPO_ROOT / PHASE_05_RUNTIME_PARENT,
        REPO_ROOT / PHASE_06_RUNTIME_PARENT,
        REPO_ROOT / PHASE_07_RUNTIME_PARENT,
    )
    for root in runtime_roots:
        runtime_path = str(root)
        if runtime_path not in sys.path:
            sys.path.insert(0, runtime_path)


ensure_runtime_import_path()


def _load_phase6_common() -> Any:
    module_path = REPO_ROOT / PHASE_06_TEST_COMMON
    spec = importlib.util.spec_from_file_location("phase6_verifier_common", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load Phase 6 verifier common module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PHASE6_VC = _load_phase6_common()


def dump_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[str]) -> list[str]:
    return [path for path in paths if not (REPO_ROOT / path).exists()]


def runtime_modules_available(module_names: tuple[str, ...]) -> bool:
    try:
        for module_name in module_names:
            importlib.import_module(module_name)
    except Exception:
        return False
    return True


def report_dependency_failures(required_reports: tuple[str, ...]) -> list[str]:
    failures: list[str] = []
    for filename in required_reports:
        report_path = EVIDENCE_DIR / filename
        if not report_path.exists():
            failures.append(filename)
            continue
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        if payload.get("status") != "pass":
            failures.append(filename)
    return failures


def build_blocked_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertion_ids: list[str],
    blocker_kind: str,
    blocker_message: str,
    missing: list[str] | None = None,
    dependency_reports: list[str] | None = None,
) -> dict[str, Any]:
    blocker: dict[str, Any] = {"kind": blocker_kind, "message": blocker_message}
    if missing:
        blocker["missing_files"] = missing
    if dependency_reports:
        blocker["dependency_reports"] = dependency_reports
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "blocked",
        "blocker": blocker,
        "checked_files": checked_files,
        "assertions": [{"id": assertion_id, "result": "blocked"} for assertion_id in assertion_ids],
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "notes": ["Phase 7 remains open", "no approval implied"],
    }


def build_pass_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertions: list[dict[str, Any]],
    anchors: Mapping[str, Any],
    notes: list[str],
) -> dict[str, Any]:
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "pass",
        "checked_files": checked_files,
        "assertions": assertions,
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "anchors": dict(anchors),
        "notes": [*notes, "Phase 7 remains open", "no approval implied"],
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
        if payload.get("phase") != PHASE:
            invalid_reports.append(filename)
        if payload.get("verifier") != EXPECTED_REPORT_VERIFIERS[filename]:
            invalid_reports.append(filename)
        if payload.get("outputs", {}).get("report") != rel(report_path):
            invalid_reports.append(filename)
        assertions = payload.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            invalid_reports.append(filename)
        reports.append(
            {
                "report_id": filename.removeprefix("phase_07_").removesuffix("_report.json"),
                "path": rel(report_path),
                "status": status,
            }
        )
    invalid_reports = sorted(set(invalid_reports))
    overall_pass = (
        not missing_reports
        and not invalid_reports
        and len(reports) == len(REQUIRED_REPORT_FILES)
        and all(report["status"] == "pass" for report in reports)
    )
    manifest = {
        "phase": PHASE,
        "phase_remains_open": True,
        "required_report_count": len(REQUIRED_REPORT_FILES),
        "available_report_count": len(reports),
        "missing_reports": missing_reports,
        "invalid_reports": invalid_reports,
        "reports": reports,
        "status": "phase_7_verifier_family_pass" if overall_pass else "phase_7_verifier_family_incomplete",
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 7 remains open",
            "manifest is rebuilt from actual report files on disk",
            "no approval implied",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def build_memory_review_state() -> dict[str, Any]:
    from agifcore_phase4_memory.memory_review import MemoryReviewQueue

    queue = MemoryReviewQueue()
    review_ref = queue.submit_candidate(
        candidate_id="phase7-turn-1",
        source_plane="working",
        target_plane="continuity",
        candidate_kind="conversation_turn",
        proposed_tier="warm",
        payload={"turn_id": "turn-1", "phase": "7"},
        provenance_refs=["turn://conv-1/turn-1", "phase7/demo"],
    )
    queue.decide(
        review_ref=review_ref,
        decision="approve",
        assigned_tier="warm",
        rationale="phase7 verifier fixture review",
        reviewer="phase-07-reviewer",
    )
    return queue.export_state()


def extend_continuity_state(base_state: dict[str, Any], memory_review_ref: str) -> dict[str, Any]:
    from agifcore_phase4_memory.continuity_memory import ContinuityMemoryStore

    store = ContinuityMemoryStore()
    store.load_state(base_state)
    store.record_anchor(
        anchor_id="phase7-self-capability-1",
        subject="agifcore_local_runtime",
        continuity_kind="self_capability",
        statement="I can answer only from this local AGIFCore workspace and the approved Phase 4 to 6 exports.",
        provenance_refs=[memory_review_ref],
    )
    store.record_anchor(
        anchor_id="phase7-self-limit-1",
        subject="agifcore_local_runtime",
        continuity_kind="self_limit",
        statement="I do not perform live external search inside Phase 7.",
        provenance_refs=[memory_review_ref],
    )
    store.record_anchor(
        anchor_id="phase7-self-status-1",
        subject="agifcore_local_runtime",
        continuity_kind="self_status",
        statement="Phase 7 remains open during verifier and demo runs.",
        provenance_refs=[memory_review_ref],
    )
    return store.export_state()


def build_conversation_fixture(
    *,
    raw_text: str,
    conversation_id: str = "conv-1",
    turn_id: str = "turn-1",
    active_context_refs: list[str] | None = None,
    support_selection_result_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from agifcore_phase7_conversation.conversation_turn import ConversationTurnEngine

    base = PHASE6_VC.build_fixture_chain()
    memory_review_state = build_memory_review_state()
    review_ref = memory_review_state["candidates"][0]["review_ref"]
    continuity_memory_state = extend_continuity_state(base["continuity_memory_state"], review_ref)

    engine = ConversationTurnEngine()
    turn = engine.run_turn(
        conversation_id=conversation_id,
        turn_id=turn_id,
        raw_text=raw_text,
        continuity_memory_state=continuity_memory_state,
        working_memory_state=base["working_memory_state"],
        memory_review_state=memory_review_state,
        support_selection_result=support_selection_result_override or base["support_selection_result"],
        world_model_state=base["world_model_snapshot"].to_dict(),
        what_if_simulation_state=base["what_if_simulation_snapshot"].to_dict(),
        conflict_lane_state=base["conflict_lane_snapshot"].to_dict(),
        usefulness_state=base["usefulness_snapshot"].to_dict(),
        active_context_refs=active_context_refs or ["phase7/demo", f"turn://{conversation_id}/{turn_id}"],
    )
    return {
        **base,
        "memory_review_state": memory_review_state,
        "continuity_memory_state": continuity_memory_state,
        "conversation_turn_snapshot": turn,
    }
