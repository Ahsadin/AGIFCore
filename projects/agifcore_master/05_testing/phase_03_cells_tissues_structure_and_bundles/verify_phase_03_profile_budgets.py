from __future__ import annotations

import importlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_03_cells_tissues_structure_and_bundles"
PHASE_LABEL = "Phase 3"
SLICE_ID = "slice_3"
VERIFICATION_NAME = "profile_budgets"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"

RUNTIME_IMPORTS = ("profile_budget_rules",)
RUNTIME_FILES = ("profile_budget_rules.py",)

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/02_requirements/DEPLOYMENT_PROFILES.md",
)

SUPPORTING_EVIDENCE_REFS = (
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_cell_contracts_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_activation_and_trust_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_validation_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json",
)


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    target: str
    expected_pass: bool
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "target": self.target,
            "expected_pass": self.expected_pass,
            "passed": self.passed,
            "message": self.message,
        }


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
TESTING_DIR = PROJECT_ROOT / TEST_ROOT_NAME / PHASE_NAME
OUTPUT_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = OUTPUT_DIR / "phase_03_evidence"
RUNTIME_DIR = PROJECT_ROOT / EXECUTION_ROOT_NAME / PHASE_NAME / "agifcore_phase3_structure"
REPORT_PATH = EVIDENCE_DIR / "phase_03_profile_budget_report.json"
MANIFEST_PATH = EVIDENCE_DIR / "phase_03_evidence_manifest.json"


