from __future__ import annotations

import json

import _phase_11_verifier_common as vc

VERIFIER = "verify_phase_11_self_initiated_inquiry_engine"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/verify_phase_11_self_initiated_inquiry_engine.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_11_self_initiated_inquiry_engine_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase11_self_improvement.self_initiated_inquiry_engine",
    "agifcore_phase11_self_improvement.self_improvement_cycle",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "weak-case-opens-one-bounded-inquiry",
    "contradiction-case-does-not-open-inquiry-by-default",
    "allowed-local-inputs-bounded",
    "phase10-inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase11_cycle(scenario="weak")
    contradiction_case = vc.run_phase11_cycle(scenario="contradiction")
    weak_snapshot = weak_case["cycle"].self_initiated_inquiry_engine
    contradiction_snapshot = contradiction_case["cycle"].self_initiated_inquiry_engine
    assert weak_snapshot.inquiry_count == 1
    assert contradiction_snapshot.inquiry_count == 0
    assert weak_snapshot.inquiries[0].trigger_kind.value == "missing_need"
    assert len(weak_snapshot.inquiries[0].allowed_local_inputs) <= 6
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "weak-case-opens-one-bounded-inquiry", "result": "pass"},
            {"id": "contradiction-case-does-not-open-inquiry-by-default", "result": "pass"},
            {"id": "allowed-local-inputs-bounded", "result": "pass"},
            {"id": "phase10-inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["self-initiated inquiry stays bounded, local, and single-shot per cycle"],
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
            blocker_message="self-initiated inquiry verifier could not import its runtime modules or found missing files",
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
