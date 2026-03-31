from __future__ import annotations

from .contracts import (
    ClarificationQuestion,
    ClarificationRequest,
    MAX_CLARIFICATION_QUESTIONS,
    NextAction,
    Phase7ConversationError,
    require_schema,
    stable_hash_payload,
)


class ClarificationError(Phase7ConversationError):
    """Raised when clarification behavior exceeds the bounded Phase 7 surface."""


class ClarificationEngine:
    """Generate targeted clarification questions only when support-state requires it."""

    def build_request(
        self,
        *,
        question_interpretation_state: dict[str, object],
        support_state_resolution_state: dict[str, object],
    ) -> ClarificationRequest:
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
        if support_state.get("next_action") != NextAction.CLARIFY.value:
            return ClarificationRequest(
                schema="agifcore.phase_07.clarification.v1",
                question_count=0,
                questions=(),
                request_hash=stable_hash_payload({"questions": []}),
            )

        missing_variables: list[str] = []
        if interpretation.get("target_domain_hint") is None:
            missing_variables.append("target_domain")
        if interpretation.get("ambiguous_request"):
            missing_variables.append("referent")
        if interpretation.get("live_current_requested"):
            missing_variables.append("time_window")
        if not missing_variables:
            missing_variables.append("specific_scope")
        question_text = (
            "I can answer this, but I need one detail first: "
            "which local workflow, file, or domain do you mean?"
        )
        if "time_window" in missing_variables:
            question_text = (
                "I can answer this, but I need one detail first: "
                "which exact local artifact or time window do you want me to use?"
            )
        question_id = f"clarify::{stable_hash_payload({'missing_variables': missing_variables, 'question_text': question_text})[:12]}"
        question = ClarificationQuestion(
            question_id=question_id,
            question_text=question_text,
            missing_variables=tuple(missing_variables[:3]),
            reason_code=str(support_state.get("knowledge_gap_reason")),
            question_hash=stable_hash_payload({"question_id": question_id, "missing_variables": missing_variables}),
        )
        questions = (question,)
        if len(questions) > MAX_CLARIFICATION_QUESTIONS:
            raise ClarificationError("clarification count exceeds Phase 7 ceiling")
        return ClarificationRequest(
            schema="agifcore.phase_07.clarification.v1",
            question_count=len(questions),
            questions=questions,
            request_hash=stable_hash_payload({"questions": [item.to_dict() for item in questions]}),
        )
