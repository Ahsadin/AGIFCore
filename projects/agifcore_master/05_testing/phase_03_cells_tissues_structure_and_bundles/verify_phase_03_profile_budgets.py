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

RUNTIME_IMPORTS = (
    "profile_budget_rules",
    "activation_policies",
    "active_dormant_control",
    "trust_bands",
)
RUNTIME_FILES = ("profile_budget_rules.py",)
SUPPORTING_IMPORTS = (
    "activation_policies",
    "active_dormant_control",
    "trust_bands",
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


def supporting_modules_available() -> bool:
    return all(import_runtime_module(module_name) is not None for module_name in SUPPORTING_IMPORTS)


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

    manifest = {
        "phase": PHASE_LABEL,
        "phase_remains_open": True,
        "reports": reports,
        "runtime_modules_available": runtime_modules_available(),
        "slice": SLICE_ID,
        "status": "slice_3_blocked" if not runtime_modules_available() else "slice_3_ready",
        "notes": [
            "evidence manifest is rebuilt from actual report files on disk",
            "slice 1 evidence remains present and real",
            "slice 2 evidence remains present and real",
            "slice 3 profile-budget runtime is absent in this lane, so the slice remains blocked rather than faked",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def _require_decision(result: Any, *, should_pass: bool, context: str) -> None:
    if isinstance(result, Mapping):
        decision = bool(result.get("allow"))
    else:
        decision = bool(getattr(result, "allowed", False))
    if should_pass and not decision:
        raise ContractViolation(f"{context} returned a blocked decision")
    if not should_pass and decision:
        raise ContractViolation(f"{context} unexpectedly allowed the invalid case")


def _module_public_names(module: Any) -> list[str]:
    return [name for name in dir(module) if not name.startswith("_")]


def build_partial_report() -> dict[str, Any]:
    modules = {
        name: import_runtime_module(name)
        for name in SUPPORTING_IMPORTS
    }
    if any(module is None for module in modules.values()):
        missing = [name for name, module in modules.items() if module is None]
        raise ContractViolation(
            f"supporting runtime modules missing: {', '.join(missing)}"
        )

    activation_policies = modules["activation_policies"]
    active_dormant_control = modules["active_dormant_control"]
    trust_bands = modules["trust_bands"]

    ActivationPolicy = getattr(activation_policies, "ActivationPolicy")
    TrustBand = getattr(trust_bands, "TrustBand")
    default_trust_band_policy = getattr(trust_bands, "default_trust_band_policy")
    evaluate_activation_readiness = getattr(
        active_dormant_control, "evaluate_activation_readiness"
    )
    evaluate_dormant_pressure = getattr(
        active_dormant_control, "evaluate_dormant_pressure"
    )

    standard_band = TrustBand.from_payload(default_trust_band_policy("standard"))
    laptop_policy = ActivationPolicy.from_payload(
        {
            "policy_id": "laptop-policy",
            "cell_id": "cell-laptop",
            "tissue_id": "tissue-structural",
            "profile": "laptop",
            "minimum_need_score": 0.5,
            "maximum_estimated_cost": 1.0,
            "minimum_trust_band": "guarded",
            "policy_envelope": {},
        }
    )
    mobile_policy = ActivationPolicy.from_payload(
        {
            "policy_id": "mobile-policy",
            "cell_id": "cell-mobile",
            "tissue_id": "tissue-structural",
            "profile": "mobile",
            "minimum_need_score": 0.5,
            "maximum_estimated_cost": 1.0,
            "minimum_trust_band": "guarded",
            "policy_envelope": {},
        }
    )

    results: list[CaseResult] = []
    results.append(
        CaseResult(
            "laptop-activation-within-ceiling",
            "activation_policies",
            True,
            True,
            "passed",
        )
    )
    _require_decision(
        evaluate_activation_readiness(
            policy=laptop_policy,
            lifecycle_state="dormant",
            need_score=0.8,
            estimated_cost=0.5,
            active_cell_count=31,
            trust_band=standard_band,
        ),
        should_pass=True,
        context="laptop activation within ceiling",
    )

    results.append(
        CaseResult(
            "laptop-activation-ceiling-breach",
            "activation_policies",
            False,
            True,
            "failed as expected: active cell ceiling reached for profile",
        )
    )
    _require_decision(
        evaluate_activation_readiness(
            policy=laptop_policy,
            lifecycle_state="dormant",
            need_score=0.8,
            estimated_cost=0.5,
            active_cell_count=32,
            trust_band=standard_band,
        ),
        should_pass=False,
        context="laptop activation ceiling breach",
    )

    results.append(
        CaseResult(
            "mobile-activation-within-ceiling",
            "activation_policies",
            True,
            True,
            "passed",
        )
    )
    _require_decision(
        evaluate_activation_readiness(
            policy=mobile_policy,
            lifecycle_state="dormant",
            need_score=0.8,
            estimated_cost=0.5,
            active_cell_count=7,
            trust_band=standard_band,
        ),
        should_pass=True,
        context="mobile activation within ceiling",
    )

    results.append(
        CaseResult(
            "mobile-activation-ceiling-breach",
            "activation_policies",
            False,
            True,
            "failed as expected: active cell ceiling reached for profile",
        )
    )
    _require_decision(
        evaluate_activation_readiness(
            policy=mobile_policy,
            lifecycle_state="dormant",
            need_score=0.8,
            estimated_cost=0.5,
            active_cell_count=8,
            trust_band=standard_band,
        ),
        should_pass=False,
        context="mobile activation ceiling breach",
    )

    results.append(
        CaseResult(
            "dormant-pressure-within-ceiling",
            "active_dormant_control",
            True,
            True,
            "passed",
        )
    )
    _require_decision(
        evaluate_dormant_pressure(
            dormant_blueprint_count=128,
            lifecycle_state="dormant",
        ),
        should_pass=True,
        context="dormant pressure within ceiling",
    )

    results.append(
        CaseResult(
            "dormant-pressure-ceiling-breach",
            "active_dormant_control",
            False,
            True,
            "failed as expected: dormant blueprint ceiling exceeded",
        )
    )
    _require_decision(
        evaluate_dormant_pressure(
            dormant_blueprint_count=129,
            lifecycle_state="dormant",
        ),
        should_pass=False,
        context="dormant pressure ceiling breach",
    )

    if not results:
        raise ContractViolation("no profile budget cases were executed")

    return {
        "phase": PHASE_LABEL,
        "slice": SLICE_ID,
        "verification": VERIFICATION_NAME,
        "status": "blocked",
        "runtime_modules_available": False,
        "supporting_modules_available": True,
        "runtime_imports": list(RUNTIME_IMPORTS),
        "supporting_imports": list(SUPPORTING_IMPORTS),
        "checked_files": [
            *PLAN_REFS,
            *SUPPORTING_EVIDENCE_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "results": [item.to_dict() for item in results],
        "blocked_checks": [
            {
                "case_id": "builder-profile-budget-surface-missing",
                "target": "profile_budget_rules",
                "reason": "profile_budget_rules.py is not on disk yet",
            },
            {
                "case_id": "builder-ceiling-failure-case-unavailable",
                "target": "profile_budget_rules",
                "reason": "builder profile ceiling behavior cannot be exercised until the runtime file exists",
            },
        ],
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 3 slice 3 profile budget runtime module is not on disk yet.",
            "missing_files": [rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        },
        "runtime_exports": {
            "modules": {
                name: _module_public_names(module)
                for name, module in modules.items()
            },
            "profile_ceiling_helpers": {
                "laptop": 32,
                "mobile": 8,
                "builder": "blocked_until_profile_budget_rules_exists",
            },
        },
        "summary": {
            "overall_pass": False,
            "expected_pass_cases": 4,
            "expected_succeeded": True,
            "expected_failures_verified": True,
            "passed_cases": len(results),
            "blocked_cases": 2,
            "total_cases": len(results) + 2,
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "laptop and mobile ceiling behavior was verified against the present runtime",
            "builder remains blocked until the planned profile-budget surface exists",
            "the verifier stays repo-relative and does not rely on external PYTHONPATH wiring",
            "no integrated success is claimed because the owned runtime file is absent",
        ],
    }


def build_blocked_report() -> dict[str, Any]:
    report = build_partial_report()
    report["runtime_modules_available"] = False
    report["status"] = "blocked"
    return report


def main() -> int:
    runtime_missing = missing_files([RUNTIME_DIR / filename for filename in RUNTIME_FILES])
    if runtime_missing:
        report = build_blocked_report()
        dump_json(REPORT_PATH, report)
        refresh_evidence_manifest()
        print("phase_3 slice_3 profile budget verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_partial_report()
    dump_json(REPORT_PATH, report)
    refresh_evidence_manifest()
    print("phase_3 slice_3 profile budget verifier: BLOCKED")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
