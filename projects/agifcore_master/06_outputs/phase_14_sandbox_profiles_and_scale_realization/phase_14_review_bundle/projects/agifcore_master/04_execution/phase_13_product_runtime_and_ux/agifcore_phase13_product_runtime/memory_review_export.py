from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_EVIDENCE_REFS,
    MAX_MEMORY_REVIEW_EXPORT_BYTES,
    MEMORY_REVIEW_EXPORT_SCHEMA,
    PHASE2_MEMORY_REVIEW_EXPORT_SCHEMA,
    bounded_unique,
    canonical_size_bytes,
    stable_hash_payload,
)


def build_memory_review_export(
    *,
    session_open: Mapping[str, Any],
    conversation_turn: Mapping[str, Any],
    phase11_cycle_state: Mapping[str, Any],
    phase12_cycle_state: Mapping[str, Any],
) -> dict[str, Any]:
    workspace_id = f"phase13-runtime-{session_open['session_id']}"
    phase11_overlay = dict(phase11_cycle_state.get("overlay_contract", {}))
    phase12_overlay = dict(phase12_cycle_state.get("overlay_contract", {}))
    continuity_refs = bounded_unique(
        [
            str(phase11_cycle_state.get("snapshot_hash", "")),
            str(phase12_cycle_state.get("snapshot_hash", "")),
            str(conversation_turn.get("turn_hash", "")),
        ],
        ceiling=6,
        field_name="memory_review_continuity_refs",
    )
    source_export = {
        "schema": PHASE2_MEMORY_REVIEW_EXPORT_SCHEMA,
        "workspace_id": workspace_id,
        "memory_review_refs": [
            {
                "memory_review_ref": str(conversation_turn.get("memory_review_ref", "")),
                "conversation_id": str(session_open.get("conversation_id", "")),
                "turn_id": str(session_open.get("turn_id", "")),
            }
        ],
        "retention_candidate_refs": list(
            bounded_unique(
                [
                    *list(phase11_overlay.get("adopted_proposal_ids", [])),
                    *list(phase12_overlay.get("candidate_theory_ids", [])),
                    *list(phase12_overlay.get("candidate_domain_ids", [])),
                    *list(phase12_overlay.get("candidate_procedure_ids", [])),
                ],
                ceiling=MAX_EVIDENCE_REFS,
                field_name="retention_candidate_refs",
                allow_empty=True,
            )
        ),
        "notes": [
            "references only",
            "no semantic memory",
            "no procedural memory auto-execution",
            "review export stays inspectable and bounded",
        ],
    }
    payload = {
        "schema": MEMORY_REVIEW_EXPORT_SCHEMA,
        "session_id": str(session_open.get("session_id", "")),
        "conversation_id": str(session_open.get("conversation_id", "")),
        "turn_id": str(session_open.get("turn_id", "")),
        "source_memory_review_export": source_export,
        "continuity_refs": list(continuity_refs),
        "payload_size_bytes": canonical_size_bytes(source_export),
    }
    if payload["payload_size_bytes"] > MAX_MEMORY_REVIEW_EXPORT_BYTES:
        raise ValueError("memory review export exceeds planning ceiling")
    return {
        **payload,
        "snapshot_hash": stable_hash_payload(payload),
    }
