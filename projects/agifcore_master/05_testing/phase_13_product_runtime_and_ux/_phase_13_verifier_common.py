from __future__ import annotations

import importlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

PHASE = "13"
PHASE_NAME = "phase_13_product_runtime_and_ux"
OUTPUT_ROOT_NAME = "06_outputs"
RUNTIME_PACKAGE = "agifcore_phase13_product_runtime"
PHASE_13_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux"
PHASE_12_TEST_PARENT = "projects/agifcore_master/05_testing/phase_12_structural_growth"

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md",
    "projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/01_plan/DEMO_PROTOCOL.md",
    "projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md",
    "projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md",
    "projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md",
    "projects/agifcore_master/03_design/SANDBOX_MODEL.md",
    "projects/agifcore_master/03_design/PUBLIC_RELEASE_MODEL.md",
)

CONTRACT_REFS = (
    "projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/workspace_state.py",
    "projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_bus.py",
    "projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/replay_ledger.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/contracts.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/meta_cognition_turn.py",
    "projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/self_improvement_cycle.py",
    "projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/structural_growth_cycle.py",
    "projects/agifcore_master/05_testing/phase_12_structural_growth/_phase_12_verifier_common.py",
)

RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/contracts.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/embeddable_runtime_api.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/local_runner.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/local_gateway.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/desktop_ui.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/state_export.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/trace_export.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/memory_review_export.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/safe_shutdown.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/fail_closed_ux.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/installer_distribution.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/product_runtime_shell.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/__init__.py",
)

COMMON_TEST_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/_phase_13_verifier_common.py"

REQUIRED_REPORT_FILES = (
    "phase_13_runtime_api_report.json",
    "phase_13_local_runner_report.json",
    "phase_13_local_gateway_report.json",
    "phase_13_desktop_ui_report.json",
    "phase_13_state_export_report.json",
    "phase_13_trace_export_report.json",
    "phase_13_memory_review_export_report.json",
    "phase_13_safe_shutdown_report.json",
    "phase_13_fail_closed_ux_report.json",
    "phase_13_installer_distribution_report.json",
)

EXPECTED_REPORT_VERIFIERS = {
    "phase_13_runtime_api_report.json": "verify_phase_13_runtime_api",
    "phase_13_local_runner_report.json": "verify_phase_13_local_runner",
    "phase_13_local_gateway_report.json": "verify_phase_13_local_gateway",
    "phase_13_desktop_ui_report.json": "verify_phase_13_desktop_ui",
    "phase_13_state_export_report.json": "verify_phase_13_state_export",
    "phase_13_trace_export_report.json": "verify_phase_13_trace_export",
    "phase_13_memory_review_export_report.json": "verify_phase_13_memory_review_export",
    "phase_13_safe_shutdown_report.json": "verify_phase_13_safe_shutdown",
    "phase_13_fail_closed_ux_report.json": "verify_phase_13_fail_closed_ux",
    "phase_13_installer_distribution_report.json": "verify_phase_13_installer_distribution",
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
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_13_evidence"
DEMO_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_13_demo_bundle"
MANIFEST_PATH = EVIDENCE_DIR / "phase_13_evidence_manifest.json"


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_paths() -> None:
    for runtime_parent in (
        REPO_ROOT / PHASE_13_RUNTIME_PARENT,
        REPO_ROOT / PHASE_12_TEST_PARENT,
    ):
        runtime_str = str(runtime_parent)
        if runtime_str not in sys.path:
            sys.path.insert(0, runtime_str)


ensure_runtime_import_paths()

import _phase_12_verifier_common as p12c
from agifcore_phase13_product_runtime.contracts import canonical_size_bytes
from agifcore_phase13_product_runtime.product_runtime_shell import ProductRuntimeShell


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
        "notes": ["Phase 13 remains open", "no approval implied"],
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
        "notes": [*notes, "Phase 13 remains open", "no approval implied"],
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
                "report_id": filename.removeprefix("phase_13_").removesuffix("_report.json"),
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
        "status": "phase_13_verifier_family_pass" if overall_pass else "phase_13_verifier_family_incomplete",
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 13 remains open",
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


def run_phase13_shell(*, scenario: str, build_distribution_bundle: bool = False) -> dict[str, Any]:
    result = p12c.run_phase12_cycle(scenario=scenario)
    phase10_turn = deepcopy(result["phase10_turn"])
    phase11_cycle = deepcopy(result["phase11_cycle"])
    phase12_cycle = result["cycle"].to_dict()
    before_phase10 = deepcopy(phase10_turn)
    before_phase11 = deepcopy(phase11_cycle)
    before_phase12 = deepcopy(phase12_cycle)
    shell = ProductRuntimeShell(
        fixture=result["fixture"],
        phase10_turn_state=phase10_turn,
        phase11_cycle_state=phase11_cycle,
        phase12_cycle_state=phase12_cycle,
    )
    if build_distribution_bundle:
        shell.installer_distribution(output_dir=DEMO_DIR)
    assert_inputs_unchanged(before_phase10, phase10_turn, f"phase13 {scenario} phase10_turn_state")
    assert_inputs_unchanged(before_phase11, phase11_cycle, f"phase13 {scenario} phase11_cycle_state")
    assert_inputs_unchanged(before_phase12, phase12_cycle, f"phase13 {scenario} phase12_cycle_state")
    return {
        "fixture": result["fixture"],
        "phase10_turn": phase10_turn,
        "phase11_cycle": phase11_cycle,
        "phase12_cycle": phase12_cycle,
        "shell": shell,
        "shell_snapshot": shell.shell_snapshot(),
    }


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
            "phase_13_end_to_end_product_demo.json",
            "phase_13_fail_closed_ux_demo.json",
            "phase_13_installer_distribution_demo.json",
        ],
        "supporting_evidence_manifest": "phase_13_evidence_manifest.json",
        "notes": [
            "summary only",
            "Phase 13 remains open",
            "no approval implied",
        ],
    }
    write_demo_payload(filename="phase_13_demo_index.json", payload=index_json)
    write_demo_markdown(
        filename="phase_13_demo_index.md",
        lines=[
            "# Phase 13 Demo Index",
            "",
            "Phase 13 remains `open`. This bundle is for inspection only and does not imply approval or finality.",
            "",
            "Demo scenarios:",
            "",
            "- `phase_13_end_to_end_product_demo.md` for the governed local product shell path.",
            "- `phase_13_fail_closed_ux_demo.md` for the fail-closed product behavior path.",
            "- `phase_13_installer_distribution_demo.md` for the local distribution bundle path.",
            "",
            "Supporting demo payloads:",
            "",
            "- `phase_13_end_to_end_product_demo.json`",
            "- `phase_13_fail_closed_ux_demo.json`",
            "- `phase_13_installer_distribution_demo.json`",
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
