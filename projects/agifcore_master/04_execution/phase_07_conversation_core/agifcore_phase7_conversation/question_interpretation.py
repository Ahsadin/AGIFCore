from __future__ import annotations

import re

from .contracts import (
    MAX_PARSED_SIGNALS,
    DiscourseMode,
    Phase7ConversationError,
    QuestionCategory,
    QuestionInterpretation,
    RawTextIntakeRecord,
    require_non_empty_str,
    stable_hash_payload,
)

_TOKEN_RE = re.compile(r"[a-z0-9']+")
_AMBIGUOUS_REFERENCE_TOKENS = {"it", "that", "this", "there", "here", "something", "anything"}
_AMBIGUOUS_ACTION_TOKENS = {"check", "tell", "explain", "handle", "help", "review", "mean", "do"}
_LIVE_TIME_CUES = {"current", "latest", "live", "now", "recent", "today", "tonight", "updated"}
_LIVE_SUBJECT_CUES = {"news", "price", "score", "stock", "temperature", "time", "weather"}
_CORRECTION_CUES = {"actually", "correct", "correction", "instead", "meant", "sorry"}
_REPEAT_CUES = {"again", "before", "earlier", "previous", "repeat", "same", "still"}
_COMPARISON_CUES = {"better", "less", "more", "than", "versus", "vs", "worse", "compare"}
_LOCAL_ARTIFACT_CUES = {
    "file",
    "files",
    "path",
    "paths",
    "doc",
    "docs",
    "document",
    "documents",
    "readme",
    "changelog",
    "plan",
    "repo",
    "repository",
    "code",
    "module",
    "json",
    "markdown",
}
_LOCAL_ACTION_CUES = {"show", "find", "locate", "where", "which", "list", "open", "inspect", "read"}
_SELF_KNOWLEDGE_GROUPS = (
    ({"who", "identity"}, {"you", "yourself", "system", "agifcore"}),
    ({"can", "capabilities", "capability", "able"}, {"do", "handle", "support"}),
    ({"phase", "status", "state"}, {"you", "agifcore", "repo"}),
    ({"allowed", "forbidden", "cannot", "cant", "blocked"}, {"do", "action", "actions"}),
)
_EXPLAIN_CUES = {"explain", "why", "how", "because"}
_PLAN_CUES = {"plan", "steps", "sequence", "roadmap", "next"}
_STATUS_CUES = {"status", "state", "ready", "blocked"}
_DOMAIN_HINTS = {
    "finance_document_workflows": {"invoice", "finance", "document", "workflow"},
    "pos_store_operations": {"store", "restock", "inventory", "pos"},
    "claims_case_handling": {"claim", "claims", "case", "evidence"},
    "planning_coordination_workflows": {"plan", "planning", "schedule", "project", "route"},
}


class QuestionInterpretationError(Phase7ConversationError):
    """Raised when question interpretation exceeds Phase 7 bounds."""


def _tokens(value: str) -> list[str]:
    return _TOKEN_RE.findall(value.lower())


def _matches_groups(token_set: set[str], groups: tuple[set[str], set[str]] | tuple[set[str], set[str], set[str]]) -> bool:
    return all(token_set.intersection(group) for group in groups)


def _target_domain_hint(token_set: set[str]) -> str | None:
    for domain_id, cues in _DOMAIN_HINTS.items():
        if token_set.intersection(cues):
            return domain_id
    return None


