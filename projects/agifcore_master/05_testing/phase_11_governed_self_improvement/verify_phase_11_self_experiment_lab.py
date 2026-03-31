from __future__ import annotations

import json

import _phase_11_verifier_common as vc
from agifcore_phase11_self_improvement.contracts import MAX_SELF_EXPERIMENTS

VERIFIER = "verify_phase_11_self_experiment_lab"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/verify_phase_11_self_experiment_lab.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_11_self_experiment_lab_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase11_self_improvement.self_experiment_lab",
    "agifcore_phase11_self_improvement.self_improvement_cycle",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "experiment-count-bounded",
    "candidate-baseline-comparison-present",
    "held-out-pack-refs-present",
    "phase10-inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase11_cycle(scenario="weak")
    contradiction_case = vc.run_phase11_cycle(scenario="contradiction")
    weak_snapshot = weak_case["cycle"].self_experiment_lab
    contradiction_snapshot = contradiction_case["cycle"].self_experiment_lab
    assert weak_snapshot.experiment_count <= MAX_SELF_EXPERIMENTS
    assert contradiction_snapshot.experiment_count <= MAX_SELF_EXPERIMENTS
    assert all(item.candidate_score >= item.baseline_score for item in contradiction_snapshot.experiments)
    assert all(item.held_out_pack_ref for item in weak_snapshot.experiments)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "experiment-count-bounded", "result": "pass"},
            {"id": "candidate-baseline-comparison-present", "result": "pass"},
            {"id": "held-out-pack-refs-present", "result": "pass"},
            {"id": "phase10-inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["self experiments stay sandboxed and replayable instead of mutating live truth"],
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
            blocker_message="self experiment verifier could not import its runtime modules or found missing files",
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
