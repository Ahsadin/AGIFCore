from __future__ import annotations

import importlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

PHASE = "11"
PHASE_NAME = "phase_11_governed_self_improvement"
OUTPUT_ROOT_NAME = "06_outputs"
RUNTIME_PACKAGE = "agifcore_phase11_self_improvement"
PHASE_11_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_11_governed_self_improvement"
PHASE_10_TEST_PARENT = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique"
PHASE_10_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique"
PHASE_09_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition"
PHASE_08_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness"
PHASE_07_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_07_conversation_core"

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_11_GOVERNED_SELF_IMPROVEMENT.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/01_plan/DEMO_PROTOCOL.md",
)

CONTRACT_REFS = (
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/contracts.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/meta_cognition_turn.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/science_world_turn.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/contracts.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/rich_expression_turn.py",
)

RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/contracts.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/offline_reflection_and_consolidation.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/idle_reflection.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/proposal_generation.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/self_experiment_lab.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/shadow_evaluation.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/before_after_measurement.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/adoption_or_rejection_pipeline.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/post_adoption_monitoring.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/rollback_proof.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/thought_episodes.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/self_initiated_inquiry_engine.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/self_improvement_cycle.py",
)

COMMON_TEST_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/_phase_11_verifier_common.py"

REQUIRED_REPORT_FILES = (
    "phase_11_offline_reflection_and_consolidation_report.json",
    "phase_11_idle_reflection_report.json",
    "phase_11_proposal_generation_report.json",
    "phase_11_self_experiment_lab_report.json",
    "phase_11_shadow_evaluation_report.json",
    "phase_11_before_after_measurement_report.json",
    "phase_11_adoption_or_rejection_pipeline_report.json",
    "phase_11_post_adoption_monitoring_report.json",
    "phase_11_rollback_proof_report.json",
    "phase_11_thought_episodes_report.json",
    "phase_11_self_initiated_inquiry_engine_report.json",
    "phase_11_self_improvement_cycle_report.json",
)

EXPECTED_REPORT_VERIFIERS = {
    "phase_11_offline_reflection_and_consolidation_report.json": "verify_phase_11_offline_reflection_and_consolidation",
    "phase_11_idle_reflection_report.json": "verify_phase_11_idle_reflection",
    "phase_11_proposal_generation_report.json": "verify_phase_11_proposal_generation",
    "phase_11_self_experiment_lab_report.json": "verify_phase_11_self_experiment_lab",
    "phase_11_shadow_evaluation_report.json": "verify_phase_11_shadow_evaluation",
    "phase_11_before_after_measurement_report.json": "verify_phase_11_before_after_measurement",
    "phase_11_adoption_or_rejection_pipeline_report.json": "verify_phase_11_adoption_or_rejection_pipeline",
    "phase_11_post_adoption_monitoring_report.json": "verify_phase_11_post_adoption_monitoring",
    "phase_11_rollback_proof_report.json": "verify_phase_11_rollback_proof",
    "phase_11_thought_episodes_report.json": "verify_phase_11_thought_episodes",
    "phase_11_self_initiated_inquiry_engine_report.json": "verify_phase_11_self_initiated_inquiry_engine",
    "phase_11_self_improvement_cycle_report.json": "verify_phase_11_self_improvement_cycle",
}


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
TEST_ROOT = PROJECT_ROOT / "05_testing" / PHASE_NAME
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_11_evidence"
DEMO_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_11_demo_bundle"
MANIFEST_PATH = EVIDENCE_DIR / "phase_11_evidence_manifest.json"


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_paths() -> None:
    for runtime_parent in (
        REPO_ROOT / PHASE_11_RUNTIME_PARENT,
        REPO_ROOT / PHASE_10_TEST_PARENT,
        REPO_ROOT / PHASE_10_RUNTIME_PARENT,
        REPO_ROOT / PHASE_09_RUNTIME_PARENT,
        REPO_ROOT / PHASE_08_RUNTIME_PARENT,
        REPO_ROOT / PHASE_07_RUNTIME_PARENT,
    ):
        runtime_str = str(runtime_parent)
        if runtime_str not in sys.path:
            sys.path.insert(0, runtime_str)


ensure_runtime_import_paths()

