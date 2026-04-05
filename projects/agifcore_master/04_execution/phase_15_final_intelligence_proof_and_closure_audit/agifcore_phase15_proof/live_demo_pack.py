from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .contracts import LIVE_DEMO_PACK_SCHEMA, MAX_LIVE_DEMO_PACK_COUNT, stable_hash_payload


def build_live_demo_pack(
    *,
    phase13_shell_snapshot: Mapping[str, Any],
    phase14_shell_snapshot: Mapping[str, Any],
) -> dict[str, object]:
    sessions = [
        {"case_id": "demo_session_open", "session_kind": "session_open", "scenario": "weak"},
        {
            "case_id": "demo_weak_conversation",
            "session_kind": "conversation_turn",
            "scenario": "weak",
            "prompt_text": "show the local-first product shell path",
        },
        {"case_id": "demo_weak_state_export", "session_kind": "state_export", "scenario": "weak"},
        {"case_id": "demo_weak_trace_export", "session_kind": "trace_export", "scenario": "weak"},
        {"case_id": "demo_weak_memory_review", "session_kind": "memory_review_export", "scenario": "weak"},
        {
            "case_id": "demo_contradiction_conversation",
            "session_kind": "conversation_turn",
            "scenario": "contradiction",
            "prompt_text": "please clarify the contradiction safely",
        },
        {
            "case_id": "demo_interactive_turn",
            "session_kind": "interactive_turn",
            "scenario": "weak",
            "prompt_text": "what can you do",
        },
        {
            "case_id": "demo_interactive_desktop_ui",
            "session_kind": "interactive_desktop_ui",
            "scenario": "weak",
            "prompts": [
                "what can you do",
                "what evidence supports that",
            ],
        },
        {"case_id": "demo_safe_shutdown", "session_kind": "safe_shutdown", "scenario": "contradiction"},
        {
            "case_id": "demo_laptop_profile_manifest",
            "session_kind": "profile_manifest",
            "scenario": "weak",
            "profile": "laptop",
        },
        {
            "case_id": "demo_mobile_profile_manifest",
            "session_kind": "profile_manifest",
            "scenario": "weak",
            "profile": "mobile",
        },
        {
            "case_id": "demo_sandbox_allowed",
            "session_kind": "sandbox_execute",
            "scenario": "weak",
            "execution_request": {
                "profile": "laptop",
                "function_name": "add",
                "function_args": [1, 2],
            },
        },
        {
            "case_id": "demo_sandbox_tampered",
            "session_kind": "sandbox_execute",
            "scenario": "weak",
            "execution_request": {
                "profile": "laptop",
                "function_name": "add",
                "function_args": [1, 2],
                "variant": "tampered",
            },
        },
        {"case_id": "demo_manifest_audit", "session_kind": "manifest_audit", "scenario": "weak"},
    ]
    packs = [
        {
            "pack_id": "phase15_final_demo_pack",
            "session_count": len(sessions),
            "coverage_types": [
                "product_runtime",
                "bounded_honesty",
                "trace_and_memory_export",
                "interactive_chat_runtime",
                "interactive_desktop_ui_host",
                "safe_shutdown",
                "profile_contract",
                "sandbox_enforcement",
                "manifest_audit",
            ],
            "sessions": sessions,
            "phase13_hash": phase13_shell_snapshot["snapshot_hash"],
            "phase14_hash": phase14_shell_snapshot["snapshot_hash"],
        }
    ]
    if len(packs) > MAX_LIVE_DEMO_PACK_COUNT:
        raise ValueError("live-demo pack count exceeds planning ceiling")
    payload = {
        "schema": LIVE_DEMO_PACK_SCHEMA,
        "live_demo_pack_count": len(packs),
        "packs": packs,
        "phase16_blocked": True,
    }
    return {**payload, "catalog_hash": stable_hash_payload(payload)}


