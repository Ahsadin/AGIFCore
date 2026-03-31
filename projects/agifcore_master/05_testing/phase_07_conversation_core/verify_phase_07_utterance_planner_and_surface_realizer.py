from __future__ import annotations

import json

import _phase_07_verifier_common as vc

VERIFIER = "verify_phase_07_utterance_planner_and_surface_realizer"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_07_utterance_planner_and_surface_realizer_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase7_conversation.contracts",
    "agifcore_phase7_conversation.utterance_planner",
    "agifcore_phase7_conversation.surface_realizer",
    "agifcore_phase7_conversation.conversation_turn",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/utterance_planner.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/surface_realizer.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/conversation_turn.py",
)
DEPENDENCIES = (
    "phase_07_raw_text_intake_report.json",
    "phase_07_question_interpretation_report.json",
    "phase_07_support_state_logic_report.json",
    "phase_07_self_knowledge_surface_report.json",
    "phase_07_clarification_report.json",
)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase7_conversation.contracts import MAX_RESPONSE_CHARACTERS

    grounded = vc.build_conversation_fixture(raw_text="please explain the invoice workflow status")
    ambiguous = vc.build_conversation_fixture(raw_text="can you check that thing again?")
    self_knowledge = vc.build_conversation_fixture(raw_text="what can you do in this agifcore repo?")

    grounded_turn = grounded["conversation_turn_snapshot"]
    ambiguous_turn = ambiguous["conversation_turn_snapshot"]
    self_knowledge_turn = self_knowledge["conversation_turn_snapshot"]

    if grounded_turn.utterance_plan.discourse_mode.value not in {"status", "explain"}:
        raise ValueError("grounded utterance plan drifted outside the expected discourse modes")
    if grounded_turn.response_surface.response_text != grounded_turn.guardrail_result.output_text:
        raise ValueError("final grounded response no longer matches the guardrail-approved output")
    if len(grounded_turn.response_surface.response_text) > MAX_RESPONSE_CHARACTERS:
        raise ValueError("grounded response exceeded the Phase 7 response ceiling")
    if ambiguous_turn.utterance_plan.discourse_mode.value != "clarify":
        raise ValueError("ambiguous utterance plan did not stay on the clarify path")
    if ambiguous_turn.response_surface.final_answer_mode.value != "clarify":
        raise ValueError("ambiguous response did not preserve the clarify answer mode")
    if self_knowledge_turn.utterance_plan.discourse_mode.value != "self_knowledge":
        raise ValueError("self-knowledge utterance plan did not stay on the self-knowledge path")
    if "live external search" not in self_knowledge_turn.response_surface.response_text.lower():
        raise ValueError("self-knowledge response did not preserve the bounded local limit")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS)
        + list(RUNTIME_FILES)
        + [vc.rel(vc.EVIDENCE_DIR / item) for item in DEPENDENCIES],
        assertions=[
            {"id": "utterance-planner-runtime-importable", "result": "pass"},
            {"id": "surface-realizer-runtime-importable", "result": "pass"},
            {"id": "clarify-plan-remains-separate", "result": "pass"},
            {"id": "self-knowledge-plan-remains-separate", "result": "pass"},
            {"id": "response-text-stays-bounded", "result": "pass"},
            {"id": "final-surface-matches-guardrail-output", "result": "pass"},
        ],
        anchors={
            "grounded_plan": grounded_turn.utterance_plan.to_dict(),
            "grounded_response": grounded_turn.response_surface.to_dict(),
            "clarification_plan": ambiguous_turn.utterance_plan.to_dict(),
            "clarification_response": ambiguous_turn.response_surface.to_dict(),
            "self_knowledge_plan": self_knowledge_turn.utterance_plan.to_dict(),
            "self_knowledge_response": self_knowledge_turn.response_surface.to_dict(),
        },
        notes=["utterance planning remains structural and surface realization remains bounded"],
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
                "utterance-planner-runtime-importable",
                "surface-realizer-runtime-importable",
                "clarify-plan-remains-separate",
                "self-knowledge-plan-remains-separate",
                "response-text-stays-bounded",
                "final-surface-matches-guardrail-output",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 7 utterance planner or surface realizer runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 utterance_planner_and_surface_realizer verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "utterance-planner-runtime-importable",
                "surface-realizer-runtime-importable",
                "clarify-plan-remains-separate",
                "self-knowledge-plan-remains-separate",
                "response-text-stays-bounded",
                "final-surface-matches-guardrail-output",
            ],
            blocker_kind="missing_phase7_report_dependencies",
            blocker_message="Required earlier Phase 7 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 utterance_planner_and_surface_realizer verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_07 utterance_planner_and_surface_realizer verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
