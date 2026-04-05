from __future__ import annotations

import json

import _phase_15_verifier_common as vc

VERIFIER = "verify_phase_15_hidden_packs"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_hidden_packs.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_15_hidden_pack_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase15_proof.hidden_packs",
    "agifcore_phase15_proof.live_demo_pack",
    "agifcore_phase15_proof.proof_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "hidden-pack-count-bounded",
    "hidden-pack-results-pass",
    "hidden-cases-stay-out-of-live-demo",
]


def build_pass_report() -> dict[str, object]:
    from agifcore_phase15_proof.hidden_packs import run_hidden_pack_catalog

    shells = vc.run_phase15_shells()
    weak_shell = shells["proof_shells"]["weak"]
    live_demo_catalog = weak_shell.live_demo_pack()
    live_demo_case_ids = {
        session["case_id"]
        for pack in live_demo_catalog["packs"]
        for session in pack["sessions"]
    }
    hidden_catalog = weak_shell.hidden_packs()
    result = run_hidden_pack_catalog(
        pack_catalog=hidden_catalog,
        proof_shells=shells["proof_shells"],
        live_demo_case_ids=live_demo_case_ids,
        output_dir=vc.EVIDENCE_DIR,
    )

    assert hidden_catalog["hidden_pack_count"] == 2
    assert result["total_case_count"] == 5
    assert result["passed_case_count"] == 5
    assert result["status"] == "pass"
    assert all(pack["live_demo_excluded"] is True for pack in hidden_catalog["packs"])

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "hidden-pack-count-bounded", "result": "pass"},
            {"id": "hidden-pack-results-pass", "result": "pass"},
            {"id": "hidden-cases-stay-out-of-live-demo", "result": "pass"},
        ],
        anchors={
            "hidden_pack_catalog": hidden_catalog,
            "hidden_pack_result": result,
            "live_demo_case_ids": sorted(live_demo_case_ids),
            "evidence_manifest": vc.evidence_manifest_anchor(),
        },
        notes=[
            "hidden cases remain separated from the user-facing live-demo inventory",
            "resource-limit and fail-closed hidden checks stay machine-verifiable",
        ],
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
            blocker_message="hidden-pack verifier could not import its runtime modules or found missing files",
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
