from __future__ import annotations

import json
from typing import Any

import _phase_08_verifier_common as vc

VERIFIER = "verify_phase_08_science_reflection"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_08_science_reflection_report.json"
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
    "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_science_reflection.py",
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
) -> tuple[Any, Any, Any, Any, Any]:
    from agifcore_phase8_science_world_awareness.bounded_current_world_reasoning import (
        BoundedCurrentWorldReasoningEngine,
    )
    from agifcore_phase8_science_world_awareness.causal_chain_reasoning import CausalChainReasoningEngine
    from agifcore_phase8_science_world_awareness.entity_request_inference import EntityRequestInferenceEngine
    from agifcore_phase8_science_world_awareness.science_reflection import ScienceReflectionEngine
    from agifcore_phase8_science_world_awareness.scientific_priors import ScientificPriorsEngine
    from agifcore_phase8_science_world_awareness.world_region_selection import WorldRegionSelectionEngine

    inference_engine = EntityRequestInferenceEngine()
    priors_engine = ScientificPriorsEngine()
    region_engine = WorldRegionSelectionEngine()
    chain_engine = CausalChainReasoningEngine()
    current_engine = BoundedCurrentWorldReasoningEngine()
    reflection_engine = ScienceReflectionEngine()

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
    reflection = reflection_engine.build_snapshot(
        scientific_priors_state=priors.to_dict(),
        causal_chain_state=chain.to_dict(),
        bounded_current_world_reasoning_state=current.to_dict(),
    )
    return inference, priors, chain, current, reflection


def build_pass_report() -> dict[str, object]:
    from agifcore_phase8_science_world_awareness.contracts import MAX_REFLECTION_RECORDS

    strong_inference, strong_priors, strong_chain, strong_current, strong_reflection = _run_pipeline(
        conversation_id="conv-sr",
        turn_id="turn-sr-1",
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
    strong_kinds = {record.kind.value for record in strong_reflection.records}
    if strong_reflection.record_count != 1:
        raise RuntimeError("strong reflection should only record the next verification step")
    if strong_reflection.uncertainty_should_increase:
        raise RuntimeError("strong reflection should not increase uncertainty")
    if strong_kinds != {"next_verification_step"}:
        raise RuntimeError("strong reflection should only contain the next verification step record")
    if strong_reflection.records[0].kind.value != "next_verification_step":
        raise RuntimeError("strong reflection did not preserve the next verification step record")
    if strong_reflection.records[0].increases_uncertainty:
        raise RuntimeError("strong reflection next-step record should not increase uncertainty")

    weak_inference, weak_priors, weak_chain, weak_current, weak_reflection = _run_pipeline(
        conversation_id="conv-sr",
        turn_id="turn-sr-2",
        raw_text="What is the weather in Boston right now?",
        extracted_terms=("weather", "boston", "right", "now"),
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
    weak_kinds = [record.kind.value for record in weak_reflection.records]
    if weak_reflection.record_count > MAX_REFLECTION_RECORDS:
        raise RuntimeError("weak reflection exceeded the reflection-record ceiling")
    if not weak_reflection.uncertainty_should_increase:
        raise RuntimeError("weak reflection should increase uncertainty")
    if "weak_prior_choice" not in weak_kinds:
        raise RuntimeError("weak reflection did not record the weak prior choice")
    if "missing_variable" not in weak_kinds:
        raise RuntimeError("weak reflection did not record the missing variable")
    if "falsifier" not in weak_kinds:
        raise RuntimeError("weak reflection did not record the falsifier")
    if "next_verification_step" not in weak_kinds:
        raise RuntimeError("weak reflection did not record the next verification step")
    if "uncertainty_increase" not in weak_kinds:
        raise RuntimeError("weak reflection did not record the uncertainty increase")
    if weak_reflection.records[-1].kind.value != "uncertainty_increase":
        raise RuntimeError("weak reflection should end with the uncertainty increase record")
    if not any(record.increases_uncertainty for record in weak_reflection.records if record.kind.value != "next_verification_step"):
        raise RuntimeError("weak reflection did not mark uncertainty-bearing records correctly")
    if "fresh local measurement" not in weak_chain.missing_variables:
        raise RuntimeError("weak reflection did not preserve the freshness gap in the causal chain")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(vc.RUNTIME_FILES) + list(OWNED_FILES),
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "strong-reflection-stays-minimal", "result": "pass"},
            {"id": "strong-reflection-keeps-uncertainty-down", "result": "pass"},
            {"id": "weak-reflection-records-falsifier-and-missing-variable", "result": "pass"},
            {"id": "weak-reflection-records-next-step-and-uncertainty", "result": "pass"},
            {"id": "reflection-record-ceiling-is-respected", "result": "pass"},
        ],
        anchors={
            "strong_inference": strong_inference.to_dict(),
            "strong_priors": strong_priors.to_dict(),
            "strong_chain": strong_chain.to_dict(),
            "strong_current": strong_current.to_dict(),
            "strong_reflection": strong_reflection.to_dict(),
            "weak_inference": weak_inference.to_dict(),
            "weak_priors": weak_priors.to_dict(),
            "weak_chain": weak_chain.to_dict(),
            "weak_current": weak_current.to_dict(),
            "weak_reflection": weak_reflection.to_dict(),
        },
        notes=["science reflection records remain bounded and expose weak-prior plus freshness gaps"],
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
                "strong-reflection-stays-minimal",
                "strong-reflection-keeps-uncertainty-down",
                "weak-reflection-records-falsifier-and-missing-variable",
                "weak-reflection-records-next-step-and-uncertainty",
                "reflection-record-ceiling-is-respected",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 8 science reflection runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_08 science_reflection verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_08 science_reflection verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
