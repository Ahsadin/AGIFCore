from __future__ import annotations

import json
from typing import Any

import _phase_08_verifier_common as vc

VERIFIER = "verify_phase_08_bounded_current_world_reasoning"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_08_bounded_current_world_reasoning_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase8_science_world_awareness.contracts",
    "agifcore_phase8_science_world_awareness.scientific_priors",
    "agifcore_phase8_science_world_awareness.entity_request_inference",
    "agifcore_phase8_science_world_awareness.world_region_selection",
    "agifcore_phase8_science_world_awareness.causal_chain_reasoning",
    "agifcore_phase8_science_world_awareness.bounded_current_world_reasoning",
    "agifcore_phase8_science_world_awareness.visible_reasoning_summaries",
    "agifcore_phase8_science_world_awareness.science_reflection",
    "agifcore_phase8_science_world_awareness.science_world_turn",
)
OWNED_FILES = (
    "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/_phase_08_verifier_common.py",
    "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_bounded_current_world_reasoning.py",
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


def _build_target_domains() -> dict[str, Any]:
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


def _build_world_model() -> dict[str, Any]:
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
                "world_confidence": 0.72,
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


def _build_simulation_state(*, source_entity_id: str, confidence: float) -> dict[str, Any]:
    return {
        "schema": "agifcore.phase_06.what_if_simulation.v1",
        "snapshot_hash": "sim::snapshot::phase8",
        "entries": [
            {
                "simulation_entry_id": "sim::phase8::weather_climate::01",
                "future_id": "sim::future::01",
                "source_entity_id": source_entity_id,
                "target_domain": "weather_climate",
                "outcome": "stable_local_pattern",
                "confidence": confidence,
                "fail_closed": False,
                "reason_codes": ["bounded_local_support"],
            },
            {
                "simulation_entry_id": "sim::phase8::weather_climate::02",
                "future_id": "sim::future::02",
                "source_entity_id": "world::entity::coast",
                "target_domain": "place_region_context",
                "outcome": "context_shifted",
                "confidence": 0.35,
                "fail_closed": True,
                "reason_codes": ["counterfactual_context"],
            },
        ],
    }


def _build_usefulness_state(*, weighted_score: float) -> dict[str, Any]:
    return {
        "schema": "agifcore.phase_06.usefulness_scoring.v1",
        "snapshot_hash": "usefulness::snapshot::phase8",
        "overall_outcome": "qualified",
        "domain_scores": [
            {
                "domain_id": "weather_climate",
                "weighted_score": weighted_score,
                "outcome": "qualified",
            },
            {
                "domain_id": "place_region_context",
                "weighted_score": 0.42,
                "outcome": "insufficient",
            },
        ],
    }


def _build_pipeline(
    *,
    conversation_id: str,
    turn_id: str,
    raw_text: str,
    extracted_terms: tuple[str, ...],
    live_current_requested: bool,
    support_state: str,
    knowledge_gap_reason: str,
    next_action: str,
    simulation_confidence: float,
    usefulness_score: float,
) -> tuple[Any, Any, Any, Any]:
    from agifcore_phase8_science_world_awareness.bounded_current_world_reasoning import (
        BoundedCurrentWorldReasoningEngine,
    )
    from agifcore_phase8_science_world_awareness.causal_chain_reasoning import CausalChainReasoningEngine
    from agifcore_phase8_science_world_awareness.entity_request_inference import EntityRequestInferenceEngine
    from agifcore_phase8_science_world_awareness.scientific_priors import ScientificPriorsEngine
    from agifcore_phase8_science_world_awareness.world_region_selection import WorldRegionSelectionEngine

    inference_engine = EntityRequestInferenceEngine()
    priors_engine = ScientificPriorsEngine()
    region_engine = WorldRegionSelectionEngine()
    chain_engine = CausalChainReasoningEngine()
    current_engine = BoundedCurrentWorldReasoningEngine()

    support = _build_support_state(
        support_state=support_state,
        knowledge_gap_reason=knowledge_gap_reason,
        next_action=next_action,
    )
    inference = inference_engine.build_snapshot(
        intake_state=_build_intake(conversation_id=conversation_id, turn_id=turn_id, raw_text=raw_text),
        question_interpretation_state=_build_interpretation(
            extracted_terms=extracted_terms,
            live_current_requested=live_current_requested,
            ambiguous_request=False,
            self_knowledge_requested=False,
            target_domain_hint="weather_climate",
        ),
        support_state_resolution_state=support,
    )
    priors = priors_engine.build_snapshot(entity_request_inference_state=inference.to_dict())
    region = region_engine.build_snapshot(
        entity_request_inference_state=inference.to_dict(),
        target_domain_registry_state=_build_target_domains(),
        world_model_state=_build_world_model(),
    )
    chain = chain_engine.build_snapshot(
        entity_request_inference_state=inference.to_dict(),
        scientific_priors_state=priors.to_dict(),
        world_region_selection_state=region.to_dict(),
        world_model_state=_build_world_model(),
        what_if_simulation_state=_build_simulation_state(
            source_entity_id="world::entity::boston",
            confidence=simulation_confidence,
        ),
        usefulness_scoring_state=_build_usefulness_state(weighted_score=usefulness_score),
    )
    current = current_engine.build_snapshot(
        entity_request_inference_state=inference.to_dict(),
        causal_chain_state=chain.to_dict(),
        support_state_resolution_state=support,
    )
    return inference, priors, region, chain, current


def build_pass_report() -> dict[str, object]:
    bounded_inference, bounded_priors, bounded_region, bounded_chain, bounded_current = _build_pipeline(
        conversation_id="conv-cwr",
        turn_id="turn-cwr-1",
        raw_text="What is the latest weather in Boston today?",
        extracted_terms=("weather", "boston", "today"),
        live_current_requested=True,
        support_state="grounded",
        knowledge_gap_reason="none",
        next_action="answer",
        simulation_confidence=0.84,
        usefulness_score=0.83,
    )
    if bounded_current.decision.value != "bounded_local_support":
        raise RuntimeError("bounded current-world case did not resolve to bounded local support")
    if not bounded_current.live_current_requested:
        raise RuntimeError("bounded current-world case did not preserve the live-current cue")
    if bounded_current.needs_fresh_information or bounded_current.live_measurement_required:
        raise RuntimeError("bounded current-world case should not require fresh measurement")
    if bounded_current.exact_current_fact_allowed:
        raise RuntimeError("bounded current-world case should not allow an exact current fact claim")
    if "bounded_local_support_available" not in bounded_current.reason_codes:
        raise RuntimeError("bounded current-world case did not record bounded local support")

    freshness_inference, freshness_priors, freshness_region, freshness_chain, freshness_current = _build_pipeline(
        conversation_id="conv-cwr",
        turn_id="turn-cwr-2",
        raw_text="Tell me about Boston weather.",
        extracted_terms=("boston", "weather"),
        live_current_requested=False,
        support_state="search_needed",
        knowledge_gap_reason="needs_fresh_information",
        next_action="search_external",
        simulation_confidence=0.72,
        usefulness_score=0.79,
    )
    if freshness_current.decision.value != "needs_fresh_information":
        raise RuntimeError("freshness case did not resolve to needs_fresh_information")
    if not freshness_current.live_current_requested:
        raise RuntimeError("freshness case did not promote the support-state cue to live-current")
    if freshness_current.live_measurement_required:
        raise RuntimeError("freshness case should not require a live measurement")
    if "fresh_information_required_by_phase7_honesty" not in freshness_current.reason_codes:
        raise RuntimeError("freshness case did not preserve the freshness honesty reason code")
    if freshness_chain.fail_closed is False:
        raise RuntimeError("freshness case should have a fail-closed causal chain")

    exact_measurement_inference, exact_measurement_priors, exact_measurement_region, exact_measurement_chain, exact_measurement_current = _build_pipeline(
        conversation_id="conv-cwr",
        turn_id="turn-cwr-3",
        raw_text="What is the latest weather in Boston today?",
        extracted_terms=("weather", "boston", "today"),
        live_current_requested=True,
        support_state="search_needed",
        knowledge_gap_reason="needs_fresh_information",
        next_action="search_external",
        simulation_confidence=0.72,
        usefulness_score=0.79,
    )
    if exact_measurement_current.decision.value != "live_measurement_required":
        raise RuntimeError("exact-current case did not resolve to live_measurement_required")
    if not exact_measurement_current.live_measurement_required:
        raise RuntimeError("exact-current case did not require a live measurement")
    if "exact_current_fact_requires_live_measurement" not in exact_measurement_current.reason_codes:
        raise RuntimeError("exact-current case did not record the live-measurement reason code")
    if exact_measurement_current.exact_current_fact_allowed:
        raise RuntimeError("exact-current case should not allow an exact current fact claim")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(vc.RUNTIME_FILES) + list(OWNED_FILES),
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "bounded-local-support-kept-bounded", "result": "pass"},
            {"id": "freshness-gap-stays-fail-closed", "result": "pass"},
            {"id": "live-measurement-is-required-when-facts-are-exact", "result": "pass"},
            {"id": "current-world-evidence-remains-bounded", "result": "pass"},
        ],
        anchors={
            "bounded_inference": bounded_inference.to_dict(),
            "bounded_priors": bounded_priors.to_dict(),
            "bounded_region": bounded_region.to_dict(),
            "bounded_chain": bounded_chain.to_dict(),
            "bounded_current": bounded_current.to_dict(),
            "freshness_inference": freshness_inference.to_dict(),
            "freshness_priors": freshness_priors.to_dict(),
            "freshness_region": freshness_region.to_dict(),
            "freshness_chain": freshness_chain.to_dict(),
            "freshness_current": freshness_current.to_dict(),
            "exact_measurement_inference": exact_measurement_inference.to_dict(),
            "exact_measurement_priors": exact_measurement_priors.to_dict(),
            "exact_measurement_region": exact_measurement_region.to_dict(),
            "exact_measurement_chain": exact_measurement_chain.to_dict(),
            "exact_measurement_current": exact_measurement_current.to_dict(),
        },
        notes=["bounded current-world reasoning keeps exact claims local, fresh, and fail-closed"],
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
                "bounded-local-support-kept-bounded",
                "freshness-gap-stays-fail-closed",
                "live-measurement-is-required-when-facts-are-exact",
                "current-world-evidence-remains-bounded",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 8 bounded-current-world runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_08 bounded_current_world_reasoning verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_08 bounded_current_world_reasoning verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
