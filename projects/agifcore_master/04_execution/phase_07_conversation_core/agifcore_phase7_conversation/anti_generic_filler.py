from __future__ import annotations

from .contracts import (
    GuardrailResult,
    GuardrailStatus,
    GuardrailViolation,
    NextAction,
    Phase7ConversationError,
    RealizationDraft,
    require_schema,
    stable_hash_payload,
)

_GENERIC_OPENERS = (
    "based on the information provided",
    "here are some things to consider",
    "in general",
    "it depends",
)
_GENERIC_STOPWORDS = {
    "a",
    "about",
    "again",
    "an",
    "and",
    "are",
    "ask",
    "at",
    "be",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "of",
    "on",
    "or",
    "please",
    "the",
    "this",
    "to",
    "we",
    "what",
    "when",
    "where",
    "who",
    "why",
    "you",
}
_UNSUPPORTED_SELF_WORDS = {"feel", "believe", "want", "hope", "wish"}


class AntiGenericFillerError(Phase7ConversationError):
    """Raised when anti-filler enforcement cannot produce a safe output."""


def _violation(reason_code: str, detail: str) -> GuardrailViolation:
    payload = {"reason_code": reason_code, "detail": detail}
    return GuardrailViolation(
        violation_id=f"violation::{stable_hash_payload(payload)[:12]}",
        reason_code=reason_code,
        detail=detail,
        violation_hash=stable_hash_payload(payload),
    )


class AntiGenericFillerEngine:
    """Detect generic filler and force honest fallback text when needed."""

    def enforce(
        self,
        *,
        question_interpretation_state: dict[str, object],
        support_state_resolution_state: dict[str, object],
        self_knowledge_state: dict[str, object],
        clarification_state: dict[str, object],
        realization_draft: RealizationDraft,
    ) -> GuardrailResult:
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
        lowered = realization_draft.response_text.lower().strip()
        violations: list[GuardrailViolation] = []
        if any(lowered.startswith(prefix) for prefix in _GENERIC_OPENERS):
            violations.append(_violation("generic_opener_detected", "response starts with a generic framing phrase"))
        if support_state.get("next_action") == NextAction.CLARIFY.value and "?" not in realization_draft.response_text:
            violations.append(_violation("clarification_missing_question_mark", "clarification output is not phrased as a question"))
        if support_state.get("next_action") in {NextAction.SEARCH_EXTERNAL.value, NextAction.SEARCH_LOCAL.value, NextAction.ABSTAIN.value}:
            if "can't answer" not in lowered and "do not have enough" not in lowered and "don't have enough" not in lowered:
                violations.append(_violation("missing_honest_limit_language", "non-answer route did not preserve an explicit limit"))
        if interpretation.get("self_knowledge_requested"):
            if any(word in lowered for word in _UNSUPPORTED_SELF_WORDS):
                violations.append(_violation("unsupported_self_assertion", "self-knowledge output used unsupported self-assertion language"))
            if self_knowledge.get("statement_count", 0) == 0:
                violations.append(_violation("missing_self_knowledge_anchor", "self-knowledge answer lacked continuity-backed statements"))
        if support_state.get("support_state") in {"grounded", "inferred"}:
            meaningful_terms = [
                str(term)
                for term in interpretation.get("extracted_terms", [])
                if str(term) not in _GENERIC_STOPWORDS
            ]
            if meaningful_terms and not any(term in lowered for term in meaningful_terms[:6]):
                violations.append(_violation("missing_question_specific_terms", "answer text does not echo any question-specific terms"))

        output_text = realization_draft.response_text
        status = GuardrailStatus.PASS
        fallback_action = NextAction(str(support_state.get("next_action")))
        if violations:
            status = GuardrailStatus.FALLBACK_APPLIED
            if clarification.get("question_count", 0):
                output_text = clarification["questions"][0]["question_text"]
            elif support_state.get("next_action") == NextAction.SEARCH_EXTERNAL.value:
                output_text = (
                    "I can't answer that honestly from local AGIFCore state because it needs fresh external information. "
                    "The correct next step is search_external."
                )
            elif support_state.get("next_action") == NextAction.SEARCH_LOCAL.value:
                output_text = (
                    "I don't have enough grounded local evidence in the current turn to answer directly. "
                    "The correct next step is search_local."
                )
            elif support_state.get("next_action") == NextAction.ABSTAIN.value:
                output_text = (
                    "I don't have enough grounded local evidence to answer that honestly. "
                    "The correct result is to abstain."
                )
            elif self_knowledge.get("statement_count", 0):
                statements = [item["statement"] for item in self_knowledge.get("statements", [])]
                output_text = "From this local AGIFCore state: " + " ".join(statements)
            else:
                raise AntiGenericFillerError("guardrail fallback could not produce a safe output")

        payload = {
            "status": status.value,
            "fallback_action": fallback_action.value,
            "output_text": output_text,
            "violations": [item.to_dict() for item in violations],
        }
        return GuardrailResult(
            schema="agifcore.phase_07.anti_generic_filler.v1",
            status=status,
            fallback_action=fallback_action,
            output_text=output_text,
            violations=tuple(violations),
            guardrail_hash=stable_hash_payload(payload),
        )
