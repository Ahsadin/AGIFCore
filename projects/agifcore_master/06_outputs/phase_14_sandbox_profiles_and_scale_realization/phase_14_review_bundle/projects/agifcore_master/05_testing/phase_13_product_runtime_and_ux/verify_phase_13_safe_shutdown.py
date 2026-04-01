from __future__ import annotations

import json

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_safe_shutdown"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_safe_shutdown.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_safe_shutdown_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.safe_shutdown",
    "agifcore_phase13_product_runtime.product_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "shutdown-schema-correct",
    "flush-complete",
    "blocked-surfaces-listed-after-shutdown",
    "rollback-refs-linked",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase13_shell(scenario="weak")
    shutdown = weak_case["shell"].safe_shutdown()
    assert shutdown["schema"] == "agifcore.phase_13.safe_shutdown.v1"
    assert shutdown["shutdown_status"] == "safe_stopped"
    assert shutdown["flush_complete"] is True
    assert len(shutdown["blocked_surfaces_after_shutdown"]) == 8
    assert shutdown["rollback_refs"] == weak_case["phase11_cycle"]["overlay_contract"]["rollback_refs"]
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "shutdown-schema-correct", "result": "pass"},
            {"id": "flush-complete", "result": "pass"},
            {"id": "blocked-surfaces-listed-after-shutdown", "result": "pass"},
            {"id": "rollback-refs-linked", "result": "pass"},
        ],
        anchors={"safe_shutdown": shutdown},
        notes=["safe shutdown emits a receipt and preserves rollback anchors instead of hiding stop behavior"],
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
            blocker_message="safe shutdown verifier could not import its runtime modules or found missing files",
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
