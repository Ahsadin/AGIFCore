from __future__ import annotations

import json

import _phase_14_verifier_common as vc

VERIFIER = "verify_phase_14_active_cell_budget"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_active_cell_budget.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_14_active_cell_budget_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase14_sandbox.active_cell_budget",
    "agifcore_phase14_sandbox.sandbox_profile_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "within-budget-admits",
    "near-ceiling-admits-with-warning",
    "ceiling-blocks",
    "hibernate-required-blocks",
    "profile-mismatch-blocks",
]


def _first_mobile_ineligible_cell_id(shell) -> str:
    manifest = shell.cell_manifest()
    for cell in manifest["cells"]:
        if "mobile" not in set(cell["allowed_profiles"]):
            return str(cell["cell_id"])
    raise AssertionError("expected at least one cell that is not mobile-eligible")


def build_pass_report() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    within_budget = shell.active_cell_budget(profile="mobile", requested_active_cells=12)
    near_ceiling = shell.active_cell_budget(profile="laptop", requested_active_cells=120)
    ceiling_blocked = shell.active_cell_budget(profile="mobile", requested_active_cells=30)
    hibernate_required = shell.active_cell_budget(
        profile="builder",
        requested_active_cells=160,
        current_active_cells=300,
        current_active_tissues=32,
    )
    profile_mismatch = shell.active_cell_budget(
        profile="mobile",
        requested_active_cells=8,
        requested_cell_ids=[_first_mobile_ineligible_cell_id(shell)],
    )
    assert within_budget["allowed"] is True and within_budget["budget_state"] == "within_budget"
    assert near_ceiling["allowed"] is True and near_ceiling["budget_state"] == "near_ceiling"
    assert ceiling_blocked["allowed"] is False and ceiling_blocked["budget_state"] == "ceiling_blocked"
    assert hibernate_required["allowed"] is False and hibernate_required["budget_state"] == "hibernate_required"
    assert profile_mismatch["allowed"] is False and profile_mismatch["budget_state"] == "profile_mismatch"
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "within-budget-admits", "result": "pass"},
            {"id": "near-ceiling-admits-with-warning", "result": "pass"},
            {"id": "ceiling-blocks", "result": "pass"},
            {"id": "hibernate-required-blocks", "result": "pass"},
            {"id": "profile-mismatch-blocks", "result": "pass"},
        ],
        anchors={
            "within_budget": within_budget,
            "near_ceiling": near_ceiling,
            "ceiling_blocked": ceiling_blocked,
            "hibernate_required": hibernate_required,
            "profile_mismatch": profile_mismatch,
        },
        notes=["budget enforcement stays explicit and does not silently widen profile bands"],
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
            blocker_message="active-cell budget verifier could not import its runtime modules or found missing files",
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
