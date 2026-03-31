from __future__ import annotations

from .contracts import (
    ClarificationRequest,
    DiscourseMode,
    MAX_UTTERANCE_PLAN_BRANCHES,
    Phase7ConversationError,
    SelfKnowledgeSnapshot,
    SupportStateResolution,
    UtterancePlan,
    require_schema,
    stable_hash_payload,
)


class UtterancePlannerError(Phase7ConversationError):
    """Raised when utterance planning escapes the bounded Phase 7 surface."""


class UtterancePlannerEngine:
    """Produce a bounded structural plan for the final response."""

    def build_plan(
        self,
        *,
        question_interpretation_state: dict[str, object],
        support_state_resolution_state: dict[str, object],
        self_knowledge_state: dict[str, object],
        clarification_state: dict[str, object],
    ) -> UtterancePlan:
        interpretation = require_schema(
            question_interpretation_state,
            "agifcore.phase_07.question_interpretation.v1",
            "question_interpretation_state",
        )
        support_state = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )
        self_knowledge = require_schema(
            self_knowledge_state,
            "agifcore.phase_07.self_knowledge_surface.v1",
            "self_knowledge_state",
        )
        clarification = require_schema(
            clarification_state,
            "agifcore.phase_07.clarification.v1",
            "clarification_state",
        )
        if clarification.get("question_count", 0):
            discourse_mode = DiscourseMode.CLARIFY
            response_sections = ("clarification",)
            obligations = ("ask_one_specific_question", "state_missing_variable")
            constraint_slots = ("no_generic_filler", "max_two_questions")
            branch_count = 1
        elif self_knowledge.get("statement_count", 0):
            discourse_mode = DiscourseMode.SELF_KNOWLEDGE
            response_sections = ("self_knowledge", "limits")
            obligations = ("cite_continuity_backed_self_knowledge", "state_limit_if_present")
            constraint_slots = ("no_unsupported_self_assertion",)
            branch_count = 2
        elif support_state.get("next_action") == "abstain":
            discourse_mode = DiscourseMode.ABSTAIN
            response_sections = ("abstain", "next_step")
            obligations = ("state_missing_support", "preserve_honest_limit")
            constraint_slots = ("no_polished_bluff",)
            branch_count = 1
        else:
            discourse_mode = DiscourseMode(str(interpretation.get("discourse_mode_hint")))
            response_sections = ("answer", "evidence", "next_step")
            obligations = ("state_local_scope", "preserve_support_state")
            constraint_slots = ("no_live_execution", "no_rich_expression")
            branch_count = 1 if not interpretation.get("comparison_requested") else 2
        if branch_count > MAX_UTTERANCE_PLAN_BRANCHES:
            raise UtterancePlannerError("utterance-plan branch count exceeds Phase 7 ceiling")
        payload = {
            "turn_id": interpretation.get("turn_id"),
            "discourse_mode": discourse_mode.value,
            "response_sections": list(response_sections),
            "branch_count": branch_count,
        }
        planner_trace_ref = f"planner::{stable_hash_payload(payload)[:12]}"
        return UtterancePlan(
            schema="agifcore.phase_07.utterance_plan.v1",
            plan_id=f"plan::{stable_hash_payload({**payload, 'kind': 'utterance_plan'})[:12]}",
            discourse_mode=discourse_mode,
            response_sections=response_sections,
            sentence_obligations=obligations,
            constraint_slots=constraint_slots,
            branch_count=branch_count,
            planner_trace_ref=planner_trace_ref,
            plan_hash=stable_hash_payload({**payload, "planner_trace_ref": planner_trace_ref}),
        )
