from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    DESKTOP_UI_VIEWS,
    LOCAL_DESKTOP_UI_SCHEMA,
    MAX_DESKTOP_UI_VIEWS,
    stable_hash_payload,
)


class LocalDesktopUI:
    def render(
        self,
        *,
        shell_snapshot: Mapping[str, Any],
        session_open: Mapping[str, Any],
        conversation_turn: Mapping[str, Any],
        state_export: Mapping[str, Any],
        trace_export: Mapping[str, Any],
        memory_review_export: Mapping[str, Any],
        fail_closed_catalog: Mapping[str, Any],
        installer_snapshot: Mapping[str, Any],
    ) -> dict[str, Any]:
        views = [
            {
                "view_id": "session_overview",
                "title": "Session Overview",
                "status": "ready",
                "summary_lines": [
                    f"session_id={session_open['session_id']}",
                    f"support_state={session_open['support_state']}",
                    f"available_surfaces={len(session_open['available_surfaces'])}",
                ],
                "evidence_refs": list(session_open.get("evidence_refs", []))[:4],
            },
            {
                "view_id": "conversation_result",
                "title": "Conversation Result",
                "status": "ready",
                "summary_lines": [
                    conversation_turn["response_text"],
                    f"final_answer_mode={conversation_turn['final_answer_mode']}",
                    f"next_action={conversation_turn['next_action']}",
                ],
                "evidence_refs": list(conversation_turn.get("evidence_refs", []))[:4],
            },
            {
                "view_id": "trace_export_view",
                "title": "Trace Export",
                "status": "ready",
                "summary_lines": [
                    f"trace_record_count={trace_export['trace_record_count']}",
                    f"trace_anchor_hash={trace_export['trace_anchor_hash']}",
                ],
                "evidence_refs": list(trace_export.get("evidence_refs", []))[:4],
            },
            {
                "view_id": "state_export_view",
                "title": "State Export",
                "status": "ready",
                "summary_lines": [
                    f"state_schema={state_export['source_state_export']['schema']}",
                    f"payload_bytes={state_export['source_payload_bytes']}",
                ],
                "evidence_refs": list(state_export["source_state_export"].get("evidence_refs", []))[:4],
            },
            {
                "view_id": "memory_review_view",
                "title": "Memory Review Export",
                "status": "ready",
                "summary_lines": [
                    f"memory_ref_count={len(memory_review_export['source_memory_review_export']['memory_review_refs'])}",
                    f"continuity_ref_count={len(memory_review_export['continuity_refs'])}",
                ],
                "evidence_refs": list(memory_review_export.get("continuity_refs", []))[:4],
            },
            {
                "view_id": "fail_closed_help_view",
                "title": "Fail-Closed Help",
                "status": "blocked_states_visible",
                "summary_lines": [
                    f"blocked_state_count={fail_closed_catalog['state_count']}",
                    "reserved surfaces stay explicit and inspectable",
                ],
                "evidence_refs": list(
                    fail_closed_catalog.get("states", [{}])[0].get("evidence_refs", [])
                )[:4],
            },
            {
                "view_id": "installer_distribution_view",
                "title": "Installer Distribution",
                "status": "local_only",
                "summary_lines": [
                    f"artifact_count={installer_snapshot['artifact_count']}",
                    f"public_release_blocked={installer_snapshot['public_release_blocked']}",
                ],
                "evidence_refs": [installer_snapshot["integrity_manifest"]["integrity_hash"]],
            },
        ]
        if len(views) > MAX_DESKTOP_UI_VIEWS:
            raise ValueError("desktop UI exceeds planning ceiling")
        payload = {
            "schema": LOCAL_DESKTOP_UI_SCHEMA,
            "session_id": shell_snapshot["session_id"],
            "selected_view": DESKTOP_UI_VIEWS[0],
            "view_count": len(views),
            "views": views,
        }
        return {
            **payload,
            "snapshot_hash": stable_hash_payload(payload),
        }
