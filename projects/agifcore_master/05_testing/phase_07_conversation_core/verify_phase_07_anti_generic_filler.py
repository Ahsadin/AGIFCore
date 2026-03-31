from __future__ import annotations

import json

import _phase_07_verifier_common as vc

VERIFIER = "verify_phase_07_anti_generic_filler"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_07_anti_generic_filler_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase7_conversation.contracts",
    "agifcore_phase7_conversation.anti_generic_filler",
    "agifcore_phase7_conversation.conversation_turn",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/anti_generic_filler.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/conversation_turn.py",
)
DEPENDENCIES = (
    "phase_07_raw_text_intake_report.json",
    "phase_07_question_interpretation_report.json",
    "phase_07_support_state_logic_report.json",
    "phase_07_self_knowledge_surface_report.json",
    "phase_07_clarification_report.json",
    "phase_07_utterance_planner_and_surface_realizer_report.json",
)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase7_conversation.anti_generic_filler import AntiGenericFillerEngine
    from agifcore_phase7_conversation.contracts import FinalAnswerMode, GuardrailStatus, RealizationDraft, stable_hash_payload

    grounded = vc.build_conversation_fixture(raw_text="please explain the invoice workflow status")
    self_knowledge = vc.build_conversation_fixture(raw_text="what can you do in this agifcore repo?")
    search_needed = vc.build_conversation_fixture(raw_text="what is the latest weather today?")

    if grounded["conversation_turn_snapshot"].guardrail_result.status.value != "pass":
        raise ValueError("normal grounded answer should pass the anti-filler guardrails")

    engine = AntiGenericFillerEngine()
    search_fallback = engine.enforce(
        question_interpretation_state=search_needed["conversation_turn_snapshot"].interpretation.to_dict(),
        support_state_resolution_state=search_needed["conversation_turn_snapshot"].support_resolution.to_dict(),
        self_knowledge_state=search_needed["conversation_turn_snapshot"].self_knowledge.to_dict(),
        clarification_state=search_needed["conversation_turn_snapshot"].clarification.to_dict(),
        realization_draft=RealizationDraft(
            draft_id="draft::search-fallback",
            response_text="In general, it depends.",
            final_answer_mode=FinalAnswerMode.SEARCH_NEEDED,
            cited_evidence_refs=(),
            draft_hash=stable_hash_payload({"draft_id": "draft::search-fallback"}),
        ),
    )
    if search_fallback.status != GuardrailStatus.FALLBACK_APPLIED:
        raise ValueError("generic search-needed draft did not trigger a fallback")
    if "search_external" not in search_fallback.output_text:
        raise ValueError("search-needed fallback did not preserve the honest next action")

    self_fallback = engine.enforce(
        question_interpretation_state=self_knowledge["conversation_turn_snapshot"].interpretation.to_dict(),
        support_state_resolution_state=self_knowledge["conversation_turn_snapshot"].support_resolution.to_dict(),
        self_knowledge_state=self_knowledge["conversation_turn_snapshot"].self_knowledge.to_dict(),
        clarification_state=self_knowledge["conversation_turn_snapshot"].clarification.to_dict(),
        realization_draft=RealizationDraft(
            draft_id="draft::self-fallback",
            response_text="I feel ready to help with that.",
            final_answer_mode=FinalAnswerMode.GROUNDED_FACT,
            cited_evidence_refs=(),
            draft_hash=stable_hash_payload({"draft_id": "draft::self-fallback"}),
        ),
    )
    if self_fallback.status != GuardrailStatus.FALLBACK_APPLIED:
        raise ValueError("unsupported self-knowledge draft did not trigger a fallback")
    if "From this local AGIFCore state:" not in self_fallback.output_text:
        raise ValueError("self-knowledge fallback did not return to continuity-backed language")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS)
        + list(RUNTIME_FILES)
        + [vc.rel(vc.EVIDENCE_DIR / item) for item in DEPENDENCIES],
        assertions=[
            {"id": "anti-filler-runtime-importable", "result": "pass"},
            {"id": "normal-grounded-output-passes", "result": "pass"},
            {"id": "generic-search-needed-output-falls-back", "result": "pass"},
            {"id": "unsupported-self-knowledge-output-falls-back", "result": "pass"},
            {"id": "guardrail-results-remain-machine-checkable", "result": "pass"},
        ],
        anchors={
            "grounded_guardrail_result": grounded["conversation_turn_snapshot"].guardrail_result.to_dict(),
            "search_fallback_result": search_fallback.to_dict(),
            "self_knowledge_fallback_result": self_fallback.to_dict(),
        },
        notes=["anti-generic filler guardrails remain active constraints, not style advice"],
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
                "anti-filler-runtime-importable",
                "normal-grounded-output-passes",
                "generic-search-needed-output-falls-back",
                "unsupported-self-knowledge-output-falls-back",
                "guardrail-results-remain-machine-checkable",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 7 anti-generic filler runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 anti_generic_filler verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "anti-filler-runtime-importable",
                "normal-grounded-output-passes",
                "generic-search-needed-output-falls-back",
                "unsupported-self-knowledge-output-falls-back",
                "guardrail-results-remain-machine-checkable",
            ],
            blocker_kind="missing_phase7_report_dependencies",
            blocker_message="Required earlier Phase 7 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 anti_generic_filler verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_07 anti_generic_filler verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
