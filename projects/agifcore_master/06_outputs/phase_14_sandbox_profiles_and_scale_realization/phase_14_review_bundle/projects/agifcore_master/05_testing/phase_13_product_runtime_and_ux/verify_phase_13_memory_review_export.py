from __future__ import annotations

import json

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_memory_review_export"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_memory_review_export.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_memory_review_export_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.memory_review_export",
    "agifcore_phase13_product_runtime.product_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "wrapper-schema-correct",
    "phase2-memory-review-shape-preserved",
    "memory-review-refs-present",
    "continuity-refs-visible",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase13_shell(scenario="weak")
    memory_export = weak_case["shell"].memory_review_export()
    source_export = memory_export["source_memory_review_export"]
    assert memory_export["schema"] == "agifcore.phase_13.memory_review_export.v1"
    assert source_export["schema"] == "agifcore.phase_02.memory_review_export.v1"
    assert source_export["memory_review_refs"]
    assert memory_export["continuity_refs"]
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "wrapper-schema-correct", "result": "pass"},
            {"id": "phase2-memory-review-shape-preserved", "result": "pass"},
            {"id": "memory-review-refs-present", "result": "pass"},
            {"id": "continuity-refs-visible", "result": "pass"},
        ],
        anchors={"memory_review_export": memory_export},
        notes=["memory review export stays reference-only and preserves continuity anchors"],
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
            blocker_message="memory review export verifier could not import its runtime modules or found missing files",
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
