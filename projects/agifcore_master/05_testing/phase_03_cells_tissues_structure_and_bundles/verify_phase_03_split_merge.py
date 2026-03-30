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
VERIFICATION_NAME = "split_merge"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"

RUNTIME_IMPORTS = ("split_merge_rules",)
RUNTIME_FILES = ("split_merge_rules.py",)
SUPPORTING_IMPORTS = (
    "cell_contracts",
    "tissue_manifests",
    "trust_bands",
    "active_dormant_control",
)

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
REPORT_PATH = EVIDENCE_DIR / "phase_03_split_merge_report.json"
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


def supporting_modules_available() -> bool:
    return all(import_runtime_module(module_name) is not None for module_name in SUPPORTING_IMPORTS)


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
            "slice 3 split/merge runtime is absent in this lane unless the runtime files are present in the configured worktree",
            f"manifest readiness derived from real report files: {str(manifest_ready).lower()}",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def _runtime_api() -> dict[str, Any]:
    modules = {module_name: import_runtime_module(module_name) for module_name in (*RUNTIME_IMPORTS, *SUPPORTING_IMPORTS)}
    if any(module is None for module in modules.values()):
        missing = [name for name, module in modules.items() if module is None]
        raise ContractViolation(f"runtime import failed: {', '.join(missing)}")

    split_merge_rules = modules["split_merge_rules"]
    trust_bands = modules["trust_bands"]
    tissue_manifests = modules["tissue_manifests"]
    cell_contracts = modules["cell_contracts"]

    return {
        "modules": modules,
        "SplitProposal": getattr(split_merge_rules, "SplitProposal"),
        "MergeProposal": getattr(split_merge_rules, "MergeProposal"),
        "evaluate_split_proposal": getattr(split_merge_rules, "evaluate_split_proposal"),
        "evaluate_merge_proposal": getattr(split_merge_rules, "evaluate_merge_proposal"),
        "TrustBand": getattr(trust_bands, "TrustBand"),
        "default_trust_band_policy": getattr(trust_bands, "default_trust_band_policy"),
        "validate_tissue_manifest_payload": getattr(tissue_manifests, "validate_tissue_manifest_payload"),
        "validate_cell_contract_payload": getattr(cell_contracts, "validate_cell_contract_payload"),
    }


def _decision_allowed(result: Any) -> bool:
    if isinstance(result, Mapping):
        return bool(result.get("allowed"))
    return bool(getattr(result, "allowed", False))


def _decision_reason(result: Any) -> str:
    if isinstance(result, Mapping):
        return str(result.get("reason", ""))
    return str(getattr(result, "reason", ""))


def _require_allowed(result: Any, *, context: str) -> Any:
    if not _decision_allowed(result):
        raise ContractViolation(f"{context} blocked: {_decision_reason(result)}")
    return result


def _require_blocked(result: Any, *, context: str) -> Any:
    if _decision_allowed(result):
        raise ContractViolation(f"{context} unexpectedly allowed")
    return result


def _module_public_names(module: Any) -> list[str]:
    return [name for name in dir(module) if not name.startswith("_")]


def _cell_contract_payload(
    *,
    cell_id: str,
    bundle_ref: str,
    role_family: str,
    role_name: str,
    allowed_tissues: list[str],
    lineage_id: str,
) -> dict[str, Any]:
    return {
        "cell_id": cell_id,
        "bundle_ref": bundle_ref,
        "role_family": role_family,
        "role_name": role_name,
        "allowed_tissues": allowed_tissues,
        "split_policy": {"mode": "governed"},
        "merge_policy": {"mode": "governed"},
        "trust_profile": {"lineage_id": lineage_id},
        "policy_envelope": {"lineage_id": lineage_id},
    }


def _tissue_manifest_payload(*, tissue_id: str, member_cell_ids: list[str], allowed_role_families: list[str]) -> dict[str, Any]:
    return {
        "tissue_id": tissue_id,
        "tissue_name": "Structural Tissue",
        "allowed_role_families": allowed_role_families,
        "member_cell_ids": member_cell_ids,
        "routing_targets": ["bundle-validation"],
        "policy_envelope": {"tissue_id": tissue_id},
    }


def _split_parent_record(*, cell_id: str, lineage_id: str, role_family: str, lifecycle_state: str = "active") -> dict[str, Any]:
    return {
        "cell_id": cell_id,
        "lineage_id": lineage_id,
        "role_family": role_family,
        "lifecycle_state": lifecycle_state,
    }


def _merge_record(*, cell_id: str, lineage_id: str, role_family: str, lifecycle_state: str = "dormant") -> dict[str, Any]:
    return {
        "cell_id": cell_id,
        "lineage_id": lineage_id,
        "role_family": role_family,
        "lifecycle_state": lifecycle_state,
    }


