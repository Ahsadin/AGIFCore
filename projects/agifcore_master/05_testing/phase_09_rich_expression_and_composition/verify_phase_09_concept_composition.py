from __future__ import annotations

import json

import _phase_09_verifier_common as vc
from agifcore_phase9_rich_expression.concept_composition import ConceptCompositionEngine

VERIFIER = "verify_phase_09_concept_composition"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_09_concept_composition_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase9_rich_expression.contracts",
    "agifcore_phase9_rich_expression.concept_composition",
)


def _case(*, request_id: str, support_state: str) -> dict[str, object]:
    raw_text = "Compose the supported concepts into a bounded composite view."
    intake = vc.build_phase7_intake_state(
        conversation_id="conv-p9-comp",
        turn_id=request_id,
        raw_text=raw_text,
    )
    support = vc.build_phase7_support_resolution_state(
        conversation_id="conv-p9-comp",
        turn_id=request_id,
        support_state=support_state,
        knowledge_gap_reason="missing_local_evidence" if support_state in {"search_needed", "unknown"} else "none",
        next_action="clarify" if support_state in {"search_needed", "unknown"} else "answer",
        evidence_refs=("phase7.support.ref.050",),
        selected_domain_ids=("weather_climate",),
        reason_codes=("bounded_local_support",),
    )
    inference = vc.build_phase8_entity_request_inference_state(
        conversation_id="conv-p9-comp",
        turn_id=request_id,
        normalized_text="compose the supported concepts into a bounded composite view",
        extracted_terms=("compose", "concepts", "bounded"),
        science_topic_cues=("weather_climate", "humidity", "sunset"),
        hidden_variable_cues=("gradient", "measurement"),
        candidates=(
            vc.build_entity_request_candidate(
                candidate_id="cand-comp",
                entity_label="weather_climate",
                entity_class="process",
                request_type="science_explanation",
                science_topic_cues=("weather_climate",),
                matched_terms=("weather", "climate"),
                hidden_variable_cues=("gradient",),
                target_domain_hint="weather_climate",
                region_hint=None,
                live_current_requested=False,
                ambiguous_request=False,
                confidence=0.88,
                reason_codes=("explicit_topic_cue",),
            ),
        ),
        support_state_hint=support_state,
        knowledge_gap_reason_hint="missing_local_evidence" if support_state in {"search_needed", "unknown"} else "none",
        inference_notes=("concept composition input is bounded",),
    )
    priors = vc.build_phase8_scientific_priors_state(
        request_id=request_id,
        selected_prior_specs=(
            {
                "selection_id": "sel-prior-001",
                "cell_id": "cell-prior-001",
                "family_name": "scientific_prior",
                "principle_id": "measurement_uncertainty",
                "seed_topic": "measurement and uncertainty",
                "plain_language_law": "Freshness and instrumentation limits control how much certainty is safe.",
                "variables": ("measurement_error", "missing_variables"),
                "causal_mechanism": "Observed values are filtered through sensor and sampling limits.",
                "scope_limits": "Required guardrail for weak or current-fact requests.",
                "failure_case": "A stale reading can look precise while being wrong.",
                "worked_example": "One outdated reading cannot prove the current state of a system.",
                "transfer_hint": "Fail closed when the evidence is weak or freshness is unclear.",
                "cue_terms": ("current", "exact", "uncertain"),
                "hidden_variable_hints": ("live reading", "sampling limits"),
                "provenance_refs": ("phase1.provenance.ref.001",),
                "matched_cue_terms": ("current", "uncertain"),
                "matched_hidden_variables": ("live reading",),
                "relevance_score": 0.91,
                "reason_codes": ("measurements_need_freshness",),
            },
            {
                "selection_id": "sel-prior-002",
                "cell_id": "cell-prior-002",
                "family_name": "scientific_prior",
                "principle_id": "coastal_weather_baseline",
                "seed_topic": "weather and climate",
                "plain_language_law": "Coastal conditions shift through local water, wind, and cooling cycles.",
                "variables": ("coastal_proximity", "humidity", "sunset"),
                "causal_mechanism": "Sea-air exchange and evening cooling can change near-shore conditions.",
                "scope_limits": "Gives bounded directional guidance, not exact live readings.",
                "failure_case": "An inland front can overpower the coastal baseline.",
                "worked_example": "A shoreline block can stay muggy after sunset while inland air cools faster.",
                "transfer_hint": "Check coast, time of day, and moisture before drawing conclusions.",
                "cue_terms": ("coastal", "humidity", "sunset"),
                "hidden_variable_hints": ("sea breeze", "night cooling"),
                "provenance_refs": ("phase1.provenance.ref.002",),
                "matched_cue_terms": ("coastal", "humidity"),
                "matched_hidden_variables": ("sea breeze",),
                "relevance_score": 0.83,
                "reason_codes": ("coastal_conditions",),
            },
        ),
        selection_notes=("prior selection stays bounded and traceable",),
    )
    summary = vc.build_phase8_visible_reasoning_summary_state(
        request_id=request_id,
        what_is_known=("Two governed concepts can be combined safely.",),
        what_is_inferred=("The composite view should stay trace-linked.",),
        uncertainty=("No live field measurement is included.",),
        what_would_verify=("Confirm the selected concepts before widening the composition.",),
        principle_refs=("measurement_uncertainty", "coastal_weather_baseline"),
        causal_chain_ref="chain::comp::001",
        uncertainty_band="moderate",
        live_measurement_required=False,
        evidence_refs=("phase8.summary.ref.050", "phase8.summary.ref.051"),
    )
    return {
        "intake": intake,
        "support": support,
        "inference": inference,
        "priors": priors,
        "summary": summary,
    }


