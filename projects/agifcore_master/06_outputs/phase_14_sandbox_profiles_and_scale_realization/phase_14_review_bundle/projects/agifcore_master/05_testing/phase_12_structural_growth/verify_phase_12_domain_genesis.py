from __future__ import annotations

import json

import _phase_12_verifier_common as vc

VERIFIER = "verify_phase_12_domain_genesis"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_domain_genesis.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_12_domain_genesis_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase12_structural_growth.domain_genesis",
    "agifcore_phase12_structural_growth.contracts",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "single-domain-candidate-bounded",
    "boundary-fields-present",
    "proof-domain-parent-stays-locked",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase12_cycle(scenario="contradiction")
    snapshot = contradiction_case["cycle"].domain_genesis
    assert snapshot.candidate_count == 1
    candidate = snapshot.candidates[0]
    assert candidate.boundary_statement
    assert candidate.rejection_path
    assert candidate.parent_domain_ref == "building_home_infrastructure_events"
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "single-domain-candidate-bounded", "result": "pass"},
            {"id": "boundary-fields-present", "result": "pass"},
            {"id": "proof-domain-parent-stays-locked", "result": "pass"},
        ],
        anchors={"contradiction_case": snapshot.to_dict()},
        notes=["domain genesis stays candidate-bound and tied to the locked proof-domain vocabulary"],
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
            blocker_message="domain genesis verifier could not import its runtime modules or found missing files",
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
