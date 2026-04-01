from __future__ import annotations

import json

import _phase_13_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase13_shell(scenario="contradiction")
    shell = result["shell"]
    blocked_task = shell.api.task_submit(task_payload={"task": "blocked"})
    blocked_policy = shell.api.policy_update(policy_payload={"policy": "blocked"})
    unknown_route = shell.gateway.route_request(
        route="/api/not-real",
        payload={},
        session_id=shell.session_open()["session_id"],
        policy_hash=shell.gateway.policy_hash,
    )
    return {
        "phase": "13",
        "demo_id": "fail_closed_ux",
        "status": "open",
        "product_shell": shell.shell_snapshot(),
        "fail_closed_catalog": shell.fail_closed_catalog(),
        "blocked_task_submit": blocked_task,
        "blocked_policy_update": blocked_policy,
        "blocked_unknown_route": unknown_route,
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_13_local_gateway_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_13_fail_closed_ux_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_13_desktop_ui_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only fail-closed UX demo",
            "Phase 13 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    blocked_task = payload["blocked_task_submit"]["gateway_response"]["response"]
    blocked_policy = payload["blocked_policy_update"]["gateway_response"]["response"]
    unknown_route = payload["blocked_unknown_route"]["response"]
    return [
        "# Phase 13 Demo: Fail-Closed UX",
        "",
        "Phase 13 remains `open`. This demo is inspectable review material only.",
        "",
        "## Explicit Blocked States",
        "",
        f"- task_submit reason: `{blocked_task['reason_code']}`",
        f"- policy_update reason: `{blocked_policy['reason_code']}`",
        f"- unknown route reason: `{unknown_route['reason_code']}`",
        "",
        "## Why The UX Is Fail-Closed",
        "",
        f"- task_submit guidance: `{blocked_task['user_guidance']}`",
        f"- policy_update guidance: `{blocked_policy['user_guidance']}`",
        f"- unknown route guidance: `{unknown_route['user_guidance']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- blocked paths stay visible instead of being dressed up as success",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_13_fail_closed_ux_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_13_fail_closed_ux_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
