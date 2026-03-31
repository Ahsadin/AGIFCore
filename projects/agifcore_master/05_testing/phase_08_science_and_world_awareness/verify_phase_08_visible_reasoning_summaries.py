from __future__ import annotations

import json
from typing import Any

import _phase_08_verifier_common as vc

VERIFIER = "verify_phase_08_visible_reasoning_summaries"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_08_visible_reasoning_summaries_report.json"
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
    "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_visible_reasoning_summaries.py",
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


def _build_simulation_state(*, source_entity_id: str, target_domain: str, outcome: str, confidence: float) -> dict[str, Any]:
    return {
        "schema": "agifcore.phase_06.what_if_simulation.v1",
        "snapshot_hash": f"sim::snapshot::{target_domain}",
        "entries": [
            {
                "simulation_entry_id": f"sim::phase8::{target_domain}::01",
                "future_id": "sim::future::01",
                "source_entity_id": source_entity_id,
                "target_domain": target_domain,
                "outcome": outcome,
                "confidence": confidence,
                "fail_closed": False,
                "reason_codes": ["bounded_local_support"],
            },
            {
                "simulation_entry_id": f"sim::phase8::{target_domain}::02",
                "future_id": "sim::future::02",
                "source_entity_id": "world::entity::coast",
                "target_domain": "place_region_context" if target_domain == "weather_climate" else "weather_climate",
                "outcome": "context_shifted",
                "confidence": 0.35,
                "fail_closed": True,
                "reason_codes": ["counterfactual_context"],
            },
        ],
    }


def _build_usefulness_state(*, target_domain: str, weighted_score: float) -> dict[str, Any]:
    other_domain = "place_region_context" if target_domain == "weather_climate" else "weather_climate"
    return {
        "schema": "agifcore.phase_06.usefulness_scoring.v1",
        "snapshot_hash": f"usefulness::snapshot::{target_domain}",
        "overall_outcome": "qualified",
        "domain_scores": [
            {
                "domain_id": target_domain,
                "weighted_score": weighted_score,
                "outcome": "qualified",
            },
            {
                "domain_id": other_domain,
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
    target_domain_hint: str,
    source_entity_id: str,
    simulation_outcome: str,
    simulation_confidence: float,
    usefulness_score: float,
) -> tuple[Any, Any, Any, Any, Any, Any]:
    from agifcore_phase8_science_world_awareness.bounded_current_world_reasoning import (
        BoundedCurrentWorldReasoningEngine,
    )
    from agifcore_phase8_science_world_awareness.causal_chain_reasoning import CausalChainReasoningEngine
    from agifcore_phase8_science_world_awareness.entity_request_inference import EntityRequestInferenceEngine
    from agifcore_phase8_science_world_awareness.scientific_priors import ScientificPriorsEngine
    from agifcore_phase8_science_world_awareness.visible_reasoning_summaries import (
        VisibleReasoningSummaryEngine,
    )
    from agifcore_phase8_science_world_awareness.world_region_selection import WorldRegionSelectionEngine

    inference_engine = EntityRequestInferenceEngine()
    priors_engine = ScientificPriorsEngine()
    region_engine = WorldRegionSelectionEngine()
    chain_engine = CausalChainReasoningEngine()
    current_engine = BoundedCurrentWorldReasoningEngine()
    summary_engine = VisibleReasoningSummaryEngine()

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
            target_domain_hint=target_domain_hint,
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
            source_entity_id=source_entity_id,
            target_domain=target_domain_hint,
            outcome=simulation_outcome,
            confidence=simulation_confidence,
        ),
        usefulness_scoring_state=_build_usefulness_state(
            target_domain=target_domain_hint,
            weighted_score=usefulness_score,
        ),
    )
    current = current_engine.build_snapshot(
        entity_request_inference_state=inference.to_dict(),
        causal_chain_state=chain.to_dict(),
        support_state_resolution_state=support,
    )
    summary = summary_engine.build_summary(
        causal_chain_state=chain.to_dict(),
        bounded_current_world_reasoning_state=current.to_dict(),
    )
    return inference, priors, region, chain, current, summary