def build_pass_report() -> dict[str, object]:
    engine = ConceptCompositionEngine()
    grounded_fixture = _case(request_id="turn-p9-comp-01", support_state="grounded")
    before_grounded = vc.deep_copy(grounded_fixture)
    grounded_snapshot = engine.build_snapshot(
        entity_request_inference_state=grounded_fixture["inference"],
        scientific_priors_state=grounded_fixture["priors"],
        visible_reasoning_summary_state=grounded_fixture["summary"],
        support_state_resolution_state=grounded_fixture["support"],
    )
    vc.assert_inputs_unchanged(before_grounded, grounded_fixture, "concept composition grounded inputs")

    weak_fixture = _case(request_id="turn-p9-comp-02", support_state="unknown")
    before_weak = vc.deep_copy(weak_fixture)
    weak_snapshot = engine.build_snapshot(
        entity_request_inference_state=weak_fixture["inference"],
        scientific_priors_state=weak_fixture["priors"],
        visible_reasoning_summary_state=weak_fixture["summary"],
        support_state_resolution_state=weak_fixture["support"],
    )
    vc.assert_inputs_unchanged(before_weak, weak_fixture, "concept composition weak inputs")

    assert grounded_snapshot.element_count <= 6
    assert grounded_snapshot.concept_composition_ref
    assert grounded_snapshot.fail_closed is False
    assert weak_snapshot.fail_closed is True
    assert weak_snapshot.element_count <= 6

    checked_files = vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_concept_composition.py")
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "concept-elements-bounded", "result": "pass"},
            {"id": "concept-composition-ref-present", "result": "pass"},
            {"id": "fail-closed-on-weak-support", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "grounded_case": {
                "fixture": grounded_fixture,
                "snapshot": grounded_snapshot.to_dict(),
            },
            "weak_case": {
                "fixture": weak_fixture,
                "snapshot": weak_snapshot.to_dict(),
            },
        },
        notes=["concept composition stays bounded and carries its own trace ref"],
    )


def main() -> int:
    missing = vc.missing_files(vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_concept_composition.py"))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_concept_composition.py"),
            assertion_ids=["runtime-imports-available", "concept-elements-bounded", "concept-composition-ref-present"],
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="concept composition lane verifier could not import its runtime modules or found missing files",
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
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_concept_composition.py"),
            assertion_ids=["runtime-imports-available", "concept-elements-bounded", "concept-composition-ref-present"],
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
