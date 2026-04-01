from __future__ import annotations

import json

import _phase_14_verifier_common as vc

VERIFIER = "verify_phase_14_sandbox"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_sandbox.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_14_sandbox_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase14_sandbox.sandbox_policy",
    "agifcore_phase14_sandbox.sandbox_profile_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "policy-catalog-bounded",
    "valid-packaged-execution-passes",
    "tampered-package-fail-closed",
    "profile-mismatch-fail-closed",
]


def build_pass_report() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    policies = shell.sandbox_policies()
    allowed_receipt = shell.sandbox_execute(
        profile="laptop",
        function_name="add",
        function_args=[1, 2],
        output_dir=vc.EVIDENCE_DIR,
    )
    tampered_receipt = shell.sandbox_execute(
        profile="laptop",
        function_name="add",
        function_args=[1, 2],
        output_dir=vc.EVIDENCE_DIR,
        variant="tampered",
    )
    mismatch_receipt = shell.sandbox_execute(
        profile="mobile",
        function_name="add",
        function_args=[1, 2],
        output_dir=vc.EVIDENCE_DIR,
        allowed_profiles=("laptop",),
    )
    assert policies["policy_count"] <= 12
    assert allowed_receipt["status"] == "pass"
    assert allowed_receipt["stdout"] == "3"
    assert tampered_receipt["status"] == "blocked"
    assert tampered_receipt["reason_code"] == "BUNDLE_INTEGRITY_REQUIRED"
    assert mismatch_receipt["status"] == "blocked"
    assert mismatch_receipt["reason_code"] == "PROFILE_NOT_ALLOWED"
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "policy-catalog-bounded", "result": "pass"},
            {"id": "valid-packaged-execution-passes", "result": "pass"},
            {"id": "tampered-package-fail-closed", "result": "pass"},
            {"id": "profile-mismatch-fail-closed", "result": "pass"},
        ],
        anchors={
            "shell_snapshot": shell.shell_snapshot(),
            "policy_catalog": policies,
            "allowed_receipt": allowed_receipt,
            "tampered_receipt": tampered_receipt,
            "profile_mismatch_receipt": mismatch_receipt,
        },
        notes=["sandbox execution uses a dedicated local wasmtime subprocess when available"],
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
            blocker_message="sandbox verifier could not import its runtime modules or found missing files",
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
