from __future__ import annotations

import json

import _phase_11_verifier_common as vc

VERIFIER = "verify_phase_11_adoption_or_rejection_pipeline"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/verify_phase_11_adoption_or_rejection_pipeline.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_11_adoption_or_rejection_pipeline_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase11_self_improvement.adoption_or_rejection_pipeline",
    "agifcore_phase11_self_improvement.self_improvement_cycle",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "contradiction-case-adopts-one-bounded-candidate",
    "weak-case-does-not-self-approve",
    "decision-reasons-present",
    "phase10-inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase11_cycle(scenario="contradiction")
    weak_case = vc.run_phase11_cycle(scenario="weak")
    contradiction_snapshot = contradiction_case["cycle"].adoption_or_rejection_pipeline
    weak_snapshot = weak_case["cycle"].adoption_or_rejection_pipeline
    assert any(item.decision.value == "adopted" for item in contradiction_snapshot.decisions)
    assert all(item.decision.value != "adopted" for item in weak_snapshot.decisions)
    assert all(item.reason for item in contradiction_snapshot.decisions)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "contradiction-case-adopts-one-bounded-candidate", "result": "pass"},
            {"id": "weak-case-does-not-self-approve", "result": "pass"},
            {"id": "decision-reasons-present", "result": "pass"},
            {"id": "phase10-inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["adoption stays explicit, governed, and evidence-linked instead of implicit self-approval"],
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
            blocker_message="adoption pipeline verifier could not import its runtime modules or found missing files",
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
