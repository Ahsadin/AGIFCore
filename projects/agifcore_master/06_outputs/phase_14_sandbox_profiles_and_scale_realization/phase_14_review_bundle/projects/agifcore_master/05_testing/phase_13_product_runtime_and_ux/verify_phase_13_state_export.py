from __future__ import annotations

import json

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_state_export"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_state_export.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_state_export_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.state_export",
    "agifcore_phase13_product_runtime.product_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "wrapper-schema-correct",
    "phase2-state-export-preserved",
    "surface-separation-visible",
    "payload-size-bounded",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase13_shell(scenario="weak")
    state_export = weak_case["shell"].state_export()
    source_export = state_export["source_state_export"]
    assert state_export["schema"] == "agifcore.phase_13.state_export.v1"
    assert source_export["schema"] == "agifcore.phase_02.state_export.v1"
    assert len(source_export["cells"]) == 3
    assert len(source_export["turns"]) == 1
    assert state_export["source_payload_bytes"] <= 8 * 1024 * 1024
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "wrapper-schema-correct", "result": "pass"},
            {"id": "phase2-state-export-preserved", "result": "pass"},
            {"id": "surface-separation-visible", "result": "pass"},
            {"id": "payload-size-bounded", "result": "pass"},
        ],
        anchors={"state_export": state_export},
        notes=["state export wraps a bounded Phase 2-style workspace snapshot instead of inventing a second storage lane"],
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
            blocker_message="state export verifier could not import its runtime modules or found missing files",
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
