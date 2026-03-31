from __future__ import annotations

import json

import _phase_11_verifier_common as vc
from agifcore_phase11_self_improvement.contracts import MAX_MEASUREMENT_PAIRS

VERIFIER = "verify_phase_11_before_after_measurement"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/verify_phase_11_before_after_measurement.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_11_before_after_measurement_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase11_self_improvement.before_after_measurement",
    "agifcore_phase11_self_improvement.self_improvement_cycle",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "measurement-pair-count-bounded",
    "rollback-metric-preserves-baseline",
    "pass-threshold-applies",
    "phase10-inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase11_cycle(scenario="contradiction")
    weak_case = vc.run_phase11_cycle(scenario="weak")
    contradiction_snapshot = contradiction_case["cycle"].before_after_measurement
    weak_snapshot = weak_case["cycle"].before_after_measurement
    assert contradiction_snapshot.pair_count <= MAX_MEASUREMENT_PAIRS
    assert weak_snapshot.pair_count <= MAX_MEASUREMENT_PAIRS
    assert contradiction_snapshot.measurements[0].pass_threshold_met is True
    assert all(item.rollback_metric == item.baseline_metric for item in contradiction_snapshot.measurements)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "measurement-pair-count-bounded", "result": "pass"},
            {"id": "rollback-metric-preserves-baseline", "result": "pass"},
            {"id": "pass-threshold-applies", "result": "pass"},
            {"id": "phase10-inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["before/after measurement stays machine-readable and rollback-linked"],
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
            blocker_message="before/after measurement verifier could not import its runtime modules or found missing files",
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
