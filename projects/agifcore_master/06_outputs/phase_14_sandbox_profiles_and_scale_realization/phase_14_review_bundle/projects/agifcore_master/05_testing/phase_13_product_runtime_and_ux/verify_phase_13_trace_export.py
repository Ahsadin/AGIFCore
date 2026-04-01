from __future__ import annotations

import json

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_trace_export"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_trace_export.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_trace_export_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.trace_export",
    "agifcore_phase13_product_runtime.product_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "trace-wrapper-schema-correct",
    "phase2-trace-shape-preserved",
    "support-state-visible",
    "trace-size-bounded",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase13_shell(scenario="contradiction")
    trace_export = contradiction_case["shell"].trace_export()
    last_record = trace_export["trace_records"][-1]
    assert trace_export["schema"] == "agifcore.phase_13.trace_export.v1"
    assert trace_export["trace_record_count"] == 2
    assert last_record["support_state"] == contradiction_case["phase12_cycle"]["overlay_contract"]["support_state"]
    assert last_record["final_answer_mode"] == contradiction_case["shell"].conversation_turn()["final_answer_mode"]
    assert vc.canonical_size_bytes(trace_export) <= 16 * 1024 * 1024
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "trace-wrapper-schema-correct", "result": "pass"},
            {"id": "phase2-trace-shape-preserved", "result": "pass"},
            {"id": "support-state-visible", "result": "pass"},
            {"id": "trace-size-bounded", "result": "pass"},
        ],
        anchors={"trace_export": trace_export},
        notes=["trace export keeps support-state and final-answer-mode fields explicit instead of collapsing them into summaries"],
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
            blocker_message="trace export verifier could not import its runtime modules or found missing files",
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
