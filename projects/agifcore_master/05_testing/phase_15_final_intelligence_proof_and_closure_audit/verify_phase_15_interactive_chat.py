from __future__ import annotations

import json

import _phase_15_verifier_common as vc

VERIFIER = "verify_phase_15_interactive_chat"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_interactive_chat.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_15_interactive_chat_report.json"
REQUIRED_MODULES = (
    "agifcore_phase13_product_runtime.interactive_turn",
    "agifcore_phase13_product_runtime.product_runtime_shell",
    "agifcore_phase15_proof.proof_runtime_shell",
)
ASSERTION_IDS = [
    "interactive-path-covers-broad-question-classes",
    "interactive-path-binds-follow-ups-to-session-state",
    "interactive-path-answers-supported-local-questions-from-local-truth",
    "interactive-path-handles-bounded-math-and-planning",
    "interactive-path-differentiates-current-world-target-grounding",
    "interactive-path-fails-closed-on-unsupported-questions",
    "interactive-path-records-selective-phase-usage",
    "interactive-path-records-full-phase-chain-in-order",
    "interactive-path-delays-final-answer-until-full-chain-completion",
    "interactive-path-records-real-local-sources-and-turn-evidence",
]

PROMPT_GROUPS = [
    {
        "group_id": "identity",
        "prompts": [
            {"id": "who_are_you", "prompt": "who are you", "expected_class": "self_system_status"},
            {"id": "who_built_you", "prompt": "who built you", "expected_class": "self_system_status"},
        ],
    },
    {
        "group_id": "project_status",
        "prompts": [
            {"id": "what_is_agif", "prompt": "what is AGIF", "expected_class": "project_phase_capability"},
            {"id": "what_phase_on", "prompt": "what phase are you on", "expected_class": "local_truth_evidence"},
            {"id": "what_can_you_do", "prompt": "what can you do", "expected_class": "project_phase_capability"},
            {"id": "what_can_you_not_do", "prompt": "what can you not do", "expected_class": "project_phase_capability"},
        ],
    },
    {
        "group_id": "follow_up_support",
        "prompts": [
            {"id": "seed_capability", "prompt": "what can you do", "expected_class": "project_phase_capability"},
            {"id": "evidence_supports_that", "prompt": "what evidence supports that", "expected_class": "support_diagnostics"},
            {"id": "what_did_i_ask", "prompt": "what did I ask", "expected_class": "session_history"},
            {"id": "follow_up_why", "prompt": "why", "expected_class": "session_history"},
            {"id": "follow_up_why_is_that", "prompt": "why is that", "expected_class": "session_history"},
        ],
    },
    {
        "group_id": "math_reasoning",
        "prompts": [
            {"id": "help_math", "prompt": "help me with math", "expected_class": "reasoning_math"},
            {"id": "multiply_17_19", "prompt": "what is 17 * 19", "expected_class": "reasoning_math"},
        ],
    },
    {
        "group_id": "comparison_planning",
        "prompts": [
            {"id": "compare_enf_agif", "prompt": "compare ENF and AGIF", "expected_class": "comparison_planning"},
            {"id": "plan_verify_phase_truth", "prompt": "make a short plan to verify phase truth", "expected_class": "comparison_planning"},
        ],
    },
    {
        "group_id": "current_world",
        "prompts": [
            {"id": "weather_berlin", "prompt": "what is the weather in Berlin", "expected_class": "current_world"},
            {"id": "weather_antarctica", "prompt": "what is the weather in Antarctica", "expected_class": "current_world"},
            {"id": "weather_moon", "prompt": "what is the weather on the Moon", "expected_class": "current_world"},
            {"id": "is_it_night", "prompt": "is it night", "expected_class": "current_world"},
            {"id": "is_it_cold", "prompt": "is it cold outside", "expected_class": "current_world"},
        ],
    },
    {
        "group_id": "contradiction",
        "prompts": [
            {
                "id": "phase15_contradiction",
                "prompt": "is there any contradiction between the phase index and gate checklist for phase 15",
                "expected_class": "contradiction",
            },
            {
                "id": "phase14_open_and_approved",
                "prompt": "check whether phase 14 is both open and approved",
                "expected_class": "contradiction",
            },
        ],
    },
    {
        "group_id": "unsupported_and_missing_support",
        "prompts": [
            {"id": "who_is_ahmad", "prompt": "who is Ahmad", "expected_class": "unsupported"},
            {"id": "what_support_missing", "prompt": "what support is missing", "expected_class": "support_diagnostics"},
            {"id": "are_you_sure", "prompt": "are you sure", "expected_class": "support_diagnostics"},
            {"id": "capital_france", "prompt": "what is the capital of france", "expected_class": "unsupported"},
            {"id": "diff_search", "prompt": "what exact diff line changed last in the repo", "expected_class": "local_truth_evidence"},
        ],
    },
]


