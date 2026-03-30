from __future__ import annotations

import importlib
import json
import sys
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_03_cells_tissues_structure_and_bundles"
PHASE_LABEL = "Phase 3"
SLICE_ID = "slice_4"
VERIFICATION_NAME = "bundle_integrity"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"

RUNTIME_IMPORTS = (
    "bundle_integrity_checks",
    "bundle_manifest",
    "bundle_schema_validation",
    "cell_contracts",
    "tissue_manifests",
)

RUNTIME_FILES = (
    "bundle_integrity_checks.py",
    "bundle_manifest.py",
    "bundle_schema_validation.py",
    "cell_contracts.py",
    "tissue_manifests.py",
    "schemas/phase_03_bundle_manifest.schema.json",
    "schemas/phase_03_cell_contract.schema.json",
    "schemas/phase_03_tissue_manifest.schema.json",
)

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
)

SUPPORTING_EVIDENCE_REFS = (
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_cell_contracts_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_activation_and_trust_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_validation_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_profile_budget_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_split_merge_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_tissue_orchestration_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json",
)

MAX_BUNDLE_SIZE_BYTES = 8 * 1024 * 1024


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
REPORT_PATH = EVIDENCE_DIR / "phase_03_bundle_integrity_report.json"
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


def _coerce_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    for attr_name in ("to_dict", "to_payload", "model_dump"):
        if hasattr(value, attr_name):
            candidate = getattr(value, attr_name)()
            if isinstance(candidate, Mapping):
                return candidate
    if hasattr(value, "__dict__") and getattr(value, "__dict__"):
        return dict(value.__dict__)
    raise ContractViolation(f"{field_name} must be a mapping or dataclass instance")


def _require_success(result: Any, context: str) -> Any:
    if result is None:
        return None
    if isinstance(result, bool):
        if not result:
            raise ContractViolation(f"{context} returned false")
        return result
    if not _decision_value(result):
        raise ContractViolation(f"{context} blocked: {_decision_reason(result)}")
    return result


def _require_blocked(result: Any, context: str) -> Any:
    if result is None:
        return None
    if isinstance(result, bool):
        if result:
            return result
        raise ContractViolation(f"{context} blocked: {_decision_reason(result)}")
    if not _decision_value(result):
        raise ContractViolation(f"{context} blocked: {_decision_reason(result)}")
    return result


def _module_public_names(module: Any) -> list[str]:
    return [name for name in dir(module) if not name.startswith("_")]


