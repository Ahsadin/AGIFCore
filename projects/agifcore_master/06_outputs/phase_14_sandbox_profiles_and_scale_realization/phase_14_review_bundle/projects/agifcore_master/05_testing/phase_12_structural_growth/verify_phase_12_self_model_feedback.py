from __future__ import annotations

import json

import _phase_12_verifier_common as vc
from agifcore_phase12_structural_growth.contracts import MAX_SELF_MODEL_FEEDBACK_ITEMS

VERIFIER = "verify_phase_12_self_model_feedback"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_self_model_feedback.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_12_self_model_feedback_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase12_structural_growth.self_model_feedback",
    "agifcore_phase12_structural_growth.contracts",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "item-count-stays-bounded",
    "lanes-are-typed",
    "supporting-refs-present",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase12_cycle(scenario="weak")
    contradiction_case = vc.run_phase12_cycle(scenario="contradiction")
    weak_snapshot = weak_case["cycle"].self_model_feedback
    contradiction_snapshot = contradiction_case["cycle"].self_model_feedback
    assert 1 <= weak_snapshot.item_count <= MAX_SELF_MODEL_FEEDBACK_ITEMS
    assert 1 <= contradiction_snapshot.item_count <= MAX_SELF_MODEL_FEEDBACK_ITEMS
    assert all(item.recommended_lane for item in weak_snapshot.items)
    assert all(item.supporting_refs for item in contradiction_snapshot.items)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "item-count-stays-bounded", "result": "pass"},
            {"id": "lanes-are-typed", "result": "pass"},
            {"id": "supporting-refs-present", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["self-model feedback stays typed and bounded before any structural candidate runs"],
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
            blocker_message="self model feedback verifier could not import its runtime modules or found missing files",
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
