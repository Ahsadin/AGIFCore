from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .contracts import HIDDEN_PACK_SCHEMA, MAX_HIDDEN_PACK_COUNT, stable_hash_payload


def build_hidden_pack_catalog(
    *,
    phase13_shell_snapshot: Mapping[str, Any],
    phase14_shell_snapshot: Mapping[str, Any],
) -> dict[str, object]:
    packs = [
        {
            "pack_id": "hidden_fail_closed_edge_pack",
            "pack_class": "sandbox_edge_cases",
            "live_demo_excluded": True,
            "case_count": 2,
            "cases": [
                {
                    "case_id": "hidden_invalid_module_block",
                    "case_kind": "sandbox_execute",
                    "scenario": "weak",
                    "execution_request": {
                        "profile": "laptop",
                        "function_name": "add",
                        "function_args": [1, 2],
                        "variant": "invalid",
                    },
                    "expected_contract": {
                        "status": "blocked",
                        "reason_code": "INVALID_WASM_MODULE",
                    },
                },
                {
                    "case_id": "hidden_profile_mismatch_block",
                    "case_kind": "sandbox_execute",
                    "scenario": "weak",
                    "execution_request": {
                        "profile": "mobile",
                        "function_name": "add",
                        "function_args": [1, 2],
                        "allowed_profiles": ["laptop"],
                    },
                    "expected_contract": {
                        "status": "blocked",
                        "reason_code": "PROFILE_NOT_ALLOWED",
                    },
                },
            ],
            "phase13_hash": phase13_shell_snapshot["snapshot_hash"],
            "phase14_hash": phase14_shell_snapshot["snapshot_hash"],
        },
        {
            "pack_id": "hidden_resource_limit_pack",
            "pack_class": "resource_limit_edges",
            "live_demo_excluded": True,
            "case_count": 3,
            "cases": [
                {
                    "case_id": "hidden_fuel_limit_block",
                    "case_kind": "sandbox_execute",
                    "scenario": "weak",
                    "execution_request": {
                        "profile": "mobile",
                        "function_name": "spin",
                    },
                    "expected_contract": {
                        "status": "blocked",
                        "reason_code": "FUEL_LIMIT_EXCEEDED",
                    },
                },
                {
                    "case_id": "hidden_memory_limit_block",
                    "case_kind": "sandbox_execute",
                    "scenario": "weak",
                    "execution_request": {
                        "profile": "mobile",
                        "policy_id": "strict_fail_closed_policy",
                        "function_name": "grow_to_pages",
                        "function_args": [600],
                    },
                    "expected_contract": {
                        "status": "blocked",
                        "reason_code": "MEMORY_LIMIT_EXCEEDED",
                    },
                },
                {
                    "case_id": "hidden_timeout_block",
                    "case_kind": "sandbox_execute",
                    "scenario": "weak",
                    "execution_request": {
                        "profile": "mobile",
                        "policy_id": "strict_fail_closed_policy",
                        "function_name": "spin",
                    },
                    "expected_contract": {
                        "status": "blocked",
                        "reason_code": "WALL_TIMEOUT_EXCEEDED",
                    },
                },
            ],
            "phase13_hash": phase13_shell_snapshot["snapshot_hash"],
            "phase14_hash": phase14_shell_snapshot["snapshot_hash"],
        },
    ]
    if len(packs) > MAX_HIDDEN_PACK_COUNT:
        raise ValueError("hidden pack count exceeds planning ceiling")
    payload = {
        "schema": HIDDEN_PACK_SCHEMA,
        "hidden_pack_count": len(packs),
        "packs": packs,
        "phase16_blocked": True,
    }
    return {**payload, "catalog_hash": stable_hash_payload(payload)}


def run_hidden_pack_catalog(
    *,
    pack_catalog: Mapping[str, Any],
    proof_shells: Mapping[str, Any],
    live_demo_case_ids: set[str],
    output_dir: Path | None = None,
) -> dict[str, object]:
    pack_results: list[dict[str, Any]] = []
    total_case_count = 0
    passed_case_count = 0
    for pack in pack_catalog["packs"]:
        case_results: list[dict[str, Any]] = []
        for case in pack["cases"]:
            shell = proof_shells[str(case["scenario"])]
            receipt = shell.phase14_shell.sandbox_execute(output_dir=output_dir, **dict(case["execution_request"]))
            observed = {
                "status": receipt["status"],
                "reason_code": receipt["reason_code"],
                "live_demo_excluded": case["case_id"] not in live_demo_case_ids,
                "receipt_hash": receipt["receipt_hash"],
            }
            expected = dict(case["expected_contract"])
            expected["live_demo_excluded"] = True
            passed = all(observed.get(key) == value for key, value in expected.items())
            case_results.append(
                {
                    "case_id": case["case_id"],
                    "scenario": case["scenario"],
                    "expected_contract": expected,
                    "observed": observed,
                    "passed": passed,
                }
            )
            total_case_count += 1
            if passed:
                passed_case_count += 1
        pack_results.append(
            {
                "pack_id": pack["pack_id"],
                "pack_class": pack["pack_class"],
                "live_demo_excluded": pack["live_demo_excluded"],
                "case_count": len(case_results),
                "passed_case_count": sum(1 for case in case_results if case["passed"]),
                "pack_passed": all(case["passed"] for case in case_results),
                "case_results": case_results,
            }
        )
    payload = {
        "schema": HIDDEN_PACK_SCHEMA,
        "hidden_pack_count": len(pack_results),
        "total_case_count": total_case_count,
        "passed_case_count": passed_case_count,
        "status": "pass" if total_case_count == passed_case_count else "blocked",
        "pack_results": pack_results,
        "phase16_blocked": True,
    }
    return {**payload, "result_hash": stable_hash_payload(payload)}

