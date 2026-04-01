from __future__ import annotations

import json

import _phase_14_verifier_common as vc

VERIFIER = "verify_phase_14_profile_manifests"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_profile_manifests.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_14_profile_manifest_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase14_sandbox.profile_manifests",
    "agifcore_phase14_sandbox.sandbox_profile_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "exact-profile-count",
    "same-contract-hash-preserved",
    "no-correctness-privilege",
]


def build_pass_report() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    manifests = result["shell"].profile_manifests()
    profiles = list(manifests["profiles"])
    contract_hashes = {profile["same_contract_hash"] for profile in profiles}
    assert manifests["manifest_count"] == 3
    assert len(contract_hashes) == 1
    assert all(profile["correctness_privilege"] is False for profile in profiles)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "exact-profile-count", "result": "pass"},
            {"id": "same-contract-hash-preserved", "result": "pass"},
            {"id": "no-correctness-privilege", "result": "pass"},
        ],
        anchors={
            "profile_manifests": manifests,
        },
        notes=["mobile, laptop, and builder preserve the same public contract while differing only in explicit bounded budgets"],
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
            blocker_message="profile manifest verifier could not import its runtime modules or found missing files",
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
