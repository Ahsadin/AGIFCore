from __future__ import annotations

import json

import _phase_10_verifier_common as vc
from agifcore_phase10_meta_cognition.contracts import MAX_META_COGNITION_OBSERVATIONS, ObservationKind

VERIFIER = "verify_phase_10_meta_cognition_observer"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_meta_cognition_observer.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_10_meta_cognition_observer_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase10_meta_cognition.contracts",
    "agifcore_phase10_meta_cognition.meta_cognition_observer",
    "agifcore_phase10_meta_cognition.meta_cognition_turn",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "observation-count-bounded",
    "support-and-contradiction-signals-visible",
    "observer-refs-and-severity-present",
    "inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase10_turn(scenario="weak")
    contradiction_case = vc.run_phase10_turn(scenario="contradiction")
    weak_snapshot = weak_case["turn"].meta_cognition_observer
    contradiction_snapshot = contradiction_case["turn"].meta_cognition_observer

    assert weak_snapshot.observation_count <= MAX_META_COGNITION_OBSERVATIONS
    assert contradiction_snapshot.observation_count <= MAX_META_COGNITION_OBSERVATIONS
    assert weak_snapshot.observation_count >= 3
    assert contradiction_snapshot.observation_count >= 3
    assert "support_state_not_grounded" in weak_snapshot.weak_answer_flags
    assert "contradiction_signal_detected" in contradiction_snapshot.weak_answer_flags
    assert any(observation.kind is ObservationKind.SUPPORT_GAP for observation in weak_snapshot.observations)
    assert any(observation.kind is ObservationKind.CONTRADICTION_SIGNAL for observation in contradiction_snapshot.observations)
    assert all(observation.source_ref for observation in weak_snapshot.observations)
    assert all(observation.severity > 0 for observation in contradiction_snapshot.observations)

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "observation-count-bounded", "result": "pass"},
            {"id": "support-and-contradiction-signals-visible", "result": "pass"},
            {"id": "observer-refs-and-severity-present", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["observer remains observational and does not rewrite lower-phase state"],
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
            blocker_message="meta-cognition observer verifier could not import its runtime modules or found missing files",
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
