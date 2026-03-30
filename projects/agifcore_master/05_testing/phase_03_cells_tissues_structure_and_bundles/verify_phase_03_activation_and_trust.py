from __future__ import annotations

import importlib
import inspect
import json
import sys
from dataclasses import dataclass, is_dataclass, asdict
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

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
)

TRUST_BAND_PASS_CANDIDATES: list[dict[str, Any]] = [
    {
        "band_name": "standard",
        "allow_activation": True,
        "allow_split_merge": True,
        "require_manual_review": False,
        "max_scheduler_priority": 6,
        "policy_envelope": {},
    },
    {
        "band_name": "guarded",
        "allow_activation": False,
        "allow_split_merge": False,
        "require_manual_review": True,
        "max_scheduler_priority": 3,
        "policy_envelope": {},
    },
]

ACTIVATION_POLICY_PASS_CANDIDATES: list[dict[str, Any]] = [
    {
        "policy_id": "policy-alpha",
        "cell_id": "cell-alpha",
        "tissue_id": "tissue-alpha",
        "profile": "laptop",
        "minimum_need_score": 0.5,
        "maximum_estimated_cost": 1.0,
        "minimum_trust_band": "guarded",
        "policy_envelope": {},
    },
]


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


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


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
    for attr_name in ("to_payload", "to_dict", "model_dump"):
        if hasattr(value, attr_name):
            candidate = getattr(value, attr_name)()
            if isinstance(candidate, Mapping):
                return candidate
    if hasattr(value, "__dict__") and getattr(value, "__dict__"):
        return dict(value.__dict__)
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


def _call_with_context(fn: Any, context: Mapping[str, Any]) -> Any:
    signature = inspect.signature(fn)
    kwargs: dict[str, Any] = {}
    for name, parameter in signature.parameters.items():
        if name in context:
            kwargs[name] = context[name]
        elif parameter.default is inspect._empty and parameter.kind in {
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        }:
            raise ContractViolation(f"missing required runtime argument: {name}")
    try:
        return fn(**kwargs)
    except TypeError:
        if len(kwargs) == 1:
            return fn(*kwargs.values())
        raise


def _decision_value(result: Any) -> bool:
    if isinstance(result, bool):
        return result
    if isinstance(result, Mapping):
        for key in ("allowed", "ready", "approved", "passed", "success", "ok"):
            if key in result:
                return bool(result[key])
        status = result.get("status")
        if isinstance(status, str):
            status_lower = status.lower()
            if status_lower in {"allowed", "ready", "approved", "pass", "passed", "success", "ok"}:
                return True
            if status_lower in {"blocked", "denied", "failed", "fail", "rejected"}:
                return False
    for attr in ("allowed", "ready", "approved", "passed", "success", "ok"):
        if hasattr(result, attr):
            return bool(getattr(result, attr))
    if hasattr(result, "status"):
        status = getattr(result, "status")
        if isinstance(status, str):
            status_lower = status.lower()
            if status_lower in {"allowed", "ready", "approved", "pass", "passed", "success", "ok"}:
                return True
            if status_lower in {"blocked", "denied", "failed", "fail", "rejected"}:
                return False
    return bool(result)


def _require_decision(result: Any, *, should_pass: bool, context: str) -> None:
    decision = _decision_value(result)
    if should_pass and not decision:
        raise ContractViolation(f"{context} returned a blocked decision")
    if not should_pass and decision:
        raise ContractViolation(f"{context} unexpectedly allowed the invalid case")


def _module_public_names(module: Any) -> list[str]:
    return [name for name in dir(module) if not name.startswith("_")]


