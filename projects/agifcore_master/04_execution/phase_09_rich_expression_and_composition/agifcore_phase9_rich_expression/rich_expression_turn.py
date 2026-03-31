from __future__ import annotations

from typing import Any, Mapping

from .analogy import AnalogyEngine
from .audience_aware_explanation_quality import AudienceAwareExplanationQualityEngine
from .comparison import ComparisonEngine
from .concept_composition import ConceptCompositionEngine
from .contracts import (
    ExpressionLane,
    MAX_PUBLIC_RESPONSE_CHARACTERS,
    Phase9OverlayContract,
    Phase9RichExpressionError,
    RichExpressionTurnSnapshot,
    coerce_bool,
    make_trace_ref,
    require_mapping,
    require_non_empty_str,
    require_phase7_intake_state,
    require_schema,
    stable_hash_payload,
)
from .cross_domain_composition import CrossDomainCompositionEngine
from .planning import PlanningEngine
from .synthesis import SynthesisEngine
from .teaching import TeachingEngine


class RichExpressionTurnError(Phase9RichExpressionError):
    """Raised when the composed Phase 9 rich-expression turn is inconsistent."""


def _clean_items(values: list[str], *, ceiling: int) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in values:
        cleaned = " ".join(str(raw).split()).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
        if len(result) >= ceiling:
            break
    return tuple(result)


def _selected_lane(utterance_plan: Mapping[str, Any], interpretation: Mapping[str, Any]) -> ExpressionLane:
    discourse_mode = str(utterance_plan.get("discourse_mode", "")).strip().lower()
    user_intent = str(interpretation.get("user_intent", "")).strip().lower()
    extracted_terms = [str(item).strip().lower() for item in list(interpretation.get("extracted_terms", ())) if str(item).strip()]
    intent_text = " ".join([user_intent, *extracted_terms])

    if "cross-domain" in intent_text or "cross domain" in intent_text or "across domains" in intent_text:
        return ExpressionLane.CROSS_DOMAIN_COMPOSITION
    if "composition" in intent_text or "compose" in intent_text:
        return ExpressionLane.CONCEPT_COMPOSITION
    if discourse_mode == "teach":
        return ExpressionLane.TEACHING
    if discourse_mode == "compare":
        return ExpressionLane.COMPARISON
    if discourse_mode == "plan":
        return ExpressionLane.PLANNING
    if discourse_mode == "analogy":
        return ExpressionLane.ANALOGY
    if discourse_mode == "synthesize":
        return ExpressionLane.SYNTHESIS
    return ExpressionLane.SYNTHESIS


def _clip_text(text: str, *, ceiling: int = MAX_PUBLIC_RESPONSE_CHARACTERS) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= ceiling:
        return cleaned
    return cleaned[: ceiling - 1].rstrip() + "…"