def _fresh_shell():
    return vc.run_phase15_shells()["proof_shells"]["weak"].phase13_shell


def _result_record(
    *,
    group_id: str,
    prompt_id: str,
    prompt: str,
    result: dict[str, object],
) -> dict[str, object]:
    return {
        "group_id": group_id,
        "id": prompt_id,
        "prompt": prompt,
        "request_text": result["request_text"],
        "question_class": result["question_class"],
        "extracted_target": result.get("extracted_target"),
        "target_grounded": result.get("target_grounded"),
        "support_state": result["support_state"],
        "final_support_state": result["final_support_state"],
        "next_action": result["next_action"],
        "answer_mode": result["answer_mode"],
        "uncertainty_band": result["uncertainty_band"],
        "live_measurement_required": result["live_measurement_required"],
        "final_answer_mode": result["final_answer_mode"],
        "final_response": result["final_response"],
        "follow_up_bound": result["follow_up_bound"],
        "local_truth_refs": result["local_truth_refs"],
        "local_sources_consulted": result["local_sources_consulted"],
        "source_set_used": result["source_set_used"],
        "phase_results": result["phase_results"],
        "phase_chain_phase_ids": result["phase_chain_phase_ids"],
        "phase_chain_completed": result["phase_chain_completed"],
        "phases_exercised": result["phases_exercised"],
        "phases_used_count": result["phases_used_count"],
        "phases_no_op_count": result["phases_no_op_count"],
        "phases_blocked_count": result["phases_blocked_count"],
        "phases_insufficient_input_count": result["phases_insufficient_input_count"],
        "phase_usage": result["phase_usage"],
        "memory_consulted": result["memory_consulted"],
        "graph_support_consulted": result["graph_support_consulted"],
        "simulation_world_model_consulted": result["simulation_world_model_consulted"],
        "critique_diagnosis_fired": result["critique_diagnosis_fired"],
        "response_text": result["response_text"],
        "final_critique_complete": result["final_critique_complete"],
        "proof_record_written": result["proof_record_written"],
        "final_answer_released_after_full_chain": result["final_answer_released_after_full_chain"],
        "turn_hash": result["turn_hash"],
    }


