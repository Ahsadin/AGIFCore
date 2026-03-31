from __future__ import annotations

import json

import _phase_07_verifier_common as vc

VERIFIER = "verify_phase_07_answer_contract"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_07_answer_contract_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase7_conversation.contracts",
    "agifcore_phase7_conversation.answer_contract",
    "agifcore_phase7_conversation.conversation_turn",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/answer_contract.py",
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
    from agifcore_phase7_conversation.contracts import MAX_CONTRACT_FIELDS

    grounded = vc.build_conversation_fixture(raw_text="please explain the invoice workflow status")
    search_needed = vc.build_conversation_fixture(raw_text="what is the latest weather today?")

    grounded_turn = grounded["conversation_turn_snapshot"]
    search_turn = search_needed["conversation_turn_snapshot"]
    grounded_contract = grounded_turn.answer_contract
    search_contract = search_turn.answer_contract

    if grounded_contract.response_text != grounded_turn.response_surface.response_text:
        raise ValueError("grounded answer contract response text drifted away from the final surface")
    if grounded_contract.support_state.value != grounded_turn.support_resolution.support_state.value:
        raise ValueError("grounded answer contract support_state drifted away from support resolution")
    if grounded_contract.next_action.value != grounded_turn.support_resolution.next_action.value:
        raise ValueError("grounded answer contract next_action drifted away from support resolution")
    if grounded_contract.discourse_mode.value != grounded_turn.utterance_plan.discourse_mode.value:
        raise ValueError("grounded answer contract discourse_mode drifted away from utterance planning")
    if grounded_contract.memory_review_ref not in grounded_contract.evidence_refs:
        raise ValueError("grounded answer contract dropped the memory review reference")
    if len(grounded_contract.to_dict()) > MAX_CONTRACT_FIELDS:
        raise ValueError("grounded answer contract exceeded the top-level field ceiling")
    if search_contract.abstain_or_answer != "abstain":
        raise ValueError("search-needed answer contract did not stay on the abstain path")
    if search_contract.next_action.value != "search_external":
        raise ValueError("search-needed answer contract did not preserve the search_external next action")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS)
        + list(RUNTIME_FILES)
        + [vc.rel(vc.EVIDENCE_DIR / item) for item in DEPENDENCIES],
        assertions=[
            {"id": "answer-contract-runtime-importable", "result": "pass"},
            {"id": "machine-checkable-envelope-present", "result": "pass"},
            {"id": "response-to-contract-alignment-enforced", "result": "pass"},
            {"id": "support-routing-alignment-enforced", "result": "pass"},
            {"id": "contract-field-ceiling-enforced", "result": "pass"},
            {"id": "search-needed-contract-honesty-preserved", "result": "pass"},
        ],
        anchors={
            "grounded_answer_contract": grounded_contract.to_dict(),
            "search_needed_answer_contract": search_contract.to_dict(),
        },
        notes=["answer contract remains machine-checkable and aligned to the final surface"],
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
                "answer-contract-runtime-importable",
                "machine-checkable-envelope-present",
                "response-to-contract-alignment-enforced",
                "support-routing-alignment-enforced",
                "contract-field-ceiling-enforced",
                "search-needed-contract-honesty-preserved",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 7 answer contract runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 answer_contract verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "answer-contract-runtime-importable",
                "machine-checkable-envelope-present",
                "response-to-contract-alignment-enforced",
                "support-routing-alignment-enforced",
                "contract-field-ceiling-enforced",
                "search-needed-contract-honesty-preserved",
            ],
            blocker_kind="missing_phase7_report_dependencies",
            blocker_message="Required earlier Phase 7 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 answer_contract verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_07 answer_contract verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
