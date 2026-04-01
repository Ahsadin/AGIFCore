from __future__ import annotations

import json

import _phase_12_verifier_common as vc
from agifcore_phase12_structural_growth.contracts import MAX_CURIOSITY_GAP_SELECTION_ITEMS

VERIFIER = "verify_phase_12_curiosity_gap_selection"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_curiosity_gap_selection.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_12_curiosity_gap_selection_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase12_structural_growth.curiosity_gap_selection",
    "agifcore_phase12_structural_growth.contracts",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "gap-count-stays-bounded",
    "priorities-stay-ordered",
    "stop-conditions-present",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase12_cycle(scenario="weak")
    contradiction_case = vc.run_phase12_cycle(scenario="contradiction")
    for case in (weak_case, contradiction_case):
        snapshot = case["cycle"].curiosity_gap_selection
        assert 1 <= snapshot.gap_count <= MAX_CURIOSITY_GAP_SELECTION_ITEMS
        priorities = [item.ranked_priority for item in snapshot.gaps]
        assert priorities == sorted(priorities)
        assert len(set(priorities)) == len(priorities)
        assert all(item.stop_condition for item in snapshot.gaps)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "gap-count-stays-bounded", "result": "pass"},
            {"id": "priorities-stay-ordered", "result": "pass"},
            {"id": "stop-conditions-present", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_case["cycle"].curiosity_gap_selection.to_dict(),
            "contradiction_case": contradiction_case["cycle"].curiosity_gap_selection.to_dict(),
        },
        notes=["curiosity and gap selection stays bounded, ranked, and explicitly stoppable"],
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
            blocker_message="curiosity gap selection verifier could not import its runtime modules or found missing files",
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
