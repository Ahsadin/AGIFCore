from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


def _ensure_runtime_import_path() -> None:
    repo_root = _find_repo_root()
    runtime_dir = (
        repo_root
        / "projects"
        / "agifcore_master"
        / "04_execution"
        / "phase_03_cells_tissues_structure_and_bundles"
        / "agifcore_phase3_structure"
    )
    runtime_path = str(runtime_dir)
    if runtime_path not in sys.path:
        sys.path.insert(0, runtime_path)


_ensure_runtime_import_path()

from verify_phase_03_cell_contracts import (
    DEMO_DIR,
    EVIDENCE_DIR,
    PHASE_LABEL,
    ContractViolation,
    build_contract_report,
    canonical_size_bytes,
    dump_json,
    dump_json_like_markdown,
    runtime_modules_available,
    validate_cell_contract,
    validate_tissue_manifest,
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


def _require_non_empty_str(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ContractViolation(f"{field_name} must be a non-empty string")


def _require_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractViolation(f"{field_name} must be a mapping")
    return value


def _require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractViolation(f"{field_name} must be a list")
    return value


def validate_bundle_manifest(bundle: Mapping[str, Any]) -> None:
    required_fields = (
        "bundle_id",
        "bundle_version",
        "bundle_type",
        "entry_contracts",
        "schema_refs",
        "payload_inventory",
        "provenance_fields",
    )
    for field in required_fields:
        if field not in bundle:
            raise ContractViolation(f"missing required bundle manifest field: {field}")

    _require_non_empty_str(bundle["bundle_id"], "bundle_id")
    _require_non_empty_str(bundle["bundle_version"], "bundle_version")
    _require_non_empty_str(bundle["bundle_type"], "bundle_type")
    entry_contracts = _require_list(bundle["entry_contracts"], "entry_contracts")
    schema_refs = _require_mapping(bundle["schema_refs"], "schema_refs")
    payload_inventory = _require_mapping(bundle["payload_inventory"], "payload_inventory")
    provenance_fields = _require_mapping(bundle["provenance_fields"], "provenance_fields")

    if len({str(item) for item in entry_contracts}) != len(entry_contracts):
        raise ContractViolation("entry_contracts contains duplicate entries")
    if "cell_contract" not in schema_refs or "tissue_manifest" not in schema_refs or "bundle_manifest" not in schema_refs:
        raise ContractViolation("bundle manifest is missing required schema refs")
    if "cell_contract" not in payload_inventory or "tissue_manifest" not in payload_inventory:
        raise ContractViolation("bundle payload inventory must include cell_contract and tissue_manifest")
    _require_mapping(payload_inventory["cell_contract"], "payload_inventory.cell_contract")
    _require_mapping(payload_inventory["tissue_manifest"], "payload_inventory.tissue_manifest")
    _require_mapping(provenance_fields, "provenance_fields")

    if canonical_size_bytes(dict(bundle)) > MAX_BUNDLE_SIZE_BYTES:
        raise ContractViolation("bundle manifest exceeds max bundle payload size")


def _bundle_fixture() -> dict[str, Any]:
    cell_contract = {
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
    tissue_manifest = {
        "tissue_id": "tissue-orchestration",
        "tissue_name": "Orchestration Tissue",
        "allowed_role_families": ["planner"],
        "member_cell_ids": ["cell-alpha"],
        "routing_targets": ["bundle-validation"],
        "policy_envelope": {"max_members": 1},
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
            "notes": "slice_1_only",
        },
    }


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


def run_bundle_case_suite() -> list[CaseResult]:
    bundle = _bundle_fixture()
    cell_contract = bundle["payload_inventory"]["cell_contract"]
    tissue_manifest = bundle["payload_inventory"]["tissue_manifest"]
    contract_map = {cell_contract["cell_id"]: cell_contract}

    cases = [
        (
            "bundle-pass",
            "bundle_manifest",
            True,
            lambda: (
                validate_bundle_manifest(bundle),
                validate_cell_contract(cell_contract),
                validate_tissue_manifest(tissue_manifest, cell_contracts_by_id=contract_map),
            ),
        ),
        (
            "missing-manifest-field",
            "bundle_manifest",
            False,
            lambda: validate_bundle_manifest({k: v for k, v in bundle.items() if k != "bundle_type"}),
        ),
        (
            "invalid-object-shape",
            "bundle_manifest",
            False,
            lambda: validate_bundle_manifest("not-a-manifest"),  # type: ignore[arg-type]
        ),
        (
            "missing-schema-ref",
            "bundle_manifest",
            False,
            lambda: validate_bundle_manifest(
                {
                    **bundle,
                    "schema_refs": {
                        "cell_contract": "schemas/phase_03_cell_contract.schema.json",
                        "tissue_manifest": "schemas/phase_03_tissue_manifest.schema.json",
                    },
                }
            ),
        ),
        (
            "invalid-cell-contract-payload",
            "cell_contract",
            False,
            lambda: validate_cell_contract(
                {
                    **cell_contract,
                    "allowed_tissues": "tissue-orchestration",  # type: ignore[assignment]
                }
            ),
        ),
        (
            "invalid-tissue-manifest-payload",
            "tissue_manifest",
            False,
            lambda: validate_tissue_manifest(
                {
                    **tissue_manifest,
                    "member_cell_ids": ["cell-alpha", "cell-alpha"],
                },
                cell_contracts_by_id=contract_map,
            ),
        ),
    ]
    return [_run_case(*case) for case in cases]


def build_bundle_report() -> dict[str, Any]:
    results = run_bundle_case_suite()
    passed_count = sum(1 for item in results if item.passed)
    expected_pass_count = sum(1 for item in results if item.expected_pass)
    all_expected_succeeded = all(item.passed for item in results if item.expected_pass)
    all_expected_failures_failed = all(item.passed for item in results if not item.expected_pass)
    return {
        "phase": PHASE_LABEL,
        "slice": "slice_1",
        "verification": "bundle_validation",
        "runtime_modules_available": runtime_modules_available(),
        "runtime_imports": [
            "bundle_manifest",
            "bundle_schema_validation",
            "cell_contracts",
            "tissue_manifests",
        ],
        "max_bundle_size_bytes": MAX_BUNDLE_SIZE_BYTES,
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
            "bundle validation checks manifest structure and nested payloads",
            "verifier resolves runtime modules from the repo-relative execution path",
        ],
    }


def write_demo_docs(contract_report: Mapping[str, Any], bundle_report: Mapping[str, Any]) -> None:
    demo_index = f"""# Phase 3 Slice 1 Demo Index

Phase 3 remains open. This demo package covers slice 1 only.

Governor can rerun the same verifiers later without external `PYTHONPATH` wiring.

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
- later Governor runs resolve the runtime modules from the repo layout directly

## Report Status

- cell-contract report overall pass: {str(contract_report["summary"]["overall_pass"]).lower()}
- bundle-validation report overall pass: {str(bundle_report["summary"]["overall_pass"]).lower()}
"""
    bundle_demo = f"""# Phase 3 Bundle Validation Demo

Phase 3 remains open. This is slice 1 only.

Governor can rerun the same verifier later without external `PYTHONPATH` wiring.

## Review

- `{EVIDENCE_DIR / "phase_03_bundle_validation_report.json"}`
- `{EVIDENCE_DIR / "phase_03_evidence_manifest.json"}`

## Good Looks Like

- the bundle report shows a valid pass case
- the bundle report shows fail-closed cases for missing fields, bad shape, missing schema refs, and invalid nested payloads
- the evidence manifest references the actual report files on disk
- the verifier resolves the runtime directory from the repo layout directly
- nothing claims Phase 3 is closed

## Failure Looks Like

- the report is missing
- the report is narrative only
- the demo path points to files that do not exist
- the demo text claims Phase 3 is approved or closed
"""
    dump_json_like_markdown(DEMO_DIR / "phase_03_demo_index.md", demo_index)
    dump_json_like_markdown(DEMO_DIR / "phase_03_bundle_validation_demo.md", bundle_demo)


def main() -> int:
    contract_report_path = EVIDENCE_DIR / "phase_03_cell_contracts_report.json"
    if not contract_report_path.exists():
        contract_report = build_contract_report()
        dump_json(contract_report_path, contract_report)
    else:
        contract_report = json.loads(contract_report_path.read_text(encoding="utf-8"))

    bundle_report = build_bundle_report()
    dump_json(EVIDENCE_DIR / "phase_03_bundle_validation_report.json", bundle_report)
    write_demo_docs(contract_report, bundle_report)

    # Rebuild the evidence manifest after both reports exist.
    from verify_phase_03_cell_contracts import refresh_evidence_manifest

    refresh_evidence_manifest()
    return 0 if bundle_report["summary"]["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
