from __future__ import annotations

import json

import _phase_13_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase13_shell(scenario="weak")
    shell = result["shell"]
    session = shell.api.session_open()
    turn = shell.api.conversation_turn(user_text="show the local-first product shell path")
    state_export = shell.api.state_export()
    trace_export = shell.api.trace_export()
    memory_export = shell.api.memory_review_export()
    shutdown = shell.api.safe_shutdown()
    ui_snapshot = shell.ui_snapshot()
    return {
        "phase": "13",
        "demo_id": "end_to_end_product",
        "status": "open",
        "original_prompt": result["fixture"]["intake"]["raw_text"],
        "product_shell": shell.shell_snapshot(),
        "session_open": session,
        "conversation_turn": turn,
        "state_export": state_export,
        "trace_export": trace_export,
        "memory_review_export": memory_export,
        "safe_shutdown": shutdown,
        "desktop_ui": ui_snapshot,
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_13_runtime_api_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_13_local_runner_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_13_local_gateway_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_13_desktop_ui_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_13_state_export_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_13_trace_export_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_13_memory_review_export_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_13_safe_shutdown_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only end-to-end product demo",
            "Phase 13 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    shell = payload["product_shell"]
    turn = payload["conversation_turn"]["gateway_response"]["response"]
    trace_export = payload["trace_export"]["gateway_response"]["response"]
    return [
        "# Phase 13 Demo: End-to-End Product Runtime",
        "",
        "Phase 13 remains `open`. This demo is inspectable review material only.",
        "",
        "## Original Prompt",
        "",
        f"- `{payload['original_prompt']}`",
        "",
        "## Product Shell Surface",
        "",
        f"- session id: `{shell['session_id']}`",
        f"- support state: `{shell['support_state']}`",
        f"- allowlisted route count: `{len(shell['allowlisted_routes'])}`",
        f"- ui view count: `{shell['ui_view_count']}`",
        "",
        "## End-to-End Path",
        "",
        f"- conversation response: `{turn['response_text']}`",
        f"- final answer mode: `{turn['final_answer_mode']}`",
        f"- trace record count: `{trace_export['trace_record_count']}`",
        f"- memory review refs: `{payload['memory_review_export']['gateway_response']['response']['source_memory_review_export']['memory_review_refs']}`",
        f"- safe shutdown status: `{payload['safe_shutdown']['gateway_response']['response']['shutdown_status']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- the product shell stays above approved lower-phase runtime truth",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_13_end_to_end_product_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_13_end_to_end_product_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
