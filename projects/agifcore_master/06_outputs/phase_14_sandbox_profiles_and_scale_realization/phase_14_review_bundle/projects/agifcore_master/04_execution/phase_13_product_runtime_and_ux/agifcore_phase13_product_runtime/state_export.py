from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_EVIDENCE_REFS,
    MAX_STATE_EXPORT_BYTES,
    PHASE2_OPERATOR_COMMANDS,
    PHASE2_STATE_EXPORT_SCHEMA,
    STATE_EXPORT_SCHEMA,
    bounded_unique,
    canonical_size_bytes,
    infer_knowledge_gap_reason,
    infer_next_action,
    stable_hash_payload,
    utc_timestamp,
)


def build_state_export(
    *,
    session_open: Mapping[str, Any],
    conversation_turn: Mapping[str, Any],
    trace_export: Mapping[str, Any],
    memory_review_export: Mapping[str, Any],
    phase11_cycle_state: Mapping[str, Any],
    phase12_cycle_state: Mapping[str, Any],
) -> dict[str, Any]:
    workspace_id = f"phase13-runtime-{session_open['session_id']}"
    phase11_overlay = dict(phase11_cycle_state.get("overlay_contract", {}))
    phase12_overlay = dict(phase12_cycle_state.get("overlay_contract", {}))
    support_state = str(conversation_turn.get("support_state", "unknown"))
    selected_outcome = str(conversation_turn.get("selected_outcome", ""))
    knowledge_gap_reason = infer_knowledge_gap_reason(
        support_state=support_state,
        selected_outcome=selected_outcome,
    )
    next_action = infer_next_action(
        support_state=support_state,
        selected_outcome=selected_outcome,
    )
    latest_trace = list(trace_export.get("trace_records", []))[-1]
    now = utc_timestamp()
    turn_ref = (
        f"workspace://{workspace_id}/turn/"
        f"{session_open['conversation_id']}/{session_open['turn_id']}"
    )
    evidence_refs = bounded_unique(
        [
            *list(phase11_overlay.get("evidence_refs", [])),
            *list(phase12_overlay.get("evidence_refs", [])),
            *list(conversation_turn.get("evidence_refs", [])),
        ],
        ceiling=MAX_EVIDENCE_REFS,
        field_name="state_export_evidence_refs",
    )
    source_export = {
        "schema": PHASE2_STATE_EXPORT_SCHEMA,
        "workspace_id": workspace_id,
        "created_at": now,
        "operator_commands": list(PHASE2_OPERATOR_COMMANDS),
        "turns": [
            {
                "turn_ref": turn_ref,
                "conversation_id": session_open["conversation_id"],
                "turn_id": session_open["turn_id"],
                "user_intent": conversation_turn.get("request_text", ""),
                "active_context_refs": list(conversation_turn.get("trace_anchor_refs", []))[:4],
                "discourse_mode": "explain",
                "support_state": support_state,
                "knowledge_gap_reason": knowledge_gap_reason,
                "next_action": next_action,
                "planner_trace_ref": latest_trace["planner_trace_ref"],
                "simulation_trace_ref": latest_trace["simulation_trace_ref"],
                "critic_trace_ref": latest_trace["critic_trace_ref"],
                "governance_trace_ref": latest_trace["governance_trace_ref"],
                "last_event_type": "response_ready",
                "response_text": conversation_turn.get("response_text", ""),
                "abstain_or_answer": conversation_turn.get("abstain_or_answer"),
                "final_answer_mode": conversation_turn.get("final_answer_mode"),
                "memory_review_ref": conversation_turn.get("memory_review_ref"),
                "workspace_updated_at": now,
            }
        ],
        "cells": [
            {
                "cell_ref": f"workspace://{workspace_id}/cell/local_runner",
                "cell_id": "local_runner",
                "role_family": "product_runtime_surface",
                "lifecycle_state": "running",
                "workspace_ref": f"workspace://{workspace_id}/cell/local_runner",
                "quarantine_ref": None,
                "rollback_ref": None,
                "updated_at": now,
            },
            {
                "cell_ref": f"workspace://{workspace_id}/cell/local_gateway",
                "cell_id": "local_gateway",
                "role_family": "product_runtime_surface",
                "lifecycle_state": "serving",
                "workspace_ref": f"workspace://{workspace_id}/cell/local_gateway",
                "quarantine_ref": None,
                "rollback_ref": None,
                "updated_at": now,
            },
            {
                "cell_ref": f"workspace://{workspace_id}/cell/local_desktop_ui",
                "cell_id": "local_desktop_ui",
                "role_family": "product_runtime_surface",
                "lifecycle_state": "presenting",
                "workspace_ref": f"workspace://{workspace_id}/cell/local_desktop_ui",
                "quarantine_ref": None,
                "rollback_ref": None,
                "updated_at": now,
            },
        ],
        "replay_refs": [f"replay://phase13/{trace_export['trace_anchor_hash'][:16]}"],
        "rollback_refs": list(phase11_overlay.get("rollback_refs", [])),
        "quarantine_refs": [],
        "evidence_refs": list(evidence_refs),
        "memory_hook_surface": dict(memory_review_export.get("source_memory_review_export", {})),
        "operator_log": [
            {
                "command_class": "inspect_state",
                "turn_ref": turn_ref,
                "occurred_at": now,
            },
            {
                "command_class": "export_evidence",
                "turn_ref": turn_ref,
                "occurred_at": now,
            },
        ],
    }
    payload = {
        "schema": STATE_EXPORT_SCHEMA,
        "session_id": str(session_open.get("session_id", "")),
        "conversation_id": str(session_open.get("conversation_id", "")),
        "turn_id": str(session_open.get("turn_id", "")),
        "source_state_export": source_export,
        "source_payload_bytes": canonical_size_bytes(source_export),
        "phase11_cycle_hash": str(phase11_cycle_state.get("snapshot_hash", "")),
        "phase12_cycle_hash": str(phase12_cycle_state.get("snapshot_hash", "")),
    }
    if payload["source_payload_bytes"] > MAX_STATE_EXPORT_BYTES:
        raise ValueError("state export exceeds planning ceiling")
    return {
        **payload,
        "snapshot_hash": stable_hash_payload(payload),
    }
