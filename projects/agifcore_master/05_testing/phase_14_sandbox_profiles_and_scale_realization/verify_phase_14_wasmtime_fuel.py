from __future__ import annotations

import json

import _phase_14_verifier_common as vc

VERIFIER = "verify_phase_14_wasmtime_fuel"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_wasmtime_fuel.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_14_wasmtime_fuel_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase14_sandbox.wasmtime_fuel_limits",
    "agifcore_phase14_sandbox.sandbox_profile_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "fuel-class-count-bounded",
    "mobile-fuel-limit-trips",
    "fuel-reason-code-deterministic",
]


def build_pass_report() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    limits = shell.wasmtime_fuel_limits()
    fuel_receipt = shell.sandbox_execute(
        profile="mobile",
        function_name="spin",
        output_dir=vc.EVIDENCE_DIR,
    )
    assert limits["class_count"] <= 4
    assert fuel_receipt["status"] == "blocked"
    assert fuel_receipt["reason_code"] == "FUEL_LIMIT_EXCEEDED"
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "fuel-class-count-bounded", "result": "pass"},
            {"id": "mobile-fuel-limit-trips", "result": "pass"},
            {"id": "fuel-reason-code-deterministic", "result": "pass"},
        ],
        anchors={
            "fuel_limits": limits,
            "fuel_receipt": fuel_receipt,
        },
        notes=["fuel ceilings are explicit classed limits enforced by wasmtime"],
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
            blocker_message="fuel verifier could not import its runtime modules or found missing files",
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