def _split_proposal_payload(*, proposal_id: str, parent_cell_id: str, lineage_id: str, child_specs: list[dict[str, Any]], reason: str) -> dict[str, Any]:
    return {
        "proposal_id": proposal_id,
        "parent_cell_id": parent_cell_id,
        "lineage_id": lineage_id,
        "child_specs": child_specs,
        "reason": reason,
        "actor": "kernel",
        "policy_envelope": {"lineage_id": lineage_id},
    }


def _merge_proposal_payload(*, proposal_id: str, survivor_cell_id: str, merged_cell_id: str, lineage_id: str, reason: str) -> dict[str, Any]:
    return {
        "proposal_id": proposal_id,
        "survivor_cell_id": survivor_cell_id,
        "merged_cell_id": merged_cell_id,
        "lineage_id": lineage_id,
        "reason": reason,
        "actor": "kernel",
        "policy_envelope": {"lineage_id": lineage_id},
    }


def build_blocked_report(missing: list[str]) -> dict[str, Any]:
    return {
        "phase": PHASE_LABEL,
        "slice": SLICE_ID,
        "verification": VERIFICATION_NAME,
        "status": "blocked",
        "runtime_modules_available": False,
        "supporting_modules_available": supporting_modules_available(),
        "runtime_imports": list(RUNTIME_IMPORTS),
        "supporting_imports": list(SUPPORTING_IMPORTS),
        "checked_files": [
            *PLAN_REFS,
            *SUPPORTING_EVIDENCE_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 3 slice 3 split/merge runtime module is not on disk yet.",
            "missing_files": missing,
        },
        "planned_checks": [
            {
                "case_id": "split-happy-path-preserves-lineage",
                "target": "split_merge_rules",
                "expected_pass": True,
            },
            {
                "case_id": "split-missing-lineage-parent-fails",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
            {
                "case_id": "split-role-family-tissue-mismatch-fails",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
            {
                "case_id": "merge-happy-path-preserves-survivor-lineage",
                "target": "split_merge_rules",
                "expected_pass": True,
            },
            {
                "case_id": "merge-lineage-conflict-fails",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
            {
                "case_id": "policy-bounds-breach-fails-closed",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
            {
                "case_id": "conflict-aware-consolidation-remains-fail-closed",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
        ],
        "summary": {
            "overall_pass": False,
            "planned_checks": 7,
            "blocked_checks": 7,
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "no integrated split/merge success is claimed because the runtime file is absent",
            "the verifier stays repo-relative and does not rely on external PYTHONPATH wiring",
            "existing slice 1 and slice 2 evidence remains intact",
        ],
    }


def build_pass_report() -> dict[str, Any]:
    api = _runtime_api()
    SplitProposal = api["SplitProposal"]
    MergeProposal = api["MergeProposal"]
    evaluate_split_proposal = api["evaluate_split_proposal"]
    evaluate_merge_proposal = api["evaluate_merge_proposal"]
    TrustBand = api["TrustBand"]
    default_trust_band_policy = api["default_trust_band_policy"]
    validate_tissue_manifest_payload = api["validate_tissue_manifest_payload"]
    validate_cell_contract_payload = api["validate_cell_contract_payload"]
    modules = api["modules"]

    standard_band = TrustBand.from_payload(default_trust_band_policy("standard"))
    guarded_band = TrustBand.from_payload(default_trust_band_policy("guarded"))

    lineage_id = "lineage-structural-001"
    tissue_id = "tissue-structural"
    parent_contract = _cell_contract_payload(
        cell_id="cell-parent",
        bundle_ref="bundle-structural",
        role_family="planner",
        role_name="phase-3-planner",
        allowed_tissues=[tissue_id],
        lineage_id=lineage_id,
    )
    child_contract_ok = _cell_contract_payload(
        cell_id="cell-child-a",
        bundle_ref="bundle-structural",
        role_family="planner",
        role_name="phase-3-planner-child",
        allowed_tissues=[tissue_id],
        lineage_id=lineage_id,
    )
    child_contract_bad = _cell_contract_payload(
        cell_id="cell-child-bad",
        bundle_ref="bundle-structural",
        role_family="router",
        role_name="phase-3-router-child",
        allowed_tissues=[tissue_id],
        lineage_id=lineage_id,
    )
    tissue_manifest_ok = _tissue_manifest_payload(
        tissue_id=tissue_id,
        member_cell_ids=["cell-parent", "cell-child-a"],
        allowed_role_families=["planner"],
    )
    tissue_manifest_bad = _tissue_manifest_payload(
        tissue_id=tissue_id,
        member_cell_ids=["cell-parent", "cell-child-bad"],
        allowed_role_families=["planner"],
    )

    validate_cell_contract_payload(parent_contract)
    validate_cell_contract_payload(child_contract_ok)
    validate_tissue_manifest_payload(
        tissue_manifest_ok,
        cell_contracts_by_id={
            parent_contract["cell_id"]: parent_contract,
            child_contract_ok["cell_id"]: child_contract_ok,
        },
    )

    cases = [
        (
            "split-happy-path-preserves-lineage",
            "split_merge_rules",
            True,
            lambda: _require_allowed(
                evaluate_split_proposal(
                    proposal=SplitProposal.from_payload(
                        _split_proposal_payload(
                            proposal_id="split-001",
                            parent_cell_id=parent_contract["cell_id"],
                            lineage_id=lineage_id,
                            child_specs=[
                                {"cell_id": "cell-child-a", "role_family": "planner", "policy_envelope": {}},
                                {"cell_id": "cell-child-b", "role_family": "planner", "policy_envelope": {}},
                            ],
                            reason="split because lineage capacity is bounded",
                        )
                    ),
                    parent_record=_split_parent_record(
                        cell_id=parent_contract["cell_id"],
                        lineage_id=lineage_id,
                        role_family="planner",
                    ),
                    trust_band=standard_band,
                    tissue_member_count_before_split=8,
                ),
                context="split happy path",
            ),
        ),
        (
            "split-lineage-conflict-fails",
            "split_merge_rules",
            False,
            lambda: _require_blocked(
                evaluate_split_proposal(
                    proposal=SplitProposal.from_payload(
                        _split_proposal_payload(
                            proposal_id="split-002",
                            parent_cell_id=parent_contract["cell_id"],
                            lineage_id="lineage-wrong",
                            child_specs=[
                                {"cell_id": "cell-child-a", "role_family": "planner", "policy_envelope": {}},
                                {"cell_id": "cell-child-b", "role_family": "planner", "policy_envelope": {}},
                            ],
                            reason="split with wrong lineage",
                        )
                    ),
                    parent_record=_split_parent_record(
                        cell_id=parent_contract["cell_id"],
                        lineage_id=lineage_id,
                        role_family="planner",
                    ),
                    trust_band=standard_band,
                ),
                context="split lineage conflict",
            ),
        ),
        (
            "split-role-family-tissue-mismatch-fails",
            "tissue_manifests",
            False,
            lambda: validate_tissue_manifest_payload(
                tissue_manifest_bad,
                cell_contracts_by_id={
                    parent_contract["cell_id"]: parent_contract,
                    child_contract_bad["cell_id"]: child_contract_bad,
                },
            ),
        ),
        (
            "split-policy-bounds-breach-fails-closed",
            "split_merge_rules",
            False,
            lambda: _require_blocked(
                evaluate_split_proposal(
                    proposal=SplitProposal.from_payload(
                        _split_proposal_payload(
                            proposal_id="split-003",
                            parent_cell_id=parent_contract["cell_id"],
                            lineage_id=lineage_id,
                            child_specs=[
                                {"cell_id": "cell-child-a", "role_family": "planner", "policy_envelope": {}},
                                {"cell_id": "cell-child-b", "role_family": "planner", "policy_envelope": {}},
                            ],
                            reason="split pressure should fail closed",
                        )
                    ),
                    parent_record=_split_parent_record(
                        cell_id=parent_contract["cell_id"],
                        lineage_id=lineage_id,
                        role_family="planner",
                    ),
                    trust_band=guarded_band,
                    tissue_member_count_before_split=9,
                ),
                context="split policy bounds breach",
            ),
        ),
        (
            "merge-happy-path-preserves-survivor-lineage",
            "split_merge_rules",
            True,
            lambda: _require_allowed(
                evaluate_merge_proposal(
                    proposal=MergeProposal.from_payload(
                        _merge_proposal_payload(
                            proposal_id="merge-001",
                            survivor_cell_id="cell-survivor",
                            merged_cell_id="cell-merged",
                            lineage_id=lineage_id,
                            reason="merge after split stabilization",
                        )
                    ),
                    survivor_record=_merge_record(
                        cell_id="cell-survivor",
                        lineage_id=lineage_id,
                        role_family="planner",
                        lifecycle_state="active",
                    ),
                    merged_record=_merge_record(
                        cell_id="cell-merged",
                        lineage_id=lineage_id,
                        role_family="planner",
                        lifecycle_state="dormant",
                    ),
                    trust_band=standard_band,
                ),
                context="merge happy path",
            ),
        ),
        (
            "merge-lineage-conflict-fails",
            "split_merge_rules",
            False,
            lambda: _require_blocked(
                evaluate_merge_proposal(
                    proposal=MergeProposal.from_payload(
                        _merge_proposal_payload(
                            proposal_id="merge-002",
                            survivor_cell_id="cell-survivor",
                            merged_cell_id="cell-merged",
                            lineage_id="lineage-wrong",
                            reason="merge with lineage conflict",
                        )
                    ),
                    survivor_record=_merge_record(
                        cell_id="cell-survivor",
                        lineage_id=lineage_id,
                        role_family="planner",
                        lifecycle_state="active",
                    ),
                    merged_record=_merge_record(
                        cell_id="cell-merged",
                        lineage_id="lineage-wrong",
                        role_family="planner",
                        lifecycle_state="dormant",
                    ),
                    trust_band=standard_band,
                ),
                context="merge lineage conflict",
            ),
        ),
        (
            "merge-role-family-mismatch-fails",
            "split_merge_rules",
            False,
            lambda: _require_blocked(
                evaluate_merge_proposal(
                    proposal=MergeProposal.from_payload(
                        _merge_proposal_payload(
                            proposal_id="merge-003",
                            survivor_cell_id="cell-survivor",
                            merged_cell_id="cell-merged",
                            lineage_id=lineage_id,
                            reason="merge with role family conflict",
                        )
                    ),
                    survivor_record=_merge_record(
                        cell_id="cell-survivor",
                        lineage_id=lineage_id,
                        role_family="planner",
                        lifecycle_state="active",
                    ),
                    merged_record=_merge_record(
                        cell_id="cell-merged",
                        lineage_id=lineage_id,
                        role_family="router",
                        lifecycle_state="dormant",
                    ),
                    trust_band=standard_band,
                ),
                context="merge role-family mismatch",
            ),
        ),
    ]

    results = [run_case(*case) for case in cases]
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
        "supporting_modules_available": True,
        "runtime_imports": list(RUNTIME_IMPORTS),
        "supporting_imports": list(SUPPORTING_IMPORTS),
        "checked_files": [
            *PLAN_REFS,
            *SUPPORTING_EVIDENCE_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "results": [item.to_dict() for item in results],
        "runtime_exports": {
            "modules": {name: _module_public_names(module) for name, module in modules.items()},
            "trust_band": {
                "standard_type": type(standard_band).__name__,
                "guarded_type": type(guarded_band).__name__,
            },
            "fixtures": {
                "lineage_id": lineage_id,
                "tissue_id": tissue_id,
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
            "split/merge checks are case-driven and use the actual runtime API when the runtime file exists",
            "lineage, role-family/tissue compatibility, and policy bounds are exercised explicitly",
            "no approval implied",
        ],
    }


def run_case(case_id: str, target: str, expected_pass: bool, fn) -> CaseResult:
    try:
        result = fn()
    except Exception as exc:  # noqa: BLE001 - surfaced in the report.
        if expected_pass:
            return CaseResult(case_id, target, expected_pass, False, f"unexpected failure: {exc}")
        return CaseResult(case_id, target, expected_pass, True, f"failed as expected: {exc}")
    if expected_pass:
        return CaseResult(case_id, target, expected_pass, True, "passed")
    if _decision_allowed(result):
        return CaseResult(case_id, target, expected_pass, False, "unexpected pass")
    return CaseResult(case_id, target, expected_pass, True, f"failed as expected: {_decision_reason(result)}")


def main() -> int:
    runtime_missing = missing_files([RUNTIME_DIR / filename for filename in RUNTIME_FILES])
    if runtime_missing:
        report = build_blocked_report(runtime_missing)
        dump_json(REPORT_PATH, report)
        refresh_evidence_manifest()
        print("phase_3 slice_3 split/merge verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    try:
        report = build_pass_report()
    except Exception as exc:  # noqa: BLE001 - surfaced in the report.
        report = {
            "phase": PHASE_LABEL,
            "slice": SLICE_ID,
            "verification": VERIFICATION_NAME,
            "status": "fail",
            "runtime_modules_available": True,
            "supporting_modules_available": supporting_modules_available(),
            "runtime_imports": list(RUNTIME_IMPORTS),
            "supporting_imports": list(SUPPORTING_IMPORTS),
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

    dump_json(REPORT_PATH, report)
    refresh_evidence_manifest()
    print("phase_3 slice_3 split/merge verifier: PASS" if report.get("summary", {}).get("overall_pass") else "phase_3 slice_3 split/merge verifier: FAIL")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("summary", {}).get("overall_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
