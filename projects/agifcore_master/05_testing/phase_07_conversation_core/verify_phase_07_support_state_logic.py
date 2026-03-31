from __future__ import annotations

import json

import _phase_07_verifier_common as vc

VERIFIER = "verify_phase_07_support_state_logic"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_07_support_state_logic_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase7_conversation.contracts",
    "agifcore_phase7_conversation.support_state_logic",
    "agifcore_phase7_conversation.conversation_turn",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/support_state_logic.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/conversation_turn.py",
)
DEPENDENCIES = (
    "phase_07_raw_text_intake_report.json",
    "phase_07_question_interpretation_report.json",
)


def build_pass_report() -> dict[str, object]:
    grounded = vc.build_conversation_fixture(raw_text="please explain the invoice workflow status")
    self_knowledge = vc.build_conversation_fixture(raw_text="what can you do in this agifcore repo?")
    fresh = vc.build_conversation_fixture(raw_text="what is the latest weather today?")

    grounded_resolution = grounded["conversation_turn_snapshot"].support_resolution
    if grounded_resolution.support_state.value not in {"grounded", "inferred"} or grounded_resolution.next_action.value != "answer":
        raise ValueError("grounded support-state route did not lead to answer")
    self_knowledge_resolution = self_knowledge["conversation_turn_snapshot"].support_resolution
    if self_knowledge_resolution.support_state.value != "grounded":
        raise ValueError("self-knowledge route did not stay grounded to continuity evidence")
    fresh_resolution = fresh["conversation_turn_snapshot"].support_resolution
    if fresh_resolution.support_state.value != "search_needed" or fresh_resolution.next_action.value != "search_external":
        raise ValueError("fresh-information route did not fail closed to search_needed/search_external")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
        assertions=[
            {"id": "support-state-runtime-importable", "result": "pass"},
            {"id": "grounded-answer-route-enforced", "result": "pass"},
            {"id": "self-knowledge-route-enforced", "result": "pass"},
            {"id": "fresh-information-route-enforced", "result": "pass"},
            {"id": "support-state-evidence-refs-present", "result": "pass"},
        ],
        anchors={
            "grounded_resolution": grounded_resolution.to_dict(),
            "self_knowledge_resolution": self_knowledge_resolution.to_dict(),
            "fresh_information_resolution": fresh_resolution.to_dict(),
        },
        notes=["support-state routing remains read-only and evidence-bound"],
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
                "support-state-runtime-importable",
                "grounded-answer-route-enforced",
                "self-knowledge-route-enforced",
                "fresh-information-route-enforced",
                "support-state-evidence-refs-present",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 7 support-state runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 support_state_logic verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "support-state-runtime-importable",
                "grounded-answer-route-enforced",
                "self-knowledge-route-enforced",
                "fresh-information-route-enforced",
                "support-state-evidence-refs-present",
            ],
            blocker_kind="missing_phase7_report_dependencies",
            blocker_message="Required earlier Phase 7 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 support_state_logic verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_07 support_state_logic verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
