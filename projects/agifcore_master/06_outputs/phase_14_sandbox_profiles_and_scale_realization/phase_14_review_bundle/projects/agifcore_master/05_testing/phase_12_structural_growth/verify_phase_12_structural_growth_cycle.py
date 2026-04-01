from __future__ import annotations

import json

import _phase_12_verifier_common as vc

VERIFIER = "verify_phase_12_structural_growth_cycle"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_structural_growth_cycle.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_12_structural_growth_cycle_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase12_structural_growth.structural_growth_cycle",
    "agifcore_phase12_structural_growth.contracts",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "cycle-schema-correct",
    "phase11-refs-remain-read-only",
    "overlay-evidence-refs-present",
    "cycle-size-stays-bounded",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase12_cycle(scenario="contradiction")
    cycle = contradiction_case["cycle"]
    cycle_dict = cycle.to_dict()
    assert cycle.schema == "agifcore.phase_12.structural_growth_cycle.v1"
    assert cycle.overlay_contract.read_only_phase11_refs
    assert cycle.overlay_contract.evidence_refs
    assert vc.canonical_size_bytes(cycle_dict) < 144 * 1024 * 1024
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "cycle-schema-correct", "result": "pass"},
            {"id": "phase11-refs-remain-read-only", "result": "pass"},
            {"id": "overlay-evidence-refs-present", "result": "pass"},
            {"id": "cycle-size-stays-bounded", "result": "pass"},
        ],
        anchors={"contradiction_case": cycle_dict},
        notes=["the cycle coordinator stays thin and keeps Phase 11 references read-only"],
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
            blocker_message="structural growth cycle verifier could not import its runtime modules or found missing files",
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
