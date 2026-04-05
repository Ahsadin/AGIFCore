from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import _phase_15_verifier_common as vc

VERIFIER = "verify_bounded_intelligence_gate"
VERIFIER_FILE = (
    "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py"
)
BENCHMARK_PATH = (
    vc.TEST_ROOT / "bounded_intelligence_benchmark.json"
)
REPORT_PATH = vc.EVIDENCE_DIR / "bounded_intelligence_gate_report.json"
SUMMARY_PATH = vc.EVIDENCE_DIR / "bounded_intelligence_gate_summary.json"
FAILURE_SUMMARY_PATH = vc.EVIDENCE_DIR / "bounded_intelligence_failure_summary.json"
REQUIRED_MODULES = (
    "agifcore_phase13_product_runtime.interactive_turn",
    "agifcore_phase13_product_runtime.product_runtime_shell",
    "agifcore_phase15_proof.proof_runtime_shell",
)
REQUIRED_PHASE_IDS = list(range(2, 16))

PROFILE_DEFAULTS: dict[str, dict[str, Any]] = {
    "identity_local_truth": {
        "allowed_answer_modes": ["grounded_fact"],
        "allowed_final_answer_modes": ["grounded_fact", "derived_explanation"],
        "allowed_next_actions": ["answer"],
        "min_local_sources": 2,
        "require_full_phase_chain": True,
        "require_graph_or_provenance": True,
        "forbidden_response_substrings": ["i do not have local support"],
    },
    "project_capability": {
        "allowed_answer_modes": ["grounded_fact"],
        "allowed_final_answer_modes": ["grounded_fact", "derived_explanation"],
        "allowed_next_actions": ["answer"],
        "min_local_sources": 2,
        "require_full_phase_chain": True,
        "require_graph_or_provenance": True,
        "forbidden_response_substrings": ["i do not have local support"],
    },
    "support_diagnostics": {
        "allowed_answer_modes": ["grounded_fact", "abstain"],
        "allowed_final_answer_modes": ["grounded_fact", "derived_explanation", "clarify", "unknown"],
        "allowed_next_actions": ["answer", "clarify", "abstain"],
        "min_local_sources": 1,
        "require_full_phase_chain": True,
        "require_graph_or_provenance": True,
    },
    "runtime_evidence": {
        "allowed_answer_modes": ["grounded_fact"],
        "allowed_final_answer_modes": ["grounded_fact", "derived_explanation"],
        "allowed_next_actions": ["answer"],
        "min_local_sources": 2,
        "require_full_phase_chain": True,
        "require_graph_or_provenance": True,
        "required_any_response_substrings": ["phase", "manifest", "evidence", "review", "runtime", "profile"],
        "forbidden_response_substrings": ["i do not have local support"],
    },
    "math_reasoning": {
        "allowed_answer_modes": ["grounded_fact"],
        "allowed_final_answer_modes": ["grounded_fact", "derived_explanation"],
        "allowed_next_actions": ["answer"],
        "min_local_sources": 1,
        "require_full_phase_chain": True,
        "forbidden_response_substrings": ["i do not have local support"],
    },
    "logic_reasoning": {
        "allowed_answer_modes": ["grounded_fact"],
        "allowed_final_answer_modes": ["grounded_fact", "derived_explanation"],
        "allowed_next_actions": ["answer"],
        "min_local_sources": 2,
        "require_full_phase_chain": True,
        "forbidden_response_substrings": ["i do not have local support"],
    },
    "comparison_planning": {
        "allowed_answer_modes": ["grounded_fact", "clarify"],
        "allowed_final_answer_modes": ["derived_explanation", "grounded_fact", "clarify"],
        "allowed_next_actions": ["answer", "clarify"],
        "min_local_sources": 1,
        "require_full_phase_chain": True,
        "forbidden_response_substrings": ["i do not have local support"],
    },
    "current_world_weather": {
        "allowed_answer_modes": ["bounded_estimate"],
        "allowed_final_answer_modes": ["derived_estimate"],
        "allowed_next_actions": ["answer"],
        "min_local_sources": 2,
        "require_full_phase_chain": True,
        "require_target_grounded": True,
        "require_simulation_or_world_model": True,
    },
    "current_world_moon": {
        "allowed_answer_modes": ["abstain"],
        "allowed_final_answer_modes": ["unknown"],
        "allowed_next_actions": ["abstain"],
        "min_local_sources": 1,
        "require_full_phase_chain": True,
        "require_target_grounded": True,
        "required_any_response_substrings": ["moon", "abstain", "misleading"],
    },
    "current_world_time": {
        "allowed_answer_modes": ["grounded_fact"],
        "allowed_final_answer_modes": ["grounded_fact"],
        "allowed_next_actions": ["answer"],
        "min_local_sources": 1,
        "require_full_phase_chain": True,
        "require_target_grounded": True,
    },
    "current_world_temperature": {
        "allowed_answer_modes": ["bounded_estimate", "clarify", "abstain"],
        "allowed_final_answer_modes": ["derived_estimate", "clarify", "unknown"],
        "allowed_next_actions": ["answer", "clarify", "abstain"],
        "min_local_sources": 1,
        "require_full_phase_chain": True,
        "required_any_response_substrings": ["estimate", "uncertainty", "cool", "warm", "cold"],
    },
    "contradiction_handling": {
        "allowed_answer_modes": ["grounded_fact", "clarify", "abstain"],
        "allowed_final_answer_modes": ["grounded_fact", "derived_explanation", "clarify", "unknown"],
        "allowed_next_actions": ["answer", "clarify", "abstain"],
        "min_local_sources": 1,
        "require_full_phase_chain": True,
        "require_critique_or_diagnosis": True,
        "forbidden_response_substrings": ["that is definitely fine without support"],
    },
    "follow_up": {
        "allowed_answer_modes": ["grounded_fact"],
        "allowed_final_answer_modes": ["grounded_fact", "derived_explanation"],
        "allowed_next_actions": ["answer"],
        "min_local_sources": 1,
        "require_full_phase_chain": True,
        "require_follow_up_bound": True,
        "require_memory": True,
        "forbidden_response_substrings": ["i do not have local support"],
    },
    "follow_up_support": {
        "allowed_answer_modes": ["grounded_fact", "abstain"],
        "allowed_final_answer_modes": ["grounded_fact", "derived_explanation", "unknown"],
        "allowed_next_actions": ["answer", "abstain"],
        "min_local_sources": 1,
        "require_full_phase_chain": True,
        "require_follow_up_bound": True,
        "require_memory": True,
    },
    "underspecified": {
        "allowed_answer_modes": ["abstain", "clarify"],
        "allowed_final_answer_modes": ["clarify", "unknown"],
        "allowed_next_actions": ["clarify", "abstain"],
        "min_local_sources": 0,
        "require_full_phase_chain": True,
        "forbidden_response_substrings": ["earth weather", "323", "phase 15 is approved"],
    },
    "unsupported": {
        "allowed_answer_modes": ["abstain", "search_needed"],
        "allowed_final_answer_modes": ["unknown", "search_needed"],
        "allowed_next_actions": ["abstain", "search_needed"],
        "min_local_sources": 0,
        "require_full_phase_chain": True,
        "required_any_response_substrings": ["local support", "search", "runtime state", "current information"],
    },
}

