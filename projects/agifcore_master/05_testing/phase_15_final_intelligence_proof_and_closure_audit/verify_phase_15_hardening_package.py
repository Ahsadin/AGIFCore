from __future__ import annotations

import json

import _phase_15_verifier_common as vc

VERIFIER = "verify_phase_15_hardening_package"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_hardening_package.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_15_hardening_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase15_proof.hardening_package",
    "agifcore_phase15_proof.proof_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "hardening-issue-family-count-bounded",
    "fail-closed-hardening-checks-pass",
    "phase16-publication-excluded",
    "upstream-evidence-manifests-present",
]


def build_pass_report() -> dict[str, object]:
    shells = vc.run_phase15_shells()
    weak_shell = shells["proof_shells"]["weak"]
    result = weak_shell.run_hardening(
        repo_root=vc.REPO_ROOT,
        phase15_output_root=vc.PHASE_OUTPUT_ROOT,
    )
    families = {item["issue_family_id"]: item for item in result["families"]}

    assert result["issue_family_count"] == 8
    assert result["status"] == "pass"
    assert families["tampered_bundle_fail_closed"]["observed"]["reason_code"] == "BUNDLE_INTEGRITY_REQUIRED"
    assert families["invalid_module_fail_closed"]["observed"]["reason_code"] == "INVALID_WASM_MODULE"
    assert families["profile_mismatch_fail_closed"]["observed"]["reason_code"] == "PROFILE_NOT_ALLOWED"
    assert families["fuel_limit_fail_closed"]["observed"]["reason_code"] == "FUEL_LIMIT_EXCEEDED"
    assert families["memory_limit_fail_closed"]["observed"]["reason_code"] == "MEMORY_LIMIT_EXCEEDED"
    assert families["wall_time_limit_fail_closed"]["observed"]["reason_code"] == "WALL_TIMEOUT_EXCEEDED"
    assert families["phase16_publication_excluded"]["observed"]["forbidden_keyword_hits"] == []
    assert families["upstream_phase_manifests_present"]["passed"] is True

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "hardening-issue-family-count-bounded", "result": "pass"},
            {"id": "fail-closed-hardening-checks-pass", "result": "pass"},
            {"id": "phase16-publication-excluded", "result": "pass"},
            {"id": "upstream-evidence-manifests-present", "result": "pass"},
        ],
        anchors={
            "hardening_package": result,
            "evidence_manifest": vc.evidence_manifest_anchor(),
        },
        notes=[
            "hardening stays internal and fail-closed",
            "Phase 15 does not leak Phase 16 publication or public-release behavior",
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
            blocker_message="hardening verifier could not import its runtime modules or found missing files",
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
