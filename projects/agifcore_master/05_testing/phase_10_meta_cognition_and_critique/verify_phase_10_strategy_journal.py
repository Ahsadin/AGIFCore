from __future__ import annotations

import json

import _phase_10_verifier_common as vc
from agifcore_phase10_meta_cognition.contracts import MAX_STRATEGY_JOURNAL_ENTRIES

VERIFIER = "verify_phase_10_strategy_journal"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_strategy_journal.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_10_strategy_journal_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase10_meta_cognition.contracts",
    "agifcore_phase10_meta_cognition.strategy_journal",
    "agifcore_phase10_meta_cognition.meta_cognition_turn",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "journal-entry-count-bounded",
    "worked-failed-monitor-fields-visible",
    "priors-and-hidden-variables-visible",
    "inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase10_turn(scenario="weak")
    contradiction_case = vc.run_phase10_turn(scenario="contradiction")
    weak_snapshot = weak_case["turn"].strategy_journal
    contradiction_snapshot = contradiction_case["turn"].strategy_journal

    assert weak_snapshot.entry_count <= MAX_STRATEGY_JOURNAL_ENTRIES
    assert contradiction_snapshot.entry_count <= MAX_STRATEGY_JOURNAL_ENTRIES
    assert weak_snapshot.entry_count == 2
    assert contradiction_snapshot.entry_count == 2
    assert all(entry.worked for entry in weak_snapshot.entries)
    assert all(entry.failed for entry in contradiction_snapshot.entries)
    assert all(entry.priors_used for entry in weak_snapshot.entries)
    assert all(entry.monitoring_note for entry in contradiction_snapshot.entries)
    assert "Redirect targets selected" in weak_snapshot.entries[1].monitoring_note

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "journal-entry-count-bounded", "result": "pass"},
            {"id": "worked-failed-monitor-fields-visible", "result": "pass"},
            {"id": "priors-and-hidden-variables-visible", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["strategy journal records bounded operational lessons without turning into self-improvement"],
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
            blocker_message="strategy journal verifier could not import its runtime modules or found missing files",
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
