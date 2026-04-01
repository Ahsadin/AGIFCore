from __future__ import annotations

from typing import Any, Mapping

from .contracts import ALL_SURFACES, SAFE_SHUTDOWN_SCHEMA, stable_hash_payload, utc_timestamp


def build_safe_shutdown_receipt(
    *,
    session_open: Mapping[str, Any],
    state_export: Mapping[str, Any],
    trace_export: Mapping[str, Any],
    memory_review_export: Mapping[str, Any],
    phase11_cycle_state: Mapping[str, Any],
) -> dict[str, Any]:
    phase11_overlay = dict(phase11_cycle_state.get("overlay_contract", {}))
    payload = {
        "schema": SAFE_SHUTDOWN_SCHEMA,
        "session_id": str(session_open.get("session_id", "")),
        "conversation_id": str(session_open.get("conversation_id", "")),
        "turn_id": str(session_open.get("turn_id", "")),
        "shutdown_requested_at": utc_timestamp(),
        "shutdown_status": "safe_stopped",
        "flush_complete": True,
        "dropped_work_detected": False,
        "state_export_hash": str(state_export.get("snapshot_hash", "")),
        "trace_export_hash": str(trace_export.get("snapshot_hash", "")),
        "memory_review_export_hash": str(memory_review_export.get("snapshot_hash", "")),
        "rollback_refs": list(phase11_overlay.get("rollback_refs", [])),
        "blocked_surfaces_after_shutdown": list(ALL_SURFACES),
    }
    return {
        **payload,
        "receipt_hash": stable_hash_payload(payload),
    }
