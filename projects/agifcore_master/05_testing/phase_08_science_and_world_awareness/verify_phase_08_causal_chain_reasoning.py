from __future__ import annotations

import json
from typing import Any

import _phase_08_verifier_common as vc

VERIFIER = "verify_phase_08_causal_chain_reasoning"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_08_causal_chain_reasoning_report.json"
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
    "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_causal_chain_reasoning.py",
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


def _build_simulation_state(*, source_entity_id: str, outcome: str, confidence: float) -> dict[str, Any]:
    return {
        "schema": "agifcore.phase_06.what_if_simulation.v1",
        "snapshot_hash": "sim::snapshot::phase8",
        "entries": [
            {
                "simulation_entry_id": "sim::phase8::weather_climate::01",
                "future_id": "sim::future::01",
                "source_entity_id": source_entity_id,
                "target_domain": "weather_climate",
                "outcome": outcome,
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


def _build_usefulness_state(*, weighted_score: float, outcome: str = "qualified") -> dict[str, Any]:
    return {
        "schema": "agifcore.phase_06.usefulness_scoring.v1",
        "snapshot_hash": "usefulness::snapshot::phase8",
        "overall_outcome": "qualified",
        "domain_scores": [
            {
                "domain_id": "weather_climate",
                "weighted_score": weighted_score,
                "outcome": outcome,
            },
            {
                "domain_id": "place_region_context",
                "weighted_score": 0.42,
                "outcome": "insufficient",
            },
        ],
    }


def _run_pipeline(
    *,
    conversation_id: str,
    turn_id: str,
    raw_text: str,
    extracted_terms: tuple[str, ...],
    live_current_requested: bool,
    support_state: str,
    knowledge_gap_reason: str,
    next_action: str,
    simulation_outcome: str,
    simulation_confidence: float,
    usefulness_score: float,
) -> tuple[Any, Any, Any, Any]:
    from agifcore_phase8_science_world_awareness.causal_chain_reasoning import CausalChainReasoningEngine
    from agifcore_phase8_science_world_awareness.entity_request_inference import EntityRequestInferenceEngine
    from agifcore_phase8_science_world_awareness.scientific_priors import ScientificPriorsEngine
    from agifcore_phase8_science_world_awareness.world_region_selection import WorldRegionSelectionEngine

    inference_engine = EntityRequestInferenceEngine()
    priors_engine = ScientificPriorsEngine()
    region_engine = WorldRegionSelectionEngine()
    chain_engine = CausalChainReasoningEngine()

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
    simulation = _build_simulation_state(
        source_entity_id="world::entity::boston",
        outcome=simulation_outcome,
        confidence=simulation_confidence,
    )
    usefulness = _build_usefulness_state(weighted_score=usefulness_score)
    chain = chain_engine.build_snapshot(
        entity_request_inference_state=inference.to_dict(),
        scientific_priors_state=priors.to_dict(),
        world_region_selection_state=region.to_dict(),
        world_model_state=_build_world_model(),
        what_if_simulation_state=simulation,
        usefulness_scoring_state=usefulness,
    )
    return inference, priors, region, chain


def build_pass_report() -> dict[str, object]:
    strong_inference, strong_priors, strong_region, strong_chain = _run_pipeline(
        conversation_id="conv-ccr",
        turn_id="turn-ccr-1",
        raw_text="What is the latest weather in Boston today?",
        extracted_terms=("weather", "boston", "today"),
        live_current_requested=True,
        support_state="grounded",
        knowledge_gap_reason="none",
        next_action="answer",
        simulation_outcome="stable_local_pattern",
        simulation_confidence=0.84,
        usefulness_score=0.83,
    )
    if strong_inference.candidate_count == 0 or strong_inference.selected_candidate_id is None:
        raise RuntimeError("strong causal-chain request did not produce a selected inference candidate")
    if strong_priors.selected_prior_count == 0:
        raise RuntimeError("strong causal-chain request did not select a scientific prior")
    if strong_region.unresolved or strong_region.selected_region_id is None:
        raise RuntimeError("strong causal-chain request did not resolve a world region")
    if strong_chain.step_count != 7:
        raise RuntimeError("strong causal-chain request did not build the expected seven-step chain")
    if strong_chain.fail_closed:
        raise RuntimeError("strong causal-chain request should not have been fail-closed")
    if strong_chain.missing_variables:
        raise RuntimeError("strong causal-chain request should not have missing variables")
    if strong_chain.weakest_link_reason != "none_detected":
        raise RuntimeError("strong causal-chain request should have no weakest-link failure")

    weak_inference, weak_priors, weak_region, weak_chain = _run_pipeline(
        conversation_id="conv-ccr",
        turn_id="turn-ccr-2",
        raw_text="Tell me about Boston weather.",
        extracted_terms=("boston", "weather"),
        live_current_requested=False,
        support_state="search_needed",
        knowledge_gap_reason="needs_fresh_information",
        next_action="search_external",
        simulation_outcome="bounded_context_only",
        simulation_confidence=0.72,
        usefulness_score=0.79,
    )
    if weak_inference.candidate_count == 0 or weak_inference.selected_candidate_id is None:
        raise RuntimeError("weak causal-chain request did not produce a selected inference candidate")
    if weak_priors.selected_prior_count == 0:
        raise RuntimeError("weak causal-chain request did not select a scientific prior")
    if weak_region.selected_region_id is None:
        raise RuntimeError("weak causal-chain request did not produce a region candidate")
    if not weak_chain.fail_closed:
        raise RuntimeError("weak causal-chain request should have been fail-closed")
    if "fresh local measurement" not in weak_chain.missing_variables:
        raise RuntimeError("weak causal-chain request did not preserve the freshness gap")
    if weak_chain.weakest_link_reason != "needs_fresh_information":
        raise RuntimeError("weak causal-chain request did not preserve the freshness weakest-link reason")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(vc.RUNTIME_FILES) + list(OWNED_FILES),
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "strong-chain-builds-seven-steps", "result": "pass"},
            {"id": "strong-chain-stays-bounded", "result": "pass"},
            {"id": "strong-chain-preserves-region-and-prior-anchors", "result": "pass"},
            {"id": "weak-chain-fails-closed-on-freshness-gap", "result": "pass"},
            {"id": "weak-chain-preserves-missing-variable", "result": "pass"},
        ],
        anchors={
            "strong_inference": strong_inference.to_dict(),
            "strong_priors": strong_priors.to_dict(),
            "strong_region": strong_region.to_dict(),
            "strong_chain": strong_chain.to_dict(),
            "weak_inference": weak_inference.to_dict(),
            "weak_priors": weak_priors.to_dict(),
            "weak_region": weak_region.to_dict(),
            "weak_chain": weak_chain.to_dict(),
        },
        notes=["causal chain reasoning stays bounded and fail-closed when freshness evidence is weak"],
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
                "strong-chain-builds-seven-steps",
                "strong-chain-stays-bounded",
                "strong-chain-preserves-region-and-prior-anchors",
                "weak-chain-fails-closed-on-freshness-gap",
                "weak-chain-preserves-missing-variable",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 8 causal-chain runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_08 causal_chain_reasoning verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_08 causal_chain_reasoning verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
