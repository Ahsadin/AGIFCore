from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE = "8"
PHASE_NAME = "phase_08_science_and_world_awareness"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
TEST_ROOT_NAME = "05_testing"
RUNTIME_PACKAGE = "agifcore_phase8_science_world_awareness"
PHASE_08_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness"
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/01_plan/DEMO_PROTOCOL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/__init__.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/scientific_priors.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/entity_request_inference.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/world_region_selection.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/causal_chain_reasoning.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/bounded_current_world_reasoning.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/visible_reasoning_summaries.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/science_reflection.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/science_world_turn.py",
)
REQUIRED_REPORT_FILES = (
    "phase_08_scientific_priors_report.json",
    "phase_08_entity_request_inference_report.json",
    "phase_08_world_region_selection_report.json",
    "phase_08_causal_chain_reasoning_report.json",
    "phase_08_bounded_current_world_reasoning_report.json",
    "phase_08_visible_reasoning_summaries_report.json",
    "phase_08_science_reflection_report.json",
)
EXPECTED_REPORT_VERIFIERS = {
    "phase_08_scientific_priors_report.json": "verify_phase_08_scientific_priors",
    "phase_08_entity_request_inference_report.json": "verify_phase_08_entity_request_inference",
    "phase_08_world_region_selection_report.json": "verify_phase_08_world_region_selection",
    "phase_08_causal_chain_reasoning_report.json": "verify_phase_08_causal_chain_reasoning",
    "phase_08_bounded_current_world_reasoning_report.json": "verify_phase_08_bounded_current_world_reasoning",
    "phase_08_visible_reasoning_summaries_report.json": "verify_phase_08_visible_reasoning_summaries",
    "phase_08_science_reflection_report.json": "verify_phase_08_science_reflection",
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
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_08_evidence"
DEMO_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_08_demo_bundle"
MANIFEST_PATH = EVIDENCE_DIR / "phase_08_evidence_manifest.json"


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_path() -> None:
    runtime_path = str(REPO_ROOT / PHASE_08_RUNTIME_PARENT)
    if runtime_path not in sys.path:
        sys.path.insert(0, runtime_path)


ensure_runtime_import_path()


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
        "notes": ["Phase 8 remains open", "no approval implied"],
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
        "notes": [*notes, "Phase 8 remains open", "no approval implied"],
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
                "report_id": filename.removeprefix("phase_08_").removesuffix("_report.json"),
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
        "status": "phase_8_verifier_family_pass" if overall_pass else "phase_8_verifier_family_incomplete",
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 8 remains open",
            "manifest is rebuilt from actual report files on disk",
            "no approval implied",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest
