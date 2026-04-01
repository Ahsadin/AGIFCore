from __future__ import annotations

import importlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

PHASE = "14"
PHASE_NAME = "phase_14_sandbox_profiles_and_scale_realization"
OUTPUT_ROOT_NAME = "06_outputs"
RUNTIME_PACKAGE = "agifcore_phase14_sandbox"
PHASE_14_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization"
PHASE_13_TEST_PARENT = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux"

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md",
    "projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/01_plan/DEMO_PROTOCOL.md",
    "projects/agifcore_master/03_design/SANDBOX_MODEL.md",
    "projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md",
    "projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md",
    "projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md",
)

CONTRACT_REFS = (
    "projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/active_dormant_control.py",
    "projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/profile_budget_rules.py",
    "projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/tissue_manifests.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/contracts.py",
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/product_runtime_shell.py",
    "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/_phase_13_verifier_common.py",
)

RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/contracts.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/sandbox_policy.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/wasmtime_fuel_limits.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/wasmtime_memory_limits.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/wasmtime_wall_time_limits.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/cell_manifest.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/tissue_manifest.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/profile_manifests.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/active_cell_budget.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/dormant_cell_survival.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/sandbox_profile_shell.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/__init__.py",
)

COMMON_TEST_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/_phase_14_verifier_common.py"

REQUIRED_REPORT_FILES = (
    "phase_14_sandbox_report.json",
    "phase_14_wasmtime_fuel_report.json",
    "phase_14_wasmtime_memory_report.json",
    "phase_14_wasmtime_wall_time_report.json",
    "phase_14_cell_manifest_report.json",
    "phase_14_tissue_manifest_report.json",
    "phase_14_profile_manifest_report.json",
    "phase_14_active_cell_budget_report.json",
    "phase_14_dormant_survival_report.json",
    "phase_14_manifest_differentiation_report.json",
)

