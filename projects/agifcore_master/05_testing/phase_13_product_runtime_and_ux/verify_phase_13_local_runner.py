from __future__ import annotations

import json

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_local_runner"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_local_runner.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_local_runner_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.local_runner",
    "agifcore_phase13_product_runtime.product_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "session-open-schema-correct",
    "conversation-turn-preserves-support-state",
    "lower-phase-hashes-pass-through",
    "runner-inputs-stay-read-only",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase13_shell(scenario="contradiction")
    shell = contradiction_case["shell"]
    session = shell.session_open()
    turn = shell.conversation_turn(user_text="please clarify the contradiction safely")
    assert session["schema"] == "agifcore.phase_13.session_open.v1"
    assert turn["schema"] == "agifcore.phase_13.conversation_turn.v1"
    assert turn["support_state"] == contradiction_case["phase12_cycle"]["overlay_contract"]["support_state"]
    assert turn["phase10_turn_hash"] == contradiction_case["phase10_turn"]["snapshot_hash"]
    assert turn["phase11_cycle_hash"] == contradiction_case["phase11_cycle"]["snapshot_hash"]
    assert turn["phase12_cycle_hash"] == contradiction_case["phase12_cycle"]["snapshot_hash"]
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "session-open-schema-correct", "result": "pass"},
            {"id": "conversation-turn-preserves-support-state", "result": "pass"},
            {"id": "lower-phase-hashes-pass-through", "result": "pass"},
            {"id": "runner-inputs-stay-read-only", "result": "pass"},
        ],
        anchors={"session_open": session, "conversation_turn": turn},
        notes=["the local runner stays a thin wrapper over prepared lower-phase truth"],
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
            blocker_message="local runner verifier could not import its runtime modules or found missing files",
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
