from __future__ import annotations

import json

import _phase_15_verifier_common as vc

VERIFIER = "verify_phase_15_soak_harness"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_soak_harness.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_15_soak_summary.json"
RUNTIME_IMPORTS = (
    "agifcore_phase15_proof.soak_harness",
    "agifcore_phase15_proof.proof_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "soak-duration-classes-bounded",
    "soak-total-iterations-match-contract",
    "soak-runs-pass",
]


def build_pass_report() -> dict[str, object]:
    from agifcore_phase15_proof.soak_harness import run_soak_harness

    shells = vc.run_phase15_shells()
    weak_shell = shells["proof_shells"]["weak"]
    contract = weak_shell.soak_contract()
    result = run_soak_harness(proof_shells=shells["proof_shells"])

    assert contract["duration_class_count"] == 3
    assert result["duration_class_count"] == 3
    assert result["total_iterations"] == 18
    assert result["total_failures"] == 0
    assert result["status"] == "pass"

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "soak-duration-classes-bounded", "result": "pass"},
            {"id": "soak-total-iterations-match-contract", "result": "pass"},
            {"id": "soak-runs-pass", "result": "pass"},
        ],
        anchors={
            "soak_contract": contract,
            "soak_result": result,
            "evidence_manifest": vc.evidence_manifest_anchor(),
        },
        notes=[
            "the soak harness stays bounded to local duration classes only",
            "soak checks reuse the approved runtime, manifest audit, and sandbox paths instead of inventing a separate correctness path",
        ],
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
            blocker_message="soak verifier could not import its runtime modules or found missing files",
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
