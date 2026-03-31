from __future__ import annotations

import re

from .contracts import MAX_RAW_INPUT_CHARACTERS, RawTextIntakeRecord, Phase7ConversationError, require_non_empty_str, require_unique_str_list, stable_hash_payload

_TOKEN_RE = re.compile(r"[a-z0-9']+")
_WHITESPACE_RE = re.compile(r"\s+")


class RawTextIntakeError(Phase7ConversationError):
    """Raised when raw text intake exceeds Phase 7 boundaries."""


class RawTextIntakeEngine:
    """Normalize raw user text into a replay-safe intake record."""

    def build_record(
        self,
        *,
        conversation_id: str,
        turn_id: str,
        raw_text: str,
        active_context_refs: list[str] | None = None,
    ) -> RawTextIntakeRecord:
        normalized_raw = require_non_empty_str(raw_text, "raw_text")
        if len(normalized_raw) > MAX_RAW_INPUT_CHARACTERS:
            raise RawTextIntakeError("raw_text exceeds Phase 7 input ceiling")
        normalized_text = _WHITESPACE_RE.sub(" ", normalized_raw.strip())
        payload = {
            "conversation_id": require_non_empty_str(conversation_id, "conversation_id"),
            "turn_id": require_non_empty_str(turn_id, "turn_id"),
            "normalized_text": normalized_text,
            "active_context_refs": require_unique_str_list(active_context_refs or [], "active_context_refs"),
        }
        return RawTextIntakeRecord(
            conversation_id=payload["conversation_id"],
            turn_id=payload["turn_id"],
            raw_text=normalized_raw,
            normalized_text=normalized_text,
            active_context_refs=tuple(payload["active_context_refs"]),
            token_count=len(_TOKEN_RE.findall(normalized_text.lower())),
            character_count=len(normalized_raw),
            contains_code_block="```" in normalized_raw,
            ends_with_question=normalized_raw.rstrip().endswith("?"),
            intake_hash=stable_hash_payload(payload),
        )
