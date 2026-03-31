from __future__ import annotations

import json

import _phase_08_verifier_common as vc

VERIFIER = "verify_phase_08_entity_request_inference"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_08_entity_request_inference_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase8_science_world_awareness.contracts",
    "agifcore_phase8_science_world_awareness.entity_request_inference",
)
OWNED_FILES = (
    "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/_phase_08_verifier_common.py",
    "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_entity_request_inference.py",
)


def _build_intake(*, conversation_id: str, turn_id: str, raw_text: str) -> dict[str, object]:
    normalized_text = raw_text.lower()
    return {
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "raw_text": raw_text,
        "normalized_text": normalized_text,
        "active_context_refs": [],
        "token_count": len(raw_text.split()),
        "character_count": len(raw_text),
        "contains_code_block": False,
        "ends_with_question": raw_text.rstrip().endswith("?"),
        "intake_hash": f"{conversation_id}:{turn_id}:{normalized_text}",
    }


def _build_interpretation(
    *,
    extracted_terms: tuple[str, ...],
    live_current_requested: bool,
    ambiguous_request: bool,
    self_knowledge_requested: bool,
    target_domain_hint: str | None,
) -> dict[str, object]:
    return {
        "schema": "agifcore.phase_07.question_interpretation.v1",
        "extracted_terms": list(extracted_terms),
        "live_current_requested": live_current_requested,
        "ambiguous_request": ambiguous_request,
        "self_knowledge_requested": self_knowledge_requested,
        "comparison_requested": False,
        "target_domain_hint": target_domain_hint,
    }


def _build_support_state(*, support_state: str, knowledge_gap_reason: str, next_action: str) -> dict[str, object]:
    return {
        "schema": "agifcore.phase_07.support_state_logic.v1",
        "support_state": support_state,
        "knowledge_gap_reason": knowledge_gap_reason,
        "next_action": next_action,
        "evidence_refs": [],
        "blocked_refs": [],
    }


def build_pass_report() -> dict[str, object]:
    from agifcore_phase8_science_world_awareness.contracts import MAX_INFERENCE_CANDIDATES
    from agifcore_phase8_science_world_awareness.entity_request_inference import EntityRequestInferenceEngine

    engine = EntityRequestInferenceEngine()

    self_knowledge = engine.build_snapshot(
        intake_state=_build_intake(
            conversation_id="conv-eri",
            turn_id="turn-eri-1",
            raw_text="What can you do in this AGIFCore repo?",
        ),
        question_interpretation_state=_build_interpretation(
            extracted_terms=("agifcore", "repo"),
            live_current_requested=False,
            ambiguous_request=False,
            self_knowledge_requested=True,
            target_domain_hint=None,
        ),
        support_state_resolution_state=_build_support_state(
            support_state="grounded",
            knowledge_gap_reason="none",
            next_action="answer",
        ),
    )
    if self_knowledge.candidate_count > MAX_INFERENCE_CANDIDATES:
        raise RuntimeError("self-knowledge inference exceeded the Phase 8 candidate ceiling")
    if "self_knowledge_requested_from_phase7" not in self_knowledge.inference_notes:
        raise RuntimeError("self-knowledge cue was not preserved in inference notes")

    live_current = engine.build_snapshot(
        intake_state=_build_intake(
            conversation_id="conv-eri",
            turn_id="turn-eri-2",
            raw_text="What is the latest weather in Boston today?",
        ),
        question_interpretation_state=_build_interpretation(
            extracted_terms=("weather", "boston", "today"),
            live_current_requested=True,
            ambiguous_request=False,
            self_knowledge_requested=False,
            target_domain_hint="weather_climate",
        ),
        support_state_resolution_state=_build_support_state(
            support_state="search_needed",
            knowledge_gap_reason="needs_fresh_information",
            next_action="search_external",
        ),
    )
    if live_current.candidate_count > MAX_INFERENCE_CANDIDATES:
        raise RuntimeError("live-current inference exceeded the Phase 8 candidate ceiling")
    if live_current.support_state_hint != "search_needed":
        raise RuntimeError("live-current cue or support hint was not preserved")
    if live_current.knowledge_gap_reason_hint != "needs_fresh_information":
        raise RuntimeError("fresh-information honesty was not preserved")
    if "live_current_requested_from_phase7" not in live_current.inference_notes:
        raise RuntimeError("live-current cue was not recorded in inference notes")
    if "fresh_information_honesty_preserved" not in live_current.inference_notes:
        raise RuntimeError("fresh-information honesty note was not recorded")
    if not all(candidate.live_current_requested for candidate in live_current.candidates):
        raise RuntimeError("live-current cue was not propagated to all candidates")
    if "sensor_freshness" not in live_current.hidden_variable_cues:
        raise RuntimeError("live-current request did not surface sensor freshness cues")

    ambiguous = engine.build_snapshot(
        intake_state=_build_intake(
            conversation_id="conv-eri",
            turn_id="turn-eri-3",
            raw_text="What about Boston?",
        ),
        question_interpretation_state=_build_interpretation(
            extracted_terms=("boston",),
            live_current_requested=False,
            ambiguous_request=True,
            self_knowledge_requested=False,
            target_domain_hint=None,
        ),
        support_state_resolution_state=_build_support_state(
            support_state="unknown",
            knowledge_gap_reason="none",
            next_action="answer",
        ),
    )
    if ambiguous.candidate_count > MAX_INFERENCE_CANDIDATES:
        raise RuntimeError("ambiguous inference exceeded the Phase 8 candidate ceiling")
    if not any(candidate.ambiguous_request for candidate in ambiguous.candidates):
        raise RuntimeError("ambiguity cue was not propagated to candidates")
    if ambiguous.selected_candidate_id is not None:
        raise RuntimeError("ambiguous request should not have selected a candidate")
    if "ambiguity_detected_from_phase7" not in ambiguous.inference_notes:
        raise RuntimeError("ambiguity cue was not recorded in inference notes")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(vc.RUNTIME_FILES) + list(OWNED_FILES),
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "self-knowledge-cues-preserved", "result": "pass"},
            {"id": "live-current-cues-preserved", "result": "pass"},
            {"id": "fresh-information-honesty-preserved", "result": "pass"},
            {"id": "ambiguity-cues-preserved", "result": "pass"},
            {"id": "candidate-ceiling-enforced", "result": "pass"},
        ],
        anchors={
            "self_knowledge_request": self_knowledge.to_dict(),
            "live_current_request": live_current.to_dict(),
            "ambiguous_request": ambiguous.to_dict(),
        },
        notes=["entity request inference preserves self-knowledge, live-current, and ambiguity cues"],
    )
    vc.refresh_evidence_manifest()
    return report


def main() -> int:
    missing = vc.missing_files(list(vc.PLAN_REFS) + list(vc.RUNTIME_FILES) + list(OWNED_FILES))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(vc.RUNTIME_FILES) + list(OWNED_FILES),
            assertion_ids=[
                "runtime-imports-available",
                "self-knowledge-cues-preserved",
                "live-current-cues-preserved",
                "fresh-information-honesty-preserved",
                "ambiguity-cues-preserved",
                "candidate-ceiling-enforced",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 8 entity-request inference runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_08 entity_request_inference verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_08 entity_request_inference verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
