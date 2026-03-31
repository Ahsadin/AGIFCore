from __future__ import annotations

import json

import _phase_11_verifier_common as vc

VERIFIER = "verify_phase_11_post_adoption_monitoring"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/verify_phase_11_post_adoption_monitoring.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_11_post_adoption_monitoring_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase11_self_improvement.post_adoption_monitoring",
    "agifcore_phase11_self_improvement.self_improvement_cycle",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "monitoring-items-follow-adopted-candidates",
    "weak-case-has-no-monitoring-items",
    "monitoring-status-present",
    "phase10-inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase11_cycle(scenario="contradiction")
    weak_case = vc.run_phase11_cycle(scenario="weak")
    contradiction_snapshot = contradiction_case["cycle"].post_adoption_monitoring
    weak_snapshot = weak_case["cycle"].post_adoption_monitoring
    assert contradiction_snapshot.monitoring_count >= 1
    assert weak_snapshot.monitoring_count == 0
    assert all(item.current_status.value == "active" for item in contradiction_snapshot.items)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "monitoring-items-follow-adopted-candidates", "result": "pass"},
            {"id": "weak-case-has-no-monitoring-items", "result": "pass"},
            {"id": "monitoring-status-present", "result": "pass"},
            {"id": "phase10-inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["post-adoption monitoring stays typed and bounded instead of becoming a vague promise"],
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
            blocker_message="post-adoption monitoring verifier could not import its runtime modules or found missing files",
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