def run_live_demo_pack(
    *,
    pack_catalog: Mapping[str, Any],
    proof_shells: Mapping[str, Any],
    output_dir: Path | None = None,
) -> dict[str, object]:
    pack = dict(pack_catalog["packs"][0])
    session_results: list[dict[str, Any]] = []
    for session in pack["sessions"]:
        shell = proof_shells[str(session["scenario"])]
        kind = str(session["session_kind"])
        if kind == "session_open":
            payload = shell.phase13_shell.session_open()
            summary = {
                "support_state": payload["support_state"],
                "available_surface_count": len(payload["available_surfaces"]),
            }
        elif kind == "conversation_turn":
            payload = shell.phase13_shell.api.conversation_turn(user_text=str(session["prompt_text"]))
            response = payload["gateway_response"]["response"]
            summary = {
                "final_answer_mode": response["final_answer_mode"],
                "response_kind": response["response_kind"],
                "response_text": response["response_text"],
            }
        elif kind == "interactive_turn":
            payload = shell.phase13_shell.interactive_turn(user_text=str(session["prompt_text"]))
            summary = {
                "question_class": payload["question_class"],
                "answer_mode": payload["answer_mode"],
                "final_answer_mode": payload["final_answer_mode"],
                "response_text": payload["response_text"],
            }
        elif kind == "interactive_desktop_ui":
            prompts = [str(item) for item in session.get("prompts", [])]
            for prompt in prompts:
                shell.phase13_shell.interactive_turn(user_text=prompt)
            payload = shell.phase13_shell.interactive_ui_snapshot()
            latest_turn = dict(payload.get("latest_turn", {}))
            summary = {
                "selected_view": payload["selected_view"],
                "view_count": payload["view_count"],
                "message_count": payload["message_count"],
                "latest_question_class": latest_turn.get("question_class", "unknown"),
                "latest_answer_mode": latest_turn.get("answer_mode", "unknown"),
            }
        elif kind == "state_export":
            payload = shell.phase13_shell.api.state_export()
            response = payload["gateway_response"]["response"]
            summary = {
                "state_snapshot_hash": response["snapshot_hash"],
                "source_payload_bytes": response["source_payload_bytes"],
                "turn_count": len(response["source_state_export"]["turns"]),
            }
        elif kind == "trace_export":
            payload = shell.phase13_shell.api.trace_export()
            response = payload["gateway_response"]["response"]
            summary = {
                "trace_record_count": response["trace_record_count"],
                "support_state": response["trace_records"][-1]["support_state"],
            }
        elif kind == "memory_review_export":
            payload = shell.phase13_shell.api.memory_review_export()
            response = payload["gateway_response"]["response"]
            summary = {
                "memory_review_ref_count": len(
                    response["source_memory_review_export"]["memory_review_refs"]
                ),
                "retention_candidate_count": len(
                    response["source_memory_review_export"]["retention_candidate_refs"]
                ),
            }
        elif kind == "safe_shutdown":
            payload = shell.phase13_shell.api.safe_shutdown()
            response = payload["gateway_response"]["response"]
            summary = {
                "shutdown_status": response["shutdown_status"],
                "blocked_surface_count": len(response["blocked_surfaces_after_shutdown"]),
                "flush_complete": response["flush_complete"],
            }
        elif kind == "profile_manifest":
            manifests = shell.phase14_shell.profile_manifests()
            payload = next(item for item in manifests["profiles"] if item["profile"] == session["profile"])
            summary = {
                "profile": payload["profile"],
                "same_contract_hash": payload["same_contract_hash"],
                "active_cell_band": payload["active_cell_band"],
            }
        elif kind == "sandbox_execute":
            payload = shell.phase14_shell.sandbox_execute(output_dir=output_dir, **dict(session["execution_request"]))
            summary = {
                "status": payload["status"],
                "reason_code": payload["reason_code"],
                "stdout": payload["stdout"],
            }
        elif kind == "manifest_audit":
            payload = shell.phase14_shell.manifest_audit()
            summary = {
                "audit_status": payload["audit_status"],
                "logical_cell_count": payload["logical_cell_count"],
                "tissue_count": payload["tissue_count"],
            }
        else:
            raise ValueError(f"unsupported live-demo session kind: {kind}")
        session_results.append(
            {
                "case_id": session["case_id"],
                "session_kind": kind,
                "scenario": session["scenario"],
                "summary": summary,
                "payload": payload,
            }
        )
    payload = {
        "schema": LIVE_DEMO_PACK_SCHEMA,
        "pack_id": pack["pack_id"],
        "session_count": len(session_results),
        "coverage_types": list(pack["coverage_types"]),
        "session_results": session_results,
        "status": "pass",
        "phase16_blocked": True,
    }
    return {**payload, "result_hash": stable_hash_payload(payload)}
