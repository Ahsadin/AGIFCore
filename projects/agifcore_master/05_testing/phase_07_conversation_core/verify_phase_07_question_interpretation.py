from __future__ import annotations

import json

import _phase_07_verifier_common as vc

VERIFIER = "verify_phase_07_question_interpretation"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_07_question_interpretation_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase7_conversation.contracts",
    "agifcore_phase7_conversation.raw_text_intake",
    "agifcore_phase7_conversation.question_interpretation",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/raw_text_intake.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/question_interpretation.py",
)
DEPENDENCIES = ("phase_07_raw_text_intake_report.json",)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase7_conversation.question_interpretation import QuestionInterpretationEngine, QuestionInterpretationError
    from agifcore_phase7_conversation.raw_text_intake import RawTextIntakeEngine

    intake_engine = RawTextIntakeEngine()
    engine = QuestionInterpretationEngine()
    messy = engine.build_snapshot(
        intake_record=intake_engine.build_record(
            conversation_id="conv-qi",
            turn_id="turn-qi-1",
            raw_text="pls explain invoice workflow status again??",
        )
    )
    if messy.target_domain_hint != "finance_document_workflows":
        raise QuestionInterpretationError("target domain hint was not inferred for invoice workflow question")
    if messy.user_intent not in {"status_question", "explanation_question"}:
        raise QuestionInterpretationError("question intent classification drifted outside the bounded Phase 7 surface")

    self_knowledge = engine.build_snapshot(
        intake_record=intake_engine.build_record(
            conversation_id="conv-qi",
            turn_id="turn-qi-2",
            raw_text="what can you do in this agifcore repo?",
        )
    )
    if not self_knowledge.self_knowledge_requested:
        raise QuestionInterpretationError("self-knowledge route was not detected")

    live_current = engine.build_snapshot(
        intake_record=intake_engine.build_record(
            conversation_id="conv-qi",
            turn_id="turn-qi-3",
            raw_text="what is the latest weather today?",
        )
    )
    if not live_current.live_current_requested:
        raise QuestionInterpretationError("live-current route was not detected")

    ambiguous = engine.build_snapshot(
        intake_record=intake_engine.build_record(
            conversation_id="conv-qi",
            turn_id="turn-qi-4",
            raw_text="can you check that thing again?",
        )
    )
    if not ambiguous.ambiguous_request:
        raise QuestionInterpretationError("ambiguous request was not detected")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES) + [vc.rel(vc.EVIDENCE_DIR / DEPENDENCIES[0])],
        assertions=[
            {"id": "question-interpretation-runtime-importable", "result": "pass"},
            {"id": "target-domain-cues-detected", "result": "pass"},
            {"id": "self-knowledge-cues-detected", "result": "pass"},
            {"id": "live-current-cues-detected", "result": "pass"},
            {"id": "ambiguous-request-cues-detected", "result": "pass"},
        ],
        anchors={
            "messy_question": messy.to_dict(),
            "self_knowledge_question": self_knowledge.to_dict(),
            "live_current_question": live_current.to_dict(),
            "ambiguous_question": ambiguous.to_dict(),
        },
        notes=["question interpretation stays separate from support-state routing"],
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
                "question-interpretation-runtime-importable",
                "target-domain-cues-detected",
                "self-knowledge-cues-detected",
                "live-current-cues-detected",
                "ambiguous-request-cues-detected",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 7 question interpretation runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 question_interpretation verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "question-interpretation-runtime-importable",
                "target-domain-cues-detected",
                "self-knowledge-cues-detected",
                "live-current-cues-detected",
                "ambiguous-request-cues-detected",
            ],
            blocker_kind="missing_phase7_report_dependencies",
            blocker_message="Required earlier Phase 7 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 question_interpretation verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_07 question_interpretation verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
