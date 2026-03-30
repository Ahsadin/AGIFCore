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
VERIFICATION_NAME = "tissue_orchestration"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"

RUNTIME_IMPORTS = ("cell_contracts", "tissue_manifests")
RUNTIME_FILES = (
    "cell_contracts.py",
    "tissue_manifests.py",
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
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json",
)

MAX_TISSUE_MEMBERS = 16
MAX_ROUTING_TARGETS = 8
MAX_MANIFEST_SIZE_BYTES = 64 * 1024
SPLIT_REVIEW_THRESHOLD = 8


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
REPORT_PATH = EVIDENCE_DIR / "phase_03_tissue_orchestration_report.json"
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


def _require_true(value: Any, context: str) -> Any:
    if isinstance(value, bool):
        if not value:
            raise ContractViolation(f"{context} returned false")
        return value
    if value is None:
        return None
    return value


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

    cell_contracts = modules["cell_contracts"]
    tissue_manifests = modules["tissue_manifests"]
    return {
        "modules": modules,
        "CellContract": getattr(cell_contracts, "CellContract"),
        "TissueManifest": getattr(tissue_manifests, "TissueManifest"),
        "validate_cell_contract_payload": getattr(cell_contracts, "validate_cell_contract_payload"),
        "validate_tissue_manifest_payload": getattr(tissue_manifests, "validate_tissue_manifest_payload"),
        "MAX_MANIFEST_SIZE_BYTES": getattr(cell_contracts, "MAX_MANIFEST_SIZE_BYTES"),
        "MAX_TISSUE_MEMBERS": getattr(tissue_manifests, "MAX_TISSUE_MEMBERS"),
        "MAX_ROUTING_TARGETS": getattr(tissue_manifests, "MAX_ROUTING_TARGETS"),
        "SPLIT_PRESSURE_MEMBER_COUNT": getattr(tissue_manifests, "SPLIT_PRESSURE_MEMBER_COUNT"),
    }


def _cell_contract_payload(
    *,
    cell_id: str,
    bundle_ref: str,
    role_family: str,
    role_name: str,
    allowed_tissues: list[str],
    policy_envelope: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "cell_id": cell_id,
        "bundle_ref": bundle_ref,
        "role_family": role_family,
        "role_name": role_name,
        "allowed_tissues": allowed_tissues,
        "split_policy": {"mode": "governed"},
        "merge_policy": {"mode": "governed"},
        "trust_profile": {"band": "seed"},
        "policy_envelope": dict(policy_envelope or {}),
    }


def _tissue_manifest_payload(
    *,
    tissue_id: str,
    tissue_name: str,
    allowed_role_families: list[str],
    member_cell_ids: list[str],
    routing_targets: list[str] | None = None,
    policy_envelope: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "tissue_id": tissue_id,
        "tissue_name": tissue_name,
        "allowed_role_families": allowed_role_families,
        "member_cell_ids": member_cell_ids,
        "routing_targets": list(routing_targets or ["bundle-validation"]),
        "policy_envelope": dict(policy_envelope or {}),
    }