def build_pass_report() -> dict[str, object]:
    from agifcore_phase8_science_world_awareness.contracts import MAX_CURRENT_WORLD_EVIDENCE_INPUTS, MAX_VISIBLE_REASONING_CHARACTERS

    strong_inference, strong_priors, strong_region, strong_chain, strong_current, strong_summary = _run_pipeline(
        conversation_id="conv-vrs",
        turn_id="turn-vrs-1",
        raw_text="Explain weather climate humidity wind cloud cover in Boston.",
        extracted_terms=("weather", "climate", "humidity", "wind", "cloud", "cover", "boston"),
        live_current_requested=False,
        support_state="grounded",
        knowledge_gap_reason="none",
        next_action="answer",
        target_domain_hint="weather_climate",
        source_entity_id="world::entity::boston",
        simulation_outcome="stable_local_pattern",
        simulation_confidence=0.84,
        usefulness_score=0.83,
    )
    if strong_summary.request_id != strong_current.request_id:
        raise RuntimeError("strong summary request_id did not match the bounded current-world request")
    if strong_summary.causal_chain_ref != strong_chain.chain_id:
        raise RuntimeError("strong summary did not preserve the causal-chain anchor")
    if strong_summary.character_count > MAX_VISIBLE_REASONING_CHARACTERS:
        raise RuntimeError("strong summary exceeded the visible reasoning character ceiling")
    if strong_summary.uncertainty_band.value != "low":
        raise RuntimeError("strong summary should have stayed in the low uncertainty band")
    if strong_summary.live_measurement_required:
        raise RuntimeError("strong summary should not require a live measurement")
    if not strong_summary.principle_refs:
        raise RuntimeError("strong summary did not preserve a principle anchor")
    if len(strong_summary.evidence_refs) > MAX_CURRENT_WORLD_EVIDENCE_INPUTS:
        raise RuntimeError("strong summary exceeded the evidence-ref ceiling")
    if not strong_summary.what_is_known[0].startswith("Current-world decision: not_current_world_request"):
        raise RuntimeError("strong summary did not surface the current-world decision")
    if strong_summary.what_would_verify[0] != "Re-run bounded reasoning after state changes and confirm stable evidence refs.":
        raise RuntimeError("strong summary did not keep the default verification step for bounded support")

    fresh_inference, fresh_priors, fresh_region, fresh_chain, fresh_current, fresh_summary = _run_pipeline(
        conversation_id="conv-vrs",
        turn_id="turn-vrs-2",
        raw_text="What is the latest weather in Boston today?",
        extracted_terms=("weather", "boston", "today"),
        live_current_requested=True,
        support_state="search_needed",
        knowledge_gap_reason="needs_fresh_information",
        next_action="search_external",
        target_domain_hint="weather_climate",
        source_entity_id="world::entity::boston",
        simulation_outcome="bounded_context_only",
        simulation_confidence=0.72,
        usefulness_score=0.79,
    )
    if fresh_summary.request_id != fresh_current.request_id:
        raise RuntimeError("fresh summary request_id did not match the bounded current-world request")
    if fresh_summary.causal_chain_ref != fresh_chain.chain_id:
        raise RuntimeError("fresh summary did not preserve the causal-chain anchor")
    if fresh_summary.character_count > MAX_VISIBLE_REASONING_CHARACTERS:
        raise RuntimeError("fresh summary exceeded the visible reasoning character ceiling")
    if fresh_summary.uncertainty_band.value != "high":
        raise RuntimeError("fresh summary should have been in the high uncertainty band")
    if not fresh_summary.live_measurement_required:
        raise RuntimeError("fresh summary should have required a live measurement")
    if not fresh_summary.what_would_verify[0].startswith("Collect a fresh live measurement"):
        raise RuntimeError("fresh summary did not surface the live-measurement verification step")
    if "Current-world decision: live_measurement_required." not in fresh_summary.what_is_known[0]:
        raise RuntimeError("fresh summary did not surface the live-measurement decision")
    if not any("Local evidence is insufficient" in item for item in fresh_summary.uncertainty):
        raise RuntimeError("fresh summary did not preserve the current-world uncertainty note")
    if len(fresh_summary.evidence_refs) > MAX_CURRENT_WORLD_EVIDENCE_INPUTS:
        raise RuntimeError("fresh summary exceeded the evidence-ref ceiling")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(vc.RUNTIME_FILES) + list(OWNED_FILES),
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "bounded-summary-stays-within-character-ceiling", "result": "pass"},
            {"id": "bounded-summary-keeps-request-and-chain-anchors", "result": "pass"},
            {"id": "bounded-summary-keeps-evidence-refs-bounded", "result": "pass"},
            {"id": "fresh-summary-prompts-live-measurement", "result": "pass"},
            {"id": "fresh-summary-raises-high-uncertainty", "result": "pass"},
        ],
        anchors={
            "strong_inference": strong_inference.to_dict(),
            "strong_priors": strong_priors.to_dict(),
            "strong_region": strong_region.to_dict(),
            "strong_chain": strong_chain.to_dict(),
            "strong_current": strong_current.to_dict(),
            "strong_summary": strong_summary.to_dict(),
            "fresh_inference": fresh_inference.to_dict(),
            "fresh_priors": fresh_priors.to_dict(),
            "fresh_region": fresh_region.to_dict(),
            "fresh_chain": fresh_chain.to_dict(),
            "fresh_current": fresh_current.to_dict(),
            "fresh_summary": fresh_summary.to_dict(),
        },
        notes=["visible reasoning summaries stay bounded and reflect live-measurement pressure when freshness is needed"],
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
                "bounded-summary-stays-within-character-ceiling",
                "bounded-summary-keeps-request-and-chain-anchors",
                "bounded-summary-keeps-evidence-refs-bounded",
                "fresh-summary-prompts-live-measurement",
                "fresh-summary-raises-high-uncertainty",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 8 visible reasoning summary runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_08 visible_reasoning_summaries verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_08 visible_reasoning_summaries verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
