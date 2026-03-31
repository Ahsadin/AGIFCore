from __future__ import annotations

from typing import Any, Mapping

from .bounded_current_world_reasoning import BoundedCurrentWorldReasoningEngine
from .causal_chain_reasoning import CausalChainReasoningEngine
from .contracts import (
    Phase8ScienceWorldAwarenessError,
    ScienceWorldTurnSnapshot,
    require_phase7_intake_state,
    require_schema,
    require_support_selection_result,
    stable_hash_payload,
)
from .entity_request_inference import EntityRequestInferenceEngine
from .science_reflection import ScienceReflectionEngine
from .scientific_priors import ScientificPriorsEngine
from .visible_reasoning_summaries import VisibleReasoningSummaryEngine
from .world_region_selection import WorldRegionSelectionEngine


class ScienceWorldTurnError(Phase8ScienceWorldAwarenessError):
    """Raised when the composed Phase 8 turn is inconsistent."""


class ScienceWorldTurnEngine:
    """Thin coordinator for the Phase 8 science/world awareness runtime."""

    SCHEMA = "agifcore.phase_08.science_world_turn.v1"

    def __init__(self) -> None:
        self.entity_request_inference = EntityRequestInferenceEngine()
        self.scientific_priors = ScientificPriorsEngine()
        self.world_region_selection = WorldRegionSelectionEngine()
        self.causal_chain_reasoning = CausalChainReasoningEngine()
        self.bounded_current_world_reasoning = BoundedCurrentWorldReasoningEngine()
        self.visible_reasoning_summaries = VisibleReasoningSummaryEngine()
        self.science_reflection = ScienceReflectionEngine()

    def run_turn(
        self,
        *,
        intake_state: Mapping[str, Any],
        question_interpretation_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        target_domain_registry_state: Mapping[str, Any],
        world_model_state: Mapping[str, Any],
        what_if_simulation_state: Mapping[str, Any],
        usefulness_scoring_state: Mapping[str, Any],
        continuity_memory_state: Mapping[str, Any] | None = None,
        working_memory_state: Mapping[str, Any] | None = None,
        memory_review_state: Mapping[str, Any] | None = None,
        support_selection_result: Mapping[str, Any] | None = None,
        answer_contract_state: Mapping[str, Any] | None = None,
    ) -> ScienceWorldTurnSnapshot:
        intake = require_phase7_intake_state(intake_state, "intake_state")
        interpretation = require_schema(
            question_interpretation_state,
            "agifcore.phase_07.question_interpretation.v1",
            "question_interpretation_state",
        )
        support = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )
        target_domains = require_schema(
            target_domain_registry_state,
            "agifcore.phase_06.target_domains.v1",
            "target_domain_registry_state",
        )
        world_model = require_schema(
            world_model_state,
            "agifcore.phase_06.world_model.v1",
            "world_model_state",
        )
        what_if_simulation = require_schema(
            what_if_simulation_state,
            "agifcore.phase_06.what_if_simulation.v1",
            "what_if_simulation_state",
        )
        usefulness_scoring = require_schema(
            usefulness_scoring_state,
            "agifcore.phase_06.usefulness_scoring.v1",
            "usefulness_scoring_state",
        )
        if continuity_memory_state is not None:
            require_schema(continuity_memory_state, "agifcore.phase_04.continuity_memory.v1", "continuity_memory_state")
        if working_memory_state is not None:
            require_schema(working_memory_state, "agifcore.phase_04.working_memory.v1", "working_memory_state")
        if memory_review_state is not None:
            require_schema(memory_review_state, "agifcore.phase_04.memory_review.v1", "memory_review_state")
        if support_selection_result is not None:
            require_support_selection_result(support_selection_result, "support_selection_result")
        if answer_contract_state is not None:
            require_schema(answer_contract_state, "agifcore.phase_07.answer_contract.v1", "answer_contract_state")

        entity_request_inference = self.entity_request_inference.build_snapshot(
            intake_state=intake,
            question_interpretation_state=interpretation,
            support_state_resolution_state=support,
        )
        scientific_priors = self.scientific_priors.build_snapshot(
            entity_request_inference_state=entity_request_inference.to_dict(),
        )
        world_region_selection = self.world_region_selection.build_snapshot(
            entity_request_inference_state=entity_request_inference.to_dict(),
            target_domain_registry_state=target_domains,
            world_model_state=world_model,
        )
        causal_chain = self.causal_chain_reasoning.build_snapshot(
            entity_request_inference_state=entity_request_inference.to_dict(),
            scientific_priors_state=scientific_priors.to_dict(),
            world_region_selection_state=world_region_selection.to_dict(),
            world_model_state=world_model,
            what_if_simulation_state=what_if_simulation,
            usefulness_scoring_state=usefulness_scoring,
        )
        bounded_current_world_reasoning = self.bounded_current_world_reasoning.build_snapshot(
            entity_request_inference_state=entity_request_inference.to_dict(),
            causal_chain_state=causal_chain.to_dict(),
            support_state_resolution_state=support,
        )
        visible_reasoning_summary = self.visible_reasoning_summaries.build_summary(
            causal_chain_state=causal_chain.to_dict(),
            bounded_current_world_reasoning_state=bounded_current_world_reasoning.to_dict(),
        )
        science_reflection = self.science_reflection.build_snapshot(
            scientific_priors_state=scientific_priors.to_dict(),
            causal_chain_state=causal_chain.to_dict(),
            bounded_current_world_reasoning_state=bounded_current_world_reasoning.to_dict(),
        )

        phase4_interfaces: list[str] = []
        if working_memory_state is not None:
            phase4_interfaces.append(str(working_memory_state.get("schema")))
        if continuity_memory_state is not None:
            phase4_interfaces.append(str(continuity_memory_state.get("schema")))
        if memory_review_state is not None:
            phase4_interfaces.append(str(memory_review_state.get("schema")))

        phase5_interfaces: list[str] = []
        if support_selection_result is not None:
            phase5_interfaces.append("phase5.support_selection_result")

        phase6_interfaces = [
            str(target_domains.get("schema")),
            str(world_model.get("schema")),
            str(what_if_simulation.get("schema")),
            str(usefulness_scoring.get("schema")),
        ]

        phase7_interfaces = [
            "agifcore.phase_07.raw_text_intake.v1",
            str(interpretation.get("schema")),
            str(support.get("schema")),
        ]
        if answer_contract_state is not None:
            phase7_interfaces.append(str(answer_contract_state.get("schema")))

        conversation_id = str(intake.get("conversation_id"))
        turn_id = str(intake.get("turn_id"))
        if entity_request_inference.conversation_id != conversation_id:
            raise ScienceWorldTurnError("entity_request_inference conversation_id does not match intake_state")
        if entity_request_inference.turn_id != turn_id:
            raise ScienceWorldTurnError("entity_request_inference turn_id does not match intake_state")

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "phase4_interfaces": phase4_interfaces,
            "phase5_interfaces": phase5_interfaces,
            "phase6_interfaces": phase6_interfaces,
            "phase7_interfaces": phase7_interfaces,
            "entity_request_inference_hash": entity_request_inference.inference_hash,
            "scientific_priors_hash": scientific_priors.snapshot_hash,
            "world_region_selection_hash": world_region_selection.snapshot_hash,
            "causal_chain_hash": causal_chain.snapshot_hash,
            "bounded_current_world_reasoning_hash": bounded_current_world_reasoning.snapshot_hash,
            "visible_reasoning_summary_hash": visible_reasoning_summary.summary_hash,
            "science_reflection_hash": science_reflection.reflection_hash,
        }
        return ScienceWorldTurnSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            phase4_interfaces=tuple(phase4_interfaces),
            phase5_interfaces=tuple(phase5_interfaces),
            phase6_interfaces=tuple(phase6_interfaces),
            phase7_interfaces=tuple(phase7_interfaces),
            entity_request_inference=entity_request_inference,
            scientific_priors=scientific_priors,
            world_region_selection=world_region_selection,
            causal_chain=causal_chain,
            bounded_current_world_reasoning=bounded_current_world_reasoning,
            visible_reasoning_summary=visible_reasoning_summary,
            science_reflection=science_reflection,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
