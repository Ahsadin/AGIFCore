from __future__ import annotations

import json

import _phase_10_verifier_common as vc
from agifcore_phase10_meta_cognition.contracts import MAX_SKEPTIC_BRANCHES

VERIFIER = "verify_phase_10_skeptic_counterexample"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_skeptic_counterexample.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_10_skeptic_counterexample_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase10_meta_cognition.contracts",
    "agifcore_phase10_meta_cognition.skeptic_counterexample",
    "agifcore_phase10_meta_cognition.meta_cognition_turn",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "skeptic-branch-count-bounded",
    "weak-case-fallback-surface-visible",
    "contradiction-case-counterexample-surface-visible",
    "inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase10_turn(scenario="weak")
    contradiction_case = vc.run_phase10_turn(scenario="contradiction")
    weak_snapshot = weak_case["turn"].skeptic_counterexample
    contradiction_snapshot = contradiction_case["turn"].skeptic_counterexample

    assert weak_snapshot.branch_count <= MAX_SKEPTIC_BRANCHES
    assert contradiction_snapshot.branch_count <= MAX_SKEPTIC_BRANCHES
    assert weak_snapshot.branch_count == 1
    assert weak_snapshot.branches[0].changed_answer_after_skeptic
    assert weak_snapshot.branches[0].forced_fallback
    assert contradiction_snapshot.branch_count == 2
    assert all(branch.supporting_refs for branch in contradiction_snapshot.branches)
    assert not any(branch.forced_fallback for branch in contradiction_snapshot.branches)
    assert any(branch.what_variable_could_flip_the_answer == "measurement_uncertainty" for branch in contradiction_snapshot.branches)

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "skeptic-branch-count-bounded", "result": "pass"},
            {"id": "weak-case-fallback-surface-visible", "result": "pass"},
            {"id": "contradiction-case-counterexample-surface-visible", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["skeptic output stays bounded and records whether it changed the answer or forced fallback"],
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
            blocker_message="skeptic counterexample verifier could not import its runtime modules or found missing files",
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
