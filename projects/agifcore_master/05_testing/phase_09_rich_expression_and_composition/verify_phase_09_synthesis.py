from __future__ import annotations

import json

import _phase_09_verifier_common as vc
from agifcore_phase9_rich_expression.synthesis import SynthesisEngine

VERIFIER = "verify_phase_09_synthesis"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_09_synthesis_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase9_rich_expression.contracts",
    "agifcore_phase9_rich_expression.synthesis",
)


def _case(*, request_id: str, support_state: str, needs_fresh_information: bool) -> dict[str, object]:
    raw_text = "Synthesize the supported points without hiding the uncertainty."
    intake = vc.build_phase7_intake_state(
        conversation_id="conv-p9-synth",
        turn_id=request_id,
        raw_text=raw_text,
    )
    interpretation = vc.build_phase7_question_interpretation_state(
        conversation_id="conv-p9-synth",
        turn_id=request_id,
        raw_text_hash=intake["intake_hash"],
        user_intent="synthesize the supported points",
        discourse_mode_hint="synthesize",
        question_category="ordinary",
        target_domain_hint="weather_climate",
        live_current_requested=False,
        ambiguous_request=False,
        self_knowledge_requested=False,
        local_artifact_requested=False,
        correction_hint=False,
        repeated_fact_hint=False,
        comparison_requested=False,
        extracted_terms=("synthesize", "supported", "uncertainty"),
        signal_notes=("bounded synthesis request",),
    )
    support = vc.build_phase7_support_resolution_state(
        conversation_id="conv-p9-synth",
        turn_id=request_id,
        support_state=support_state,
        knowledge_gap_reason="missing_local_evidence" if support_state in {"search_needed", "unknown"} else "none",
        next_action="clarify" if support_state in {"search_needed", "unknown"} else "answer",
        evidence_refs=("phase7.support.ref.030",),
        selected_domain_ids=("weather_climate",),
        reason_codes=("bounded_local_support",),
    )
    summary = vc.build_phase8_visible_reasoning_summary_state(
        request_id=request_id,
        what_is_known=("Local support exists for a bounded synthesis.",),
        what_is_inferred=("The synthesis should preserve uncertainty.",),
        uncertainty=("One missing variable still blocks a stronger claim.",),
        what_would_verify=("Acquire the missing variable.",),
        principle_refs=("measurement_uncertainty",),
        causal_chain_ref="chain::synth::001",
        uncertainty_band="high" if support_state in {"search_needed", "unknown"} else "moderate",
        live_measurement_required=needs_fresh_information,
        evidence_refs=("phase8.summary.ref.030", "phase8.summary.ref.031"),
    )
    reflection = vc.build_phase8_science_reflection_state(
        request_id=request_id,
        records=(
            vc.build_science_reflection_record(
                record_id=f"reflect::{request_id}::01",
                kind="falsifier",
                note="A missing variable could alter the synthesis.",
                source_ref="phase8.summary.ref.030",
                next_verification_step="Name the missing variable before generalizing.",
                increases_uncertainty=True,
            ),
        ),
        uncertainty_should_increase=needs_fresh_information,
    )
    bounded = vc.build_phase8_bounded_current_world_reasoning_state(
        request_id=request_id,
        decision="needs_fresh_information" if needs_fresh_information else "bounded_local_support",
        live_current_requested=needs_fresh_information,
        needs_fresh_information=needs_fresh_information,
        live_measurement_required=needs_fresh_information,
        exact_current_fact_allowed=False,
        bounded_local_support_refs=("phase8.boundary.ref.030",),
        evidence_refs=("phase8.boundary.ref.030",),
        reason_codes=("fresh_measurement_required",) if needs_fresh_information else ("bounded_local_support",),
    )
    return {
        "intake": intake,
        "interpretation": interpretation,
        "support": support,
        "summary": summary,
        "reflection": reflection,
        "bounded": bounded,
    }


def build_pass_report() -> dict[str, object]:
    engine = SynthesisEngine()
    fixture = _case(request_id="turn-p9-synth-01", support_state="grounded", needs_fresh_information=False)
    before = vc.deep_copy(fixture)
    snapshot = engine.build_snapshot(
        question_interpretation_state=fixture["interpretation"],
        support_state_resolution_state=fixture["support"],
        visible_reasoning_summary_state=fixture["summary"],
        science_reflection_state=fixture["reflection"],
        bounded_current_world_reasoning_state=fixture["bounded"],
    )
    vc.assert_inputs_unchanged(before, fixture, "synthesis inputs")

    assert snapshot.input_count <= 12
    assert snapshot.preserves_support_honesty is True
    assert snapshot.uncertainty_level.value in {"moderate", "high", "low"}
    assert snapshot.lane_notes
    assert snapshot.merged_summary

    checked_files = vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_synthesis.py")
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "synthesis-inputs-bounded", "result": "pass"},
            {"id": "support-honesty-preserved", "result": "pass"},
            {"id": "uncertainty-surfaced", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "fixture": fixture,
            "snapshot": snapshot.to_dict(),
        },
        notes=["synthesis lane preserves declared uncertainty instead of smoothing it away"],
    )


def main() -> int:
    missing = vc.missing_files(vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_synthesis.py"))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_synthesis.py"),
            assertion_ids=["runtime-imports-available", "synthesis-inputs-bounded", "support-honesty-preserved"],
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="synthesis lane verifier could not import its runtime modules or found missing files",
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
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_synthesis.py"),
            assertion_ids=["runtime-imports-available", "synthesis-inputs-bounded", "support-honesty-preserved"],
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
