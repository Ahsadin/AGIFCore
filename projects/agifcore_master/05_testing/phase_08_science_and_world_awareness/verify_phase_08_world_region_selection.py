from __future__ import annotations

import json

import _phase_08_verifier_common as vc

VERIFIER = "verify_phase_08_world_region_selection"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_08_world_region_selection_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase8_science_world_awareness.contracts",
    "agifcore_phase8_science_world_awareness.entity_request_inference",
    "agifcore_phase8_science_world_awareness.world_region_selection",
)
OWNED_FILES = (
    "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/_phase_08_verifier_common.py",
    "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_world_region_selection.py",
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


def _build_target_domains() -> dict[str, object]:
    return {
        "schema": "agifcore.phase_06.target_domains.v1",
        "structures": [
            {
                "domain_id": "weather_climate",
                "domain_name": "weather climate",
                "prefixes": ["weather."],
                "descriptor_tokens": ["weather", "climate"],
                "object_templates": ["weather.climate"],
                "requires_target_match": True,
                "minimum_signal_groups": 3,
                "objects": [],
            },
            {
                "domain_id": "place_region_context",
                "domain_name": "place region context",
                "prefixes": ["place."],
                "descriptor_tokens": ["place", "region", "coast"],
                "object_templates": ["place.region"],
                "requires_target_match": False,
                "minimum_signal_groups": 3,
                "objects": [],
            },
        ],
    }


def _build_world_model() -> dict[str, object]:
    return {
        "schema": "agifcore.phase_06.world_model.v1",
        "entities": [
            {
                "entity_id": "world::target::weather_climate",
                "label": "weather climate",
                "target_domain": "weather_climate",
                "status": "review_only",
                "world_confidence": 0.8,
                "source_refs": ["weather_climate"],
            },
            {
                "entity_id": "world::entity::boston",
                "label": "Boston",
                "target_domain": "weather_climate",
                "status": "review_only",
                "world_confidence": 0.7,
                "source_refs": ["boston_src"],
            },
            {
                "entity_id": "world::entity::coast",
                "label": "coast",
                "target_domain": "place_region_context",
                "status": "review_only",
                "world_confidence": 0.45,
                "source_refs": ["coast_src"],
            },
        ],
    }


def build_pass_report() -> dict[str, object]:
    from agifcore_phase8_science_world_awareness.contracts import MAX_REGION_CANDIDATES, RegionKind
    from agifcore_phase8_science_world_awareness.entity_request_inference import EntityRequestInferenceEngine
    from agifcore_phase8_science_world_awareness.world_region_selection import WorldRegionSelectionEngine

    inference_engine = EntityRequestInferenceEngine()
    region_engine = WorldRegionSelectionEngine()

    safe_inference = inference_engine.build_snapshot(
        intake_state=_build_intake(
            conversation_id="conv-wrs",
            turn_id="turn-wrs-1",
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
    safe_selection = region_engine.build_snapshot(
        entity_request_inference_state=safe_inference.to_dict(),
        target_domain_registry_state=_build_target_domains(),
        world_model_state=_build_world_model(),
    )
    if safe_selection.candidate_count > MAX_REGION_CANDIDATES:
        raise RuntimeError("safe region selection exceeded the Phase 8 candidate ceiling")
    if safe_selection.unresolved:
        raise RuntimeError("safe region selection should have resolved to a region")
    if safe_selection.selected_region_id is None:
        raise RuntimeError("safe region selection did not choose a region")
    if safe_selection.candidates[0].region_kind != RegionKind.TARGET_DOMAIN:
        raise RuntimeError("safe region selection did not prioritize the target-domain match")
    if safe_selection.candidates[0].region_id != safe_selection.selected_region_id:
        raise RuntimeError("safe region selection did not preserve the top-ranked region id")

    unresolved_inference = inference_engine.build_snapshot(
        intake_state=_build_intake(
            conversation_id="conv-wrs",
            turn_id="turn-wrs-2",
            raw_text="What about weather in Boston?",
        ),
        question_interpretation_state=_build_interpretation(
            extracted_terms=("weather", "boston"),
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
    unresolved_selection = region_engine.build_snapshot(
        entity_request_inference_state=unresolved_inference.to_dict(),
        target_domain_registry_state=_build_target_domains(),
        world_model_state=_build_world_model(),
    )
    if unresolved_selection.candidate_count > MAX_REGION_CANDIDATES:
        raise RuntimeError("unresolved region selection exceeded the Phase 8 candidate ceiling")
    if not unresolved_selection.unresolved:
        raise RuntimeError("unresolved region selection should have stayed unresolved")
    if unresolved_selection.selected_region_id is not None:
        raise RuntimeError("unresolved region selection should not have selected a region")
    if "unresolved_preserved" not in unresolved_selection.reason_codes:
        raise RuntimeError("unresolved region selection did not preserve unresolved state")
    if "no_safe_region_above_threshold" not in unresolved_selection.reason_codes:
        raise RuntimeError("unresolved region selection did not record the safety threshold miss")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(vc.RUNTIME_FILES) + list(OWNED_FILES),
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "safe-region-selection-resolves", "result": "pass"},
            {"id": "candidate-ceiling-enforced", "result": "pass"},
            {"id": "unresolved-path-preserved", "result": "pass"},
            {"id": "no-safe-region-bluff", "result": "pass"},
        ],
        anchors={
            "safe_inference": safe_inference.to_dict(),
            "safe_selection": safe_selection.to_dict(),
            "unresolved_inference": unresolved_inference.to_dict(),
            "unresolved_selection": unresolved_selection.to_dict(),
        },
        notes=["region selection stays bounded and keeps unresolved cases unresolved"],
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
                "safe-region-selection-resolves",
                "candidate-ceiling-enforced",
                "unresolved-path-preserved",
                "no-safe-region-bluff",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 8 world-region selection runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_08 world_region_selection verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_08 world_region_selection verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
