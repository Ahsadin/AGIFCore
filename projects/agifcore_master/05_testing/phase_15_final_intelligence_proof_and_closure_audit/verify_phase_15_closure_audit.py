from __future__ import annotations

import json

import _phase_15_verifier_common as vc

VERIFIER = "verify_phase_15_closure_audit"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_closure_audit.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_15_closure_audit_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase15_proof.closure_audit",
    "agifcore_phase15_proof.proof_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "upstream-phase-evidence-pass",
    "phase15-open-truth-preserved",
    "review-surfaces-present",
    "closure-audit-review-ready",
]


def build_pass_report() -> dict[str, object]:
    prerequisite_paths = [
        vc.EVIDENCE_DIR / "phase_15_blind_pack_report.json",
        vc.EVIDENCE_DIR / "phase_15_hidden_pack_report.json",
        vc.EVIDENCE_DIR / "phase_15_live_demo_pack_report.json",
        vc.EVIDENCE_DIR / "phase_15_real_desktop_chat_demo_report.json",
        vc.EVIDENCE_DIR / "phase_15_soak_summary.json",
        vc.EVIDENCE_DIR / "phase_15_hardening_report.json",
        vc.DEMO_DIR / "phase_15_real_desktop_chat_demo.json",
        vc.DEMO_DIR / "phase_15_final_demo.json",
        vc.DEMO_DIR / "phase_15_soak_summary_demo.json",
        vc.DEMO_DIR / "phase_15_demo_index.md",
    ]
    missing_prereqs = [vc.rel(path) for path in prerequisite_paths if not path.exists()]
    if missing_prereqs:
        raise RuntimeError(
            "closure audit requires prior reports and demo surfaces: "
            + ", ".join(missing_prereqs)
        )

    shells = vc.run_phase15_shells()
    weak_shell = shells["proof_shells"]["weak"]
    phase13_manifest, phase14_manifest, phase15_manifest = vc.load_upstream_manifests()
    phase_index_text, phase_gate_text = vc.load_phase_status_texts()
    review_surface_paths = vc.build_review_surface_paths()
    audit = weak_shell.closure_audit(
        phase13_manifest=phase13_manifest,
        phase14_manifest=phase14_manifest,
        phase15_manifest=phase15_manifest,
        phase_index_text=phase_index_text,
        phase_gate_text=phase_gate_text,
        review_surface_paths=review_surface_paths,
    )

    assert audit["gate_status"] == "review_ready"
    assert audit["phase15_status"] == "open"
    assert audit["phase16_status"] == "open"
    assert audit["finding_count"] == 0
    assert audit["phase15_manifest_status_before_closure_report"] in {
        "phase_15_verifier_family_incomplete",
        "phase_15_verifier_family_pass",
    }
    if audit["phase15_manifest_status_before_closure_report"] == "phase_15_verifier_family_pass":
        assert sorted(audit["phase15_missing_reports_before_closure_report"]) == []
        assert sorted(audit["phase15_non_pass_reports_before_closure_report"]) == []
    else:
        assert sorted(audit["phase15_missing_reports_before_closure_report"]) in (
            [],
            ["phase_15_reproducibility_report.json"],
            [
                "phase_15_closure_audit_report.json",
                "phase_15_reproducibility_report.json",
            ],
            ["phase_15_closure_audit_report.json"],
        )
        assert sorted(audit["phase15_non_pass_reports_before_closure_report"]) in (
            [],
            ["closure_audit_report"],
            ["closure_audit_report", "reproducibility_report"],
            ["reproducibility_report"],
        )
    assert len(audit["review_surface_paths"]) >= 8

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "upstream-phase-evidence-pass", "result": "pass"},
            {"id": "phase15-open-truth-preserved", "result": "pass"},
            {"id": "review-surfaces-present", "result": "pass"},
            {"id": "closure-audit-review-ready", "result": "pass"},
        ],
        anchors={
            "closure_audit": audit,
            "phase13_manifest": phase13_manifest,
            "phase14_manifest": phase14_manifest,
            "phase15_manifest_before_closure_report": phase15_manifest,
        },
        notes=[
            "closure audit stays inside Phase 15 and keeps the phase truth open",
            "review readiness is evidence-linked and separate from user approval",
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
            blocker_message="closure-audit verifier could not import its runtime modules or found missing files",
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
