from __future__ import annotations

import importlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

MAX_TISSUE_MEMBERS = 16
MAX_ROUTING_TARGETS = 8
MAX_MANIFEST_SIZE_BYTES = 64 * 1024

PHASE_NAME = "phase_03_cells_tissues_structure_and_bundles"
PHASE_LABEL = "Phase 3"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
RUNTIME_IMPORTS = (
    "cell_contracts",
    "tissue_manifests",
    "bundle_manifest",
    "bundle_schema_validation",
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
TESTING_DIR = PROJECT_ROOT / TEST_ROOT_NAME / "phase_03_cells_tissues_structure_and_bundles"
OUTPUT_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / "phase_03_cells_tissues_structure_and_bundles"
EVIDENCE_DIR = OUTPUT_DIR / "phase_03_evidence"
DEMO_DIR = OUTPUT_DIR / "phase_03_demo_bundle"
RUNTIME_DIR = PROJECT_ROOT / EXECUTION_ROOT_NAME / "phase_03_cells_tissues_structure_and_bundles" / "agifcore_phase3_structure"


class ContractViolation(ValueError):
    pass


def load_runtime_module(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except Exception:  # noqa: BLE001 - import availability is part of the report.
        return None


def runtime_modules_available() -> bool:
    return all(load_runtime_module(module_name) is not None for module_name in RUNTIME_IMPORTS)


def dump_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def validate_cell_contract(contract: Mapping[str, Any]) -> None:
    required_fields = (
        "cell_id",
        "bundle_ref",
        "role_family",
        "role_name",
        "allowed_tissues",
        "split_policy",
        "merge_policy",
        "trust_profile",
        "policy_envelope",
    )
    for field in required_fields:
        if field not in contract:
            raise ContractViolation(f"missing required cell contract field: {field}")
    _require_non_empty_str(contract["cell_id"], "cell_id")
    _require_non_empty_str(contract["bundle_ref"], "bundle_ref")
    _require_non_empty_str(contract["role_family"], "role_family")
    _require_non_empty_str(contract["role_name"], "role_name")
    _require_str_list(contract["allowed_tissues"], "allowed_tissues")
    _require_mapping(contract["split_policy"], "split_policy")
    _require_mapping(contract["merge_policy"], "merge_policy")
    _require_mapping(contract["trust_profile"], "trust_profile")
    _require_mapping(contract["policy_envelope"], "policy_envelope")
    if canonical_size_bytes(dict(contract)) > MAX_MANIFEST_SIZE_BYTES:
        raise ContractViolation("cell contract exceeds max manifest size")


def validate_tissue_manifest(
    manifest: Mapping[str, Any],
    *,
    cell_contracts_by_id: Mapping[str, Mapping[str, Any]] | None = None,
) -> None:
    required_fields = (
        "tissue_id",
        "tissue_name",
        "allowed_role_families",
        "member_cell_ids",
        "routing_targets",
        "policy_envelope",
    )
    for field in required_fields:
        if field not in manifest:
            raise ContractViolation(f"missing required tissue manifest field: {field}")

    _require_non_empty_str(manifest["tissue_id"], "tissue_id")
    _require_non_empty_str(manifest["tissue_name"], "tissue_name")
    allowed_role_families = _require_str_list(manifest["allowed_role_families"], "allowed_role_families")
    member_cell_ids = _require_str_list(manifest["member_cell_ids"], "member_cell_ids")
    routing_targets = _require_str_list(manifest["routing_targets"], "routing_targets")
    _require_mapping(manifest["policy_envelope"], "policy_envelope")

    if len(member_cell_ids) > MAX_TISSUE_MEMBERS:
        raise ContractViolation("tissue manifest exceeds max tissue membership fanout")
    if len(routing_targets) > MAX_ROUTING_TARGETS:
        raise ContractViolation("tissue manifest exceeds max routing targets")

    if cell_contracts_by_id:
        tissue_id = str(manifest["tissue_id"])
        for cell_id in member_cell_ids:
            cell_contract = cell_contracts_by_id.get(cell_id)
            if cell_contract is None:
                raise ContractViolation(f"unknown tissue member cell_id: {cell_id}")
            role_family = str(cell_contract.get("role_family", ""))
            allowed_tissues = cell_contract.get("allowed_tissues", [])
            if role_family not in allowed_role_families:
                raise ContractViolation(
                    f"member cell {cell_id} has disallowed role_family: {role_family}"
                )
            if tissue_id not in allowed_tissues:
                raise ContractViolation(
                    f"member cell {cell_id} does not allow tissue membership for {tissue_id}"
                )

    if canonical_size_bytes(dict(manifest)) > MAX_MANIFEST_SIZE_BYTES:
        raise ContractViolation("tissue manifest exceeds max manifest size")


def _cell_contract_fixture() -> dict[str, Any]:
    return {
        "cell_id": "cell-alpha",
        "bundle_ref": "bundle-alpha",
        "role_family": "planner",
        "role_name": "phase-3-planner",
        "allowed_tissues": ["tissue-orchestration"],
        "split_policy": {"mode": "governed"},
        "merge_policy": {"mode": "governed"},
        "trust_profile": {"band": "seed"},
        "policy_envelope": {"max_active_cells": 32},
    }


def _tissue_manifest_fixture() -> dict[str, Any]:
    return {
        "tissue_id": "tissue-orchestration",
        "tissue_name": "Orchestration Tissue",
        "allowed_role_families": ["planner"],
        "member_cell_ids": ["cell-alpha"],
        "routing_targets": ["bundle-validation"],
        "policy_envelope": {"max_members": 1},
    }


def _duplicate_member_fixture() -> dict[str, Any]:
    tissue = _tissue_manifest_fixture()
    tissue["member_cell_ids"] = ["cell-alpha", "cell-alpha"]
    return tissue


def _illegal_membership_fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    contract = _cell_contract_fixture()
    contract["allowed_tissues"] = ["tissue-other"]
    tissue = _tissue_manifest_fixture()
    return contract, tissue


def _oversized_manifest_fixture() -> dict[str, Any]:
    tissue = _tissue_manifest_fixture()
    tissue["policy_envelope"] = {"notes": "x" * (MAX_MANIFEST_SIZE_BYTES + 512)}
    return tissue


def _fanout_breach_fixture() -> dict[str, Any]:
    tissue = _tissue_manifest_fixture()
    tissue["member_cell_ids"] = [f"cell-{index}" for index in range(MAX_TISSUE_MEMBERS + 1)]
    return tissue


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


def run_contract_case_suite() -> list[CaseResult]:
    cell_contract = _cell_contract_fixture()
    tissue_manifest = _tissue_manifest_fixture()
    contract_map = {cell_contract["cell_id"]: cell_contract}
    illegal_contract, illegal_tissue = _illegal_membership_fixture()
    illegal_contract_map = {illegal_contract["cell_id"]: illegal_contract}

    cases = [
        (
            "cell-contract-pass",
            "cell_contract",
            True,
            lambda: validate_cell_contract(cell_contract),
        ),
        (
            "tissue-manifest-pass",
            "tissue_manifest",
            True,
            lambda: validate_tissue_manifest(tissue_manifest, cell_contracts_by_id=contract_map),
        ),
        (
            "missing-contract-field",
            "cell_contract",
            False,
            lambda: validate_cell_contract({k: v for k, v in cell_contract.items() if k != "bundle_ref"}),
        ),
        (
            "duplicate-tissue-member",
            "tissue_manifest",
            False,
            lambda: validate_tissue_manifest(_duplicate_member_fixture(), cell_contracts_by_id=contract_map),
        ),
        (
            "illegal-tissue-membership",
            "cross_reference",
            False,
            lambda: validate_tissue_manifest(
                illegal_tissue,
                cell_contracts_by_id=illegal_contract_map,
            ),
        ),
        (
            "manifest-size-breach",
            "tissue_manifest",
            False,
            lambda: validate_tissue_manifest(_oversized_manifest_fixture()),
        ),
        (
            "fanout-breach",
            "tissue_manifest",
            False,
            lambda: validate_tissue_manifest(_fanout_breach_fixture()),
        ),
    ]
    return [_run_case(*case) for case in cases]


def build_contract_report() -> dict[str, Any]:
    results = run_contract_case_suite()
    passed_count = sum(1 for item in results if item.passed)
    expected_pass_count = sum(1 for item in results if item.expected_pass)
    all_expected_succeeded = all(item.passed for item in results if item.expected_pass)
    all_expected_failures_failed = all(item.passed for item in results if not item.expected_pass)
    return {
        "phase": PHASE_LABEL,
        "slice": "slice_1",
        "verification": "cell_contracts",
        "runtime_modules_available": runtime_modules_available(),
        "runtime_imports": list(RUNTIME_IMPORTS),
        "max_manifest_size_bytes": MAX_MANIFEST_SIZE_BYTES,
        "max_tissue_members": MAX_TISSUE_MEMBERS,
        "max_routing_targets": MAX_ROUTING_TARGETS,
        "results": [item.to_dict() for item in results],
        "summary": {
            "total_cases": len(results),
            "passed_cases": passed_count,
            "expected_pass_cases": expected_pass_count,
            "expected_succeeded": all_expected_succeeded,
            "expected_failures_verified": all_expected_failures_failed,
            "overall_pass": all_expected_succeeded and all_expected_failures_failed,
        },
        "notes": [
            "slice-1 only",
            "later Governor runs can resolve runtime modules with PYTHONPATH pointed at the KPL runtime worktree",
            "reports are generated from executed case checks, not summary prose",
        ],
    }


def refresh_evidence_manifest() -> dict[str, Any]:
    contract_report_path = EVIDENCE_DIR / "phase_03_cell_contracts_report.json"
    bundle_report_path = EVIDENCE_DIR / "phase_03_bundle_validation_report.json"
    reports: list[dict[str, Any]] = []
    if contract_report_path.exists():
        reports.append(json.loads(contract_report_path.read_text(encoding="utf-8")))
    if bundle_report_path.exists():
        reports.append(json.loads(bundle_report_path.read_text(encoding="utf-8")))

    manifest = {
        "phase": PHASE_LABEL,
        "slice": "slice_1",
        "status": "slice_1_only",
        "phase_remains_open": True,
        "runtime_modules_available": runtime_modules_available(),
        "reports": [
            {
                "report_id": report.get("verification", "unknown"),
                "path": str(
                    contract_report_path if report.get("verification") == "cell_contracts" else bundle_report_path
                ),
                "overall_pass": report.get("summary", {}).get("overall_pass", False),
            }
            for report in reports
        ],
        "notes": [
            "evidence manifest is slice-1 only",
            "Phase 3 remains open",
            "manifest is rebuilt from actual report files on disk",
        ],
    }
    dump_json(EVIDENCE_DIR / "phase_03_evidence_manifest.json", manifest)
    return manifest


def write_demo_index(contract_report_exists: bool, bundle_report_exists: bool) -> None:
    demo_index = f"""# Phase 3 Slice 1 Demo Index

Phase 3 remains open. This demo package covers slice 1 only.

Governor can rerun the same verifiers later with `PYTHONPATH` pointed at the KPL runtime worktree.

## Inspect

- `{EVIDENCE_DIR / "phase_03_evidence_manifest.json"}`
- `{EVIDENCE_DIR / "phase_03_cell_contracts_report.json"}`
- `{EVIDENCE_DIR / "phase_03_bundle_validation_report.json"}`
- `{DEMO_DIR / "phase_03_bundle_validation_demo.md"}`

## What this proves

- the cell-contract verifier ran on slice-1 fixtures
- the bundle-validation verifier ran on slice-1 fixtures
- the evidence manifest was rebuilt from actual report files
- Phase 3 remains open
- later Governor runs can resolve the runtime modules from `PYTHONPATH`

## Report Availability

- cell-contract report present: {str(contract_report_exists).lower()}
- bundle-validation report present: {str(bundle_report_exists).lower()}
"""
    dump_json_like_markdown(DEMO_DIR / "phase_03_demo_index.md", demo_index)


def dump_json_like_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    report = build_contract_report()
    dump_json(EVIDENCE_DIR / "phase_03_cell_contracts_report.json", report)
    refresh_evidence_manifest()
    return 0 if report["summary"]["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