import _phase_10_verifier_common as p10c
from agifcore_phase11_self_improvement.contracts import canonical_size_bytes, stable_hash_payload
from agifcore_phase11_self_improvement.self_improvement_cycle import SelfImprovementCycleEngine


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


def dedupe_paths(paths: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        result.append(path)
    return result


def checked_files_for(verifier_file: str) -> list[str]:
    return dedupe_paths([*PLAN_REFS, *CONTRACT_REFS, *RUNTIME_FILES, COMMON_TEST_FILE, verifier_file])


def build_blocked_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertion_ids: list[str],
    blocker_kind: str,
    blocker_message: str,
    missing: list[str] | None = None,
) -> dict[str, Any]:
    blocker: dict[str, Any] = {"kind": blocker_kind, "message": blocker_message}
    if missing:
        blocker["missing_files"] = missing
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "blocked",
        "blocker": blocker,
        "checked_files": checked_files,
        "assertions": [{"id": item, "result": "blocked"} for item in assertion_ids],
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "notes": ["Phase 11 remains open", "no approval implied"],
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
        "notes": [*notes, "Phase 11 remains open", "no approval implied"],
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
        reports.append(
            {
                "report_id": filename.removeprefix("phase_11_").removesuffix("_report.json"),
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
        "status": "phase_11_verifier_family_pass" if overall_pass else "phase_11_verifier_family_incomplete",
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 11 remains open",
            "manifest is rebuilt from actual report files on disk",
            "no approval implied",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def write_report(report_path: Path, payload: Mapping[str, Any]) -> None:
    dump_json(report_path, payload)
    refresh_evidence_manifest()


def assert_inputs_unchanged(before: Any, after: Any, field_name: str) -> None:
    if before != after:
        raise AssertionError(f"{field_name} mutated during verification")


def run_phase11_cycle(*, scenario: str) -> dict[str, Any]:
    result = p10c.run_phase10_turn(scenario=scenario)
    phase10_turn_state = result["turn"].to_dict()
    before = deepcopy(phase10_turn_state)
    cycle = SelfImprovementCycleEngine().run_cycle(phase10_turn_state=phase10_turn_state)
    assert_inputs_unchanged(before, phase10_turn_state, f"phase11 {scenario} phase10_turn_state")
    return {"fixture": result["fixture"], "phase10_turn": phase10_turn_state, "cycle": cycle}


def write_demo_payload(*, filename: str, payload: Mapping[str, Any]) -> Path:
    path = DEMO_DIR / filename
    dump_json(path, payload)
    return path


def write_demo_markdown(*, filename: str, lines: list[str]) -> Path:
    path = DEMO_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def build_demo_index() -> None:
    index_json = {
        "phase": PHASE,
        "status": "open",
        "scenario_files": [
            "phase_11_self_improvement_demo.json",
            "phase_11_rollback_demo.json",
            "phase_11_bounded_self_initiated_inquiry_demo.json",
        ],
        "supporting_evidence_manifest": "phase_11_evidence_manifest.json",
        "notes": [
            "summary only",
            "Phase 11 remains open",
            "no approval implied",
        ],
    }
    write_demo_payload(filename="phase_11_demo_index.json", payload=index_json)
    write_demo_markdown(
        filename="phase_11_demo_index.md",
        lines=[
            "# Phase 11 Demo Index",
            "",
            "Phase 11 remains `open`. This bundle is for inspection only and does not imply approval or finality.",
            "",
            "Demo scenarios:",
            "",
            "- `phase_11_self_improvement_demo.md` for the bounded proposal, experiment, adoption, and monitoring path.",
            "- `phase_11_rollback_demo.md` for the rollback roundtrip proof path.",
            "- `phase_11_bounded_self_initiated_inquiry_demo.md` for the bounded inquiry path.",
            "",
            "Supporting demo payloads:",
            "",
            "- `phase_11_self_improvement_demo.json`",
            "- `phase_11_rollback_demo.json`",
            "- `phase_11_bounded_self_initiated_inquiry_demo.json`",
            "",
            "Evidence source:",
            "",
            f"- [{MANIFEST_PATH.name}]({MANIFEST_PATH})",
            "",
            "Truth note:",
            "",
            "- the bundle is local-file inspectable only",
            "- no approval language is used",
        ],
    )
