from __future__ import annotations

import json

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_fail_closed_ux"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_fail_closed_ux.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_fail_closed_ux_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.fail_closed_ux",
    "agifcore_phase13_product_runtime.product_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "catalog-schema-correct",
    "state-count-bounded",
    "reserved-surface-states-present",
    "transfer-execution-disabled",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase13_shell(scenario="contradiction")
    catalog = contradiction_case["shell"].fail_closed_catalog()
    states = catalog["states"]
    task_state = next(item for item in states if item["surface_name"] == "task_submit")
    policy_state = next(item for item in states if item["surface_name"] == "policy_update")
    assert catalog["schema"] == "agifcore.phase_13.fail_closed_ux_catalog.v1"
    assert catalog["state_count"] <= 10
    assert task_state["reason_code"] == "reserved_surface_fail_closed"
    assert policy_state["reason_code"] == "reserved_surface_fail_closed"
    assert all(item["transfer_execution_enabled"] is False for item in states)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "catalog-schema-correct", "result": "pass"},
            {"id": "state-count-bounded", "result": "pass"},
            {"id": "reserved-surface-states-present", "result": "pass"},
            {"id": "transfer-execution-disabled", "result": "pass"},
        ],
        anchors={"fail_closed_catalog": catalog},
        notes=["fail-closed UX stays explicit, deterministic, and non-upgrading"],
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
            blocker_message="fail-closed UX verifier could not import its runtime modules or found missing files",
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
