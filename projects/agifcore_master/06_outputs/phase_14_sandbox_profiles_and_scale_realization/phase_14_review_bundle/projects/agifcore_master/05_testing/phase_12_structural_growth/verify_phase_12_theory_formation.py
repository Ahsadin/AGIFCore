from __future__ import annotations

import json

import _phase_12_verifier_common as vc

VERIFIER = "verify_phase_12_theory_formation"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_theory_formation.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_12_theory_formation_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase12_structural_growth.theory_formation",
    "agifcore_phase12_structural_growth.contracts",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "candidate-count-stays-bounded",
    "falsifiers-present",
    "mechanism-and-next-step-present",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase12_cycle(scenario="weak")
    contradiction_case = vc.run_phase12_cycle(scenario="contradiction")
    weak_snapshot = weak_case["cycle"].theory_formation
    contradiction_snapshot = contradiction_case["cycle"].theory_formation
    assert weak_snapshot.candidate_count == 1
    assert 1 <= contradiction_snapshot.candidate_count <= 2
    for snapshot in (weak_snapshot, contradiction_snapshot):
        for candidate in snapshot.candidates:
            assert candidate.falsifier_refs
            assert candidate.mechanism_step_refs
            assert candidate.verification_next_step
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "candidate-count-stays-bounded", "result": "pass"},
            {"id": "falsifiers-present", "result": "pass"},
            {"id": "mechanism-and-next-step-present", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["theory formation stays falsifiable and grounded to bounded evidence refs"],
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
            blocker_message="theory formation verifier could not import its runtime modules or found missing files",
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