def build_pass_report() -> dict[str, object]:
    prompt_results: list[dict[str, object]] = []
    class_set: set[str] = set()
    final_mode_set: set[str] = set()
    phase_patterns: set[tuple[int, ...]] = set()
    unique_source_ids: set[str] = set()
    turn_hashes: set[str] = set()
    phase_statuses_seen: set[str] = set()

    for group in PROMPT_GROUPS:
        shell = _fresh_shell()
        for item in group["prompts"]:
            result = shell.interactive_turn(user_text=item["prompt"])
            question_class = str(result["question_class"])
            assert question_class == item["expected_class"], (item["id"], question_class)
            record = _result_record(
                group_id=str(group["group_id"]),
                prompt_id=str(item["id"]),
                prompt=str(item["prompt"]),
                result=result,
            )
            prompt_results.append(record)
            class_set.add(question_class)
            final_mode_set.add(str(result["final_answer_mode"]))
            phase_patterns.add(tuple(int(phase) for phase in result["phases_exercised"]))
            turn_hashes.add(str(result["turn_hash"]))
            unique_source_ids.update(source["source_id"] for source in result["local_sources_consulted"])
            phase_statuses_seen.update(str(phase["status"]) for phase in result["phase_results"])

    by_id = {item["id"]: item for item in prompt_results}

    assert by_id["who_are_you"]["final_answer_mode"] == "grounded_fact"
    assert by_id["who_built_you"]["final_answer_mode"] == "grounded_fact"
    assert by_id["what_is_agif"]["final_answer_mode"] == "derived_explanation"
    assert "Phase 15" in str(by_id["what_phase_on"]["response_text"])
    assert by_id["what_can_you_do"]["final_answer_mode"] == "grounded_fact"
    assert by_id["what_can_you_not_do"]["final_answer_mode"] == "grounded_fact"

    assert by_id["evidence_supports_that"]["follow_up_bound"] is True
    assert "local refs" in str(by_id["evidence_supports_that"]["response_text"]).lower()
    assert by_id["what_did_i_ask"]["follow_up_bound"] is True
    assert "what evidence supports that" in str(by_id["what_did_i_ask"]["response_text"]).lower()
    for prompt_id in ("follow_up_why", "follow_up_why_is_that"):
        assert by_id[prompt_id]["follow_up_bound"] is True
        assert by_id[prompt_id]["final_answer_mode"] == "derived_explanation"

    assert by_id["help_math"]["final_answer_mode"] == "clarify"
    assert by_id["multiply_17_19"]["final_answer_mode"] == "grounded_fact"
    assert "323" in str(by_id["multiply_17_19"]["response_text"])

    assert by_id["compare_enf_agif"]["final_answer_mode"] == "derived_explanation"
    assert "comparison" in str(by_id["compare_enf_agif"]["response_text"]).lower()
    assert by_id["plan_verify_phase_truth"]["final_answer_mode"] == "derived_explanation"
    assert "short local plan" in str(by_id["plan_verify_phase_truth"]["response_text"]).lower()

    assert by_id["weather_berlin"]["answer_mode"] == "bounded_estimate"
    assert by_id["weather_berlin"]["target_grounded"] is True
    assert by_id["weather_berlin"]["extracted_target"] == "Berlin"
    assert by_id["weather_berlin"]["live_measurement_required"] is True
    assert by_id["weather_antarctica"]["answer_mode"] == "bounded_estimate"
    assert by_id["weather_antarctica"]["target_grounded"] is True
    assert by_id["weather_antarctica"]["extracted_target"] == "Antarctica"
    assert by_id["weather_moon"]["answer_mode"] == "abstain"
    assert by_id["weather_moon"]["target_grounded"] is True
    assert "moon" in str(by_id["weather_moon"]["extracted_target"]).lower()
    assert by_id["is_it_night"]["answer_mode"] == "grounded_fact"
    assert by_id["is_it_night"]["live_measurement_required"] is False
    assert by_id["is_it_cold"]["answer_mode"] == "bounded_estimate"

    for prompt_id in ("phase15_contradiction", "phase14_open_and_approved"):
        assert by_id[prompt_id]["final_answer_mode"] == "grounded_fact"
        assert by_id[prompt_id]["phase_usage"]["phase_10"]["used"] is True

    for prompt_id in ("who_is_ahmad", "capital_france"):
        assert by_id[prompt_id]["final_answer_mode"] == "unknown"
        assert by_id[prompt_id]["next_action"] == "abstain"
    assert "missing enough approved local support" in str(by_id["what_support_missing"]["response_text"]).lower()
    assert by_id["are_you_sure"]["follow_up_bound"] is True
    assert by_id["diff_search"]["final_answer_mode"] == "search_needed"
    assert by_id["diff_search"]["next_action"] == "search_needed"

    assert "grounded_fact" in final_mode_set
    assert "derived_explanation" in final_mode_set
    assert "derived_estimate" in final_mode_set
    assert "clarify" in final_mode_set
    assert "unknown" in final_mode_set
    assert "search_needed" in final_mode_set

    assert len(class_set) >= 9
    assert len(turn_hashes) >= 18
    assert len(phase_patterns) >= 6
    assert len(unique_source_ids) >= 8
    assert "used" in phase_statuses_seen
    assert "no_op" in phase_statuses_seen
    assert "insufficient_input" in phase_statuses_seen

    for item in prompt_results:
        assert item["final_support_state"] == item["support_state"]
        assert item["final_response"] == item["response_text"]
        assert item["phase_chain_phase_ids"] == list(range(2, 16))
        assert item["phase_chain_completed"] is True
        assert item["final_critique_complete"] is True
        assert item["proof_record_written"] is True
        assert item["final_answer_released_after_full_chain"] is True
        assert item["phases_used_count"] + item["phases_no_op_count"] + item["phases_blocked_count"] + item["phases_insufficient_input_count"] == 14
        assert item["phases_used_count"] == len(item["phases_exercised"])
        assert item["phases_exercised"] == [
            phase_result["phase_id"]
            for phase_result in item["phase_results"]
            if phase_result["status"] == "used"
        ]
        assert [phase_result["phase_id"] for phase_result in item["phase_results"]] == list(range(2, 16))
        for phase_result in item["phase_results"]:
            assert phase_result["status"] in {"used", "no_op", "blocked", "insufficient_input"}
            assert isinstance(phase_result["reason"], str) and phase_result["reason"]
            assert isinstance(phase_result["inputs_used"], list)
            assert isinstance(phase_result["outputs_added"], list)
            assert "support_delta" in phase_result
            assert isinstance(phase_result["refs_used"], list)
            assert isinstance(phase_result["state_changed"], bool)
            phase_key = f"phase_{phase_result['phase_id']}"
            assert item["phase_usage"][phase_key]["status"] == phase_result["status"]
            assert item["phase_usage"][phase_key]["used"] is (phase_result["status"] == "used")
        assert item["phase_usage"]["phase_2"]["used"] is True
        assert item["phase_usage"]["phase_3"]["used"] is True
        assert item["phase_usage"]["phase_4"]["used"] is True
        assert item["phase_usage"]["phase_5"]["used"] is True
        assert item["phase_usage"]["phase_7"]["used"] is True
        assert item["phase_usage"]["phase_13"]["used"] is True
        assert item["phase_usage"]["phase_14"]["used"] is True
        assert item["phase_usage"]["phase_15"]["used"] is True
        assert item["memory_consulted"] is True
        assert item["graph_support_consulted"] is True

    assert by_id["who_are_you"]["phase_usage"]["phase_6"]["used"] is False
    assert by_id["who_are_you"]["phase_usage"]["phase_10"]["used"] is False
    assert by_id["weather_berlin"]["phase_usage"]["phase_6"]["used"] is True
    assert by_id["weather_berlin"]["phase_usage"]["phase_8"]["used"] is True
    assert by_id["weather_berlin"]["phase_usage"]["phase_10"]["used"] is True
    assert by_id["weather_berlin"]["simulation_world_model_consulted"] is True
    assert by_id["capital_france"]["phase_usage"]["phase_6"]["used"] is False
    assert by_id["compare_enf_agif"]["phase_usage"]["phase_8"]["used"] is True
    assert by_id["multiply_17_19"]["phase_usage"]["phase_6"]["used"] is True
    assert by_id["help_math"]["phase_usage"]["phase_6"]["used"] is False

    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=vc.checked_files_for(VERIFIER_FILE),
        assertions=[
            {"id": "interactive-path-covers-broad-question-classes", "result": "pass"},
            {"id": "interactive-path-binds-follow-ups-to-session-state", "result": "pass"},
            {"id": "interactive-path-answers-supported-local-questions-from-local-truth", "result": "pass"},
            {"id": "interactive-path-handles-bounded-math-and-planning", "result": "pass"},
            {"id": "interactive-path-differentiates-current-world-target-grounding", "result": "pass"},
            {"id": "interactive-path-fails-closed-on-unsupported-questions", "result": "pass"},
            {"id": "interactive-path-records-selective-phase-usage", "result": "pass"},
            {"id": "interactive-path-records-full-phase-chain-in-order", "result": "pass"},
            {"id": "interactive-path-delays-final-answer-until-full-chain-completion", "result": "pass"},
            {"id": "interactive-path-records-real-local-sources-and-turn-evidence", "result": "pass"},
        ],
        anchors={
            "interactive_prompt_results": prompt_results,
            "question_class_count": len(class_set),
            "final_answer_mode_count": len(final_mode_set),
            "unique_turn_hash_count": len(turn_hashes),
            "phase_pattern_count": len(phase_patterns),
            "phase_statuses_seen": sorted(phase_statuses_seen),
            "unique_source_id_count": len(unique_source_ids),
            "group_count": len(PROMPT_GROUPS),
            "shell_snapshot": _fresh_shell().shell_snapshot(),
            "evidence_manifest": vc.evidence_manifest_anchor(),
        },
        notes=[
            "interactive verification uses the real local question-driven turn engine",
            "the default interactive path is no longer the canned scenario path",
            "every tested turn now records the full ordered phase chain from phase 2 through phase 15",
            "final answers are emitted only after the full chain record and phase-15 proof surface are present",
            "supported local questions answer from approved AGIFCore local truth and runtime state",
            "current-world prompts differentiate grounded local facts, bounded estimates, and honest abstain by grounded target",
            "follow-up prompts bind to stored prior-turn state instead of collapsing into one fallback",
            "unsupported prompts stay fail-closed without fake grounded answers",
        ],
    )


def main() -> int:
    missing = vc.missing_files(vc.checked_files_for(VERIFIER_FILE))
    if missing:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for(VERIFIER_FILE),
            assertion_ids=ASSERTION_IDS,
            blocker_kind="missing_files",
            blocker_message="interactive chat verifier is missing required files",
            missing=missing,
        )
    elif not vc.runtime_modules_available(REQUIRED_MODULES):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for(VERIFIER_FILE),
            assertion_ids=ASSERTION_IDS,
            blocker_kind="import_failure",
            blocker_message="interactive chat verifier could not import its runtime modules",
        )
    else:
        try:
            report = build_pass_report()
        except Exception as exc:  # pragma: no cover - surfaced as machine-readable output
            report = vc.build_blocked_report(
                verifier=VERIFIER,
                report_path=REPORT_PATH,
                checked_files=vc.checked_files_for(VERIFIER_FILE),
                assertion_ids=ASSERTION_IDS,
                blocker_kind="runtime_failure",
                blocker_message=str(exc),
            )
    vc.write_report(REPORT_PATH, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
