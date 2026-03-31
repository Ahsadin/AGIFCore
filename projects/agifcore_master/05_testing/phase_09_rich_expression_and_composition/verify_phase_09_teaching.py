from __future__ import annotations

import json
from pathlib import Path

import _phase_09_verifier_common as vc
from agifcore_phase9_rich_expression.contracts import MAX_TEACHING_SECTIONS
from agifcore_phase9_rich_expression.teaching import TeachingEngine

VERIFIER = "verify_phase_09_teaching"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_09_teaching_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase9_rich_expression.contracts",
    "agifcore_phase9_rich_expression.teaching",
)
OWNED_FILES = (
    "projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/_phase_09_verifier_common.py",
    "projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_teaching.py",
)


def _run_case(*, support_state: str, request_id: str) -> dict[str, object]:
    raw_text = "Please teach this in simple terms and include how to verify it."
    intake = vc.build_phase7_intake_state(
        conversation_id="conv-p9-teach",
        turn_id=request_id,
        raw_text=raw_text,
    )
    interpretation = vc.build_phase7_question_interpretation_state(
        conversation_id="conv-p9-teach",
        turn_id=request_id,
        raw_text_hash=intake["intake_hash"],
        user_intent="teach this in simple terms",
        discourse_mode_hint="teach",
        question_category="ordinary",
        target_domain_hint="weather_climate",
        live_current_requested=False,
        ambiguous_request=False,
        self_knowledge_requested=False,
        local_artifact_requested=False,
        correction_hint=False,
        repeated_fact_hint=False,
        comparison_requested=False,
        extracted_terms=("teach", "simple", "verify"),
        signal_notes=("education-focused request",),
    )
    support = vc.build_phase7_support_resolution_state(
        conversation_id="conv-p9-teach",
        turn_id=request_id,
        support_state=support_state,
        knowledge_gap_reason="none" if support_state == "grounded" else "missing_local_evidence",
        next_action="answer" if support_state == "grounded" else "clarify",
        evidence_refs=("phase7.support.ref.001",),
        selected_domain_ids=("weather_climate",),
        reason_codes=("bounded_local_support",),
    )
    summary = vc.build_phase8_visible_reasoning_summary_state(
        request_id=request_id,
        what_is_known=("Coastal air cools more slowly after sunset.", "Humidity can remain elevated near water."),
        what_is_inferred=("A shoreline request should stay bounded to local evidence.",),
        uncertainty=("No live sensor reading is included in this turn.",),
        what_would_verify=("Check a fresh local weather station reading.",),
        principle_refs=("measurement_uncertainty", "coastal_weather_baseline"),
        causal_chain_ref="chain::teach::001",
        uncertainty_band="moderate",
        live_measurement_required=False,
        evidence_refs=("phase8.summary.ref.001", "phase8.summary.ref.002"),
    )
    return {
        "intake": intake,
        "interpretation": interpretation,
        "support": support,
        "summary": summary,
    }


def build_pass_report() -> dict[str, object]:
    engine = TeachingEngine()
    first = _run_case(support_state="grounded", request_id="turn-p9-teach-01")
    before_first = vc.deep_copy(first)
    first_snapshot = engine.build_snapshot(
        question_interpretation_state=first["interpretation"],
        support_state_resolution_state=first["support"],
        visible_reasoning_summary_state=first["summary"],
    )
    vc.assert_inputs_unchanged(before_first, first, "teaching first-case inputs")

    second = _run_case(support_state="search_needed", request_id="turn-p9-teach-02")
    before_second = vc.deep_copy(second)
    second_snapshot = engine.build_snapshot(
        question_interpretation_state=second["interpretation"],
        support_state_resolution_state=second["support"],
        visible_reasoning_summary_state=second["summary"],
    )
    vc.assert_inputs_unchanged(before_second, second, "teaching second-case inputs")

    assert first_snapshot.section_count <= MAX_TEACHING_SECTIONS
    assert second_snapshot.section_count <= MAX_TEACHING_SECTIONS
    assert first_snapshot.sections[0].title == "Known Scope"
    assert first_snapshot.sections[1].title == "Derived Understanding"
    assert first_snapshot.sections[2].title == "Uncertainty and Limits"
    assert first_snapshot.sections[3].title == "Verification Path"
    assert second_snapshot.section_count == 5
    assert second_snapshot.sections[-1].title == "Honesty Boundary"
    assert first_snapshot.lane_notes
    assert second_snapshot.prerequisite_notes

    checked_files = vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_teaching.py")
    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "teaching-sections-bounded", "result": "pass"},
            {"id": "teaching-honesty-boundary-emitted", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
            {"id": "lane-notes-present", "result": "pass"},
        ],
        anchors={
            "grounded_case": {
                "fixture": first,
                "snapshot": first_snapshot.to_dict(),
            },
            "search_needed_case": {
                "fixture": second,
                "snapshot": second_snapshot.to_dict(),
            },
        },
        notes=["teaching lane keeps uncertainty and verification steps visible"],
    )
    return report


def main() -> int:
    missing = vc.missing_files(vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_teaching.py"))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_teaching.py"),
            assertion_ids=["runtime-imports-available", "teaching-sections-bounded", "teaching-honesty-boundary-emitted"],
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="teaching lane verifier could not import its runtime modules or found missing files",
            missing=missing,
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    try:
        report = build_pass_report()
    except Exception as exc:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_teaching.py"),
            assertion_ids=["runtime-imports-available", "teaching-sections-bounded", "teaching-honesty-boundary-emitted"],
            blocker_kind="verification_failed",
            blocker_message=str(exc),
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    vc.write_report(REPORT_PATH, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