CLASS_THRESHOLDS = {
    "overall": 0.88,
    "identity_project_runtime_combined": 0.92,
    "math_logic": 0.80,
    "comparison_planning": 0.80,
    "current_world": 0.80,
    "contradiction_ambiguity": 0.80,
    "follow_up": 0.80,
    "underspecified": 0.80,
    "unsupported": 1.00,
    "phase_chain_integrity": 1.00,
}


def load_benchmark() -> dict[str, Any]:
    return json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))


def new_phase13_shell(scenario: str):
    shells = vc.run_phase15_shells()
    return shells["proof_shells"][scenario].phase13_shell


def merge_expectations(case: dict[str, Any]) -> dict[str, Any]:
    profile = PROFILE_DEFAULTS[case["evaluation_profile"]].copy()
    profile.setdefault("allowed_detected_classes", [case["expected_question_class"]])
    overrides = case.get("overrides", {})
    for key, value in overrides.items():
        profile[key] = value
    return profile


def _lower_list(items: list[str]) -> list[str]:
    return [item.lower() for item in items]


def _passes_contains_all(text: str, required: list[str]) -> bool:
    lowered = text.lower()
    return all(item.lower() in lowered for item in required)


def _passes_contains_any(text: str, required: list[str]) -> bool:
    lowered = text.lower()
    return any(item.lower() in lowered for item in required)


def _source_ids(result: dict[str, Any]) -> list[str]:
    return [str(item["source_id"]) for item in result.get("local_sources_consulted", [])]


