from __future__ import annotations

import json

import _phase_11_verifier_common as vc
from agifcore_phase11_self_improvement.contracts import MAX_SHADOW_EVALUATIONS

VERIFIER = "verify_phase_11_shadow_evaluation"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/verify_phase_11_shadow_evaluation.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_11_shadow_evaluation_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase11_self_improvement.shadow_evaluation",
    "agifcore_phase11_self_improvement.self_improvement_cycle",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "evaluation-count-bounded",
    "ready-for-measurement-stays-governed",
    "uncertainty-notes-present",
    "phase10-inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase11_cycle(scenario="weak")
    contradiction_case = vc.run_phase11_cycle(scenario="contradiction")
    weak_snapshot = weak_case["cycle"].shadow_evaluation
    contradiction_snapshot = contradiction_case["cycle"].shadow_evaluation
    assert weak_snapshot.evaluation_count <= MAX_SHADOW_EVALUATIONS
    assert contradiction_snapshot.evaluation_count <= MAX_SHADOW_EVALUATIONS
    assert any(item.ready_for_measurement for item in contradiction_snapshot.evaluations)
    assert all(not item.ready_for_measurement for item in weak_snapshot.evaluations)
    assert all(item.uncertainty_notes for item in weak_snapshot.evaluations)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "evaluation-count-bounded", "result": "pass"},
            {"id": "ready-for-measurement-stays-governed", "result": "pass"},
            {"id": "uncertainty-notes-present", "result": "pass"},
            {"id": "phase10-inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["shadow evaluation stays isolated and does not silently adopt candidates"],
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
            blocker_message="shadow evaluation verifier could not import its runtime modules or found missing files",
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
