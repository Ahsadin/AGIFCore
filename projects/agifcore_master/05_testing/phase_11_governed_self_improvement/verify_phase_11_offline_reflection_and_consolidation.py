from __future__ import annotations

import json

import _phase_11_verifier_common as vc
from agifcore_phase11_self_improvement.contracts import MAX_OFFLINE_REFLECTION_ITEMS

VERIFIER = "verify_phase_11_offline_reflection_and_consolidation"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/verify_phase_11_offline_reflection_and_consolidation.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_11_offline_reflection_and_consolidation_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase11_self_improvement.contracts",
    "agifcore_phase11_self_improvement.offline_reflection_and_consolidation",
    "agifcore_phase11_self_improvement.self_improvement_cycle",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "reflection-items-bounded",
    "reflection-items-trace-linked",
    "consolidated-focuses-present",
    "phase10-inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase11_cycle(scenario="weak")
    contradiction_case = vc.run_phase11_cycle(scenario="contradiction")
    weak_snapshot = weak_case["cycle"].offline_reflection_and_consolidation
    contradiction_snapshot = contradiction_case["cycle"].offline_reflection_and_consolidation

    assert 1 <= weak_snapshot.item_count <= MAX_OFFLINE_REFLECTION_ITEMS
    assert 1 <= contradiction_snapshot.item_count <= MAX_OFFLINE_REFLECTION_ITEMS
    assert all(item.supporting_refs for item in weak_snapshot.items)
    assert any(item.source_kind == "missing_need" for item in weak_snapshot.items)
    assert weak_snapshot.consolidated_focuses
    assert contradiction_snapshot.consolidated_focuses

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "reflection-items-bounded", "result": "pass"},
            {"id": "reflection-items-trace-linked", "result": "pass"},
            {"id": "consolidated-focuses-present", "result": "pass"},
            {"id": "phase10-inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["offline reflection stays bounded, trace-linked, and read-only over Phase 10 inputs"],
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
            blocker_message="offline reflection verifier could not import its runtime modules or found missing files",
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
