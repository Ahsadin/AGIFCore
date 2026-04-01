from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_EVIDENCE_REFS,
    MAX_TRACE_EXPORT_BYTES,
    TRACE_EXPORT_SCHEMA,
    bounded_unique,
    canonical_size_bytes,
    infer_final_answer_mode,
    infer_knowledge_gap_reason,
    infer_next_action,
    make_ref,
    stable_hash_payload,
    utc_timestamp,
)


def build_trace_export(
    *,
    session_open: Mapping[str, Any],
    conversation_turn: Mapping[str, Any],
    phase10_turn_state: Mapping[str, Any],
    phase11_cycle_state: Mapping[str, Any],
    phase12_cycle_state: Mapping[str, Any],
) -> dict[str, Any]:
    phase10_overlay = dict(phase10_turn_state.get("overlay_contract", {}))
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
    final_answer_mode = infer_final_answer_mode(
        support_state=support_state,
        selected_outcome=selected_outcome,
    )
    planner_trace_ref = str(phase10_overlay.get("strategy_journal_ref", "")) or make_ref(
        "planner_trace",
        phase10_turn_state,
    )
    simulation_trace_ref = str(phase10_turn_state.get("science_world_turn_hash", "")) or make_ref(
        "simulation_trace",
        phase10_turn_state,
    )
    critic_trace_ref = str(phase10_overlay.get("diagnosis_ref", "")) or make_ref(
        "critic_trace",
        phase10_turn_state,
    )
    governance_trace_ref = str(phase12_overlay.get("contract_hash", "")) or str(
        phase11_overlay.get("contract_hash", "")
    ) or make_ref("governance_trace", phase12_cycle_state)
    trace_records = [
        {
            "sequence": 1,
            "event_id": make_ref(
                "evt_turn_admitted",
                {
                    "session_id": session_open["session_id"],
                    "conversation_id": session_open["conversation_id"],
                    "turn_id": session_open["turn_id"],
                },
            ),
            "event_type": "turn_admitted",
            "conversation_id": session_open["conversation_id"],
            "turn_id": session_open["turn_id"],
            "producer": "phase13_local_runner",
            "discourse_mode": "explain",
            "support_state": support_state,
            "knowledge_gap_reason": knowledge_gap_reason,
            "next_action": next_action,
            "planner_trace_ref": planner_trace_ref,
            "simulation_trace_ref": simulation_trace_ref,
            "critic_trace_ref": critic_trace_ref,
            "governance_trace_ref": governance_trace_ref,
            "payload_size_bytes": canonical_size_bytes(
                {
                    "request_text": conversation_turn.get("request_text", ""),
                    "support_state": support_state,
                }
            ),
            "final_answer_mode": None,
            "occurred_at": utc_timestamp(),
        },
        {
            "sequence": 2,
            "event_id": make_ref(
                "evt_response_ready",
                {
                    "session_id": session_open["session_id"],
                    "response_text": conversation_turn.get("response_text", ""),
                    "phase12_cycle_hash": conversation_turn.get("phase12_cycle_hash", ""),
                },
            ),
            "event_type": "response_ready",
            "conversation_id": session_open["conversation_id"],
            "turn_id": session_open["turn_id"],
            "producer": "phase13_local_runner",
            "discourse_mode": "explain",
            "support_state": support_state,
            "knowledge_gap_reason": knowledge_gap_reason,
            "next_action": next_action,
            "planner_trace_ref": planner_trace_ref,
            "simulation_trace_ref": simulation_trace_ref,
            "critic_trace_ref": critic_trace_ref,
            "governance_trace_ref": governance_trace_ref,
            "payload_size_bytes": canonical_size_bytes(
                {
                    "response_text": conversation_turn.get("response_text", ""),
                    "final_answer_mode": final_answer_mode,
                }
            ),
            "final_answer_mode": final_answer_mode,
            "occurred_at": utc_timestamp(),
        },
    ]
    evidence_refs = bounded_unique(
        [
            *list(phase10_overlay.get("evidence_refs", [])),
            *list(phase11_overlay.get("evidence_refs", [])),
            *list(phase12_overlay.get("evidence_refs", [])),
            planner_trace_ref,
            simulation_trace_ref,
            critic_trace_ref,
            governance_trace_ref,
        ],
        ceiling=MAX_EVIDENCE_REFS,
        field_name="trace_export_evidence_refs",
    )
    payload = {
        "schema": TRACE_EXPORT_SCHEMA,
        "session_id": str(session_open.get("session_id", "")),
        "conversation_id": str(session_open.get("conversation_id", "")),
        "turn_id": str(session_open.get("turn_id", "")),
        "trace_records": trace_records,
        "trace_record_count": len(trace_records),
        "evidence_refs": list(evidence_refs),
        "trace_anchor_hash": stable_hash_payload(trace_records),
    }
    if canonical_size_bytes(payload) > MAX_TRACE_EXPORT_BYTES:
        raise ValueError("trace export exceeds planning ceiling")
    return {
        **payload,
        "snapshot_hash": stable_hash_payload(payload),
    }
