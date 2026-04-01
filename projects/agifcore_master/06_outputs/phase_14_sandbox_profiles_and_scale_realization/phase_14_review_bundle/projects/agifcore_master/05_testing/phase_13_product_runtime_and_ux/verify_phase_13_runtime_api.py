from __future__ import annotations

import json

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_runtime_api"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_runtime_api.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_runtime_api_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.embeddable_runtime_api",
    "agifcore_phase13_product_runtime.product_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "api-wrapper-schema-correct",
    "public-surfaces-available",
    "reserved-surfaces-fail-closed",
    "api-surface-ceiling-respected",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase13_shell(scenario="weak")
    shell = weak_case["shell"]
    session = shell.api.session_open()
    turn = shell.api.conversation_turn(user_text="phase13 runtime api smoke test")
    blocked_task = shell.api.task_submit(task_payload={"task": "blocked"})
    blocked_policy = shell.api.policy_update(policy_payload={"policy": "blocked"})
    session_surface = shell.session_open()
    assert session["schema"] == "agifcore.phase_13.embeddable_runtime_api.v1"
    assert session["status"] == "pass"
    assert turn["status"] == "pass"
    assert blocked_task["status"] == "blocked"
    assert blocked_policy["status"] == "blocked"
    total_surface_count = len(session_surface["available_surfaces"]) + len(session_surface["blocked_surfaces"])
    assert total_surface_count <= 8
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "api-wrapper-schema-correct", "result": "pass"},
            {"id": "public-surfaces-available", "result": "pass"},
            {"id": "reserved-surfaces-fail-closed", "result": "pass"},
            {"id": "api-surface-ceiling-respected", "result": "pass"},
        ],
        anchors={
            "session_open": session,
            "conversation_turn": turn,
            "blocked_task_submit": blocked_task,
            "blocked_policy_update": blocked_policy,
        },
        notes=["the embeddable API stays thin and routes every call through the local gateway"],
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
            blocker_message="runtime api verifier could not import its runtime modules or found missing files",
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