def _refs_text(result: dict[str, Any]) -> str:
    refs = [str(item) for item in result.get("local_truth_refs", [])]
    return " | ".join(refs)


def _validate_turn_evidence(result: dict[str, Any]) -> tuple[bool, str]:
    rel_path = str(result.get("phase15_turn_evidence_ref") or "").strip()
    expected_hash = str(result.get("phase15_turn_evidence_hash") or "").strip()
    if not rel_path:
        return False, "phase15 turn evidence ref was missing"
    evidence_path = vc.REPO_ROOT / rel_path
    if not evidence_path.exists():
        return False, f"phase15 turn evidence file `{rel_path}` was missing"
    try:
        evidence_payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"phase15 turn evidence file `{rel_path}` could not be read: {exc}"
    if evidence_payload.get("schema") != "agifcore.phase_15.interactive_turn_evidence.v1":
        return False, f"phase15 turn evidence schema mismatch in `{rel_path}`"
    actual_hash = str(evidence_payload.get("evidence_hash") or "").strip()
    computed_hash = vc.stable_hash_payload({k: v for k, v in evidence_payload.items() if k != "evidence_hash"})
    if not actual_hash or actual_hash != computed_hash:
        return False, f"phase15 turn evidence hash did not validate for `{rel_path}`"
    if expected_hash and actual_hash != expected_hash:
        return False, f"phase15 turn evidence hash `{actual_hash}` did not match runtime hash `{expected_hash}`"
    if evidence_payload.get("turn_id") != result.get("turn_id"):
        return False, f"phase15 turn evidence turn_id mismatch for `{rel_path}`"
    if evidence_payload.get("request_text") != result.get("request_text"):
        return False, f"phase15 turn evidence request_text mismatch for `{rel_path}`"
    if evidence_payload.get("final_response") != result.get("final_response"):
        return False, f"phase15 turn evidence final_response mismatch for `{rel_path}`"
    if list(evidence_payload.get("phases_exercised", [])) != list(result.get("phases_exercised", [])):
        return False, f"phase15 turn evidence exercised phases mismatch for `{rel_path}`"
    return True, rel_path


