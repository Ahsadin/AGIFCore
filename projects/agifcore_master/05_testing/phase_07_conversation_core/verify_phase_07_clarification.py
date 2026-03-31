from __future__ import annotations

import json

import _phase_07_verifier_common as vc

VERIFIER = "verify_phase_07_clarification"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_07_clarification_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase7_conversation.contracts",
    "agifcore_phase7_conversation.clarification",
    "agifcore_phase7_conversation.conversation_turn",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/clarification.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/conversation_turn.py",
)
DEPENDENCIES = (
    "phase_07_raw_text_intake_report.json",
    "phase_07_question_interpretation_report.json",
    "phase_07_support_state_logic_report.json",
)


def build_pass_report() -> dict[str, object]:
    fixture = vc.build_conversation_fixture(raw_text="can you check that thing again?")
    clarification = fixture["conversation_turn_snapshot"].clarification
    response_surface = fixture["conversation_turn_snapshot"].response_surface
    support_resolution = fixture["conversation_turn_snapshot"].support_resolution
    if clarification.question_count != 1:
        raise ValueError("clarification route did not emit exactly one bounded clarification question")
    question = clarification.questions[0]
    if "?" not in question.question_text or "which local workflow" not in question.question_text.lower():
        raise ValueError("clarification question drifted away from specific missing-variable wording")
    if support_resolution.next_action.value != "clarify":
        raise ValueError("support-state did not preserve the clarify route")
    if response_surface.final_answer_mode.value != "clarify":
        raise ValueError("surface realization did not preserve the clarify answer mode")
    if "target_domain" not in question.missing_variables and "referent" not in question.missing_variables:
        raise ValueError("clarification output did not preserve the missing variable set")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS)
        + list(RUNTIME_FILES)
        + [vc.rel(vc.EVIDENCE_DIR / item) for item in DEPENDENCIES],
        assertions=[
            {"id": "clarification-runtime-importable", "result": "pass"},
            {"id": "clarification-route-enforced", "result": "pass"},
            {"id": "single-specific-question-enforced", "result": "pass"},
            {"id": "missing-variable-capture-enforced", "result": "pass"},
        ],
        anchors={
            "clarification_request": clarification.to_dict(),
            "support_resolution": support_resolution.to_dict(),
            "response_surface": response_surface.to_dict(),
        },
        notes=["clarification stays bounded, specific, and distinct from abstain or answer"],
    )
    vc.refresh_evidence_manifest()
    return report


def main() -> int:
    missing = vc.missing_files(list(vc.PLAN_REFS) + list(RUNTIME_FILES))
    dependency_failures = vc.report_dependency_failures(DEPENDENCIES)
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "clarification-runtime-importable",
                "clarification-route-enforced",
                "single-specific-question-enforced",
                "missing-variable-capture-enforced",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 7 clarification runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 clarification verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "clarification-runtime-importable",
                "clarification-route-enforced",
                "single-specific-question-enforced",
                "missing-variable-capture-enforced",
            ],
            blocker_kind="missing_phase7_report_dependencies",
            blocker_message="Required earlier Phase 7 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 clarification verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_07 clarification verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
