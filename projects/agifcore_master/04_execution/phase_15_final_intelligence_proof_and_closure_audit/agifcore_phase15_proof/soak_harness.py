from __future__ import annotations

from time import perf_counter
from typing import Any, Mapping

from .contracts import MAX_SOAK_DURATION_CLASSES, SOAK_HARNESS_SCHEMA, stable_hash_payload


def build_soak_harness_contract(
    *,
    phase13_shell_snapshot: Mapping[str, Any],
    phase14_shell_snapshot: Mapping[str, Any],
) -> dict[str, object]:
    classes = [
        {"duration_class_id": "short_cycle", "iteration_count": 3},
        {"duration_class_id": "medium_cycle", "iteration_count": 6},
        {"duration_class_id": "extended_cycle", "iteration_count": 9},
    ]
    if len(classes) > MAX_SOAK_DURATION_CLASSES:
        raise ValueError("soak duration class count exceeds planning ceiling")
    payload = {
        "schema": SOAK_HARNESS_SCHEMA,
        "duration_class_count": len(classes),
        "duration_classes": classes,
        "phase13_hash": phase13_shell_snapshot["snapshot_hash"],
        "phase14_hash": phase14_shell_snapshot["snapshot_hash"],
        "bounded_local_soak_only": True,
        "phase16_blocked": True,
    }
    return {**payload, "contract_hash": stable_hash_payload(payload)}


def run_soak_harness(*, proof_shells: Mapping[str, Any]) -> dict[str, object]:
    contract = build_soak_harness_contract(
        phase13_shell_snapshot=proof_shells["weak"].phase13_shell.shell_snapshot(),
        phase14_shell_snapshot=proof_shells["weak"].phase14_shell.shell_snapshot(),
    )
    class_results: list[dict[str, Any]] = []
    total_iterations = 0
    total_failures = 0
    for duration_class in contract["duration_classes"]:
        class_id = str(duration_class["duration_class_id"])
        iteration_count = int(duration_class["iteration_count"])
        iteration_results: list[dict[str, Any]] = []
        class_start = perf_counter()
        for index in range(iteration_count):
            scenario = "weak" if index % 2 == 0 else "contradiction"
            shell = proof_shells[scenario]
            start = perf_counter()
            turn = shell.phase13_shell.conversation_turn(
                user_text=(
                    "show the local-first product shell path"
                    if scenario == "weak"
                    else "please clarify the contradiction safely"
                )
            )
            shutdown = shell.phase13_shell.safe_shutdown()
            audit = shell.phase14_shell.manifest_audit()
            receipt = shell.phase14_shell.sandbox_execute(
                profile="laptop",
                function_name="add",
                function_args=[1, 2],
            )
            iteration_ms = round((perf_counter() - start) * 1000, 3)
            passed = (
                turn["final_answer_mode"] in {"search_needed", "clarify"}
                and shutdown["shutdown_status"] == "safe_stopped"
                and audit["audit_status"] == "pass"
                and receipt["status"] == "pass"
                and receipt["stdout"] == "3"
            )
            if not passed:
                total_failures += 1
            total_iterations += 1
            iteration_results.append(
                {
                    "iteration_id": f"{class_id}::{index + 1}",
                    "scenario": scenario,
                    "final_answer_mode": turn["final_answer_mode"],
                    "shutdown_status": shutdown["shutdown_status"],
                    "audit_status": audit["audit_status"],
                    "sandbox_status": receipt["status"],
                    "iteration_ms": iteration_ms,
                    "passed": passed,
                }
            )
        class_ms = round((perf_counter() - class_start) * 1000, 3)
        class_results.append(
            {
                "duration_class_id": class_id,
                "iteration_count": iteration_count,
                "passed_iteration_count": sum(1 for item in iteration_results if item["passed"]),
                "failed_iteration_count": sum(1 for item in iteration_results if not item["passed"]),
                "class_duration_ms": class_ms,
                "iteration_results": iteration_results,
                "class_passed": all(item["passed"] for item in iteration_results),
            }
        )
    payload = {
        "schema": SOAK_HARNESS_SCHEMA,
        "duration_class_count": len(class_results),
        "total_iterations": total_iterations,
        "total_failures": total_failures,
        "class_results": class_results,
        "bounded_local_soak_only": True,
        "status": "pass" if total_failures == 0 else "blocked",
        "phase16_blocked": True,
    }
    return {**payload, "result_hash": stable_hash_payload(payload)}