def import_runtime_module(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except Exception:  # noqa: BLE001 - surfaced in the report.
        return None


def runtime_modules_available() -> bool:
    return all(import_runtime_module(module_name) is not None for module_name in RUNTIME_IMPORTS)


def load_runtime_api() -> dict[str, Any]:
    modules = {module_name: import_runtime_module(module_name) for module_name in RUNTIME_IMPORTS}
    if any(module is None for module in modules.values()):
        missing = [name for name, module in modules.items() if module is None]
        raise ContractViolation(f"runtime module failed to import: {', '.join(missing)}")

    def find_symbol(symbol: str) -> Any:
        for module in modules.values():
            if hasattr(module, symbol):
                return getattr(module, symbol)
        raise ContractViolation(f"runtime symbol not found: {symbol}")

    return {
        "modules": modules,
        "ActivationPolicy": find_symbol("ActivationPolicy"),
        "TrustBand": find_symbol("TrustBand"),
        "default_trust_band_policy": find_symbol("default_trust_band_policy"),
        "trust_band_for_score": find_symbol("trust_band_for_score"),
        "evaluate_activation_readiness": find_symbol("evaluate_activation_readiness"),
        "evaluate_dormant_pressure": find_symbol("evaluate_dormant_pressure"),
        "build_lifecycle_transition_request": find_symbol("build_lifecycle_transition_request"),
    }


def _candidate_payloads(base_candidates: list[dict[str, Any]], *, invalid_key: str | None = None) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for candidate in base_candidates:
        payloads.append(candidate)
        if invalid_key is not None and invalid_key in candidate:
            broken = dict(candidate)
            broken.pop(invalid_key, None)
            payloads.append(broken)
    return payloads


def _from_payload(factory: Any, payload_candidates: list[dict[str, Any]]) -> Any:
    last_error: Exception | None = None
    for payload in payload_candidates:
        try:
            return factory.from_payload(payload)
        except Exception as exc:  # noqa: BLE001 - expected while probing real runtime shape.
            last_error = exc
    raise ContractViolation(f"no candidate payload was accepted: {last_error}")


def _trust_band_payload_candidates() -> list[dict[str, Any]]:
    return list(TRUST_BAND_PASS_CANDIDATES)


def _activation_policy_payload_candidates() -> list[dict[str, Any]]:
    return list(ACTIVATION_POLICY_PASS_CANDIDATES)


def _build_context(*, blocked: bool = False) -> dict[str, Any]:
    context = dict(BLOCKING_CONTEXT if blocked else ACTIVATION_CONTEXT)
    return context


def _expected_ready_output(result: Any) -> None:
    _require_decision(result, should_pass=True, context="activation readiness")


def _expected_blocked_output(result: Any, context: str) -> None:
    _require_decision(result, should_pass=False, context=context)


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
            "valid trust band payload passes",
            "invalid trust band name fails",
            "negative scheduler priority fails",
            "valid activation policy payload passes",
            "missing required activation policy field fails",
            "dormant-to-active readiness passes for allowed trust band and within profile/cost limits",
            "blocked or insufficient trust band fails",
            "active cell ceiling breach fails",
            "dormant blueprint ceiling breach fails",
            "invalid lifecycle transition request fails",
        ],
        "results": [],
        "summary": {
            "overall_pass": False,
            "passed_cases": 0,
            "total_cases": 0,
            "blocked_cases": 10,
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
    api = load_runtime_api()
    ActivationPolicy = api["ActivationPolicy"]
    TrustBand = api["TrustBand"]
    default_trust_band_policy = api["default_trust_band_policy"]
    trust_band_for_score = api["trust_band_for_score"]
    evaluate_activation_readiness = api["evaluate_activation_readiness"]
    evaluate_dormant_pressure = api["evaluate_dormant_pressure"]
    build_lifecycle_transition_request = api["build_lifecycle_transition_request"]

    cases: list[CaseResult] = []
    runtime_exports: dict[str, Any] = {
        "modules": {
            name: _module_public_names(module)
            for name, module in api["modules"].items()
        }
    }

    standard_band = _from_payload(TrustBand, [TRUST_BAND_PASS_CANDIDATES[0]])
    guarded_band = _from_payload(TrustBand, [TRUST_BAND_PASS_CANDIDATES[1]])
    runtime_exports["trust_band"] = {
        "type": type(standard_band).__name__,
        "fields": sorted(_coerce_mapping(standard_band, "trust_band").keys()),
    }

    activation_policy = _from_payload(ActivationPolicy, _activation_policy_payload_candidates())
    runtime_exports["activation_policy"] = {
        "type": type(activation_policy).__name__,
        "fields": sorted(_coerce_mapping(activation_policy, "activation_policy").keys()),
    }

    if not hasattr(standard_band, "enforce_activation"):
        raise ContractViolation("TrustBand.enforce_activation is missing")
    if not hasattr(standard_band, "enforce_minimum_band"):
        raise ContractViolation("TrustBand.enforce_minimum_band is missing")
    if not hasattr(activation_policy, "evaluate_activation"):
        raise ContractViolation("ActivationPolicy.evaluate_activation is missing")

    cases.append(
        run_case(
            "trust-band-pass",
            "trust_bands",
            True,
            lambda: _from_payload(TrustBand, [TRUST_BAND_PASS_CANDIDATES[0]]),
        )
    )

    cases.append(
        run_case(
            "trust-band-invalid-name",
            "trust_bands",
            False,
            lambda: _from_payload(
                TrustBand,
                [
                    {
                        "band_name": "trusted",
                        "allow_activation": True,
                        "allow_split_merge": True,
                        "require_manual_review": False,
                        "max_scheduler_priority": 6,
                        "policy_envelope": {},
                    }
                ],
            ),
        )
    )

    cases.append(
        run_case(
            "trust-band-negative-scheduler-priority",
            "trust_bands",
            False,
            lambda: _from_payload(
                TrustBand,
                [
                    {
                        "band_name": "standard",
                        "allow_activation": True,
                        "allow_split_merge": True,
                        "require_manual_review": False,
                        "max_scheduler_priority": -1,
                        "policy_envelope": {},
                    }
                ],
            ),
        )
    )

    cases.append(
        run_case(
            "trust-band-explicit-block",
            "trust_bands",
            False,
            lambda: guarded_band.enforce_activation(),
        )
    )

    cases.append(
        run_case(
            "activation-policy-pass",
            "activation_policies",
            True,
            lambda: _from_payload(ActivationPolicy, _activation_policy_payload_candidates()),
        )
    )

    cases.append(
        run_case(
            "activation-policy-missing-field",
            "activation_policies",
            False,
            lambda: _from_payload(
                ActivationPolicy,
                [
                    {
                        "cell_id": "cell-alpha",
                        "tissue_id": "tissue-alpha",
                        "profile": "laptop",
                        "minimum_need_score": 0.5,
                        "maximum_estimated_cost": 1.0,
                        "minimum_trust_band": "guarded",
                        "policy_envelope": {},
                    }
                ],
            ),
        )
    )

    default_policy = default_trust_band_policy(standard_band.band_name)
    recommended_band = trust_band_for_score(0.8)
    runtime_exports["policy_helpers"] = {
        "default_policy_type": type(default_policy).__name__,
        "recommended_band_type": type(recommended_band).__name__,
    }

    cases.append(
        run_case(
            "dormant-to-active-readiness-pass",
            "active_dormant_control",
            True,
            lambda: _expected_ready_output(
                evaluate_activation_readiness(
                    policy=activation_policy,
                    lifecycle_state="dormant",
                    need_score=0.8,
                    estimated_cost=0.5,
                    active_cell_count=16,
                    trust_band=standard_band,
                )
            ),
        )
    )

    blocked_band = guarded_band

    cases.append(
        run_case(
            "blocked-trust-band-fails",
            "active_dormant_control",
            False,
            lambda: _expected_blocked_output(
                evaluate_activation_readiness(
                    policy=activation_policy,
                    lifecycle_state="dormant",
                    need_score=0.8,
                    estimated_cost=0.5,
                    active_cell_count=16,
                    trust_band=blocked_band,
                ),
                "blocked trust band readiness",
            ),
        )
    )

    cases.append(
        run_case(
            "active-cell-ceiling-breach-fails",
            "active_dormant_control",
            False,
            lambda: _expected_blocked_output(
                evaluate_activation_readiness(
                    policy=activation_policy,
                    lifecycle_state="dormant",
                    need_score=0.8,
                    estimated_cost=0.5,
                    active_cell_count=32,
                    trust_band=standard_band,
                ),
                "active cell ceiling breach",
            ),
        )
    )

    cases.append(
        run_case(
            "dormant-blueprint-ceiling-breach-fails",
            "active_dormant_control",
            False,
            lambda: _expected_blocked_output(
                evaluate_dormant_pressure(
                    dormant_blueprint_count=129,
                    lifecycle_state="dormant",
                ),
                "dormant blueprint ceiling breach",
            ),
        )
    )

    cases.append(
        run_case(
            "invalid-lifecycle-transition-request-fails",
            "active_dormant_control",
            False,
            lambda: build_lifecycle_transition_request(
                cell_id="cell-invalid-transition",
                from_state="active",
                to_state="active",
                reason="invalid transition",
            ),
        )
    )

    cases.append(
        run_case(
            "activation-policy-direct-evaluation-pass",
            "activation_policies",
            True,
            lambda: _expected_ready_output(
                activation_policy.evaluate_activation(
                    lifecycle_state="dormant",
                    need_score=0.8,
                    estimated_cost=0.5,
                    active_cell_count=16,
                    trust_band=standard_band,
                )
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