class QuestionInterpretationEngine:
    """Convert intake records into a bounded structured question representation."""

    def build_snapshot(self, *, intake_record: RawTextIntakeRecord) -> QuestionInterpretation:
        normalized_text = require_non_empty_str(intake_record.normalized_text, "normalized_text")
        tokens = _tokens(normalized_text)
        token_set = set(tokens)
        ambiguous_request = bool(token_set.intersection(_AMBIGUOUS_REFERENCE_TOKENS) and token_set.intersection(_AMBIGUOUS_ACTION_TOKENS))
        live_current_requested = bool(token_set.intersection(_LIVE_TIME_CUES) and token_set.intersection(_LIVE_SUBJECT_CUES))
        local_artifact_requested = bool(token_set.intersection(_LOCAL_ARTIFACT_CUES) and token_set.intersection(_LOCAL_ACTION_CUES))
        self_knowledge_requested = any(_matches_groups(token_set, groups) for groups in _SELF_KNOWLEDGE_GROUPS)
        correction_hint = bool(token_set.intersection(_CORRECTION_CUES))
        repeated_fact_hint = bool(token_set.intersection(_REPEAT_CUES))
        comparison_requested = bool(token_set.intersection(_COMPARISON_CUES))

        signal_notes: list[str] = []
        if ambiguous_request:
            signal_notes.append("ambiguous_reference_detected")
        if live_current_requested:
            signal_notes.append("fresh_information_requested")
        if local_artifact_requested:
            signal_notes.append("local_artifact_lookup_requested")
        if self_knowledge_requested:
            signal_notes.append("self_knowledge_topic_detected")
        if correction_hint:
            signal_notes.append("correction_hint_detected")
        if repeated_fact_hint:
            signal_notes.append("repeat_hint_detected")
        if comparison_requested:
            signal_notes.append("comparison_cue_detected")

        target_domain_hint = _target_domain_hint(token_set)
        if target_domain_hint is not None:
            signal_notes.append(f"target_domain:{target_domain_hint}")
        if len(signal_notes) + len(token_set) > MAX_PARSED_SIGNALS:
            raise QuestionInterpretationError("parsed question structure exceeds Phase 7 signal ceiling")

        if self_knowledge_requested:
            question_category = QuestionCategory.SELF_KNOWLEDGE
            discourse_mode_hint = DiscourseMode.SELF_KNOWLEDGE
            user_intent = "self_knowledge_question"
        elif live_current_requested:
            question_category = QuestionCategory.LIVE_CURRENT
            discourse_mode_hint = DiscourseMode.ABSTAIN
            user_intent = "current_world_question"
        elif ambiguous_request:
            question_category = QuestionCategory.AMBIGUOUS
            discourse_mode_hint = DiscourseMode.CLARIFY
            user_intent = "ambiguous_question"
        elif local_artifact_requested:
            question_category = QuestionCategory.LOCAL_ARTIFACT
            discourse_mode_hint = DiscourseMode.STATUS
            user_intent = "local_artifact_question"
        elif comparison_requested:
            question_category = QuestionCategory.ORDINARY
            discourse_mode_hint = DiscourseMode.COMPARE
            user_intent = "comparison_question"
        elif token_set.intersection(_PLAN_CUES):
            question_category = QuestionCategory.ORDINARY
            discourse_mode_hint = DiscourseMode.PLAN
            user_intent = "plan_question"
        elif token_set.intersection(_STATUS_CUES):
            question_category = QuestionCategory.ORDINARY
            discourse_mode_hint = DiscourseMode.STATUS
            user_intent = "status_question"
        elif token_set.intersection(_EXPLAIN_CUES):
            question_category = QuestionCategory.ORDINARY
            discourse_mode_hint = DiscourseMode.EXPLAIN
            user_intent = "explanation_question"
        elif correction_hint:
            question_category = QuestionCategory.CORRECTION_HINT
            discourse_mode_hint = DiscourseMode.EXPLAIN
            user_intent = "correction_question"
        elif repeated_fact_hint:
            question_category = QuestionCategory.REPEATED_FACT_HINT
            discourse_mode_hint = DiscourseMode.EXPLAIN
            user_intent = "repeat_question"
        else:
            question_category = QuestionCategory.ORDINARY
            discourse_mode_hint = DiscourseMode.EXPLAIN
            user_intent = "general_question"

        payload = {
            "conversation_id": intake_record.conversation_id,
            "turn_id": intake_record.turn_id,
            "raw_text_hash": intake_record.intake_hash,
            "user_intent": user_intent,
            "discourse_mode_hint": discourse_mode_hint.value,
            "question_category": question_category.value,
            "target_domain_hint": target_domain_hint,
            "signals": signal_notes,
            "extracted_terms": tokens[:24],
        }
        return QuestionInterpretation(
            schema="agifcore.phase_07.question_interpretation.v1",
            conversation_id=intake_record.conversation_id,
            turn_id=intake_record.turn_id,
            raw_text_hash=intake_record.intake_hash,
            user_intent=user_intent,
            discourse_mode_hint=discourse_mode_hint,
            question_category=question_category,
            target_domain_hint=target_domain_hint,
            live_current_requested=live_current_requested,
            ambiguous_request=ambiguous_request,
            self_knowledge_requested=self_knowledge_requested,
            local_artifact_requested=local_artifact_requested,
            correction_hint=correction_hint,
            repeated_fact_hint=repeated_fact_hint,
            comparison_requested=comparison_requested,
            token_count=len(tokens),
            extracted_terms=tuple(tokens[:24]),
            signal_notes=tuple(signal_notes),
            interpretation_hash=stable_hash_payload(payload),
        )
