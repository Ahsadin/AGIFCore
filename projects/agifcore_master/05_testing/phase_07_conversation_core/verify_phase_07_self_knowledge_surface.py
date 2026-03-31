from __future__ import annotations

import json

import _phase_07_verifier_common as vc

VERIFIER = "verify_phase_07_self_knowledge_surface"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_07_self_knowledge_surface_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase7_conversation.contracts",
    "agifcore_phase7_conversation.self_knowledge_surface",
    "agifcore_phase7_conversation.conversation_turn",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/self_knowledge_surface.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/conversation_turn.py",
)
DEPENDENCIES = (
    "phase_07_raw_text_intake_report.json",
    "phase_07_question_interpretation_report.json",
    "phase_07_support_state_logic_report.json",
)


def build_pass_report() -> dict[str, object]:
    fixture = vc.build_conversation_fixture(raw_text="what can you do in this agifcore repo?")
    snapshot = fixture["conversation_turn_snapshot"].self_knowledge
    if snapshot.statement_count < 2:
        raise ValueError("self-knowledge surface did not emit enough bounded statements")
    if not all(statement.anchor_refs for statement in snapshot.statements):
        raise ValueError("self-knowledge statements are missing anchor refs")
    if any("feel" in statement.statement.lower() for statement in snapshot.statements):
        raise ValueError("self-knowledge drifted into unsupported self-assertion")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
        assertions=[
            {"id": "self-knowledge-runtime-importable", "result": "pass"},
            {"id": "continuity-anchors-required", "result": "pass"},
            {"id": "unsupported-self-assertion-blocked", "result": "pass"},
        ],
        anchors={"self_knowledge_snapshot": snapshot.to_dict()},
        notes=["self-knowledge remains continuity-backed and local-only"],
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
                "self-knowledge-runtime-importable",
                "continuity-anchors-required",
                "unsupported-self-assertion-blocked",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 7 self-knowledge surface runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 self_knowledge_surface verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "self-knowledge-runtime-importable",
                "continuity-anchors-required",
                "unsupported-self-assertion-blocked",
            ],
            blocker_kind="missing_phase7_report_dependencies",
            blocker_message="Required earlier Phase 7 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 self_knowledge_surface verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_07 self_knowledge_surface verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