EXPECTED_REPORT_VERIFIERS = {
    "phase_14_sandbox_report.json": "verify_phase_14_sandbox",
    "phase_14_wasmtime_fuel_report.json": "verify_phase_14_wasmtime_fuel",
    "phase_14_wasmtime_memory_report.json": "verify_phase_14_wasmtime_memory",
    "phase_14_wasmtime_wall_time_report.json": "verify_phase_14_wasmtime_wall_time",
    "phase_14_cell_manifest_report.json": "verify_phase_14_cell_manifest",
    "phase_14_tissue_manifest_report.json": "verify_phase_14_tissue_manifest",
    "phase_14_profile_manifest_report.json": "verify_phase_14_profile_manifests",
    "phase_14_active_cell_budget_report.json": "verify_phase_14_active_cell_budget",
    "phase_14_dormant_survival_report.json": "verify_phase_14_dormant_cell_survival",
    "phase_14_manifest_differentiation_report.json": "verify_phase_14_manifest_differentiation",
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
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_14_evidence"
DEMO_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_14_demo_bundle"
MANIFEST_PATH = EVIDENCE_DIR / "phase_14_evidence_manifest.json"


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_paths() -> None:
    for runtime_parent in (
        REPO_ROOT / PHASE_14_RUNTIME_PARENT,
        REPO_ROOT / PHASE_13_TEST_PARENT,
    ):
        runtime_str = str(runtime_parent)
        if runtime_str not in sys.path:
            sys.path.insert(0, runtime_str)


ensure_runtime_import_paths()

import _phase_13_verifier_common as p13c
from agifcore_phase14_sandbox.contracts import stable_hash_payload
from agifcore_phase14_sandbox.sandbox_profile_shell import SandboxProfileRuntimeShell


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
        "notes": ["Phase 14 remains open", "no approval implied"],
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
        "notes": [*notes, "Phase 14 remains open", "no approval implied"],
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
                "report_id": filename.removeprefix("phase_14_").removesuffix("_report.json"),
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
        "status": "phase_14_verifier_family_pass" if overall_pass else "phase_14_verifier_family_incomplete",
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 14 remains open",
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


def run_phase14_shell(*, scenario: str) -> dict[str, Any]:
    phase13_result = p13c.run_phase13_shell(scenario=scenario)
    phase13_shell = phase13_result["shell"]
    session_open = phase13_shell.session_open()
    shell_snapshot = phase13_shell.shell_snapshot()
    state_export = phase13_shell.state_export()
    memory_review_export = phase13_shell.memory_review_export()
    safe_shutdown = phase13_shell.safe_shutdown()
    before_session = deepcopy(session_open)
    before_snapshot = deepcopy(shell_snapshot)
    before_state_export = deepcopy(state_export)
    before_memory_export = deepcopy(memory_review_export)
    before_shutdown = deepcopy(safe_shutdown)
    shell = SandboxProfileRuntimeShell(
        phase13_session_open=session_open,
        phase13_shell_snapshot=shell_snapshot,
        phase13_state_export=state_export,
        phase13_memory_review_export=memory_review_export,
        phase13_safe_shutdown=safe_shutdown,
    )
    assert_inputs_unchanged(before_session, session_open, "phase13 session_open")
    assert_inputs_unchanged(before_snapshot, shell_snapshot, "phase13 shell_snapshot")
    assert_inputs_unchanged(before_state_export, state_export, "phase13 state_export")
    assert_inputs_unchanged(before_memory_export, memory_review_export, "phase13 memory_review_export")
    assert_inputs_unchanged(before_shutdown, safe_shutdown, "phase13 safe_shutdown")
    return {
        "fixture": phase13_result["fixture"],
        "phase13": phase13_result,
        "shell": shell,
        "shell_snapshot": shell.shell_snapshot(),
    }


def build_manifest_differentiation_summary(
    *,
    shell: SandboxProfileRuntimeShell,
    profile: str = "laptop",
) -> dict[str, Any]:
    cell_manifest = shell.cell_manifest()
    tissue_manifest = shell.tissue_manifest()
    profile_manifests = shell.profile_manifests()
    budget = shell.active_cell_budget(profile=profile)
    proof = shell.dormant_cell_survival(profile=profile)

    family_signatures: dict[str, tuple[Any, ...]] = {}
    for cell in cell_manifest["cells"]:
        family = str(cell["role_family"])
        signature = (
            tuple(cell["allowed_actions"]),
            tuple(cell["forbidden_actions"]),
            str(cell["activation_budget_class"]),
            str(cell["export_visibility_class"]),
            str(cell["dormancy_behavior_class"]),
            str(cell["continuity_requirement_class"]),
            str(cell["evidence_requirement_class"]),
            str(cell["sandbox_policy_class"]),
            bool(cell["audit_replay_required"]),
            str(cell["routing_responsibility"]),
        )
        family_signatures.setdefault(family, signature)

    tissue_signatures: dict[str, tuple[Any, ...]] = {}
    for tissue in tissue_manifest["tissues"]:
        signature = (
            str(tissue["tissue_variant_id"]),
            str(tissue["specialization_tag"]),
            str(tissue["tissue_focus"]),
            str(tissue["evidence_lane"]),
            str(tissue["continuity_handling_class"]),
            str(tissue["escalation_handling_class"]),
            tuple(sorted(tissue["allowed_family_mix"])),
            tuple(tissue["exemplar_class_ids"]),
            tuple(sorted(tissue["active_cell_cap_by_profile"].items())),
            tuple(sorted(tissue["activation_priority_boost_by_profile"].items())),
        )
        tissue_signatures[str(tissue["tissue_id"])] = signature

    payload = {
        "profile": profile,
        "cell_manifest_hash": cell_manifest["manifest_hash"],
        "tissue_manifest_hash": tissue_manifest["manifest_hash"],
        "profile_manifest_hash": profile_manifests["manifest_hash"],
        "family_count": cell_manifest["family_count"],
        "family_signature_count": len(set(family_signatures.values())),
        "family_signature_hash": stable_hash_payload(sorted(family_signatures.items())),
        "contract_variant_count": cell_manifest["contract_variant_count"],
        "exemplar_class_count": len(cell_manifest["exemplar_class_ids"]),
        "exemplar_class_counts": cell_manifest["exemplar_class_counts"],
        "constraint_diversity": {
            "allowed_profile_pattern_count": cell_manifest["allowed_profile_pattern_count"],
            "activation_budget_class_count": cell_manifest["activation_budget_class_count"],
            "export_visibility_class_count": cell_manifest["export_visibility_class_count"],
            "dormancy_behavior_class_count": cell_manifest["dormancy_behavior_class_count"],
            "continuity_requirement_class_count": cell_manifest["continuity_requirement_class_count"],
            "evidence_requirement_class_count": cell_manifest["evidence_requirement_class_count"],
            "tissue_variant_count": cell_manifest["tissue_variant_count"],
            "operation_set_signature_count": cell_manifest["operation_set_signature_count"],
            "sandbox_required_cell_count": cell_manifest["sandbox_required_cell_count"],
            "audit_replay_required_cell_count": cell_manifest["audit_replay_required_cell_count"],
        },
        "tissue_count": tissue_manifest["tissue_count"],
        "tissue_variant_count": tissue_manifest["tissue_variant_count"],
        "tissue_variant_counts": tissue_manifest["tissue_variant_counts"],
        "tissue_signature_count": len(set(tissue_signatures.values())),
        "tissue_signature_hash": stable_hash_payload(sorted(tissue_signatures.items())),
        "focus_family_tissue_counts": tissue_manifest["focus_family_tissue_counts"],
        "continuity_handling_class_counts": tissue_manifest["continuity_handling_class_counts"],
        "escalation_handling_class_counts": tissue_manifest["escalation_handling_class_counts"],
        "per_profile_total_active_cap": tissue_manifest["per_profile_total_active_cap"],
        "budget": {
            "profile": budget["profile"],
            "selected_active_cell_count": budget["selected_active_cell_count"],
            "selected_active_tissue_count": budget["selected_active_tissue_count"],
            "selected_family_counts": budget["selected_family_counts"],
            "selected_exemplar_class_counts": budget["selected_exemplar_class_counts"],
            "selected_tissue_variant_counts": budget["selected_tissue_variant_counts"],
            "selected_dormancy_behavior_counts": budget["selected_dormancy_behavior_counts"],
            "selected_continuity_requirement_counts": budget["selected_continuity_requirement_counts"],
            "selected_audit_replay_required_count": budget["selected_audit_replay_required_count"],
            "selected_sandbox_required_count": budget["selected_sandbox_required_count"],
            "selected_activation_priority_min": budget["selected_activation_priority_min"],
            "selected_activation_priority_max": budget["selected_activation_priority_max"],
            "selected_activation_priority_total": budget["selected_activation_priority_total"],
            "budget_state": budget["budget_state"],
            "reason_code": budget["reason_code"],
        },
        "proof": {
            "case_count": proof["case_count"],
            "dormancy_behavior_class_count": proof["dormancy_behavior_class_count"],
            "continuity_requirement_class_count": proof["continuity_requirement_class_count"],
            "tissue_variant_count": proof["tissue_variant_count"],
            "exemplar_class_count": proof["exemplar_class_count"],
            "covered_dormancy_behavior_classes": proof["covered_dormancy_behavior_classes"],
            "covered_continuity_requirement_classes": proof["covered_continuity_requirement_classes"],
            "covered_evidence_requirement_classes": proof["covered_evidence_requirement_classes"],
            "covered_tissue_variant_ids": proof["covered_tissue_variant_ids"],
            "covered_exemplar_class_ids": proof["covered_exemplar_class_ids"],
        },
    }
    return {**payload, "summary_hash": stable_hash_payload(payload)}


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
            "phase_14_sandbox_enforcement_demo.json",
            "phase_14_laptop_profile_demo.json",
            "phase_14_mobile_constrained_demo.json",
            "phase_14_manifest_audit_demo.json",
        ],
        "supporting_evidence_manifest": "phase_14_evidence_manifest.json",
        "notes": [
            "summary only",
            "Phase 14 remains open",
            "no approval implied",
        ],
    }
    write_demo_payload(filename="phase_14_demo_index.json", payload=index_json)
    write_demo_markdown(
        filename="phase_14_demo_index.md",
        lines=[
            "# Phase 14 Demo Index",
            "",
            "Phase 14 remains `open`. This bundle is for inspection only and does not imply approval or finality.",
            "",
            "Demo scenarios:",
            "",
            "- `phase_14_sandbox_enforcement_demo.md` for the sandbox and Wasmtime enforcement path.",
            "- `phase_14_laptop_profile_demo.md` for the reference laptop profile path.",
            "- `phase_14_mobile_constrained_demo.md` for the constrained mobile profile path.",
            "- `phase_14_manifest_audit_demo.md` for the literal manifest and dormant-survival audit path.",
            "",
            "Supporting demo payloads:",
            "",
            "- `phase_14_sandbox_enforcement_demo.json`",
            "- `phase_14_laptop_profile_demo.json`",
            "- `phase_14_mobile_constrained_demo.json`",
            "- `phase_14_manifest_audit_demo.json`",
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
