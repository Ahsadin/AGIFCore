from __future__ import annotations

import json

import _phase_07_verifier_common as vc

VERIFIER = "verify_phase_07_raw_text_intake"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_07_raw_text_intake_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase7_conversation.contracts",
    "agifcore_phase7_conversation.raw_text_intake",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/raw_text_intake.py",
)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase7_conversation.raw_text_intake import RawTextIntakeEngine, RawTextIntakeError

    engine = RawTextIntakeEngine()
    record = engine.build_record(
        conversation_id="conv-intake",
        turn_id="turn-intake",
        raw_text="  Please explain the invoice workflow status?  ",
        active_context_refs=["phase7/test", "turn://conv-intake/turn-intake"],
    )
    if record.normalized_text != "Please explain the invoice workflow status?":
        raise RawTextIntakeError("normalized_text did not collapse whitespace as expected")
    if record.token_count < 5 or not record.ends_with_question:
        raise RawTextIntakeError("intake token counting or question detection failed")
    if engine.build_record(
        conversation_id="conv-code",
        turn_id="turn-code",
        raw_text="```python\nprint('x')\n``` what is this?",
    ).contains_code_block is not True:
        raise RawTextIntakeError("code block detection failed")
    try:
        engine.build_record(
            conversation_id="conv-long",
            turn_id="turn-long",
            raw_text="x" * 5000,
        )
        ceiling_enforced = False
    except RawTextIntakeError:
        ceiling_enforced = True
    if not ceiling_enforced:
        raise RawTextIntakeError("raw input ceiling was not enforced")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
        assertions=[
            {"id": "intake-runtime-importable", "result": "pass"},
            {"id": "whitespace-normalization-stable", "result": "pass"},
            {"id": "question-and-code-signals-preserved", "result": "pass"},
            {"id": "input-ceiling-enforced", "result": "pass"},
        ],
        anchors={
            "sample_intake": record.to_dict(),
            "context_ref_count": len(record.active_context_refs),
        },
        notes=["raw intake remains a read-only normalization step"],
    )
    vc.refresh_evidence_manifest()
    return report


def main() -> int:
    missing = vc.missing_files(list(vc.PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "intake-runtime-importable",
                "whitespace-normalization-stable",
                "question-and-code-signals-preserved",
                "input-ceiling-enforced",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 7 raw text intake runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_07 raw_text_intake verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_07 raw_text_intake verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
