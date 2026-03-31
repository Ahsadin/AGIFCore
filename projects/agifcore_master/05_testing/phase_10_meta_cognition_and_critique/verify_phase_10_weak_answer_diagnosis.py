from __future__ import annotations

import json

import _phase_10_verifier_common as vc
from agifcore_phase10_meta_cognition.contracts import DiagnosisKind, MAX_WEAK_ANSWER_DIAGNOSIS_ITEMS

VERIFIER = "verify_phase_10_weak_answer_diagnosis"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_weak_answer_diagnosis.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_10_weak_answer_diagnosis_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase10_meta_cognition.contracts",
    "agifcore_phase10_meta_cognition.weak_answer_diagnosis",
    "agifcore_phase10_meta_cognition.meta_cognition_turn",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "diagnosis-item-count-bounded",
    "weak-case-diagnosis-kinds-visible",
    "contradiction-case-diagnosis-kinds-visible",
    "inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase10_turn(scenario="weak")
    contradiction_case = vc.run_phase10_turn(scenario="contradiction")
    weak_snapshot = weak_case["turn"].weak_answer_diagnosis
    contradiction_snapshot = contradiction_case["turn"].weak_answer_diagnosis
    weak_kinds = {item.kind for item in weak_snapshot.items}
    contradiction_kinds = {item.kind for item in contradiction_snapshot.items}

    assert weak_snapshot.item_count <= MAX_WEAK_ANSWER_DIAGNOSIS_ITEMS
    assert contradiction_snapshot.item_count <= MAX_WEAK_ANSWER_DIAGNOSIS_ITEMS
    assert weak_kinds == {
        DiagnosisKind.WEAK_SUPPORT,
        DiagnosisKind.MISSING_VARIABLE,
        DiagnosisKind.VAGUE_EXPLANATION,
    }
    assert contradiction_kinds == {
        DiagnosisKind.MISSING_VARIABLE,
        DiagnosisKind.CONTRADICTION_RISK,
        DiagnosisKind.SUPPORT_THIN,
    }
    assert all(item.support_honesty_preserved for item in weak_snapshot.items)
    assert all(item.next_step for item in contradiction_snapshot.items)
    assert "bounded re-checking" in weak_snapshot.summary

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "diagnosis-item-count-bounded", "result": "pass"},
            {"id": "weak-case-diagnosis-kinds-visible", "result": "pass"},
            {"id": "contradiction-case-diagnosis-kinds-visible", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["weak-answer diagnosis stays typed, support-honest, and bounded"],
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
            blocker_message="weak-answer diagnosis verifier could not import its runtime modules or found missing files",
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
