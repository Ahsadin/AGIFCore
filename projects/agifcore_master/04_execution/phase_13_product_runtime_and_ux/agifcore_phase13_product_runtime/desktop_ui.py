from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    DESKTOP_UI_VIEWS,
    LOCAL_DESKTOP_CHAT_DEMO_SCHEMA,
    LOCAL_DESKTOP_UI_SCHEMA,
    MAX_DESKTOP_UI_VIEWS,
    stable_hash_payload,
)


class LocalDesktopUI:
    def _phase_chain_summary(
        self,
        *,
        latest_turn: Mapping[str, Any],
    ) -> list[str]:
        phase_results = list(latest_turn.get("phase_results", []))
        if not phase_results:
            return ["full_chain=none yet"]
        chain_bits = [
            f"{item.get('phase_id', '?')}:{item.get('status', 'unknown')}"
            for item in phase_results
        ]
        return [
            f"full_chain_complete={latest_turn.get('phase_chain_completed', False)}",
            f"phase_chain={', '.join(chain_bits)}",
            (
                "phase_counts="
                f"used:{latest_turn.get('phases_used_count', 0)} "
                f"no_op:{latest_turn.get('phases_no_op_count', 0)} "
                f"blocked:{latest_turn.get('phases_blocked_count', 0)} "
                f"insufficient_input:{latest_turn.get('phases_insufficient_input_count', 0)}"
            ),
        ]

    def _interactive_transcript(
        self,
        *,
        interactive_history: list[Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        transcript: list[dict[str, Any]] = []
        for turn in interactive_history[-8:]:
            question_text = str(turn.get("question_text", "")).strip()
            response_text = str(turn.get("response_text", "")).strip()
            if question_text:
                transcript.append(
                    {
                        "speaker": "user",
                        "text": question_text,
                    }
                )
            if response_text:
                transcript.append(
                    {
                        "speaker": "assistant",
                        "text": response_text,
                        "answer_mode": str(turn.get("answer_mode", "unknown")),
                        "final_answer_mode": str(turn.get("final_answer_mode", "unknown")),
                    }
                )
        return transcript

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

    def render_interactive(
        self,
        *,
        shell_snapshot: Mapping[str, Any],
        session_open: Mapping[str, Any],
        state_export: Mapping[str, Any],
        trace_export: Mapping[str, Any],
        memory_review_export: Mapping[str, Any],
        fail_closed_catalog: Mapping[str, Any],
        interactive_history: list[Mapping[str, Any]],
        latest_turn: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        transcript = self._interactive_transcript(interactive_history=interactive_history)
        latest = dict(latest_turn or {})
        latest_refs = [str(ref) for ref in latest.get("local_truth_refs", [])][:4]
        latest_phase_chain_lines = self._phase_chain_summary(latest_turn=latest)
        views = [
            {
                "view_id": "session_overview",
                "title": "Session Overview",
                "status": "ready",
                "summary_lines": [
                    f"session_id={session_open['session_id']}",
                    f"interactive_turn_count={len(interactive_history)}",
                    f"available_surfaces={len(session_open['available_surfaces'])}",
                ],
                "evidence_refs": list(session_open.get("evidence_refs", []))[:4],
            },
            {
                "view_id": "chat_workspace",
                "title": "Chat Workspace",
                "status": "ready" if transcript else "empty",
                "summary_lines": [
                    transcript[-1]["text"] if transcript else "No interactive chat turns yet.",
                    f"message_count={len(transcript)}",
                    "desktop host presents runtime truth only",
                ],
                "evidence_refs": latest_refs,
            },
            {
                "view_id": "turn_evidence_view",
                "title": "Turn Evidence",
                "status": "ready" if latest else "waiting",
                "summary_lines": [
                    f"question_class={latest.get('question_class', 'none')}",
                    f"answer_mode={latest.get('answer_mode', 'none')}",
                    f"support_state={latest.get('support_state', 'none')}",
                    f"final_answer_after_full_chain={latest.get('final_answer_released_after_full_chain', False)}",
                ],
                "evidence_refs": latest_refs,
            },
            {
                "view_id": "trace_export_view",
                "title": "Trace Export",
                "status": "ready",
                "summary_lines": [
                    f"trace_record_count={trace_export['trace_record_count']}",
                    *latest_phase_chain_lines,
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
                    "unsupported questions stay explicit and inspectable",
                ],
                "evidence_refs": list(
                    fail_closed_catalog.get("states", [{}])[0].get("evidence_refs", [])
                )[:4],
            },
        ]
        if len(views) > MAX_DESKTOP_UI_VIEWS:
            raise ValueError("interactive desktop UI exceeds planning ceiling")
        payload = {
            "schema": LOCAL_DESKTOP_CHAT_DEMO_SCHEMA,
            "session_id": shell_snapshot["session_id"],
            "selected_view": "chat_workspace",
            "view_count": len(views),
            "views": views,
            "message_count": len(transcript),
            "turn_count": len(interactive_history),
            "chat_transcript": transcript,
            "latest_turn": latest,
            "input_contract": {
                "placeholder": "Ask the local AGIFCore shell a question",
                "max_chars": 512,
            },
        }
        return {
            **payload,
            "snapshot_hash": stable_hash_payload(payload),
        }
