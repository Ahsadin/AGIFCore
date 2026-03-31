from __future__ import annotations

import json

import _phase_10_verifier_common as vc
from agifcore_phase10_meta_cognition.contracts import CritiqueOutcome

VERIFIER = "verify_phase_10_meta_cognition_layer"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_meta_cognition_layer.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_10_meta_cognition_layer_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase10_meta_cognition.contracts",
    "agifcore_phase10_meta_cognition.meta_cognition_layer",
    "agifcore_phase10_meta_cognition.meta_cognition_turn",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "selected-outcomes-bounded",
    "active-modules-visible",
    "overlay-contract-read-only-interfaces-visible",
    "inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase10_turn(scenario="weak")
    contradiction_case = vc.run_phase10_turn(scenario="contradiction")
    weak_turn = weak_case["turn"]
    contradiction_turn = contradiction_case["turn"]

    assert weak_turn.meta_cognition_layer.selected_outcome is CritiqueOutcome.RECHECK_SUPPORT
    assert contradiction_turn.meta_cognition_layer.selected_outcome is CritiqueOutcome.CLARIFY
    assert weak_turn.meta_cognition_layer.redirect_required
    assert contradiction_turn.meta_cognition_layer.redirect_required
    assert "weak_answer_diagnosis" in weak_turn.meta_cognition_layer.active_modules
    assert "surprise_engine" in contradiction_turn.meta_cognition_layer.active_modules
    assert weak_turn.overlay_contract.phase7_interfaces
    assert weak_turn.overlay_contract.phase8_interfaces
    assert weak_turn.overlay_contract.phase9_interfaces
    assert weak_turn.overlay_contract.support_honesty_preserved
    assert "Phase 10 stays read-only" in weak_turn.meta_cognition_layer.outcome_notes[-1]

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "selected-outcomes-bounded", "result": "pass"},
            {"id": "active-modules-visible", "result": "pass"},
            {"id": "overlay-contract-read-only-interfaces-visible", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": {
                "meta_cognition_layer": weak_turn.meta_cognition_layer.to_dict(),
                "overlay_contract": weak_turn.overlay_contract.to_dict(),
            },
            "contradiction_case": {
                "meta_cognition_layer": contradiction_turn.meta_cognition_layer.to_dict(),
                "overlay_contract": contradiction_turn.overlay_contract.to_dict(),
            },
        },
        notes=["the thin coordinator stays above Phase 7, 8, and 9 surfaces and does not take over response ownership"],
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
            blocker_message="meta-cognition layer verifier could not import its runtime modules or found missing files",
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
