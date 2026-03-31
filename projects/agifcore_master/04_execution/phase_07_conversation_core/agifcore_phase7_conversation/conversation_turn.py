from __future__ import annotations

from .answer_contract import AnswerContractBuilder
from .anti_generic_filler import AntiGenericFillerEngine
from .clarification import ClarificationEngine
from .contracts import (
    ConversationTurnSnapshot,
    Phase7ConversationError,
    ResponseSurface,
    require_schema,
    stable_hash_payload,
)
from .question_interpretation import QuestionInterpretationEngine
from .raw_text_intake import RawTextIntakeEngine
from .self_knowledge_surface import SelfKnowledgeSurfaceEngine
from .support_state_logic import SupportStateEngine
from .surface_realizer import SurfaceRealizer
from .utterance_planner import UtterancePlannerEngine


class ConversationTurnError(Phase7ConversationError):
    """Raised when the composed Phase 7 turn is inconsistent."""


class ConversationTurnEngine:
    """Run the full bounded Phase 7 conversation turn pipeline."""

    def __init__(self) -> None:
        self.intake = RawTextIntakeEngine()
        self.interpretation = QuestionInterpretationEngine()
        self.support_state = SupportStateEngine()
        self.self_knowledge = SelfKnowledgeSurfaceEngine()
        self.clarification = ClarificationEngine()
        self.planner = UtterancePlannerEngine()
        self.realizer = SurfaceRealizer()
        self.guardrails = AntiGenericFillerEngine()
        self.answer_contract = AnswerContractBuilder()

    def run_turn(
        self,
        *,
        conversation_id: str,
        turn_id: str,
        raw_text: str,
        continuity_memory_state: dict[str, object],
        working_memory_state: dict[str, object],
        memory_review_state: dict[str, object],
        support_selection_result: dict[str, object],
        world_model_state: dict[str, object],
        what_if_simulation_state: dict[str, object],
        conflict_lane_state: dict[str, object],
        usefulness_state: dict[str, object],
        active_context_refs: list[str] | None = None,
    ) -> ConversationTurnSnapshot:
        require_schema(continuity_memory_state, "agifcore.phase_04.continuity_memory.v1", "continuity_memory_state")
        require_schema(working_memory_state, "agifcore.phase_04.working_memory.v1", "working_memory_state")
        require_schema(memory_review_state, "agifcore.phase_04.memory_review.v1", "memory_review_state")
        require_schema(world_model_state, "agifcore.phase_06.world_model.v1", "world_model_state")
        require_schema(what_if_simulation_state, "agifcore.phase_06.what_if_simulation.v1", "what_if_simulation_state")
        require_schema(conflict_lane_state, "agifcore.phase_06.conflict_lanes.v1", "conflict_lane_state")
        require_schema(usefulness_state, "agifcore.phase_06.usefulness_scoring.v1", "usefulness_state")

        intake = self.intake.build_record(
            conversation_id=conversation_id,
            turn_id=turn_id,
            raw_text=raw_text,
            active_context_refs=active_context_refs or [],
        )
        interpretation = self.interpretation.build_snapshot(intake_record=intake)
        support_resolution = self.support_state.build_resolution(
            question_interpretation_state=interpretation.to_dict(),
            continuity_memory_state=continuity_memory_state,
            memory_review_state=memory_review_state,
            support_selection_result=support_selection_result,
            world_model_state=world_model_state,
            what_if_simulation_state=what_if_simulation_state,
            conflict_lane_state=conflict_lane_state,
            usefulness_state=usefulness_state,
        )
        self_knowledge = self.self_knowledge.build_snapshot(
            question_interpretation_state=interpretation.to_dict(),
            support_state_resolution_state=support_resolution.to_dict(),
            continuity_memory_state=continuity_memory_state,
        )
        clarification = self.clarification.build_request(
            question_interpretation_state=interpretation.to_dict(),
            support_state_resolution_state=support_resolution.to_dict(),
        )
        plan = self.planner.build_plan(
            question_interpretation_state=interpretation.to_dict(),
            support_state_resolution_state=support_resolution.to_dict(),
            self_knowledge_state=self_knowledge.to_dict(),
            clarification_state=clarification.to_dict(),
        )
        draft = self.realizer.build_draft(
            question_interpretation_state=interpretation.to_dict(),
            support_state_resolution_state=support_resolution.to_dict(),
            self_knowledge_state=self_knowledge.to_dict(),
            clarification_state=clarification.to_dict(),
            utterance_plan_state=plan.to_dict(),
        )
        guardrail_result = self.guardrails.enforce(
            question_interpretation_state=interpretation.to_dict(),
            support_state_resolution_state=support_resolution.to_dict(),
            self_knowledge_state=self_knowledge.to_dict(),
            clarification_state=clarification.to_dict(),
            realization_draft=draft,
        )
        response_surface = ResponseSurface(
            response_id=f"response::{stable_hash_payload({'draft_id': draft.draft_id, 'guardrail_hash': guardrail_result.guardrail_hash})[:12]}",
            response_text=guardrail_result.output_text,
            final_answer_mode=draft.final_answer_mode,
            cited_evidence_refs=draft.cited_evidence_refs,
            response_hash=stable_hash_payload(
                {
                    "response_text": guardrail_result.output_text,
                    "final_answer_mode": draft.final_answer_mode.value,
                    "cited_evidence_refs": list(draft.cited_evidence_refs),
                }
            ),
        )
        answer_contract = self.answer_contract.build(
            intake_state=intake.to_dict(),
            question_interpretation_state=interpretation.to_dict(),
            support_state_resolution_state=support_resolution.to_dict(),
            utterance_plan_state=plan.to_dict(),
            response_surface=response_surface,
        )
        snapshot_payload = {
            "intake_hash": intake.intake_hash,
            "interpretation_hash": interpretation.interpretation_hash,
            "resolution_hash": support_resolution.resolution_hash,
            "plan_hash": plan.plan_hash,
            "response_hash": response_surface.response_hash,
            "guardrail_hash": guardrail_result.guardrail_hash,
            "contract_hash": answer_contract.contract_hash,
        }
        return ConversationTurnSnapshot(
            schema="agifcore.phase_07.conversation_turn.v1",
            phase4_interfaces=(
                "agifcore.phase_04.working_memory.v1",
                "agifcore.phase_04.continuity_memory.v1",
                "agifcore.phase_04.memory_review.v1",
            ),
            phase5_interfaces=("phase5.support_selection_result",),
            phase6_interfaces=(
                str(world_model_state.get("schema")),
                str(what_if_simulation_state.get("schema")),
                str(conflict_lane_state.get("schema")),
                str(usefulness_state.get("schema")),
            ),
            intake=intake,
            interpretation=interpretation,
            support_resolution=support_resolution,
            self_knowledge=self_knowledge,
            clarification=clarification,
            utterance_plan=plan,
            response_surface=response_surface,
            guardrail_result=guardrail_result,
            answer_contract=answer_contract,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
