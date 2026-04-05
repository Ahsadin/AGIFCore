from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .contracts import (
    FORBIDDEN_PHASE16_KEYWORDS,
    HARDENING_PACKAGE_SCHEMA,
    MAX_HARDENING_ISSUE_FAMILY_COUNT,
    stable_hash_payload,
)


def run_hardening_package(
    *,
    proof_shells: Mapping[str, Any],
    repo_root: Path,
    phase15_output_root: Path,
) -> dict[str, object]:
    weak_shell = proof_shells["weak"]
    phase14_shell = weak_shell.phase14_shell
    families = []
    checks = [
        (
            "tampered_bundle_fail_closed",
            phase14_shell.sandbox_execute(
                profile="laptop",
                function_name="add",
                function_args=[1, 2],
                variant="tampered",
            ),
            {"status": "blocked", "reason_code": "BUNDLE_INTEGRITY_REQUIRED"},
        ),
        (
            "invalid_module_fail_closed",
            phase14_shell.sandbox_execute(
                profile="laptop",
                function_name="add",
                function_args=[1, 2],
                variant="invalid",
            ),
            {"status": "blocked", "reason_code": "INVALID_WASM_MODULE"},
        ),
        (
            "profile_mismatch_fail_closed",
            phase14_shell.sandbox_execute(
                profile="mobile",
                function_name="add",
                function_args=[1, 2],
                allowed_profiles=("laptop",),
            ),
            {"status": "blocked", "reason_code": "PROFILE_NOT_ALLOWED"},
        ),
        (
            "fuel_limit_fail_closed",
            phase14_shell.sandbox_execute(
                profile="mobile",
                function_name="spin",
            ),
            {"status": "blocked", "reason_code": "FUEL_LIMIT_EXCEEDED"},
        ),
        (
            "memory_limit_fail_closed",
            phase14_shell.sandbox_execute(
                profile="mobile",
                policy_id="strict_fail_closed_policy",
                function_name="grow_to_pages",
                function_args=[600],
            ),
            {"status": "blocked", "reason_code": "MEMORY_LIMIT_EXCEEDED"},
        ),
        (
            "wall_time_limit_fail_closed",
            phase14_shell.sandbox_execute(
                profile="mobile",
                policy_id="strict_fail_closed_policy",
                function_name="spin",
            ),
            {"status": "blocked", "reason_code": "WALL_TIMEOUT_EXCEEDED"},
        ),
    ]
    for family_id, receipt, expected in checks:
        passed = all(receipt.get(key) == value for key, value in expected.items())
        families.append(
            {
                "issue_family_id": family_id,
                "expected": expected,
                "observed": {
                    "status": receipt["status"],
                    "reason_code": receipt["reason_code"],
                    "receipt_hash": receipt["receipt_hash"],
                },
                "passed": passed,
            }
        )
    phase15_names = [path.name.lower() for path in phase15_output_root.rglob("*") if path.is_file()]
    leak_hits = [
        keyword
        for keyword in FORBIDDEN_PHASE16_KEYWORDS
        if any(keyword in name for name in phase15_names)
    ]
    families.append(
        {
            "issue_family_id": "phase16_publication_excluded",
            "expected": {"forbidden_keyword_hits": []},
            "observed": {"forbidden_keyword_hits": leak_hits},
            "passed": not leak_hits,
        }
    )
    phase13_manifest = repo_root / "projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/phase_13_evidence_manifest.json"
    phase14_manifest = repo_root / "projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_evidence_manifest.json"
    upstream_pass = phase13_manifest.exists() and phase14_manifest.exists()
    families.append(
        {
            "issue_family_id": "upstream_phase_manifests_present",
            "expected": {"phase13_manifest_present": True, "phase14_manifest_present": True},
            "observed": {
                "phase13_manifest_present": phase13_manifest.exists(),
                "phase14_manifest_present": phase14_manifest.exists(),
            },
            "passed": upstream_pass,
        }
    )
    if len(families) > MAX_HARDENING_ISSUE_FAMILY_COUNT:
        raise ValueError("hardening issue family count exceeds planning ceiling")
    payload = {
        "schema": HARDENING_PACKAGE_SCHEMA,
        "issue_family_count": len(families),
        "families": families,
        "status": "pass" if all(item["passed"] for item in families) else "blocked",
        "phase16_blocked": True,
    }
    return {**payload, "package_hash": stable_hash_payload(payload)}

