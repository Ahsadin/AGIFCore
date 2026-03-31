from __future__ import annotations

import json

import _phase_09_verifier_common as vc
from agifcore_phase9_rich_expression.cross_domain_composition import CrossDomainCompositionEngine

VERIFIER = "verify_phase_09_cross_domain_composition"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_09_cross_domain_composition_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase9_rich_expression.contracts",
    "agifcore_phase9_rich_expression.cross_domain_composition",
)


def _concept_case(
    *,
    request_id: str,
    support_state: str,
    domain_count: int,
) -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, object], dict[str, object]]:
    raw_text = "Bridge exactly two domains and fail closed if a third appears."
    intake = vc.build_phase7_intake_state(
        conversation_id="conv-p9-cross",
        turn_id=request_id,
        raw_text=raw_text,
    )
    interpretation = vc.build_phase7_question_interpretation_state(
        conversation_id="conv-p9-cross",
        turn_id=request_id,
        raw_text_hash=intake["intake_hash"],
        user_intent="bridge exactly two domains",
        discourse_mode_hint="compare",
        question_category="ordinary",
        target_domain_hint="weather_climate",
        live_current_requested=False,
        ambiguous_request=False,
        self_knowledge_requested=False,
        local_artifact_requested=False,
        correction_hint=False,
        repeated_fact_hint=False,
        comparison_requested=True,
        extracted_terms=("bridge", "domains"),
        signal_notes=("cross-domain request",),
    )
    support = vc.build_phase7_support_resolution_state(
        conversation_id="conv-p9-cross",
        turn_id=request_id,
        support_state=support_state,
        knowledge_gap_reason="none" if support_state == "grounded" else "missing_local_evidence",
        next_action="answer" if support_state == "grounded" else "clarify",
        evidence_refs=("phase7.support.ref.060",),
        selected_domain_ids=("weather_climate", "place_region_context"),
        reason_codes=("bounded_local_support",),
    )
    inference = vc.build_phase8_entity_request_inference_state(
        conversation_id="conv-p9-cross",
        turn_id=request_id,
        normalized_text="bridge exactly two domains and fail closed if a third appears",
        extracted_terms=("bridge", "domains", "fail closed"),
        science_topic_cues=("weather_climate", "place_region_context", "engineering_systems"),
        hidden_variable_cues=("shared pattern",),
        candidates=(
            vc.build_entity_request_candidate(
                candidate_id="cand-cross-001",
                entity_label="weather_climate",
                entity_class="process",
                request_type="comparison",
                science_topic_cues=("weather_climate",),
                matched_terms=("weather", "climate"),
                hidden_variable_cues=("shared pattern",),
                target_domain_hint="weather_climate",
                region_hint=None,
                live_current_requested=False,
                ambiguous_request=False,
                confidence=0.9,
                reason_codes=("explicit_topic_cue",),
            ),
            vc.build_entity_request_candidate(
                candidate_id="cand-cross-002",
                entity_label="place_region_context",
                entity_class="place",
                request_type="comparison",
                science_topic_cues=("place_region_context",),
                matched_terms=("place", "region"),
                hidden_variable_cues=("shared pattern",),
                target_domain_hint="place_region_context",
                region_hint=None,
                live_current_requested=False,
                ambiguous_request=False,
                confidence=0.87,
                reason_codes=("explicit_topic_cue",),
            ),
        ),
        support_state_hint=support_state,
        knowledge_gap_reason_hint="none" if support_state == "grounded" else "missing_local_evidence",
        inference_notes=("cross-domain candidate set is bounded",),
    )
    region_candidates: list[dict[str, object]] = [
        vc.build_world_region_candidate(
            region_id="region-weather",
            region_label="weather zone",
            region_kind="target_domain",
            target_domain="weather_climate",
            supporting_refs=("phase8.region.ref.001",),
            matched_terms=("weather", "climate"),
            reason_codes=("domain_anchor",),
            confidence=0.9,
        ),
        vc.build_world_region_candidate(
            region_id="region-place",
            region_label="place zone",
            region_kind="target_domain",
            target_domain="place_region_context",
            supporting_refs=("phase8.region.ref.002",),
            matched_terms=("place", "region"),
            reason_codes=("domain_anchor",),
            confidence=0.88,
        ),
        vc.build_world_region_candidate(
            region_id="region-extra",
            region_label="extra zone",
            region_kind="inferred_context",
            target_domain="engineering_systems",
            supporting_refs=("phase8.region.ref.003",),
            matched_terms=("engineer",),
            reason_codes=("extra_domain_probe",),
            confidence=0.4,
        ),
    ]
    region_state = vc.build_phase8_world_region_selection_state(
        request_id=request_id,
        candidates=tuple(region_candidates[:domain_count]),
        selected_region_id="region-weather",
        reason_codes=("bounded_region_choice",),
        unresolved=False,
    )
    concept = vc.build_phase09_concept_fixture_for_cross_domain(request_id=request_id, support_state=support_state)
    return interpretation, support, inference, region_state, concept


def build_pass_report() -> dict[str, object]:
    engine = CrossDomainCompositionEngine()
    exact_case = _concept_case(request_id="turn-p9-cross-01", support_state="grounded", domain_count=2)
    exact_before = vc.deep_copy(exact_case)
    exact_snapshot = engine.build_snapshot(
        question_interpretation_state=exact_case[0],
        support_state_resolution_state=exact_case[1],
        entity_request_inference_state=exact_case[2],
        world_region_selection_state=exact_case[3],
        concept_composition_state=exact_case[4],
    )
    vc.assert_inputs_unchanged(exact_before, exact_case, "cross-domain exact inputs")

    over_case = _concept_case(request_id="turn-p9-cross-02", support_state="grounded", domain_count=3)
    over_before = vc.deep_copy(over_case)
    over_snapshot = engine.build_snapshot(
        question_interpretation_state=over_case[0],
        support_state_resolution_state=over_case[1],
        entity_request_inference_state=over_case[2],
        world_region_selection_state=over_case[3],
        concept_composition_state=over_case[4],
    )
    vc.assert_inputs_unchanged(over_before, over_case, "cross-domain over-limit inputs")

    assert exact_snapshot.element_count <= 4
    assert len(exact_snapshot.domain_refs) == 2
    assert exact_snapshot.concept_composition_ref
    assert over_snapshot.element_count <= 4
    assert len(over_snapshot.domain_refs) == 2
    assert "domain_count_bounded_to_two" in over_snapshot.reason_codes

    checked_files = vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_cross_domain_composition.py")
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "exactly-two-domains-kept", "result": "pass"},
            {"id": "over-limit-domains-bounded", "result": "pass"},
            {"id": "concept-composition-ref-preserved", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "exact_case": {
                "fixture": exact_case,
                "snapshot": exact_snapshot.to_dict(),
            },
            "over_limit_case": {
                "fixture": over_case,
                "snapshot": over_snapshot.to_dict(),
            },
        },
        notes=["cross-domain composition defaults to exactly two domains and fail-closes on under-support"],
    )


def main() -> int:
    missing = vc.missing_files(vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_cross_domain_composition.py"))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_cross_domain_composition.py"),
            assertion_ids=["runtime-imports-available", "exactly-two-domains-kept", "over-limit-domains-bounded"],
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="cross-domain composition lane verifier could not import its runtime modules or found missing files",
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
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_cross_domain_composition.py"),
            assertion_ids=["runtime-imports-available", "exactly-two-domains-kept", "over-limit-domains-bounded"],
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