class RichExpressionTurnEngine:
    """Thin coordinator over read-only Phase 7 + Phase 8 snapshots."""

    SCHEMA = "agifcore.phase_09.rich_expression_turn.v1"

    def __init__(self) -> None:
        self.teaching = TeachingEngine()
        self.comparison = ComparisonEngine()
        self.planning = PlanningEngine()
        self.synthesis = SynthesisEngine()
        self.analogy = AnalogyEngine()
        self.concept_composition = ConceptCompositionEngine()
        self.cross_domain_composition = CrossDomainCompositionEngine()
        self.audience_quality = AudienceAwareExplanationQualityEngine()

    def run_turn(
        self,
        *,
        intake_state: Mapping[str, Any],
        question_interpretation_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        utterance_plan_state: Mapping[str, Any],
        answer_contract_state: Mapping[str, Any],
        science_world_turn_state: Mapping[str, Any],
        anti_generic_filler_state: Mapping[str, Any] | None = None,
    ) -> RichExpressionTurnSnapshot:
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
        utterance_plan = require_schema(
            utterance_plan_state,
            "agifcore.phase_07.utterance_plan.v1",
            "utterance_plan_state",
        )
        answer_contract = require_schema(
            answer_contract_state,
            "agifcore.phase_07.answer_contract.v1",
            "answer_contract_state",
        )
        science_world_turn = require_schema(
            science_world_turn_state,
            "agifcore.phase_08.science_world_turn.v1",
            "science_world_turn_state",
        )
        if anti_generic_filler_state is not None:
            require_schema(
                anti_generic_filler_state,
                "agifcore.phase_07.anti_generic_filler.v1",
                "anti_generic_filler_state",
            )

        conversation_id = require_non_empty_str(str(intake.get("conversation_id", "")).strip(), "conversation_id")
        turn_id = require_non_empty_str(str(intake.get("turn_id", "")).strip(), "turn_id")
        if str(interpretation.get("conversation_id", "")).strip() != conversation_id:
            raise RichExpressionTurnError("question_interpretation_state conversation_id must match intake_state")
        if str(interpretation.get("turn_id", "")).strip() != turn_id:
            raise RichExpressionTurnError("question_interpretation_state turn_id must match intake_state")
        if str(support.get("conversation_id", "")).strip() != conversation_id:
            raise RichExpressionTurnError("support_state_resolution_state conversation_id must match intake_state")
        if str(support.get("turn_id", "")).strip() != turn_id:
            raise RichExpressionTurnError("support_state_resolution_state turn_id must match intake_state")
        if str(answer_contract.get("conversation_id", "")).strip() != conversation_id:
            raise RichExpressionTurnError("answer_contract_state conversation_id must match intake_state")
        if str(answer_contract.get("turn_id", "")).strip() != turn_id:
            raise RichExpressionTurnError("answer_contract_state turn_id must match intake_state")
        if str(science_world_turn.get("conversation_id", "")).strip() != conversation_id:
            raise RichExpressionTurnError("science_world_turn_state conversation_id must match intake_state")
        if str(science_world_turn.get("turn_id", "")).strip() != turn_id:
            raise RichExpressionTurnError("science_world_turn_state turn_id must match intake_state")

        selected_lane = _selected_lane(utterance_plan, interpretation)

        entity_request_inference_state = require_mapping(
            science_world_turn.get("entity_request_inference"),
            "science_world_turn_state.entity_request_inference",
        )
        scientific_priors_state = require_mapping(
            science_world_turn.get("scientific_priors"),
            "science_world_turn_state.scientific_priors",
        )
        world_region_selection_state = require_mapping(
            science_world_turn.get("world_region_selection"),
            "science_world_turn_state.world_region_selection",
        )
        causal_chain_state = require_mapping(
            science_world_turn.get("causal_chain"),
            "science_world_turn_state.causal_chain",
        )
        bounded_current_world_reasoning_state = require_mapping(
            science_world_turn.get("bounded_current_world_reasoning"),
            "science_world_turn_state.bounded_current_world_reasoning",
        )
        visible_reasoning_summary_state = require_mapping(
            science_world_turn.get("visible_reasoning_summary"),
            "science_world_turn_state.visible_reasoning_summary",
        )
        science_reflection_state = require_mapping(
            science_world_turn.get("science_reflection"),
            "science_world_turn_state.science_reflection",
        )

        teaching_snapshot = None
        comparison_snapshot = None
        planning_snapshot = None
        synthesis_snapshot = None
        analogy_snapshot = None
        concept_composition_snapshot = None
        cross_domain_composition_snapshot = None

        if selected_lane is ExpressionLane.TEACHING:
            teaching_snapshot = self.teaching.build_snapshot(
                question_interpretation_state=interpretation,
                support_state_resolution_state=support,
                visible_reasoning_summary_state=visible_reasoning_summary_state,
            )
        elif selected_lane is ExpressionLane.COMPARISON:
            comparison_snapshot = self.comparison.build_snapshot(
                question_interpretation_state=interpretation,
                support_state_resolution_state=support,
                entity_request_inference_state=entity_request_inference_state,
                visible_reasoning_summary_state=visible_reasoning_summary_state,
            )
        elif selected_lane is ExpressionLane.PLANNING:
            planning_snapshot = self.planning.build_snapshot(
                support_state_resolution_state=support,
                bounded_current_world_reasoning_state=bounded_current_world_reasoning_state,
                visible_reasoning_summary_state=visible_reasoning_summary_state,
                science_reflection_state=science_reflection_state,
            )
        elif selected_lane is ExpressionLane.ANALOGY:
            analogy_snapshot = self.analogy.build_snapshot(
                entity_request_inference_state=entity_request_inference_state,
                visible_reasoning_summary_state=visible_reasoning_summary_state,
                support_state_resolution_state=support,
            )
        elif selected_lane is ExpressionLane.CONCEPT_COMPOSITION:
            concept_composition_snapshot = self.concept_composition.build_snapshot(
                entity_request_inference_state=entity_request_inference_state,
                scientific_priors_state=scientific_priors_state,
                visible_reasoning_summary_state=visible_reasoning_summary_state,
                support_state_resolution_state=support,
            )
        elif selected_lane is ExpressionLane.CROSS_DOMAIN_COMPOSITION:
            concept_composition_snapshot = self.concept_composition.build_snapshot(
                entity_request_inference_state=entity_request_inference_state,
                scientific_priors_state=scientific_priors_state,
                visible_reasoning_summary_state=visible_reasoning_summary_state,
                support_state_resolution_state=support,
            )
            cross_domain_composition_snapshot = self.cross_domain_composition.build_snapshot(
                question_interpretation_state=interpretation,
                support_state_resolution_state=support,
                entity_request_inference_state=entity_request_inference_state,
                world_region_selection_state=world_region_selection_state,
                concept_composition_state=concept_composition_snapshot.to_dict(),
            )
        else:
            synthesis_snapshot = self.synthesis.build_snapshot(
                question_interpretation_state=interpretation,
                support_state_resolution_state=support,
                visible_reasoning_summary_state=visible_reasoning_summary_state,
                science_reflection_state=science_reflection_state,
                bounded_current_world_reasoning_state=bounded_current_world_reasoning_state,
            )

        if selected_lane is ExpressionLane.SYNTHESIS and synthesis_snapshot is None:
            raise RichExpressionTurnError("selected synthesis lane did not produce synthesis snapshot")

        audience_quality_snapshot = self.audience_quality.build_snapshot(
            intake_state=intake,
            question_interpretation_state=interpretation,
            support_state_resolution_state=support,
            utterance_plan_state=utterance_plan,
            selected_lane=selected_lane,
            anti_generic_filler_state=anti_generic_filler_state,
        )

        known = [str(item).strip() for item in list(visible_reasoning_summary_state.get("what_is_known", ())) if str(item).strip()]
        inferred = [str(item).strip() for item in list(visible_reasoning_summary_state.get("what_is_inferred", ())) if str(item).strip()]
        uncertainty = [str(item).strip() for item in list(visible_reasoning_summary_state.get("uncertainty", ())) if str(item).strip()]
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"

        lane_text = ""
        response_sections: tuple[str, ...]
        if teaching_snapshot is not None:
            lane_text = " | ".join(f"{section.title}: {section.objective}" for section in teaching_snapshot.sections[:3])
            response_sections = ("scope", "teaching_steps", "verification")
        elif comparison_snapshot is not None:
            lane_text = " | ".join(
                f"{axis.axis_label} => {axis.left_value} vs {axis.right_value}"
                for axis in comparison_snapshot.axes[:3]
            )
            response_sections = ("comparison_axes", "asymmetry", "limits")
        elif planning_snapshot is not None:
            lane_text = " | ".join(f"{step.step_index}. {step.action}" for step in planning_snapshot.steps[:4])
            response_sections = ("step_plan", "dependencies", "stop_points")
        elif analogy_snapshot is not None:
            first = analogy_snapshot.mappings[0]
            lane_text = f"{first.source_point} -> {first.target_point}. Break limit: {first.break_limit}"
            response_sections = ("analogy_mapping", "break_limits", "verification")
        elif cross_domain_composition_snapshot is not None:
            lane_text = cross_domain_composition_snapshot.shared_pattern
            response_sections = ("domains", "shared_pattern", "boundaries")
        elif concept_composition_snapshot is not None:
            lane_text = concept_composition_snapshot.composed_view
            response_sections = ("inputs", "composed_view", "boundaries")
        elif synthesis_snapshot is not None:
            lane_text = synthesis_snapshot.merged_summary
            response_sections = ("known", "inferred", "uncertainty")
        else:
            raise RichExpressionTurnError("no lane snapshot was produced")

        honesty_prefix = ""
        if support_state in {"search_needed", "unknown"}:
            honesty_prefix = "Support is currently limited; this remains a bounded, non-upgraded expression. "
        public_response_text = _clip_text(
            honesty_prefix + lane_text + (" " + " ".join(uncertainty[:2]) if uncertainty else "")
        )
        uncertainty_statements = _clean_items(uncertainty or ["No explicit uncertainty statement was emitted."], ceiling=4)

        evidence_refs = _clean_items(
            [
                *[str(item).strip() for item in list(visible_reasoning_summary_state.get("evidence_refs", ())) if str(item).strip()],
                str(visible_reasoning_summary_state.get("summary_hash", "")).strip(),
                str(causal_chain_state.get("snapshot_hash", "")).strip(),
                str(bounded_current_world_reasoning_state.get("snapshot_hash", "")).strip(),
            ],
            ceiling=24,
        )

        analogy_trace_ref = analogy_snapshot.analogy_trace_ref if analogy_snapshot is not None else None
        concept_composition_ref = (
            concept_composition_snapshot.concept_composition_ref if concept_composition_snapshot is not None else None
        )

        revision_trace_ref = (
            make_trace_ref(
                "revision_trace",
                {"turn_id": turn_id, "selected_lane": selected_lane.value, "quality": audience_quality_snapshot.quality_hash},
            )
            if audience_quality_snapshot.rewrite_applied
            else None
        )
        consolidation_trace_ref = (
            make_trace_ref(
                "consolidation_trace",
                {"turn_id": turn_id, "selected_lane": selected_lane.value, "evidence_refs": list(evidence_refs[:4])},
            )
            if selected_lane in {ExpressionLane.SYNTHESIS, ExpressionLane.COMPARISON}
            else None
        )
        reorganization_trace_ref = (
            make_trace_ref(
                "reorganization_trace",
                {"turn_id": turn_id, "selected_lane": selected_lane.value, "response_sections": list(response_sections)},
            )
            if selected_lane in {ExpressionLane.TEACHING, ExpressionLane.PLANNING}
            else None
        )

        overlay_payload = {
            "schema": "agifcore.phase_09.overlay_contract.v1",
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "selected_lane": selected_lane.value,
            "support_state": support_state,
            "response_sections": list(response_sections),
            "public_response_text": public_response_text,
            "uncertainty_statements": list(uncertainty_statements),
            "analogy_trace_ref": analogy_trace_ref,
            "concept_composition_ref": concept_composition_ref,
            "revision_trace_ref": revision_trace_ref,
            "consolidation_trace_ref": consolidation_trace_ref,
            "reorganization_trace_ref": reorganization_trace_ref,
            "evidence_refs": list(evidence_refs),
        }
        overlay_contract = Phase9OverlayContract(
            schema="agifcore.phase_09.overlay_contract.v1",
            conversation_id=conversation_id,
            turn_id=turn_id,
            selected_lane=selected_lane,
            phase7_interfaces=(
                "agifcore.phase_07.raw_text_intake.v1",
                str(interpretation.get("schema")),
                str(support.get("schema")),
                str(utterance_plan.get("schema")),
                str(answer_contract.get("schema")),
            ),
            phase8_interfaces=(
                str(science_world_turn.get("schema")),
                str(entity_request_inference_state.get("schema")),
                str(scientific_priors_state.get("schema")),
                str(world_region_selection_state.get("schema")),
                str(causal_chain_state.get("schema")),
                str(bounded_current_world_reasoning_state.get("schema")),
                str(visible_reasoning_summary_state.get("schema")),
                str(science_reflection_state.get("schema")),
            ),
            support_state=support_state,
            support_honesty_preserved=support_state in {"grounded", "inferred", "search_needed", "unknown"},
            response_sections=response_sections,
            public_response_text=public_response_text,
            uncertainty_statements=uncertainty_statements,
            analogy_trace_ref=analogy_trace_ref,
            concept_composition_ref=concept_composition_ref,
            revision_trace_ref=revision_trace_ref,
            consolidation_trace_ref=consolidation_trace_ref,
            reorganization_trace_ref=reorganization_trace_ref,
            evidence_refs=evidence_refs,
            contract_hash=stable_hash_payload(overlay_payload),
        )

        active_lanes: list[ExpressionLane] = [selected_lane]
        if cross_domain_composition_snapshot is not None:
            active_lanes.append(ExpressionLane.CONCEPT_COMPOSITION)
        active_lanes = list(dict.fromkeys(active_lanes))

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "selected_lane": selected_lane.value,
            "active_lanes": [lane.value for lane in active_lanes],
            "intake_hash": str(intake.get("intake_hash", "")).strip(),
            "interpretation_hash": str(interpretation.get("interpretation_hash", "")).strip(),
            "support_resolution_hash": str(support.get("resolution_hash", "")).strip(),
            "utterance_plan_hash": str(utterance_plan.get("plan_hash", "")).strip(),
            "answer_contract_hash": str(answer_contract.get("contract_hash", "")).strip(),
            "science_world_turn_hash": str(science_world_turn.get("snapshot_hash", "")).strip(),
            "teaching_hash": teaching_snapshot.snapshot_hash if teaching_snapshot else None,
            "comparison_hash": comparison_snapshot.snapshot_hash if comparison_snapshot else None,
            "planning_hash": planning_snapshot.snapshot_hash if planning_snapshot else None,
            "synthesis_hash": synthesis_snapshot.snapshot_hash if synthesis_snapshot else None,
            "analogy_hash": analogy_snapshot.snapshot_hash if analogy_snapshot else None,
            "concept_composition_hash": concept_composition_snapshot.snapshot_hash if concept_composition_snapshot else None,
            "cross_domain_composition_hash": (
                cross_domain_composition_snapshot.snapshot_hash if cross_domain_composition_snapshot else None
            ),
            "audience_quality_hash": audience_quality_snapshot.quality_hash,
            "overlay_hash": overlay_contract.contract_hash,
        }
        return RichExpressionTurnSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            selected_lane=selected_lane,
            active_lanes=tuple(active_lanes),
            intake_hash=str(intake.get("intake_hash", "")).strip(),
            interpretation_hash=str(interpretation.get("interpretation_hash", "")).strip(),
            support_resolution_hash=str(support.get("resolution_hash", "")).strip(),
            utterance_plan_hash=str(utterance_plan.get("plan_hash", "")).strip(),
            answer_contract_hash=str(answer_contract.get("contract_hash", "")).strip(),
            science_world_turn_hash=str(science_world_turn.get("snapshot_hash", "")).strip(),
            teaching=teaching_snapshot,
            comparison=comparison_snapshot,
            planning=planning_snapshot,
            synthesis=synthesis_snapshot,
            analogy=analogy_snapshot,
            concept_composition=concept_composition_snapshot,
            cross_domain_composition=cross_domain_composition_snapshot,
            audience_aware_quality=audience_quality_snapshot,
            overlay_contract=overlay_contract,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