def _record_for_case(case: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    detected_question_class = str(result["question_class"])
    extracted_target = result.get("extracted_target")
    phase_results = result["phase_results"]
    return {
        "request_text": result["request_text"],
        "expected_question_class": case["expected_question_class"],
        "detected_question_class": detected_question_class,
        "extracted_target_or_entity": extracted_target,
        "target_grounded": result.get("target_grounded"),
        "local_sources_consulted": result["local_sources_consulted"],
        "support_state": result["support_state"],
        "next_action": result["next_action"],
        "answer_mode": result["answer_mode"],
        "uncertainty_band": result["uncertainty_band"],
        "live_measurement_required": result["live_measurement_required"],
        "phases_actually_exercised": result["phases_exercised"],
        "memory_used": result["memory_consulted"],
        "graph_or_provenance_used": result["graph_support_consulted"],
        "simulation_or_world_model_used": result["simulation_world_model_consulted"],
        "critique_or_diagnosis_fired": result["critique_diagnosis_fired"],
        "followup_detected": result.get("followup_detected", False),
        "followup_anchor_turn_id": result.get("followup_anchor_turn_id"),
        "followup_binding_confidence": result.get("followup_binding_confidence"),
        "followup_binding_reason": result.get("followup_binding_reason"),
        "followup_binding_success": result.get("followup_binding_success", False),
        "phase15_turn_evidence_ref": result.get("phase15_turn_evidence_ref"),
        "phase15_turn_evidence_hash": result.get("phase15_turn_evidence_hash"),
        "final_response": result["final_response"],
        "expected_behavior": case["expected_behavior"],
        "observed_behavior": (
            f"class={detected_question_class}; answer_mode={result['answer_mode']}; "
            f"final_answer_mode={result['final_answer_mode']}; support_state={result['support_state']}; "
            f"next_action={result['next_action']}"
        ),
        "phase_results": phase_results,
        "phases_used_count": result["phases_used_count"],
        "phases_no_op_count": result["phases_no_op_count"],
        "phases_blocked_count": result["phases_blocked_count"],
        "phases_insufficient_input_count": result["phases_insufficient_input_count"],
        "full_chain_complete": result["phase_chain_completed"],
        "final_answer_after_full_chain": result["final_answer_released_after_full_chain"],
        "case_id": case["id"],
        "class_group": case["class_group"],
        "session_group": case["session_group"],
        "scenario": case["scenario"],
    }


def evaluate_case(case: dict[str, Any], result: dict[str, Any]) -> tuple[bool, str, str, list[str], bool]:
    checks = merge_expectations(case)
    failures: list[tuple[str, str]] = []
    response_text = str(result["response_text"])
    detected_question_class = str(result["question_class"])
    answer_mode = str(result["answer_mode"])
    final_answer_mode = str(result["final_answer_mode"])
    next_action = str(result["next_action"])
    local_sources = result.get("local_sources_consulted", [])
    local_source_ids = _source_ids(result)
    refs_text = _refs_text(result)
    phase_chain_ids = list(result["phase_chain_phase_ids"])
    target = str(result.get("extracted_target") or "")

    if detected_question_class not in checks.get("allowed_detected_classes", []):
        failures.append(
            (
                "interpretation_failure",
                f"detected class `{detected_question_class}` not in allowed classes {checks.get('allowed_detected_classes')}",
            )
        )

    if answer_mode not in checks.get("allowed_answer_modes", []):
        failures.append(
            (
                "answerability_failure",
                f"answer mode `{answer_mode}` not in allowed answer modes {checks.get('allowed_answer_modes')}",
            )
        )

    if final_answer_mode not in checks.get("allowed_final_answer_modes", []):
        failures.append(
            (
                "answerability_failure",
                f"final answer mode `{final_answer_mode}` not in allowed final modes {checks.get('allowed_final_answer_modes')}",
            )
        )

    if next_action not in checks.get("allowed_next_actions", []):
        failures.append(
            (
                "answerability_failure",
                f"next action `{next_action}` not in allowed next actions {checks.get('allowed_next_actions')}",
            )
        )

    if checks.get("require_full_phase_chain", False):
        if phase_chain_ids != REQUIRED_PHASE_IDS:
            failures.append(
                (
                    "reasoning_integration_failure",
                    f"phase chain ids were {phase_chain_ids} instead of {REQUIRED_PHASE_IDS}",
                )
            )
        if result["phase_chain_completed"] is not True:
            failures.append(
                ("reasoning_integration_failure", "full phase chain did not complete")
            )
        if result["final_answer_released_after_full_chain"] is not True:
            failures.append(
                ("reasoning_integration_failure", "final answer was not delayed until after full-chain completion")
            )
        if result.get("proof_record_written") is not True:
            failures.append(
                ("reasoning_integration_failure", "phase 15 proof record was not written before final answer release")
            )
        evidence_ok, evidence_reason = _validate_turn_evidence(result)
        if not evidence_ok:
            failures.append(
                ("reasoning_integration_failure", evidence_reason)
            )

    if len(local_sources) < checks.get("min_local_sources", 0):
        failures.append(
            (
                "retrieval_failure",
                f"local source count {len(local_sources)} was below minimum {checks.get('min_local_sources', 0)}",
            )
        )

    if checks.get("require_follow_up_bound", False) and result.get("follow_up_bound") is not True:
        failures.append(
            ("followup_memory_failure", "follow-up prompt did not bind to prior-turn state")
        )
    if checks.get("require_follow_up_bound", False) and result.get("followup_binding_success") is not True:
        failures.append(
            ("followup_memory_failure", "follow-up binding did not produce a successful stored anchor")
        )

    if checks.get("require_memory", False) and result.get("memory_consulted") is not True:
        failures.append(
            ("followup_memory_failure", "memory was not used where follow-up binding was required")
        )

    if checks.get("require_graph_or_provenance", False) and result.get("graph_support_consulted") is not True:
        failures.append(
            ("retrieval_failure", "graph/provenance support was not consulted where required")
        )

    if checks.get("require_simulation_or_world_model", False) and result.get("simulation_world_model_consulted") is not True:
        failures.append(
            ("reasoning_integration_failure", "simulation/world-model support was not consulted where required")
        )

    if checks.get("require_critique_or_diagnosis", False) and result.get("critique_diagnosis_fired") is not True:
        failures.append(
            ("reasoning_integration_failure", "critique/diagnosis did not fire where required")
        )

    if checks.get("require_target_grounded", False) and result.get("target_grounded") is not True:
        failures.append(
            ("interpretation_failure", "target was not grounded where grounding was required")
        )

    expected_target = checks.get("expected_target_contains")
    if expected_target and expected_target.lower() not in target.lower():
        failures.append(
            (
                "interpretation_failure",
                f"target `{target}` did not contain expected target fragment `{expected_target}`",
            )
        )

    if not _passes_contains_all(response_text, checks.get("required_response_substrings", [])):
        required = checks.get("required_response_substrings", [])
        if required:
            failures.append(
                (
                    "response_composition_failure",
                    f"response did not contain required substrings {required}",
                )
            )

    if not _passes_contains_any(response_text, checks.get("required_any_response_substrings", [])):
        required_any = checks.get("required_any_response_substrings", [])
        if required_any:
            failures.append(
                (
                    "response_composition_failure",
                    f"response did not contain any required substrings {required_any}",
                )
            )

    forbidden_response_substrings = _lower_list(checks.get("forbidden_response_substrings", []))
    lowered_response = response_text.lower()
    for fragment in forbidden_response_substrings:
        if fragment in lowered_response:
            failures.append(
                (
                    "response_composition_failure",
                    f"response contained forbidden substring `{fragment}`",
                )
            )

    for required_source in checks.get("required_source_ids", []):
        if required_source not in local_source_ids:
            failures.append(
                (
                    "retrieval_failure",
                    f"required source id `{required_source}` was missing from local sources {local_source_ids}",
                )
            )

    for required_ref in checks.get("required_ref_substrings", []):
        if required_ref.lower() not in refs_text.lower():
            failures.append(
                (
                    "retrieval_failure",
                    f"required ref substring `{required_ref}` was missing from refs `{refs_text}`",
                )
            )

    hard_fail = False
    if case["class_group"] == "unsupported" and next_action not in {"abstain", "search_needed"}:
        hard_fail = True
    if case["class_group"] == "current_world":
        expected_target = checks.get("expected_target_contains")
        if expected_target and expected_target.lower() not in target.lower():
            hard_fail = True
    if phase_chain_ids != REQUIRED_PHASE_IDS or result["phase_chain_completed"] is not True:
        hard_fail = True
    if result["final_answer_released_after_full_chain"] is not True:
        hard_fail = True
    if (
        len(result["phases_exercised"]) == len(REQUIRED_PHASE_IDS)
        and result["phases_no_op_count"] == 0
        and result["phases_insufficient_input_count"] == 0
    ):
        hard_fail = True

    if failures:
        primary_failure_type, short_reason = failures[0]
        return False, primary_failure_type, short_reason, [item[1] for item in failures], hard_fail
    return True, "pass", "all checks passed", [], hard_fail


def build_outputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    benchmark = load_benchmark()
    cases = benchmark["cases"]
    session_shells: dict[tuple[str, str], Any] = {}
    records: list[dict[str, Any]] = []
    failure_counts: Counter[str] = Counter()
    class_totals: Counter[str] = Counter()
    class_passes: Counter[str] = Counter()
    hard_fail_reasons: list[str] = []

    for case in cases:
        session_key = (case["scenario"], case["session_group"])
        if session_key not in session_shells:
            session_shells[session_key] = new_phase13_shell(case["scenario"])
        shell = session_shells[session_key]
        result = shell.interactive_turn(user_text=case["prompt"])
        record = _record_for_case(case, result)
        passed, failure_type, short_reason, all_failures, hard_fail = evaluate_case(case, result)
        record["pass_or_fail"] = "pass" if passed else "fail"
        record["primary_failure_type"] = failure_type
        record["short_failure_reason"] = short_reason
        record["all_failure_reasons"] = all_failures
        records.append(record)

        class_group = case["class_group"]
        class_totals[class_group] += 1
        if passed:
            class_passes[class_group] += 1
        failure_counts[failure_type] += 1
        if hard_fail:
            hard_fail_reasons.append(f"{case['id']}: {short_reason}")

    prompt_count = len(records)
    passed_count = sum(1 for item in records if item["pass_or_fail"] == "pass")
    failed_count = prompt_count - passed_count
    overall_pass_rate = passed_count / prompt_count if prompt_count else 0.0

    class_results: dict[str, dict[str, Any]] = {}
    for class_group, total in sorted(class_totals.items()):
        passed = class_passes[class_group]
        class_results[class_group] = {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total else 0.0,
        }

    combined_groups = ("identity_system", "project_phase_capability", "local_runtime_evidence")
    combined_total = sum(class_totals[group] for group in combined_groups)
    combined_passed = sum(class_passes[group] for group in combined_groups)
    combined_rate = combined_passed / combined_total if combined_total else 0.0

    phase_chain_ok = all(
        item["full_chain_complete"] is True
        and item["final_answer_after_full_chain"] is True
        and [phase["phase_id"] for phase in item["phase_results"]] == REQUIRED_PHASE_IDS
        for item in records
    )

    threshold_results = {
        "overall": overall_pass_rate >= CLASS_THRESHOLDS["overall"],
        "identity_project_runtime_combined": combined_rate >= CLASS_THRESHOLDS["identity_project_runtime_combined"],
        "math_logic": class_results["math_logic"]["pass_rate"] >= CLASS_THRESHOLDS["math_logic"],
        "comparison_planning": class_results["comparison_planning"]["pass_rate"] >= CLASS_THRESHOLDS["comparison_planning"],
        "current_world": class_results["current_world"]["pass_rate"] >= CLASS_THRESHOLDS["current_world"],
        "contradiction_ambiguity": class_results["contradiction_ambiguity"]["pass_rate"] >= CLASS_THRESHOLDS["contradiction_ambiguity"],
        "follow_up": class_results["follow_up"]["pass_rate"] >= CLASS_THRESHOLDS["follow_up"],
        "underspecified": class_results["underspecified"]["pass_rate"] >= CLASS_THRESHOLDS["underspecified"],
        "unsupported": class_results["unsupported"]["pass_rate"] >= CLASS_THRESHOLDS["unsupported"],
        "phase_chain_integrity": phase_chain_ok,
    }

    gate_passed = all(threshold_results.values()) and not hard_fail_reasons

    report = {
        "benchmark_id": benchmark["benchmark_id"],
        "benchmark_version": benchmark["version"],
        "prompt_count": prompt_count,
        "status": "bounded_intelligence_gate_pass" if gate_passed else "bounded_intelligence_gate_fail",
        "gate_passed": gate_passed,
        "records": records,
        "notes": [
            "broad chat intelligence is not claimed here",
            "Phase 15 remains open unless later closure work passes",
            "Phase 16 remains open unless later closure work passes",
            "no approval implied",
        ],
    }

    summary = {
        "benchmark_id": benchmark["benchmark_id"],
        "prompt_count": prompt_count,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "overall_pass_rate": overall_pass_rate,
        "class_results": class_results,
        "combined_identity_project_runtime": {
            "total": combined_total,
            "passed": combined_passed,
            "pass_rate": combined_rate,
        },
        "threshold_results": threshold_results,
        "hard_fail_count": len(hard_fail_reasons),
        "hard_fail_reasons": hard_fail_reasons,
        "failure_counts_by_primary_failure_type": dict(sorted(failure_counts.items())),
        "gate_passed": gate_passed,
        "final_claim_if_passed": "AGIFCore as bounded intelligence only; broad chat intelligence remains unproven/deferred",
    }

    ranked_failures = sorted(
        (
            {
                "case_id": item["case_id"],
                "class_group": item["class_group"],
                "primary_failure_type": item["primary_failure_type"],
                "short_failure_reason": item["short_failure_reason"],
            }
            for item in records
            if item["pass_or_fail"] == "fail"
        ),
        key=lambda item: (item["primary_failure_type"], item["case_id"]),
    )

    failure_summary = {
        "benchmark_id": benchmark["benchmark_id"],
        "gate_passed": gate_passed,
        "failure_counts_by_primary_failure_type": dict(sorted(failure_counts.items())),
        "hard_fail_reasons": hard_fail_reasons,
        "ranked_failures": ranked_failures,
        "next_step": (
            "bounded closeout may proceed to audit/verification packaging"
            if gate_passed
            else "keep Phase 15 and Phase 16 open and repair the ranked failures before any closeout claim"
        ),
    }

    return report, summary, failure_summary


def main() -> int:
    missing = vc.missing_files([VERIFIER_FILE, str(BENCHMARK_PATH.relative_to(vc.REPO_ROOT))])
    if missing:
        raise SystemExit(f"missing bounded gate inputs: {missing}")
    if not vc.runtime_modules_available(REQUIRED_MODULES):
        raise SystemExit("required runtime modules for bounded-intelligence gate are unavailable")

    report, summary, failure_summary = build_outputs()
    vc.dump_json(REPORT_PATH, report)
    vc.dump_json(SUMMARY_PATH, summary)
    vc.dump_json(FAILURE_SUMMARY_PATH, failure_summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
