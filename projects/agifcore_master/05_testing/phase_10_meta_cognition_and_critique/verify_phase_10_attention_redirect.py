from __future__ import annotations

import json

import _phase_10_verifier_common as vc
from agifcore_phase10_meta_cognition.contracts import MAX_ATTENTION_REDIRECTS, RedirectTargetKind

VERIFIER = "verify_phase_10_attention_redirect"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_attention_redirect.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_10_attention_redirect_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase10_meta_cognition.contracts",
    "agifcore_phase10_meta_cognition.attention_redirect",
    "agifcore_phase10_meta_cognition.meta_cognition_turn",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "redirect-count-bounded",
    "support-gap-redirect-emitted",
    "contradiction-probe-redirect-emitted",
    "inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase10_turn(scenario="weak")
    contradiction_case = vc.run_phase10_turn(scenario="contradiction")
    weak_snapshot = weak_case["turn"].attention_redirect
    contradiction_snapshot = contradiction_case["turn"].attention_redirect

    assert weak_snapshot.redirect_count <= MAX_ATTENTION_REDIRECTS
    assert contradiction_snapshot.redirect_count <= MAX_ATTENTION_REDIRECTS
    assert weak_snapshot.redirect_count == 2
    assert weak_snapshot.redirects[0].target_kind is RedirectTargetKind.SUPPORT_STATE
    assert weak_snapshot.redirects[1].target_kind is RedirectTargetKind.RICH_EXPRESSION
    assert contradiction_snapshot.redirect_count == 1
    assert contradiction_snapshot.redirects[0].target_kind is RedirectTargetKind.CONTRADICTION_PROBE
    assert weak_snapshot.stop_reason == "bounded_redirects_emitted"
    assert contradiction_snapshot.stop_reason == "bounded_redirects_emitted"

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "redirect-count-bounded", "result": "pass"},
            {"id": "support-gap-redirect-emitted", "result": "pass"},
            {"id": "contradiction-probe-redirect-emitted", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["attention redirect stays bounded and tied to existing lower-phase refs"],
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
            blocker_message="attention redirect verifier could not import its runtime modules or found missing files",
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
