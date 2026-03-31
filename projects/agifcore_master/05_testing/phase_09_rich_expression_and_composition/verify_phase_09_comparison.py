from __future__ import annotations

import json

import _phase_09_verifier_common as vc
from agifcore_phase9_rich_expression.comparison import ComparisonEngine

VERIFIER = "verify_phase_09_comparison"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_09_comparison_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase9_rich_expression.contracts",
    "agifcore_phase9_rich_expression.comparison",
)


def _case(*, request_id: str, comparison_requested: bool) -> dict[str, object]:
    raw_text = "Compare the coastal and inland cases with clear axes."
    intake = vc.build_phase7_intake_state(
        conversation_id="conv-p9-compare",
        turn_id=request_id,
        raw_text=raw_text,
    )
    interpretation = vc.build_phase7_question_interpretation_state(
        conversation_id="conv-p9-compare",
        turn_id=request_id,
        raw_text_hash=intake["intake_hash"],
        user_intent="compare the coastal and inland cases",
        discourse_mode_hint="compare",
        question_category="ordinary",
        target_domain_hint="weather_climate",
        live_current_requested=False,
        ambiguous_request=False,
        self_knowledge_requested=False,
        local_artifact_requested=False,
        correction_hint=False,
        repeated_fact_hint=False,
        comparison_requested=comparison_requested,
        extracted_terms=("coastal", "inland", "compare"),
        signal_notes=("bounded comparison request",),
    )
    support = vc.build_phase7_support_resolution_state(
        conversation_id="conv-p9-compare",
        turn_id=request_id,
        support_state="grounded",
        knowledge_gap_reason="none",
        next_action="answer",
        evidence_refs=("phase7.support.ref.010",),
        selected_domain_ids=("weather_climate",),
        reason_codes=("bounded_local_support",),
    )
    inference = vc.build_phase8_entity_request_inference_state(
        conversation_id="conv-p9-compare",
        turn_id=request_id,
        normalized_text="compare the coastal and inland cases with clear axes",
        extracted_terms=("coastal", "inland", "compare"),
        science_topic_cues=("weather_climate", "coast", "inland"),
        hidden_variable_cues=("wind", "humidity"),
        candidates=(
            vc.build_entity_request_candidate(
                candidate_id="cand-coast",
                entity_label="coast",
                entity_class="place",
                request_type="comparison",
                science_topic_cues=("weather_climate",),
                matched_terms=("coastal",),
                hidden_variable_cues=("humidity",),
                target_domain_hint="weather_climate",
                region_hint="coast",
                live_current_requested=False,
                ambiguous_request=False,
                confidence=0.92,
                reason_codes=("explicit_request_target",),
            ),
            vc.build_entity_request_candidate(
                candidate_id="cand-inland",
                entity_label="inland",
                entity_class="place",
                request_type="comparison",
                science_topic_cues=("weather_climate",),
                matched_terms=("inland",),
                hidden_variable_cues=("temperature",),
                target_domain_hint="weather_climate",
                region_hint="inland",
                live_current_requested=False,
                ambiguous_request=False,
                confidence=0.88,
                reason_codes=("explicit_request_target",),
            ),
        ),
        support_state_hint="grounded",
        knowledge_gap_reason_hint="none",
        inference_notes=("comparison candidate set is bounded",),
    )
    summary = vc.build_phase8_visible_reasoning_summary_state(
        request_id=request_id,
        what_is_known=("Both places can be described with bounded local evidence.",),
        what_is_inferred=("Each side may differ in humidity and cooling rate.",),
        uncertainty=("No live field measurement is included.",),
        what_would_verify=("Check a fresh station reading for each place.",),
        principle_refs=("measurement_uncertainty",),
        causal_chain_ref="chain::compare::001",
        uncertainty_band="moderate",
        live_measurement_required=False,
        evidence_refs=("phase8.summary.ref.010", "phase8.summary.ref.011"),
    )
    return {
        "intake": intake,
        "interpretation": interpretation,
        "support": support,
        "inference": inference,
        "summary": summary,
    }


def build_pass_report() -> dict[str, object]:
    engine = ComparisonEngine()
    fixture = _case(request_id="turn-p9-compare-01", comparison_requested=True)
    before = vc.deep_copy(fixture)
    snapshot = engine.build_snapshot(
        question_interpretation_state=fixture["interpretation"],
        support_state_resolution_state=fixture["support"],
        entity_request_inference_state=fixture["inference"],
        visible_reasoning_summary_state=fixture["summary"],
    )
    vc.assert_inputs_unchanged(before, fixture, "comparison inputs")

    assert snapshot.axis_count <= 5
    assert snapshot.axis_count == 4
    assert snapshot.axes[0].axis_label == "Support State"
    assert snapshot.axes[1].axis_label == "Known vs Inferred Coverage"
    assert snapshot.axes[2].axis_label == "Uncertainty Exposure"
    assert snapshot.axes[3].axis_label == "Intent Alignment"
    assert all(axis.supporting_refs for axis in snapshot.axes)

    checked_files = vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_comparison.py")
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "comparison-axes-bounded", "result": "pass"},
            {"id": "comparison-intent-respected", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
            {"id": "supporting-refs-present", "result": "pass"},
        ],
        anchors={
            "fixture": fixture,
            "snapshot": snapshot.to_dict(),
        },
        notes=["comparison lane keeps asymmetry explicit and bounded"],
    )


def main() -> int:
    missing = vc.missing_files(vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_comparison.py"))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_comparison.py"),
            assertion_ids=["runtime-imports-available", "comparison-axes-bounded", "comparison-intent-respected"],
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="comparison lane verifier could not import its runtime modules or found missing files",
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
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_comparison.py"),
            assertion_ids=["runtime-imports-available", "comparison-axes-bounded", "comparison-intent-respected"],
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
