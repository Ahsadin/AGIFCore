from __future__ import annotations

import json

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_local_gateway"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_local_gateway.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_local_gateway_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.local_gateway",
    "agifcore_phase13_product_runtime.fail_closed_ux",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "allowlisted-route-count-bounded",
    "conversation-route-passes",
    "reserved-surfaces-blocked",
    "unknown-route-and-policy-mismatch-blocked",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase13_shell(scenario="weak")
    shell = weak_case["shell"]
    good = shell.gateway.route_request(
        route="/api/conversation-turn",
        payload={"user_text": "gateway pass path"},
        session_id=shell.session_open()["session_id"],
        policy_hash=shell.gateway.policy_hash,
    )
    blocked = shell.gateway.route_request(
        route="/api/task-submit",
        payload={"task": "blocked"},
        session_id=shell.session_open()["session_id"],
        policy_hash=shell.gateway.policy_hash,
    )
    unknown = shell.gateway.route_request(
        route="/api/not-real",
        payload={},
        session_id=shell.session_open()["session_id"],
        policy_hash=shell.gateway.policy_hash,
    )
    mismatch = shell.gateway.route_request(
        route="/api/conversation-turn",
        payload={"user_text": "mismatch"},
        session_id=shell.session_open()["session_id"],
        policy_hash="bad-policy-hash",
    )
    assert good["status"] == "pass"
    assert blocked["status"] == "blocked"
    assert unknown["status"] == "blocked"
    assert mismatch["status"] == "blocked"
    assert len(good["envelope"]["allowlisted_routes"]) <= 10
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "allowlisted-route-count-bounded", "result": "pass"},
            {"id": "conversation-route-passes", "result": "pass"},
            {"id": "reserved-surfaces-blocked", "result": "pass"},
            {"id": "unknown-route-and-policy-mismatch-blocked", "result": "pass"},
        ],
        anchors={
            "conversation_route": good,
            "blocked_reserved_surface": blocked,
            "blocked_unknown_route": unknown,
            "blocked_policy_mismatch": mismatch,
        },
        notes=["the local gateway enforces allowlisted routes, policy hash checks, and fail-closed blocking"],
    )


def main() -> int:
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    missing = vc.missing_files(checked_files)
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=checked_files,
            assertion_ids=ASSERTION_IDS,
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="local gateway verifier could not import its runtime modules or found missing files",
            missing=missing,
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    try:
        report = build_pass_report()
    except Exception as exc:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=checked_files,
            assertion_ids=ASSERTION_IDS,
            blocker_kind="verification_failed",
            blocker_message=str(exc),
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    vc.write_report(REPORT_PATH, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
