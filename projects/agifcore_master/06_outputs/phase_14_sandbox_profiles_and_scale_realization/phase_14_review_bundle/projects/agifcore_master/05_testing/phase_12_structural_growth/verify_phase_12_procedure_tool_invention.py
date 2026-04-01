from __future__ import annotations

import json

import _phase_12_verifier_common as vc

VERIFIER = "verify_phase_12_procedure_tool_invention"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_procedure_tool_invention.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_12_procedure_tool_invention_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase12_structural_growth.procedure_tool_invention",
    "agifcore_phase12_structural_growth.contracts",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "single-candidate-bounded",
    "skill-anchor-present",
    "non-auto-execute-enforced",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase12_cycle(scenario="weak")
    contradiction_case = vc.run_phase12_cycle(scenario="contradiction")
    weak_snapshot = weak_case["cycle"].procedure_tool_invention
    contradiction_snapshot = contradiction_case["cycle"].procedure_tool_invention
    for snapshot in (weak_snapshot, contradiction_snapshot):
        assert snapshot.candidate_count == 1
        candidate = snapshot.candidates[0]
        assert candidate.skill_anchor_ref.startswith("skill::")
        assert candidate.non_auto_execute is True
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "single-candidate-bounded", "result": "pass"},
            {"id": "skill-anchor-present", "result": "pass"},
            {"id": "non-auto-execute-enforced", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["procedure and tool invention stays candidate-only and anchored to the governed skill surface"],
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
            blocker_message="procedure tool invention verifier could not import its runtime modules or found missing files",
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
