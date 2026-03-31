from __future__ import annotations

import json

import _phase_09_verifier_common as vc
from agifcore_phase9_rich_expression.audience_aware_explanation_quality import (
    AudienceAwareExplanationQualityEngine,
)
from agifcore_phase9_rich_expression.contracts import AudienceProfile, BrevityLevel, ExpressionLane, TerminologyDensity

VERIFIER = "verify_phase_09_audience_aware_explanation_quality"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_09_audience_aware_explanation_quality_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase9_rich_expression.contracts",
    "agifcore_phase9_rich_expression.audience_aware_explanation_quality",
)


def _case(*, request_id: str, user_intent: str, selected_lane: ExpressionLane, support_state: str) -> dict[str, object]:
    raw_text = user_intent
    intake = vc.build_phase7_intake_state(
        conversation_id="conv-p9-audience",
        turn_id=request_id,
        raw_text=raw_text,
    )
    interpretation = vc.build_phase7_question_interpretation_state(
        conversation_id="conv-p9-audience",
        turn_id=request_id,
        raw_text_hash=intake["intake_hash"],
        user_intent=user_intent,
        discourse_mode_hint=selected_lane.value,
        question_category="ordinary",
        target_domain_hint="weather_climate",
        live_current_requested=False,
        ambiguous_request=False,
        self_knowledge_requested=False,
        local_artifact_requested=False,
        correction_hint=False,
        repeated_fact_hint=False,
        comparison_requested=selected_lane is ExpressionLane.COMPARISON,
        extracted_terms=tuple(word for word in user_intent.lower().split() if word),
        signal_notes=("audience adaptation request",),
    )
    support = vc.build_phase7_support_resolution_state(
        conversation_id="conv-p9-audience",
        turn_id=request_id,
        support_state=support_state,
        knowledge_gap_reason="missing_local_evidence" if support_state in {"search_needed", "unknown"} else "none",
        next_action="clarify" if support_state in {"search_needed", "unknown"} else "answer",
        evidence_refs=("phase7.support.ref.070",),
        selected_domain_ids=("weather_climate",),
        reason_codes=("bounded_local_support",),
    )
    utterance_plan = vc.build_phase7_utterance_plan_state(
        conversation_id="conv-p9-audience",
        turn_id=request_id,
        discourse_mode=selected_lane.value,
        response_sections=("scope", "steps", "verification"),
        sentence_obligations=("keep_uncertainty_visible", "avoid_generic_openers"),
        constraint_slots=("support_honesty", "audience_profile"),
        branch_count=4,
    )
    return {
        "intake": intake,
        "interpretation": interpretation,
        "support": support,
        "utterance_plan": utterance_plan,
        "selected_lane": selected_lane,
    }


def build_pass_report() -> dict[str, object]:
    engine = AudienceAwareExplanationQualityEngine()
    novice_fixture = _case(
        request_id="turn-p9-audience-01",
        user_intent="Please explain this simply for a beginner.",
        selected_lane=ExpressionLane.TEACHING,
        support_state="unknown",
    )
    novice_before = vc.deep_copy(novice_fixture)
    novice_snapshot = engine.build_snapshot(
        intake_state=novice_fixture["intake"],
        question_interpretation_state=novice_fixture["interpretation"],
        support_state_resolution_state=novice_fixture["support"],
        utterance_plan_state=novice_fixture["utterance_plan"],
        selected_lane=novice_fixture["selected_lane"],
    )
    vc.assert_inputs_unchanged(novice_before, novice_fixture, "audience-quality novice inputs")

    technical_fixture = _case(
        request_id="turn-p9-audience-02",
        user_intent="Provide a technical explanation with exact terms.",
        selected_lane=ExpressionLane.COMPARISON,
        support_state="grounded",
    )
    technical_before = vc.deep_copy(technical_fixture)
    technical_snapshot = engine.build_snapshot(
        intake_state=technical_fixture["intake"],
        question_interpretation_state=technical_fixture["interpretation"],
        support_state_resolution_state=technical_fixture["support"],
        utterance_plan_state=technical_fixture["utterance_plan"],
        selected_lane=technical_fixture["selected_lane"],
    )
    vc.assert_inputs_unchanged(technical_before, technical_fixture, "audience-quality technical inputs")

    assert novice_snapshot.audience_profile is AudienceProfile.NOVICE
    assert novice_snapshot.terminology_density is TerminologyDensity.LOW
    assert novice_snapshot.brevity_level is BrevityLevel.BALANCED
    assert novice_snapshot.section_order == ("scope", "steps", "misconceptions", "verification")
    assert novice_snapshot.uncertainty_preserved is True
    assert novice_snapshot.caution_preserved is True
    assert novice_snapshot.rewrite_applied is True
    assert technical_snapshot.audience_profile is AudienceProfile.TECHNICAL
    assert technical_snapshot.terminology_density is TerminologyDensity.HIGH
    assert technical_snapshot.section_order == ("axes", "asymmetry", "limits", "verification")
    assert len(technical_snapshot.section_order) <= 4
    assert len(novice_snapshot.anti_filler_checks) <= 8

    checked_files = vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_audience_aware_explanation_quality.py")
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "audience-profile-selected", "result": "pass"},
            {"id": "terminology-and-brevity-bounded", "result": "pass"},
            {"id": "uncertainty-and-caution-preserved", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "novice_case": {
                "fixture": novice_fixture,
                "snapshot": novice_snapshot.to_dict(),
            },
            "technical_case": {
                "fixture": technical_fixture,
                "snapshot": technical_snapshot.to_dict(),
            },
        },
        notes=["audience-aware quality stays clarity-oriented and does not become persuasion"],
    )


def main() -> int:
    missing = vc.missing_files(vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_audience_aware_explanation_quality.py"))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_audience_aware_explanation_quality.py"),
            assertion_ids=["runtime-imports-available", "audience-profile-selected", "terminology-and-brevity-bounded"],
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="audience-quality lane verifier could not import its runtime modules or found missing files",
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
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_audience_aware_explanation_quality.py"),
            assertion_ids=["runtime-imports-available", "audience-profile-selected", "terminology-and-brevity-bounded"],
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
