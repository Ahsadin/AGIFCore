from __future__ import annotations

import json

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_desktop_ui"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_desktop_ui.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_desktop_ui_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.desktop_ui",
    "agifcore_phase13_product_runtime.product_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "ui-schema-correct",
    "view-count-bounded",
    "fail-closed-view-present",
    "ui-does-not-rewrite-runner-output",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase13_shell(scenario="weak")
    shell = weak_case["shell"]
    ui_snapshot = shell.ui_snapshot()
    conversation_turn = shell.conversation_turn()
    view_ids = [item["view_id"] for item in ui_snapshot["views"]]
    conversation_view = next(item for item in ui_snapshot["views"] if item["view_id"] == "conversation_result")
    assert ui_snapshot["schema"] == "agifcore.phase_13.local_desktop_ui.v1"
    assert ui_snapshot["view_count"] <= 7
    assert "fail_closed_help_view" in view_ids
    assert conversation_turn["response_text"] in conversation_view["summary_lines"][0]
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "ui-schema-correct", "result": "pass"},
            {"id": "view-count-bounded", "result": "pass"},
            {"id": "fail-closed-view-present", "result": "pass"},
            {"id": "ui-does-not-rewrite-runner-output", "result": "pass"},
        ],
        anchors={"ui_snapshot": ui_snapshot},
        notes=["the desktop UI stays presentation-only and keeps blocked states visible"],
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
            blocker_message="desktop UI verifier could not import its runtime modules or found missing files",
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
