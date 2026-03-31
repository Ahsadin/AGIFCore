from __future__ import annotations

from .contracts import (
    FinalAnswerMode,
    MAX_RESPONSE_CHARACTERS,
    Phase7ConversationError,
    RealizationDraft,
    require_schema,
    stable_hash_payload,
)


class SurfaceRealizerError(Phase7ConversationError):
    """Raised when surface realization violates the bounded Phase 7 surface."""


class SurfaceRealizer:
    """Build plain, truthful response drafts from the utterance plan."""

    def build_draft(
        self,
        *,
        question_interpretation_state: dict[str, object],
        support_state_resolution_state: dict[str, object],
        self_knowledge_state: dict[str, object],
        clarification_state: dict[str, object],
        utterance_plan_state: dict[str, object],
    ) -> RealizationDraft:
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
        plan = require_schema(
            utterance_plan_state,
            "agifcore.phase_07.utterance_plan.v1",
            "utterance_plan_state",
        )

        selected_domain = next(iter(support_state.get("selected_domain_ids", [])), interpretation.get("target_domain_hint"))
        evidence_refs = [str(item) for item in support_state.get("evidence_refs", [])[:5]]

        if clarification.get("question_count", 0):
            question_text = clarification["questions"][0]["question_text"]
            response_text = question_text
            final_answer_mode = FinalAnswerMode.CLARIFY
            cited_refs = tuple(item["question_id"] for item in clarification["questions"])
        elif self_knowledge.get("statement_count", 0):
            statements = [item["statement"] for item in self_knowledge.get("statements", [])]
            response_text = "From this local AGIFCore state: " + " ".join(statements)
            final_answer_mode = FinalAnswerMode.GROUNDED_FACT
            cited_refs = tuple(
                dict.fromkeys(
                    ref
                    for statement in self_knowledge.get("statements", [])
                    for ref in statement.get("anchor_refs", [])
                )
            )
        elif support_state.get("next_action") == "search_external":
            response_text = (
                "I can't answer that honestly from local AGIFCore state because it needs fresh external information. "
                "The correct next step is search_external."
            )
            final_answer_mode = FinalAnswerMode.SEARCH_NEEDED
            cited_refs = tuple(evidence_refs)
        elif support_state.get("next_action") == "search_local":
            response_text = (
                "I don't have enough grounded local evidence in the current turn to answer directly. "
                "The correct next step is search_local."
            )
            final_answer_mode = FinalAnswerMode.SEARCH_NEEDED
            cited_refs = tuple(evidence_refs)
        elif support_state.get("next_action") == "abstain":
            response_text = (
                "I don't have enough grounded local evidence to answer that honestly. "
                "The correct result is to abstain."
            )
            final_answer_mode = FinalAnswerMode.ABSTAIN
            cited_refs = tuple(evidence_refs)
        elif support_state.get("support_state") == "grounded":
            response_text = (
                f"From the local AGIFCore evidence, this maps to {selected_domain}. "
                "The support is review-only and execution-disabled, so I can explain the current local state but not run it."
            )
            final_answer_mode = FinalAnswerMode.GROUNDED_FACT
            cited_refs = tuple(evidence_refs)
        else:
            response_text = (
                f"The local AGIFCore evidence points to {selected_domain}, but it stays partial. "
                "I can give a bounded explanation, not a stronger claim."
            )
            final_answer_mode = FinalAnswerMode.DERIVED_EXPLANATION
            cited_refs = tuple(evidence_refs)
        if len(response_text) > MAX_RESPONSE_CHARACTERS:
            raise SurfaceRealizerError("response text exceeds the Phase 7 response ceiling")

        payload = {
            "plan_id": plan.get("plan_id"),
            "response_text": response_text,
            "final_answer_mode": final_answer_mode.value,
            "cited_evidence_refs": list(cited_refs),
        }
        return RealizationDraft(
            draft_id=f"draft::{stable_hash_payload(payload)[:12]}",
            response_text=response_text,
            final_answer_mode=final_answer_mode,
            cited_evidence_refs=cited_refs,
            draft_hash=stable_hash_payload(payload),
        )
