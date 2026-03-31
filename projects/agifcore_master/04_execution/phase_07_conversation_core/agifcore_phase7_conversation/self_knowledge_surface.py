from __future__ import annotations

from .contracts import (
    Phase7ConversationError,
    SelfKnowledgeSnapshot,
    SelfKnowledgeStatement,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)


class SelfKnowledgeSurfaceError(Phase7ConversationError):
    """Raised when the self-knowledge surface is not evidence-bound."""


class SelfKnowledgeSurfaceEngine:
    """Expose only continuity-backed self-knowledge statements."""

    @staticmethod
    def _matches_requested_terms(statement_text: str, requested_terms: set[str]) -> bool:
        lowered = statement_text.lower()
        if {"phase", "status"} & requested_terms:
            return "phase" in lowered or "open" in lowered or "status" in lowered
        if {"can", "capabilities", "capability", "able", "support"} & requested_terms:
            return "can" in lowered or "support" in lowered or "limit" in lowered or "do not" in lowered
        if {"allowed", "forbidden", "cannot", "cant", "blocked"} & requested_terms:
            return "do not" in lowered or "cannot" in lowered or "only" in lowered
        return True

    def build_snapshot(
        self,
        *,
        question_interpretation_state: dict[str, object],
        support_state_resolution_state: dict[str, object],
        continuity_memory_state: dict[str, object],
    ) -> SelfKnowledgeSnapshot:
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
        continuity_state = require_schema(
            continuity_memory_state,
            "agifcore.phase_04.continuity_memory.v1",
            "continuity_memory_state",
        )
        statements: list[SelfKnowledgeStatement] = []
        if not bool(interpretation.get("self_knowledge_requested")):
            return SelfKnowledgeSnapshot(
                schema="agifcore.phase_07.self_knowledge_surface.v1",
                statement_count=0,
                statements=(),
                snapshot_hash=stable_hash_payload({"statements": []}),
            )

        requested_terms = set(str(item) for item in interpretation.get("extracted_terms", []))
        anchors = [require_mapping(item, "continuity_anchor") for item in continuity_state.get("anchors", [])]
        fallback_statements: list[SelfKnowledgeStatement] = []
        for anchor in anchors:
            anchor_id = require_non_empty_str(anchor.get("anchor_id"), "anchor_id")
            subject = str(anchor.get("subject", "")).lower()
            continuity_kind = str(anchor.get("continuity_kind", "")).lower()
            statement_text = require_non_empty_str(anchor.get("statement"), "statement")
            if "agifcore" not in subject and "self" not in continuity_kind and "runtime" not in subject:
                continue
            anchor_refs = [anchor_id, *list(anchor.get("provenance_refs", []))]
            statement_id = f"self-knowledge::{stable_hash_payload({'anchor_id': anchor_id, 'statement': statement_text})[:12]}"
            statement = SelfKnowledgeStatement(
                statement_id=statement_id,
                statement_kind=continuity_kind or "self_knowledge",
                statement=statement_text,
                anchor_refs=tuple(anchor_refs),
                statement_hash=stable_hash_payload({"statement_id": statement_id, "anchor_refs": anchor_refs}),
            )
            if self._matches_requested_terms(statement_text, requested_terms):
                statements.append(statement)
            else:
                fallback_statements.append(statement)
        if len(statements) < 2:
            for statement in fallback_statements:
                if statement.statement_id in {item.statement_id for item in statements}:
                    continue
                statements.append(statement)
                if len(statements) >= 2:
                    break
        if not statements and support_state.get("knowledge_gap_reason") != "none":
            raise SelfKnowledgeSurfaceError("self-knowledge requested but no continuity-backed statements were available")
        payload = {"statements": [statement.to_dict() for statement in statements[:4]]}
        return SelfKnowledgeSnapshot(
            schema="agifcore.phase_07.self_knowledge_surface.v1",
            statement_count=len(statements[:4]),
            statements=tuple(statements[:4]),
            snapshot_hash=stable_hash_payload(payload),
        )
