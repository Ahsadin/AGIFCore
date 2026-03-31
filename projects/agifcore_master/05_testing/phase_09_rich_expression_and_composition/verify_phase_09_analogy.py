from __future__ import annotations

import json

import _phase_09_verifier_common as vc
from agifcore_phase9_rich_expression.analogy import AnalogyEngine
from agifcore_phase9_rich_expression.contracts import MAX_ANALOGIES_PER_RESPONSE

VERIFIER = "verify_phase_09_analogy"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_09_analogy_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase9_rich_expression.contracts",
    "agifcore_phase9_rich_expression.analogy",
)


def _case(*, request_id: str, cue: str) -> dict[str, object]:
    raw_text = "Use one bounded analogy, show where it breaks, and do not overclaim."
    intake = vc.build_phase7_intake_state(
        conversation_id="conv-p9-analogy",
        turn_id=request_id,
        raw_text=raw_text,
    )
    support = vc.build_phase7_support_resolution_state(
        conversation_id="conv-p9-analogy",
        turn_id=request_id,
        support_state="grounded",
        knowledge_gap_reason="none",
        next_action="answer",
        evidence_refs=("phase7.support.ref.040",),
        selected_domain_ids=("weather_climate",),
        reason_codes=("bounded_local_support",),
    )
    inference = vc.build_phase8_entity_request_inference_state(
        conversation_id="conv-p9-analogy",
        turn_id=request_id,
        normalized_text=f"use one bounded analogy about {cue}",
        extracted_terms=("analogy", cue),
        science_topic_cues=(cue,),
        hidden_variable_cues=("gradient",),
        candidates=(
            vc.build_entity_request_candidate(
                candidate_id="cand-analogy",
                entity_label=cue,
                entity_class="process",
                request_type="science_explanation",
                science_topic_cues=(cue,),
                matched_terms=(cue,),
                hidden_variable_cues=("gradient",),
                target_domain_hint="weather_climate",
                region_hint=None,
                live_current_requested=False,
                ambiguous_request=False,
                confidence=0.9,
                reason_codes=("explicit_topic_cue",),
            ),
        ),
        support_state_hint="grounded",
        knowledge_gap_reason_hint="none",
        inference_notes=("analogy candidate set is bounded",),
    )
    summary = vc.build_phase8_visible_reasoning_summary_state(
        request_id=request_id,
        what_is_known=("A bounded structural mapping can help explanation.",),
        what_is_inferred=("The analogy should not be mistaken for proof.",),
        uncertainty=("The metaphor breaks when the systems differ materially.",),
        what_would_verify=("Check the underlying mechanism directly.",),
        principle_refs=("measurement_uncertainty",),
        causal_chain_ref="chain::analogy::001",
        uncertainty_band="moderate",
        live_measurement_required=False,
        evidence_refs=("phase8.summary.ref.040", "phase8.summary.ref.041"),
    )
    return {
        "intake": intake,
        "support": support,
        "inference": inference,
        "summary": summary,
    }


def build_pass_report() -> dict[str, object]:
    engine = AnalogyEngine()
    fixture = _case(request_id="turn-p9-analogy-01", cue="thermodynamics")
    before = vc.deep_copy(fixture)
    snapshot = engine.build_snapshot(
        entity_request_inference_state=fixture["inference"],
        visible_reasoning_summary_state=fixture["summary"],
        support_state_resolution_state=fixture["support"],
    )
    vc.assert_inputs_unchanged(before, fixture, "analogy inputs")

    assert snapshot.analogy_count <= MAX_ANALOGIES_PER_RESPONSE
    assert snapshot.analogy_count == 1
    assert snapshot.analogy_trace_ref
    assert snapshot.support_refs
    assert snapshot.mappings[0].break_limit
    assert snapshot.mappings[0].supporting_refs

    checked_files = vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_analogy.py")
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "analogy-count-bounded", "result": "pass"},
            {"id": "analogy-trace-ref-present", "result": "pass"},
            {"id": "break-limits-and-support-refs-present", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "fixture": fixture,
            "snapshot": snapshot.to_dict(),
        },
        notes=["analogy lane is illustrative only and never treats metaphor as proof"],
    )


def main() -> int:
    missing = vc.missing_files(vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_analogy.py"))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_analogy.py"),
            assertion_ids=["runtime-imports-available", "analogy-count-bounded", "analogy-trace-ref-present"],
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="analogy lane verifier could not import its runtime modules or found missing files",
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
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_analogy.py"),
            assertion_ids=["runtime-imports-available", "analogy-count-bounded", "analogy-trace-ref-present"],
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