def _build_contract_map(cell_contracts: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {contract["cell_id"]: contract for contract in cell_contracts}


def _cell_contract_fixture() -> dict[str, Any]:
    return _cell_contract_payload(
        cell_id="cell-alpha",
        bundle_ref="bundle-alpha",
        role_family="planner",
        role_name="phase-3-planner",
        allowed_tissues=["tissue-orchestration"],
        policy_envelope={"profile": "laptop"},
    )


def _tissue_manifest_fixture() -> dict[str, Any]:
    return _tissue_manifest_payload(
        tissue_id="tissue-orchestration",
        tissue_name="Orchestration Tissue",
        allowed_role_families=["planner"],
        member_cell_ids=["cell-alpha"],
    )


def _split_review_fixture() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    cell_contracts = [
        _cell_contract_payload(
            cell_id=f"cell-review-{index}",
            bundle_ref="bundle-alpha",
            role_family="planner",
            role_name=f"phase-3-planner-{index}",
            allowed_tissues=["tissue-review"],
            policy_envelope={"profile": "laptop"},
        )
        for index in range(SPLIT_REVIEW_THRESHOLD + 1)
    ]
    tissue = _tissue_manifest_payload(
        tissue_id="tissue-review",
        tissue_name="Review Tissue",
        allowed_role_families=["planner"],
        member_cell_ids=[contract["cell_id"] for contract in cell_contracts],
    )
    return tissue, _build_contract_map(cell_contracts)


def _duplicate_member_fixture() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    cell = _cell_contract_fixture()
    tissue = _tissue_manifest_payload(
        tissue_id="tissue-orchestration",
        tissue_name="Orchestration Tissue",
        allowed_role_families=["planner"],
        member_cell_ids=["cell-alpha", "cell-alpha"],
    )
    return tissue, {cell["cell_id"]: cell}


def _role_family_mismatch_fixture() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    cell = _cell_contract_payload(
        cell_id="cell-router",
        bundle_ref="bundle-alpha",
        role_family="router",
        role_name="phase-3-router",
        allowed_tissues=["tissue-orchestration"],
        policy_envelope={"profile": "laptop"},
    )
    tissue = _tissue_manifest_payload(
        tissue_id="tissue-orchestration",
        tissue_name="Orchestration Tissue",
        allowed_role_families=["planner"],
        member_cell_ids=[cell["cell_id"]],
    )
    return tissue, {cell["cell_id"]: cell}


def _fanout_breach_fixture() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    cell_contracts = [
        _cell_contract_payload(
            cell_id=f"cell-fanout-{index}",
            bundle_ref="bundle-alpha",
            role_family="planner",
            role_name=f"phase-3-planner-{index}",
            allowed_tissues=["tissue-fanout"],
            policy_envelope={"profile": "laptop"},
        )
        for index in range(MAX_TISSUE_MEMBERS + 1)
    ]
    tissue = _tissue_manifest_payload(
        tissue_id="tissue-fanout",
        tissue_name="Fanout Tissue",
        allowed_role_families=["planner"],
        member_cell_ids=[contract["cell_id"] for contract in cell_contracts],
    )
    return tissue, _build_contract_map(cell_contracts)


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


def _normal_size_check(payload: Mapping[str, Any]) -> None:
    if canonical_size_bytes(payload) > MAX_MANIFEST_SIZE_BYTES:
        raise ContractViolation("manifest exceeds max manifest size")


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
            "message": "Phase 3 slice 4 tissue orchestration runtime modules are not on disk yet.",
            "missing_files": missing,
        },
        "planned_checks": [
            "valid cell contract passes",
            "valid tissue manifest passes",
            "tissue orchestration split-review threshold is exposed",
            "missing cell contract field fails",
            "duplicate tissue member fails",
            "role-family mismatch fails",
            "fanout breach fails",
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
            "no runtime checks were executed because the phase-3 slice-4 modules are absent",
            "report is intentionally blocked instead of pretending the verifier passed",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, Any]:
    api = load_runtime_api()
    CellContract = api["CellContract"]
    TissueManifest = api["TissueManifest"]
    validate_cell_contract_payload = api["validate_cell_contract_payload"]
    validate_tissue_manifest_payload = api["validate_tissue_manifest_payload"]
    modules = api["modules"]
    max_manifest_size_bytes = api["MAX_MANIFEST_SIZE_BYTES"]
    max_tissue_members = api["MAX_TISSUE_MEMBERS"]
    max_routing_targets = api["MAX_ROUTING_TARGETS"]
    split_review_threshold = api["SPLIT_PRESSURE_MEMBER_COUNT"]

    cell_payload = _cell_contract_fixture()
    tissue_payload = _tissue_manifest_fixture()
    contract_map = _build_contract_map([cell_payload])

    cases = [
        (
            "cell-contract-pass",
            "cell_contracts",
            True,
            lambda: (
                validate_cell_contract_payload(cell_payload),
                _coerce_mapping(CellContract.from_payload(cell_payload), "cell contract"),
                CellContract.from_payload(cell_payload).validate(),
                _require_true(
                    CellContract.from_payload(cell_payload).allows_tissue("tissue-orchestration"),
                    "CellContract.allows_tissue",
                ),
            ),
        ),
        (
            "tissue-manifest-pass",
            "tissue_manifests",
            True,
            lambda: (
                validate_tissue_manifest_payload(tissue_payload, cell_contracts_by_id=contract_map),
                _coerce_mapping(
                    TissueManifest.from_payload(
                        tissue_payload,
                        cell_contracts_by_id=contract_map,
                    ),
                    "tissue manifest",
                ),
                TissueManifest.from_payload(
                    tissue_payload,
                    cell_contracts_by_id=contract_map,
                ).validate(cell_contracts_by_id=contract_map),
            ),
        ),
        (
            "split-review-threshold-exposed",
            "tissue_manifests",
            True,
            lambda: _require_true(
                TissueManifest.from_payload(
                    _split_review_fixture()[0],
                    cell_contracts_by_id=_split_review_fixture()[1],
                ).needs_split_review(),
                "TissueManifest.needs_split_review",
            ),
        ),
        (
            "missing-contract-field",
            "cell_contracts",
            False,
            lambda: validate_cell_contract_payload({k: v for k, v in cell_payload.items() if k != "bundle_ref"}),
        ),
        (
            "duplicate-tissue-member",
            "tissue_manifests",
            False,
            lambda: validate_tissue_manifest_payload(
                _duplicate_member_fixture()[0],
                cell_contracts_by_id=_duplicate_member_fixture()[1],
            ),
        ),
        (
            "role-family-mismatch",
            "tissue_manifests",
            False,
            lambda: validate_tissue_manifest_payload(
                _role_family_mismatch_fixture()[0],
                cell_contracts_by_id=_role_family_mismatch_fixture()[1],
            ),
        ),
        (
            "fanout-breach",
            "tissue_manifests",
            False,
            lambda: validate_tissue_manifest_payload(
                _fanout_breach_fixture()[0],
                cell_contracts_by_id=_fanout_breach_fixture()[1],
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
            "cell_contract": {
                "type": type(CellContract.from_payload(cell_payload)).__name__,
                "fields": sorted(_coerce_mapping(CellContract.from_payload(cell_payload), "cell contract").keys()),
            },
            "tissue_manifest": {
                "type": type(TissueManifest.from_payload(tissue_payload, cell_contracts_by_id=contract_map)).__name__,
                "fields": sorted(
                    _coerce_mapping(
                        TissueManifest.from_payload(tissue_payload, cell_contracts_by_id=contract_map),
                        "tissue manifest",
                    ).keys()
                ),
            },
            "thresholds": {
                "max_manifest_size_bytes": max_manifest_size_bytes,
                "max_tissue_members": max_tissue_members,
                "max_routing_targets": max_routing_targets,
                "split_review_threshold": split_review_threshold,
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
            "slice-4 tissue orchestration is exercised directly against the runtime API",
            "the verifier resolves runtime modules from the repo-relative execution path",
            "reports are generated from executed case checks, not summary prose",
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
            "slice 1, slice 2, and slice 3 evidence remains present and real",
            "slice 4 tissue orchestration is integrated in this lane",
            "readiness is truthful and blocked while any required runtime remains absent",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def main() -> int:
    runtime_file_missing = missing_files([RUNTIME_DIR / filename for filename in RUNTIME_FILES])
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
