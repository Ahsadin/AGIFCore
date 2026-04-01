from __future__ import annotations

import json

import _phase_12_verifier_common as vc
from agifcore_phase12_structural_growth.contracts import MAX_REFLECTION_CONTROL_ACTIONS

VERIFIER = "verify_phase_12_reflection_control"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_reflection_control.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_12_reflection_control_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase12_structural_growth.reflection_control",
    "agifcore_phase12_structural_growth.contracts",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "action-count-stays-bounded",
    "decisions-stay-governed",
    "supporting-feedback-ids-present",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase12_cycle(scenario="contradiction")
    snapshot = contradiction_case["cycle"].reflection_control
    assert 1 <= snapshot.action_count <= MAX_REFLECTION_CONTROL_ACTIONS
    assert all(action.decision.value in {"advance", "hold", "halt"} for action in snapshot.actions)
    assert all(action.supporting_feedback_ids for action in snapshot.actions)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "action-count-stays-bounded", "result": "pass"},
            {"id": "decisions-stay-governed", "result": "pass"},
            {"id": "supporting-feedback-ids-present", "result": "pass"},
        ],
        anchors={"contradiction_case": snapshot.to_dict()},
        notes=["reflection control limits the number of structural-growth lanes that can move in one cycle"],
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
            blocker_message="reflection control verifier could not import its runtime modules or found missing files",
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