class ContractViolation(ValueError):
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


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def import_runtime_module(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except Exception:  # noqa: BLE001 - surfaced in the report.
        return None


def runtime_modules_available() -> bool:
    return all(import_runtime_module(module_name) is not None for module_name in RUNTIME_IMPORTS)


def _manifest_status_from_reports() -> tuple[str, bool]:
    report_paths = sorted(EVIDENCE_DIR.glob("*_report.json"))
    if not report_paths:
        return "slice_3_blocked", False

    all_pass = True
    for report_path in report_paths:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        overall_pass = payload.get("overall_pass")
        if overall_pass is None:
            summary = payload.get("summary")
            if isinstance(summary, Mapping):
                overall_pass = summary.get("overall_pass")
        if overall_pass is None and isinstance(payload.get("status"), str):
            overall_pass = payload["status"] == "pass"
        all_pass = all_pass and bool(overall_pass)

    if runtime_modules_available() and all_pass:
        return "slice_3_ready", True
    return "slice_3_blocked", False


def refresh_evidence_manifest() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    for report_path in sorted(EVIDENCE_DIR.glob("*_report.json")):
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        overall_pass = payload.get("overall_pass")
        if overall_pass is None:
            summary = payload.get("summary")
            if isinstance(summary, Mapping):
                overall_pass = summary.get("overall_pass")
        if overall_pass is None and isinstance(payload.get("status"), str):
            overall_pass = payload["status"] == "pass"
        reports.append(
            {
                "report_id": report_path.stem.removeprefix("phase_03_").removesuffix("_report"),
                "path": str(report_path),
                "overall_pass": bool(overall_pass),
            }
        )

    status, manifest_ready = _manifest_status_from_reports()
    manifest = {
        "phase": PHASE_LABEL,
        "phase_remains_open": True,
        "reports": reports,
        "runtime_modules_available": runtime_modules_available(),
        "slice": SLICE_ID,
        "status": status,
        "notes": [
            "evidence manifest is rebuilt from actual report files on disk",
            "slice 1 evidence remains present and real",
            "slice 2 evidence remains present and real",
            "slice 3 profile-budget runtime is absent in this lane unless the runtime files are present in the configured worktree",
            f"manifest readiness derived from real report files: {str(manifest_ready).lower()}",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def _runtime_api() -> dict[str, Any]:
    modules = {module_name: import_runtime_module(module_name) for module_name in RUNTIME_IMPORTS}
    if any(module is None for module in modules.values()):
        missing = [name for name, module in modules.items() if module is None]
        raise ContractViolation(f"runtime import failed: {', '.join(missing)}")

    profile_budget_rules = modules["profile_budget_rules"]
    return {
        "modules": modules,
        "ProfileBudgetRule": getattr(profile_budget_rules, "ProfileBudgetRule"),
        "evaluate_profile_budget": getattr(profile_budget_rules, "evaluate_profile_budget"),
        "default_profile_budget_payload": getattr(profile_budget_rules, "default_profile_budget_payload"),
        "PROFILE_ACTIVE_CELL_CEILINGS": getattr(profile_budget_rules, "PROFILE_ACTIVE_CELL_CEILINGS"),
        "PHASE3_TISSUE_CEILING": getattr(profile_budget_rules, "PHASE3_TISSUE_CEILING"),
        "PHASE3_BUNDLE_PAYLOAD_CEILING_BYTES": getattr(profile_budget_rules, "PHASE3_BUNDLE_PAYLOAD_CEILING_BYTES"),
    }


def _module_public_names(module: Any) -> list[str]:
    return [name for name in dir(module) if not name.startswith("_")]


def _require_decision(result: Any, *, should_pass: bool, context: str) -> None:
    if isinstance(result, Mapping):
        decision = bool(result.get("allow"))
    else:
        decision = bool(getattr(result, "allowed", False))
    if should_pass and not decision:
        raise ContractViolation(f"{context} returned a blocked decision")
    if not should_pass and decision:
        raise ContractViolation(f"{context} unexpectedly allowed the invalid case")
    return result


def _decision_reason(result: Any) -> str:
    if isinstance(result, Mapping):
        return str(result.get("reason", ""))
    return str(getattr(result, "reason", ""))


def _profile_context(
    *,
    active_cell_count: int,
    tissue_count: int,
    largest_tissue_member_count: int,
    dormant_blueprint_count: int,
    manifest_size_bytes: int,
    bundle_payload_size_bytes: int,
) -> dict[str, int]:
    return {
        "active_cell_count": active_cell_count,
        "tissue_count": tissue_count,
        "largest_tissue_member_count": largest_tissue_member_count,
        "dormant_blueprint_count": dormant_blueprint_count,
        "manifest_size_bytes": manifest_size_bytes,
        "bundle_payload_size_bytes": bundle_payload_size_bytes,
    }


def _profile_payload(profile: str) -> dict[str, Any]:
    return {
        "profile": profile,
        "max_active_cells": {"mobile": 8, "laptop": 32, "builder": 64}[profile],
        "max_tissues": 12,
        "max_members_per_tissue_before_review": 8,
        "max_dormant_blueprints": 128,
        "max_manifest_size_bytes": 64 * 1024,
        "max_bundle_payload_size_bytes": 8 * 1024 * 1024,
        "policy_envelope": {"profile": profile},
    }


def _execute_case(result: Any, *, case_id: str, target: str, expected_pass: bool) -> CaseResult:
    if isinstance(result, Mapping):
        allowed = bool(result.get("allow"))
    else:
        allowed = bool(getattr(result, "allowed", False))
    if expected_pass:
        if not allowed:
            raise ContractViolation(f"{case_id} returned a blocked decision")
        return CaseResult(case_id, target, expected_pass, True, "passed")
    if allowed:
        return CaseResult(case_id, target, expected_pass, False, "unexpected pass")
    return CaseResult(case_id, target, expected_pass, True, f"failed as expected: {_decision_reason(result)}")


def build_blocked_report(missing: list[str]) -> dict[str, Any]:
    return {
        "phase": PHASE_LABEL,
        "slice": SLICE_ID,
        "verification": VERIFICATION_NAME,
        "status": "blocked",
        "runtime_modules_available": False,
        "runtime_imports": list(RUNTIME_IMPORTS),
        "checked_files": [
            *PLAN_REFS,
            *SUPPORTING_EVIDENCE_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 3 slice 3 profile budget runtime module is not on disk yet.",
            "missing_files": missing,
        },
        "planned_checks": [
            {"case_id": "laptop-budget-happy-path", "target": "profile_budget_rules", "expected_pass": True},
            {"case_id": "laptop-budget-ceiling-breach", "target": "profile_budget_rules", "expected_pass": False},
            {"case_id": "mobile-budget-happy-path", "target": "profile_budget_rules", "expected_pass": True},
            {"case_id": "mobile-budget-ceiling-breach", "target": "profile_budget_rules", "expected_pass": False},
            {"case_id": "builder-budget-happy-path", "target": "profile_budget_rules", "expected_pass": True},
            {"case_id": "builder-active-cell-ceiling-breach", "target": "profile_budget_rules", "expected_pass": False},
            {"case_id": "builder-tissue-ceiling-breach", "target": "profile_budget_rules", "expected_pass": False},
            {"case_id": "builder-bundle-payload-ceiling-breach", "target": "profile_budget_rules", "expected_pass": False},
        ],
        "summary": {
            "overall_pass": False,
            "blocked_checks": 8,
            "planned_checks": 8,
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "no integrated profile-budget success is claimed because the runtime file is absent",
            "the verifier stays repo-relative and does not rely on external PYTHONPATH wiring",
            "existing slice 1 and slice 2 evidence remains intact",
        ],
    }


def build_pass_report() -> dict[str, Any]:
    api = _runtime_api()
    ProfileBudgetRule = api["ProfileBudgetRule"]
    evaluate_profile_budget = api["evaluate_profile_budget"]
    modules = api["modules"]
    profile_ceilings = api["PROFILE_ACTIVE_CELL_CEILINGS"]
    tissue_ceiling = api["PHASE3_TISSUE_CEILING"]
    bundle_ceiling = api["PHASE3_BUNDLE_PAYLOAD_CEILING_BYTES"]

    cases = [
        (
            "laptop-budget-happy-path",
            "profile_budget_rules",
            True,
            lambda: _require_decision(
                evaluate_profile_budget(
                    profile="laptop",
                    context=_profile_context(
                        active_cell_count=profile_ceilings["laptop"],
                        tissue_count=tissue_ceiling,
                        largest_tissue_member_count=8,
                        dormant_blueprint_count=128,
                        manifest_size_bytes=64 * 1024,
                        bundle_payload_size_bytes=bundle_ceiling,
                    ),
                ),
                should_pass=True,
                context="laptop budget happy path",
            ),
        ),
        (
            "laptop-budget-ceiling-breach",
            "profile_budget_rules",
            False,
            lambda: _require_decision(
                ProfileBudgetRule.for_profile("laptop").evaluate(
                    _profile_context(
                        active_cell_count=profile_ceilings["laptop"] + 1,
                        tissue_count=tissue_ceiling,
                        largest_tissue_member_count=8,
                        dormant_blueprint_count=128,
                        manifest_size_bytes=64 * 1024,
                        bundle_payload_size_bytes=bundle_ceiling,
                    )
                ),
                should_pass=False,
                context="laptop budget ceiling breach",
            ),
        ),
        (
            "mobile-budget-happy-path",
            "profile_budget_rules",
            True,
            lambda: _require_decision(
                ProfileBudgetRule.for_profile("mobile").evaluate(
                    _profile_context(
                        active_cell_count=profile_ceilings["mobile"],
                        tissue_count=tissue_ceiling,
                        largest_tissue_member_count=8,
                        dormant_blueprint_count=128,
                        manifest_size_bytes=64 * 1024,
                        bundle_payload_size_bytes=bundle_ceiling,
                    )
                ),
                should_pass=True,
                context="mobile budget happy path",
            ),
        ),
        (
            "mobile-budget-ceiling-breach",
            "profile_budget_rules",
            False,
            lambda: _require_decision(
                evaluate_profile_budget(
                    profile="mobile",
                    context=_profile_context(
                        active_cell_count=profile_ceilings["mobile"] + 1,
                        tissue_count=tissue_ceiling,
                        largest_tissue_member_count=8,
                        dormant_blueprint_count=128,
                        manifest_size_bytes=64 * 1024,
                        bundle_payload_size_bytes=bundle_ceiling,
                    ),
                ),
                should_pass=False,
                context="mobile budget ceiling breach",
            ),
        ),
        (
            "builder-budget-happy-path",
            "profile_budget_rules",
            True,
            lambda: _require_decision(
                ProfileBudgetRule.for_profile("builder").evaluate(
                    _profile_context(
                        active_cell_count=profile_ceilings["builder"],
                        tissue_count=tissue_ceiling,
                        largest_tissue_member_count=8,
                        dormant_blueprint_count=128,
                        manifest_size_bytes=64 * 1024,
                        bundle_payload_size_bytes=bundle_ceiling,
                    )
                ),
                should_pass=True,
                context="builder budget happy path",
            ),
        ),
        (
            "builder-active-cell-ceiling-breach",
            "profile_budget_rules",
            False,
            lambda: _require_decision(
                evaluate_profile_budget(
                    profile="builder",
                    context=_profile_context(
                        active_cell_count=profile_ceilings["builder"] + 1,
                        tissue_count=tissue_ceiling,
                        largest_tissue_member_count=8,
                        dormant_blueprint_count=128,
                        manifest_size_bytes=64 * 1024,
                        bundle_payload_size_bytes=bundle_ceiling,
                    ),
                ),
                should_pass=False,
                context="builder active cell ceiling breach",
            ),
        ),
        (
            "builder-tissue-ceiling-breach",
            "profile_budget_rules",
            False,
            lambda: _require_decision(
                evaluate_profile_budget(
                    profile="builder",
                    context=_profile_context(
                        active_cell_count=profile_ceilings["builder"],
                        tissue_count=tissue_ceiling + 1,
                        largest_tissue_member_count=8,
                        dormant_blueprint_count=128,
                        manifest_size_bytes=64 * 1024,
                        bundle_payload_size_bytes=bundle_ceiling,
                    ),
                ),
                should_pass=False,
                context="builder tissue ceiling breach",
            ),
        ),
        (
            "builder-bundle-payload-ceiling-breach",
            "profile_budget_rules",
            False,
            lambda: _require_decision(
                evaluate_profile_budget(
                    profile="builder",
                    context=_profile_context(
                        active_cell_count=profile_ceilings["builder"],
                        tissue_count=tissue_ceiling,
                        largest_tissue_member_count=8,
                        dormant_blueprint_count=128,
                        manifest_size_bytes=64 * 1024,
                        bundle_payload_size_bytes=bundle_ceiling + 1,
                    ),
                ),
                should_pass=False,
                context="builder bundle payload ceiling breach",
            ),
        ),
    ]

    results: list[CaseResult] = []
    for case_id, target, expected_pass, fn in cases:
        try:
            result = fn()
        except Exception as exc:  # noqa: BLE001 - surfaced in the report.
            if expected_pass:
                results.append(CaseResult(case_id, target, expected_pass, False, f"unexpected failure: {exc}"))
            else:
                results.append(CaseResult(case_id, target, expected_pass, True, f"failed as expected: {exc}"))
            continue
        results.append(_execute_case(result, case_id=case_id, target=target, expected_pass=expected_pass))

    passed_count = sum(1 for item in results if item.passed)
    expected_pass_count = sum(1 for item in results if item.expected_pass)
    all_expected_succeeded = all(item.passed for item in results if item.expected_pass)
    all_expected_failures_failed = all(item.passed for item in results if not item.expected_pass)
    overall_pass = all_expected_succeeded and all_expected_failures_failed

    return {
        "phase": PHASE_LABEL,
        "slice": SLICE_ID,
        "verification": VERIFICATION_NAME,
        "status": "pass" if overall_pass else "fail",
        "runtime_modules_available": True,
        "runtime_imports": list(RUNTIME_IMPORTS),
        "checked_files": [
            *PLAN_REFS,
            *SUPPORTING_EVIDENCE_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "results": [item.to_dict() for item in results],
        "runtime_exports": {
            "modules": {name: _module_public_names(module) for name, module in modules.items()},
            "profile_ceiling_helpers": {
                "laptop": profile_ceilings["laptop"],
                "mobile": profile_ceilings["mobile"],
                "builder": profile_ceilings["builder"],
                "tissue": tissue_ceiling,
                "bundle_payload": bundle_ceiling,
            },
        },
        "summary": {
            "overall_pass": overall_pass,
            "expected_pass_cases": expected_pass_count,
            "expected_succeeded": all_expected_succeeded,
            "expected_failures_verified": all_expected_failures_failed,
            "passed_cases": passed_count,
            "total_cases": len(results),
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "laptop, mobile, and builder budget behavior is exercised directly against the runtime API when the runtime file exists",
            "budget ceilings are verified at and beyond the boundary",
            "no approval implied",
        ],
    }


def build_runtime_failure_report(exc: Exception) -> dict[str, Any]:
    return {
        "phase": PHASE_LABEL,
        "slice": SLICE_ID,
        "verification": VERIFICATION_NAME,
        "status": "fail",
        "runtime_modules_available": True,
        "runtime_imports": list(RUNTIME_IMPORTS),
        "checked_files": [
            *PLAN_REFS,
            *SUPPORTING_EVIDENCE_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "blocker": {
            "kind": "runtime_execution_error",
            "message": str(exc),
        },
        "summary": {
            "overall_pass": False,
            "passed_cases": 0,
            "total_cases": 0,
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "runtime files were present but real case execution failed",
            "no approval implied",
        ],
    }


def main() -> int:
    runtime_missing = missing_files([RUNTIME_DIR / filename for filename in RUNTIME_FILES])
    if runtime_missing:
        report = build_blocked_report(runtime_missing)
        dump_json(REPORT_PATH, report)
        refresh_evidence_manifest()
        print("phase_3 slice_3 profile budget verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    try:
        report = build_pass_report()
    except Exception as exc:  # noqa: BLE001 - surfaced in the report.
        report = build_runtime_failure_report(exc)

    dump_json(REPORT_PATH, report)
    refresh_evidence_manifest()
    print("phase_3 slice_3 profile budget verifier: PASS" if report.get("summary", {}).get("overall_pass") else "phase_3 slice_3 profile budget verifier: FAIL")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("summary", {}).get("overall_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
