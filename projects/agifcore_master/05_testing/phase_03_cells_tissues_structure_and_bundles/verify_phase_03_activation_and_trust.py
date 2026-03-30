from __future__ import annotations

import importlib
import json
import sys
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_03_cells_tissues_structure_and_bundles"
PHASE_LABEL = "Phase 3"
SLICE_ID = "slice_2"
VERIFICATION_NAME = "activation_and_trust"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"

RUNTIME_IMPORTS = (
    "activation_policies",
    "trust_bands",
    "active_dormant_control",
)

RUNTIME_FILES = (
    "activation_policies.py",
    "trust_bands.py",
    "active_dormant_control.py",
)

EXPECTED_PUBLIC_HINTS = {
    "activation_policies": ("activation", "policy"),
    "trust_bands": ("trust", "band"),
    "active_dormant_control": ("active", "dormant", "control"),
}

EXPECTED_SURFACE_KEYS = {
    "activation_policies": ("policy_id", "rules", "fail_closed"),
    "trust_bands": ("band_id", "rank", "fail_closed"),
    "active_dormant_control": ("control_id", "active_states", "dormant_states", "profile_scope"),
}

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
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
REPORT_PATH = EVIDENCE_DIR / "phase_03_activation_and_trust_report.json"
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


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def _require_non_empty_str(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ContractViolation(f"{field_name} must be a non-empty string")


def _require_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractViolation(f"{field_name} must be a mapping")
    return value


def _coerce_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    raise ContractViolation(f"{field_name} must be a mapping or dataclass instance")


def _require_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ContractViolation(f"{field_name} must be a list")
    result: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ContractViolation(f"{field_name} entries must be non-empty strings")
        if item in seen:
            raise ContractViolation(f"{field_name} contains duplicate entries")
        seen.add(item)
        result.append(item)
    return result


def _module_public_names(module: Any) -> list[str]:
    return [name for name in dir(module) if not name.startswith("_")]


def _pick_surface_object(module: Any, module_name: str) -> tuple[str, Any]:
    public_names = _module_public_names(module)
    hints = EXPECTED_PUBLIC_HINTS[module_name]
    preferred_names = [
        name
        for name in getattr(module, "__all__", [])
        if name in public_names
    ]
    preferred_names.extend(
        name
        for name in public_names
        if any(hint in name.lower() for hint in hints)
    )
    preferred_names.extend(
        name
        for name in public_names
        if name.isupper()
    )

    seen: set[str] = set()
    for name in preferred_names:
        if name in seen:
            continue
        seen.add(name)
        value = getattr(module, name)
        if isinstance(value, Mapping) or (is_dataclass(value) and not isinstance(value, type)):
            return name, value
    raise ContractViolation(
        f"{module_name} did not expose an inspectable policy surface"
    )


def validate_activation_policy(policy: Mapping[str, Any]) -> None:
    for field in EXPECTED_SURFACE_KEYS["activation_policies"]:
        if field not in policy:
            raise ContractViolation(f"missing required activation policy field: {field}")
    _require_non_empty_str(policy["policy_id"], "policy_id")
    _require_mapping(policy["rules"], "rules")
    if not isinstance(policy["fail_closed"], bool):
        raise ContractViolation("fail_closed must be a boolean")
    if canonical_size_bytes(dict(policy)) > 64 * 1024:
        raise ContractViolation("activation policy exceeds max manifest size")


def validate_trust_band(trust_band: Mapping[str, Any]) -> None:
    for field in EXPECTED_SURFACE_KEYS["trust_bands"]:
        if field not in trust_band:
            raise ContractViolation(f"missing required trust band field: {field}")
    _require_non_empty_str(trust_band["band_id"], "band_id")
    if not isinstance(trust_band["rank"], int) or trust_band["rank"] < 0:
        raise ContractViolation("rank must be a non-negative integer")
    if not isinstance(trust_band["fail_closed"], bool):
        raise ContractViolation("fail_closed must be a boolean")
    if canonical_size_bytes(dict(trust_band)) > 64 * 1024:
        raise ContractViolation("trust band exceeds max manifest size")


def validate_active_dormant_control(control: Mapping[str, Any]) -> None:
    for field in EXPECTED_SURFACE_KEYS["active_dormant_control"]:
        if field not in control:
            raise ContractViolation(f"missing required active/dormant control field: {field}")
    _require_non_empty_str(control["control_id"], "control_id")
    _require_str_list(control["active_states"], "active_states")
    _require_str_list(control["dormant_states"], "dormant_states")
    _require_non_empty_str(control["profile_scope"], "profile_scope")
    if not isinstance(control["fail_closed"], bool):
        raise ContractViolation("fail_closed must be a boolean")
    if canonical_size_bytes(dict(control)) > 64 * 1024:
        raise ContractViolation("active/dormant control exceeds max manifest size")


def import_runtime_module(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except Exception:  # noqa: BLE001 - surfaced in the report.
        return None


def runtime_modules_available() -> bool:
    return all(import_runtime_module(module_name) is not None for module_name in RUNTIME_IMPORTS)


def run_case(case_id: str, target: str, expected_pass: bool, fn) -> CaseResult:
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 - surfaced in the report.
        if expected_pass:
            return CaseResult(case_id, target, expected_pass, False, f"unexpected failure: {exc}")
        return CaseResult(case_id, target, expected_pass, True, f"failed as expected: {exc}")
    if expected_pass:
        return CaseResult(case_id, target, expected_pass, True, "passed")
    return CaseResult(case_id, target, expected_pass, False, "unexpected pass")


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
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 3 slice 2 activation/trust runtime modules are not on disk yet.",
            "missing_files": missing,
        },
        "planned_checks": [
            "activation-policy-surface-importable",
            "trust-band-surface-importable",
            "active-dormant-control-surface-importable",
            "activation-policy-rejects-missing-required-fields",
            "trust-band-rejects-invalid-rank-and-band-id",
            "active-dormant-control-rejects-empty-state-lists",
        ],
        "results": [],
        "summary": {
            "overall_pass": False,
            "passed_cases": 0,
            "total_cases": 0,
            "blocked_cases": 3,
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "no runtime checks were executed because the phase-3 slice-2 modules are absent",
            "report is intentionally blocked instead of pretending the verifier passed",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, Any]:
    modules = {module_name: import_runtime_module(module_name) for module_name in RUNTIME_IMPORTS}
    cases: list[CaseResult] = []
    runtime_exports: dict[str, Any] = {}

    for module_name, module in modules.items():
        if module is None:
            raise ContractViolation(f"runtime module failed to import: {module_name}")
        surface_name, surface_value = _pick_surface_object(module, module_name)
        surface = _coerce_mapping(surface_value, f"{module_name}.{surface_name}")
        runtime_exports[module_name] = {
            "surface_name": surface_name,
            "public_names": _module_public_names(module),
            "surface_keys": sorted(surface.keys()),
        }
        if module_name == "activation_policies":
            validate_activation_policy(surface)
            cases.append(
                run_case(
                    "activation-policy-pass",
                    "activation_policies",
                    True,
                    lambda: validate_activation_policy(surface),
                )
            )
            cases.append(
                run_case(
                    "activation-policy-missing-field",
                    "activation_policies",
                    False,
                    lambda: validate_activation_policy(
                        {
                            **surface,
                            "rules": {k: v for k, v in surface["rules"].items() if k != "fail_closed"},
                        }
                    ),
                )
            )
        elif module_name == "trust_bands":
            validate_trust_band(surface)
            cases.append(
                run_case(
                    "trust-band-pass",
                    "trust_bands",
                    True,
                    lambda: validate_trust_band(surface),
                )
            )
            cases.append(
                run_case(
                    "trust-band-invalid-rank",
                    "trust_bands",
                    False,
                    lambda: validate_trust_band({**surface, "rank": -1}),
                )
            )
        elif module_name == "active_dormant_control":
            validate_active_dormant_control(surface)
            cases.append(
                run_case(
                    "active-dormant-control-pass",
                    "active_dormant_control",
                    True,
                    lambda: validate_active_dormant_control(surface),
                )
            )
            cases.append(
                run_case(
                    "active-dormant-control-empty-state-lists",
                    "active_dormant_control",
                    False,
                    lambda: validate_active_dormant_control(
                        {**surface, "active_states": [], "dormant_states": []}
                    ),
                )
            )

    if not cases:
        raise ContractViolation("no activation/trust cases were executed")

    passed_count = sum(1 for item in cases if item.passed)
    expected_pass_count = sum(1 for item in cases if item.expected_pass)
    all_expected_succeeded = all(item.passed for item in cases if item.expected_pass)
    all_expected_failures_failed = all(item.passed for item in cases if not item.expected_pass)

    return {
        "phase": PHASE_LABEL,
        "slice": SLICE_ID,
        "verification": VERIFICATION_NAME,
        "status": "pass" if all_expected_succeeded and all_expected_failures_failed else "fail",
        "runtime_modules_available": True,
        "runtime_imports": list(RUNTIME_IMPORTS),
        "runtime_exports": runtime_exports,
        "checked_files": [
            *PLAN_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "results": [item.to_dict() for item in cases],
        "summary": {
            "overall_pass": all_expected_succeeded and all_expected_failures_failed,
            "expected_pass_cases": expected_pass_count,
            "expected_succeeded": all_expected_succeeded,
            "expected_failures_verified": all_expected_failures_failed,
            "passed_cases": passed_count,
            "total_cases": len(cases),
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "activation trust checks remain local-first and fail-closed",
            "no approval implied",
        ],
    }


def build_manifest() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    for report_path in sorted(EVIDENCE_DIR.glob("*_report.json")):
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        overall_pass = payload.get("overall_pass")
        if overall_pass is None:
            summary = payload.get("summary")
            if isinstance(summary, Mapping):
                overall_pass = summary.get("overall_pass")
        reports.append(
            {
                "report_id": report_path.stem.removeprefix("phase_03_").removesuffix("_report"),
                "path": str(report_path),
                "overall_pass": bool(overall_pass),
            }
        )
    runtime_files_exist = all((RUNTIME_DIR / filename).exists() for filename in RUNTIME_FILES)
    return {
        "notes": [
            "evidence manifest is rebuilt from actual report files on disk",
            "slice 2 is blocked until the phase-3 activation and trust runtime exists",
            "slice 1 evidence remains present and real",
        ],
        "phase": PHASE_LABEL,
        "phase_remains_open": True,
        "reports": reports,
        "runtime_modules_available": runtime_files_exist,
        "slice": SLICE_ID,
        "status": "slice_2_blocked" if not runtime_files_exist else "slice_2_ready",
    }


def main() -> int:
    runtime_missing = missing_files([RUNTIME_DIR / filename for filename in RUNTIME_FILES])
    if runtime_missing:
        report = build_blocked_report(runtime_missing)
        dump_json(REPORT_PATH, report)
        dump_json(MANIFEST_PATH, build_manifest())
        print("phase_3 slice_2 activation/trust verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    dump_json(REPORT_PATH, report)
    dump_json(MANIFEST_PATH, build_manifest())
    print("phase_3 slice_2 activation/trust verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
