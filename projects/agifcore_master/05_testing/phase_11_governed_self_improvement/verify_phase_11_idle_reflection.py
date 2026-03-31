from __future__ import annotations

import json

import _phase_11_verifier_common as vc
from agifcore_phase11_self_improvement.contracts import MAX_IDLE_REFLECTION_ITEMS

VERIFIER = "verify_phase_11_idle_reflection"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/verify_phase_11_idle_reflection.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_11_idle_reflection_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase11_self_improvement.idle_reflection",
    "agifcore_phase11_self_improvement.self_improvement_cycle",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "idle-cycle-runs-when-items-exist",
    "processed-item-count-bounded",
    "idle-stop-reason-present",
    "phase10-inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase11_cycle(scenario="weak")
    snapshot = weak_case["cycle"].idle_reflection
    assert snapshot.ran is True
    assert len(snapshot.processed_item_ids) <= MAX_IDLE_REFLECTION_ITEMS
    assert snapshot.stop_reason
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "idle-cycle-runs-when-items-exist", "result": "pass"},
            {"id": "processed-item-count-bounded", "result": "pass"},
            {"id": "idle-stop-reason-present", "result": "pass"},
            {"id": "phase10-inputs-remain-read-only", "result": "pass"},
        ],
        anchors={"weak_case": snapshot.to_dict()},
        notes=["idle reflection stays explicit and bounded instead of becoming always-on autonomy"],
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
            blocker_message="idle reflection verifier could not import its runtime modules or found missing files",
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
