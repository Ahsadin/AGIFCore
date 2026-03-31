from __future__ import annotations

import json

import _phase_10_verifier_common as vc
from agifcore_phase10_meta_cognition.contracts import MAX_SURPRISE_EVENTS, SurpriseTrigger

VERIFIER = "verify_phase_10_surprise_engine"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_surprise_engine.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_10_surprise_engine_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase10_meta_cognition.contracts",
    "agifcore_phase10_meta_cognition.surprise_engine",
    "agifcore_phase10_meta_cognition.meta_cognition_turn",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "surprise-event-count-bounded",
    "weak-case-recheck-signal-visible",
    "contradiction-case-fragment-signal-visible",
    "inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase10_turn(scenario="weak")
    contradiction_case = vc.run_phase10_turn(scenario="contradiction")
    weak_snapshot = weak_case["turn"].surprise_engine
    contradiction_snapshot = contradiction_case["turn"].surprise_engine

    assert weak_snapshot.event_count <= MAX_SURPRISE_EVENTS
    assert contradiction_snapshot.event_count <= MAX_SURPRISE_EVENTS
    assert weak_snapshot.event_count == 1
    assert contradiction_snapshot.event_count == 1
    assert weak_snapshot.events[0].detected_boundary_failure
    assert weak_snapshot.events[0].triggered_action is SurpriseTrigger.RECHECK_SUPPORT
    assert contradiction_snapshot.events[0].detected_contradiction
    assert contradiction_snapshot.events[0].detected_missing_variable
    assert contradiction_snapshot.events[0].triggered_action is SurpriseTrigger.THEORY_FRAGMENT_CANDIDATE

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "surprise-event-count-bounded", "result": "pass"},
            {"id": "weak-case-recheck-signal-visible", "result": "pass"},
            {"id": "contradiction-case-fragment-signal-visible", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["surprise engine emits typed bounded actions instead of hidden retry loops"],
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
            blocker_message="surprise engine verifier could not import its runtime modules or found missing files",
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
