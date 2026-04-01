from __future__ import annotations

import json

import _phase_14_verifier_common as vc

VERIFIER = "verify_phase_14_wasmtime_memory"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_wasmtime_memory.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_14_wasmtime_memory_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase14_sandbox.wasmtime_memory_limits",
    "agifcore_phase14_sandbox.sandbox_profile_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "memory-class-count-bounded",
    "memory-limit-trips",
    "grow-failure-traps",
]


def build_pass_report() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    limits = shell.wasmtime_memory_limits()
    memory_receipt = shell.sandbox_execute(
        profile="mobile",
        policy_id="strict_fail_closed_policy",
        function_name="grow_to_pages",
        function_args=[600],
        output_dir=vc.EVIDENCE_DIR,
    )
    assert limits["class_count"] <= 4
    assert memory_receipt["status"] == "blocked"
    assert memory_receipt["reason_code"] == "MEMORY_LIMIT_EXCEEDED"
    assert memory_receipt["exit_code"] == 1
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "memory-class-count-bounded", "result": "pass"},
            {"id": "memory-limit-trips", "result": "pass"},
            {"id": "grow-failure-traps", "result": "pass"},
        ],
        anchors={
            "memory_limits": limits,
            "memory_receipt": memory_receipt,
        },
        notes=["memory.grow failures are trapped explicitly instead of being ignored"],
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
            blocker_message="memory verifier could not import its runtime modules or found missing files",
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
