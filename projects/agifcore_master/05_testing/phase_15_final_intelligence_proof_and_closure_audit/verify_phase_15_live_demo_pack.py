from __future__ import annotations

import json

import _phase_15_verifier_common as vc

VERIFIER = "verify_phase_15_live_demo_pack"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_live_demo_pack.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_15_live_demo_pack_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase15_proof.live_demo_pack",
    "agifcore_phase15_proof.proof_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "live-demo-pack-count-bounded",
    "live-demo-session-catalog-complete",
    "live-demo-results-pass",
    "live-demo-covers-runtime-and-sandbox-paths",
]


def build_pass_report() -> dict[str, object]:
    from agifcore_phase15_proof.live_demo_pack import run_live_demo_pack

    shells = vc.run_phase15_shells()
    weak_shell = shells["proof_shells"]["weak"]
    catalog = weak_shell.live_demo_pack()
    result = run_live_demo_pack(
        pack_catalog=catalog,
        proof_shells=shells["proof_shells"],
        output_dir=vc.EVIDENCE_DIR,
    )
    by_case_id = {item["case_id"]: item for item in result["session_results"]}

    assert catalog["live_demo_pack_count"] == 1
    assert result["session_count"] == 14
    assert result["status"] == "pass"
    assert by_case_id["demo_weak_conversation"]["summary"]["final_answer_mode"] == "search_needed"
    assert by_case_id["demo_contradiction_conversation"]["summary"]["final_answer_mode"] == "clarify"
    assert by_case_id["demo_interactive_turn"]["summary"]["question_class"] == "project_phase_capability"
    assert by_case_id["demo_interactive_turn"]["summary"]["answer_mode"] == "grounded_fact"
    assert by_case_id["demo_interactive_desktop_ui"]["summary"]["selected_view"] == "chat_workspace"
    assert by_case_id["demo_interactive_desktop_ui"]["summary"]["view_count"] == 7
    assert by_case_id["demo_interactive_desktop_ui"]["summary"]["message_count"] >= 4
    assert by_case_id["demo_interactive_desktop_ui"]["summary"]["latest_question_class"] == "support_diagnostics"
    assert by_case_id["demo_sandbox_allowed"]["summary"]["status"] == "pass"
    assert (
        by_case_id["demo_sandbox_tampered"]["summary"]["reason_code"]
        == "BUNDLE_INTEGRITY_REQUIRED"
    )
    assert by_case_id["demo_manifest_audit"]["summary"]["audit_status"] == "pass"
    assert by_case_id["demo_weak_trace_export"]["summary"]["trace_record_count"] >= 1
    assert by_case_id["demo_weak_memory_review"]["summary"]["memory_review_ref_count"] >= 1
    assert by_case_id["demo_weak_memory_review"]["summary"]["retention_candidate_count"] >= 1

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "live-demo-pack-count-bounded", "result": "pass"},
            {"id": "live-demo-session-catalog-complete", "result": "pass"},
            {"id": "live-demo-results-pass", "result": "pass"},
            {"id": "live-demo-covers-runtime-and-sandbox-paths", "result": "pass"},
        ],
        anchors={
            "live_demo_catalog": catalog,
            "live_demo_result": result,
            "evidence_manifest": vc.evidence_manifest_anchor(),
        },
        notes=[
            "the live-demo pack remains user-facing and separate from blind and hidden packs",
            "the demo pack covers runtime honesty, the repaired interactive path, the desktop UI host, export paths, safe shutdown, profiles, sandbox enforcement, and manifest audit",
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
            blocker_message="live-demo verifier could not import its runtime modules or found missing files",
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
