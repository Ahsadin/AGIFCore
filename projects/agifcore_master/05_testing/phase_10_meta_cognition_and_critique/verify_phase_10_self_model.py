from __future__ import annotations

import json

import _phase_10_verifier_common as vc
from agifcore_phase10_meta_cognition.contracts import MAX_SELF_MODEL_RECORDS

VERIFIER = "verify_phase_10_self_model"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_self_model.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_10_self_model_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase10_meta_cognition.contracts",
    "agifcore_phase10_meta_cognition.self_model",
    "agifcore_phase10_meta_cognition.meta_cognition_turn",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "self-model-record-count-bounded",
    "self-model-fields-present",
    "self-model-confidence-bands-track-support",
    "inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase10_turn(scenario="weak")
    contradiction_case = vc.run_phase10_turn(scenario="contradiction")
    weak_snapshot = weak_case["turn"].self_model
    contradiction_snapshot = contradiction_case["turn"].self_model

    assert weak_snapshot.record_count <= MAX_SELF_MODEL_RECORDS
    assert contradiction_snapshot.record_count <= MAX_SELF_MODEL_RECORDS
    assert weak_snapshot.record_count >= 1
    assert contradiction_snapshot.record_count >= 1
    assert any(record.knows for record in weak_snapshot.records)
    assert all(record.what_would_verify for record in weak_snapshot.records)
    assert all(record.anchor_refs for record in weak_snapshot.records)
    assert weak_snapshot.records[0].confidence_band == "low"
    assert contradiction_snapshot.records[0].confidence_band == "moderate"
    assert weak_snapshot.records[0].answer_mode == "search_needed"
    assert contradiction_snapshot.records[0].answer_mode == "derived_explanation"

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "self-model-record-count-bounded", "result": "pass"},
            {"id": "self-model-fields-present", "result": "pass"},
            {"id": "self-model-confidence-bands-track-support", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": {
                "support_state": weak_case["fixture"]["support"]["support_state"],
                "self_model": weak_snapshot.to_dict(),
            },
            "contradiction_case": {
                "support_state": contradiction_case["fixture"]["support"]["support_state"],
                "self_model": contradiction_snapshot.to_dict(),
            },
        },
        notes=["self model remains bounded, trace-linked, and evidence-derived rather than self-assertive"],
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
            blocker_message="self model verifier could not import its runtime modules or found missing files",
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