def import_runtime_module(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except Exception:  # noqa: BLE001 - surfaced in the report.
        return None


def runtime_modules_available() -> bool:
    return all(import_runtime_module(module_name) is not None for module_name in RUNTIME_IMPORTS)


def supporting_modules_available() -> bool:
    return all(import_runtime_module(module_name) is not None for module_name in RUNTIME_IMPORTS if module_name != "bundle_integrity_checks")


def _decision_value(result: Any) -> bool:
    if isinstance(result, bool):
        return result
    if isinstance(result, Mapping):
        for key in ("allowed", "passed", "ok", "success", "integrity_ok", "allow"):
            if key in result:
                return bool(result[key])
        status = result.get("status")
        if isinstance(status, str):
            lowered = status.lower()
            if lowered in {"allowed", "ready", "approved", "pass", "passed", "success", "ok"}:
                return True
            if lowered in {"blocked", "denied", "failed", "fail", "rejected"}:
                return False
    for attr in ("allowed", "passed", "ok", "success", "integrity_ok", "allow"):
        if hasattr(result, attr):
            return bool(getattr(result, attr))
    if hasattr(result, "status"):
        status = getattr(result, "status")
        if isinstance(status, str):
            lowered = status.lower()
            if lowered in {"allowed", "ready", "approved", "pass", "passed", "success", "ok"}:
                return True
            if lowered in {"blocked", "denied", "failed", "fail", "rejected"}:
                return False
    return bool(result)


def _decision_reason(result: Any) -> str:
    if isinstance(result, Mapping):
        for key in ("reason", "message", "detail"):
            if key in result:
                return str(result.get(key, ""))
        return ""
    for attr in ("reason", "message", "detail"):
        if hasattr(result, attr):
            return str(getattr(result, attr))
    return ""


def _module_entrypoint(module: Any) -> tuple[str, Any]:
    for name in (
        "validate_bundle_integrity_payload",
        "validate_bundle_integrity",
        "evaluate_bundle_integrity",
        "check_bundle_integrity",
    ):
        if hasattr(module, name):
            return name, getattr(module, name)
    for name in ("BundleIntegrityCheck", "BundleIntegrity"):
        if hasattr(module, name):
            return name, getattr(module, name)
    raise ContractViolation(
        "runtime symbol not found: validate_bundle_integrity_payload, validate_bundle_integrity, evaluate_bundle_integrity, check_bundle_integrity, BundleIntegrityCheck, BundleIntegrity"
    )


def _invoke_entrypoint(entry_kind: str, entrypoint: Any, payload: Mapping[str, Any]) -> Any:
    if entry_kind in {"validate_bundle_integrity_payload", "validate_bundle_integrity", "evaluate_bundle_integrity", "check_bundle_integrity"}:
        return entrypoint(payload)
    instance = None
    if hasattr(entrypoint, "from_payload"):
        instance = entrypoint.from_payload(payload)
    else:
        instance = entrypoint(payload)
    if hasattr(instance, "validate"):
        return instance.validate()
    if hasattr(instance, "evaluate"):
        return instance.evaluate()
    if hasattr(instance, "check"):
        return instance.check()
    return instance


def _bundle_manifest_fixture() -> dict[str, Any]:
    cell_contract = {
        "cell_id": "cell-alpha",
        "bundle_ref": "bundle-alpha",
        "role_family": "planner",
        "role_name": "phase-3-planner",
        "allowed_tissues": ["tissue-orchestration"],
        "split_policy": {"mode": "governed"},
        "merge_policy": {"mode": "governed"},
        "trust_profile": {"band": "seed"},
        "policy_envelope": {"profile": "laptop"},
    }
    tissue_manifest = {
        "tissue_id": "tissue-orchestration",
        "tissue_name": "Orchestration Tissue",
        "allowed_role_families": ["planner"],
        "member_cell_ids": ["cell-alpha"],
        "routing_targets": ["bundle-validation"],
        "policy_envelope": {"profile": "laptop"},
    }
    return {
        "bundle_id": "bundle-alpha",
        "bundle_version": "1.0.0",
        "bundle_type": "phase_3_structure",
        "entry_contracts": ["cell-alpha"],
        "schema_refs": {
            "cell_contract": "schemas/phase_03_cell_contract.schema.json",
            "tissue_manifest": "schemas/phase_03_tissue_manifest.schema.json",
            "bundle_manifest": "schemas/phase_03_bundle_manifest.schema.json",
        },
        "payload_inventory": {
            "cell_contract": cell_contract,
            "tissue_manifest": tissue_manifest,
        },
        "provenance_fields": {
            "source_plan": "projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md",
            "phase": "phase_3",
            "integrity_mode": "slice_4",
        },
    }


def _broken_missing_manifest_field() -> dict[str, Any]:
    payload = _bundle_manifest_fixture()
    payload.pop("bundle_type", None)
    return payload


def _broken_missing_schema_ref() -> dict[str, Any]:
    payload = _bundle_manifest_fixture()
    payload["schema_refs"] = {
        "cell_contract": "schemas/phase_03_cell_contract.schema.json",
        "tissue_manifest": "schemas/phase_03_tissue_manifest.schema.json",
    }
    return payload


def _broken_nested_cell_contract() -> dict[str, Any]:
    payload = _bundle_manifest_fixture()
    payload["payload_inventory"]["cell_contract"]["allowed_tissues"] = "tissue-orchestration"  # type: ignore[assignment]
    return payload


def _broken_nested_tissue_manifest() -> dict[str, Any]:
    payload = _bundle_manifest_fixture()
    payload["payload_inventory"]["tissue_manifest"]["member_cell_ids"] = ["cell-alpha", "cell-alpha"]
    return payload


def _broken_inventory_missing_entry() -> dict[str, Any]:
    payload = _bundle_manifest_fixture()
    payload["payload_inventory"].pop("tissue_manifest", None)
    return payload


def _broken_oversized_bundle() -> dict[str, Any]:
    payload = _bundle_manifest_fixture()
    payload["provenance_fields"]["notes"] = "x" * (MAX_BUNDLE_SIZE_BYTES + 1024)
    return payload


def _run_case(case_id: str, target: str, expected_pass: bool, fn) -> CaseResult:
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
        "supporting_modules_available": supporting_modules_available(),
        "runtime_imports": list(RUNTIME_IMPORTS),
        "checked_files": [
            *PLAN_REFS,
            *SUPPORTING_EVIDENCE_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 3 slice 4 bundle integrity runtime module is not on disk yet.",
            "missing_files": missing,
        },
        "planned_checks": [
            "valid bundle manifest passes",
            "missing bundle field fails",
            "missing schema ref fails",
            "nested cell contract failure is caught",
            "nested tissue manifest failure is caught",
            "missing inventory entry fails",
            "oversized bundle fails",
        ],
        "results": [],
        "summary": {
            "overall_pass": False,
            "passed_cases": 0,
            "total_cases": 0,
            "blocked_cases": 7,
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "no runtime checks were executed because bundle_integrity_checks.py is absent",
            "the verifier stays repo-relative and does not rely on external PYTHONPATH wiring",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, Any]:
    runtime = import_runtime_module("bundle_integrity_checks")
    if runtime is None:
        raise ContractViolation("runtime module failed to import: bundle_integrity_checks")
    bundle_manifest_module = import_runtime_module("bundle_manifest")
    bundle_schema_module = import_runtime_module("bundle_schema_validation")
    cell_contracts_module = import_runtime_module("cell_contracts")
    tissue_manifests_module = import_runtime_module("tissue_manifests")
    if any(module is None for module in (bundle_manifest_module, bundle_schema_module, cell_contracts_module, tissue_manifests_module)):
        missing = [
            name
            for name, module in {
                "bundle_manifest": bundle_manifest_module,
                "bundle_schema_validation": bundle_schema_module,
                "cell_contracts": cell_contracts_module,
                "tissue_manifests": tissue_manifests_module,
            }.items()
            if module is None
        ]
        raise ContractViolation(f"runtime module failed to import: {', '.join(missing)}")

    entry_kind, entrypoint = _module_entrypoint(runtime)
    modules = {
        "bundle_integrity_checks": runtime,
        "bundle_manifest": bundle_manifest_module,
        "bundle_schema_validation": bundle_schema_module,
        "cell_contracts": cell_contracts_module,
        "tissue_manifests": tissue_manifests_module,
    }

    from bundle_schema_validation import validate_bundle_schema_foundation

    bundle = _bundle_manifest_fixture()
    validate_bundle_schema_foundation(bundle, base_dir=RUNTIME_DIR)
    _require_success(_invoke_entrypoint(entry_kind, entrypoint, bundle), "bundle integrity happy path")

    cases = [
        (
            "bundle-integrity-pass",
            "bundle_integrity_checks",
            True,
            lambda: _require_success(
                _invoke_entrypoint(entry_kind, entrypoint, _bundle_manifest_fixture()),
                "bundle integrity happy path",
            ),
        ),
        (
            "missing-bundle-field",
            "bundle_integrity_checks",
            False,
            lambda: _require_blocked(
                _invoke_entrypoint(entry_kind, entrypoint, _broken_missing_manifest_field()),
                "missing bundle field",
            ),
        ),
        (
            "missing-schema-ref",
            "bundle_schema_validation",
            False,
            lambda: validate_bundle_schema_foundation(_broken_missing_schema_ref(), base_dir=RUNTIME_DIR),
        ),
        (
            "nested-cell-contract-failure",
            "cell_contracts",
            False,
            lambda: validate_bundle_schema_foundation(_broken_nested_cell_contract(), base_dir=RUNTIME_DIR),
        ),
        (
            "nested-tissue-manifest-failure",
            "tissue_manifests",
            False,
            lambda: validate_bundle_schema_foundation(_broken_nested_tissue_manifest(), base_dir=RUNTIME_DIR),
        ),
        (
            "missing-inventory-entry",
            "bundle_integrity_checks",
            False,
            lambda: _require_blocked(
                _invoke_entrypoint(entry_kind, entrypoint, _broken_inventory_missing_entry()),
                "missing inventory entry",
            ),
        ),
        (
            "oversized-bundle",
            "bundle_integrity_checks",
            False,
            lambda: _require_blocked(
                _invoke_entrypoint(entry_kind, entrypoint, _broken_oversized_bundle()),
                "oversized bundle",
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
        if expected_pass:
            results.append(CaseResult(case_id, target, expected_pass, True, "passed"))
        else:
            results.append(CaseResult(case_id, target, expected_pass, False, "unexpected pass"))

    passed_count = sum(1 for item in results if item.passed)
    expected_pass_count = sum(1 for item in results if item.expected_pass)
    all_expected_succeeded = all(item.passed for item in results if item.expected_pass)
    all_expected_failures_failed = all(item.passed for item in results if not item.expected_pass)
    overall_pass = all_expected_succeeded and all_expected_failures_failed

    bundle = _bundle_manifest_fixture()
    return {
        "phase": PHASE_LABEL,
        "slice": SLICE_ID,
        "verification": VERIFICATION_NAME,
        "status": "pass" if overall_pass else "fail",
        "runtime_modules_available": True,
        "supporting_modules_available": True,
        "runtime_imports": list(RUNTIME_IMPORTS),
        "checked_files": [
            *PLAN_REFS,
            *SUPPORTING_EVIDENCE_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "results": [item.to_dict() for item in results],
        "runtime_exports": {
            "entrypoint_kind": entry_kind,
            "modules": {name: _module_public_names(module) for name, module in modules.items()},
            "bundle_manifest_fields": sorted(bundle.keys()),
            "bundle_payload_size_bytes": canonical_size_bytes(bundle),
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
            "bundle integrity is exercised directly against the runtime API when the runtime file exists",
            "schema validation is checked as part of integrity, not as a substitute for it",
            "no approval implied",
        ],
    }


def refresh_evidence_manifest() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    runtime_available = True
    overall_pass = True
    for report_path in sorted(EVIDENCE_DIR.glob("*_report.json")):
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        summary = payload.get("summary")
        report_pass = payload.get("overall_pass")
        if report_pass is None and isinstance(summary, Mapping):
            report_pass = summary.get("overall_pass")
        if report_pass is None and isinstance(payload.get("status"), str):
            report_pass = payload["status"] == "pass"
        report_runtime_available = bool(payload.get("runtime_modules_available", False))
        reports.append(
            {
                "report_id": report_path.stem.removeprefix("phase_03_").removesuffix("_report"),
                "path": str(report_path),
                "overall_pass": bool(report_pass),
                "status": str(payload.get("status", "pass" if report_pass else "blocked")),
                "runtime_modules_available": report_runtime_available,
            }
        )
        overall_pass = overall_pass and bool(report_pass)
        runtime_available = runtime_available and report_runtime_available

    status = "slice_4_ready" if reports and overall_pass and runtime_available else "slice_4_blocked"
    manifest = {
        "phase": PHASE_LABEL,
        "phase_remains_open": True,
        "reports": reports,
        "runtime_modules_available": runtime_available,
        "slice": SLICE_ID,
        "status": status,
        "notes": [
            "evidence manifest is rebuilt from actual report files on disk",
            "slice 1, slice 2, slice 3, and slice 4 evidence remains present and real",
            "readiness is truthful and blocked while any required runtime remains absent",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def main() -> int:
    runtime_file_missing = missing_files([RUNTIME_DIR / "bundle_integrity_checks.py"])
    if runtime_file_missing:
        report = build_blocked_report(runtime_file_missing)
        dump_json(REPORT_PATH, report)
        refresh_evidence_manifest()
        return 1

    try:
        report = build_pass_report()
    except ContractViolation as exc:
        report = {
            "phase": PHASE_LABEL,
            "slice": SLICE_ID,
            "verification": VERIFICATION_NAME,
            "status": "blocked",
            "runtime_modules_available": runtime_modules_available(),
            "supporting_modules_available": supporting_modules_available(),
            "runtime_imports": list(RUNTIME_IMPORTS),
            "checked_files": [
                *PLAN_REFS,
                *SUPPORTING_EVIDENCE_REFS,
                *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
            ],
            "blocker": {
                "kind": "runtime_contract_violation",
                "message": str(exc),
            },
            "results": [],
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
                "the runtime is present but one of the checks failed before completion",
                "no approval implied",
            ],
        }
        dump_json(REPORT_PATH, report)
        refresh_evidence_manifest()
        return 1

    dump_json(REPORT_PATH, report)
    refresh_evidence_manifest()
    return 0 if report["summary"]["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
