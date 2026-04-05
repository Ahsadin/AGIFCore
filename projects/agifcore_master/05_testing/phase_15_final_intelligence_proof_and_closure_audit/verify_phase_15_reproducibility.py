from __future__ import annotations

import json

import _phase_15_verifier_common as vc

VERIFIER = "verify_phase_15_reproducibility"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_reproducibility.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_15_reproducibility_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase15_proof.reproducibility_package",
    "agifcore_phase15_proof.proof_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "required-report-and-demo-surfaces-present",
    "reproducibility-artifact-count-bounded",
    "verification-command-set-recorded",
    "bundle-size-within-planning-ceiling",
]


def build_pass_report() -> dict[str, object]:
    required_reports = {
        key: path
        for key, path in vc.build_report_path_map().items()
        if key != "reproducibility_report"
    }
    required_demos = vc.build_demo_path_map()
    missing_prereqs = [
        vc.rel(path)
        for path in [*required_reports.values(), *required_demos.values()]
        if not path.exists()
    ]
    if missing_prereqs:
        raise RuntimeError(
            "reproducibility requires prior reports and demos: " + ", ".join(missing_prereqs)
        )

    shells = vc.run_phase15_shells()
    weak_shell = shells["proof_shells"]["weak"]
    package = weak_shell.reproducibility_package(
        repo_root=vc.REPO_ROOT,
        report_paths=required_reports,
        demo_paths=required_demos,
        evidence_manifest_path=vc.MANIFEST_PATH,
    )

    assert package["artifact_count"] == 12
    assert len(package["tracked_artifacts"]) == 12
    assert package["evidence_manifest_tracked_by_path_only"] is True
    assert len(package["verification_commands"]) == 16
    assert any(
        command.endswith(
            "python3 -m compileall projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime"
        )
        for command in package["verification_commands"]
    )
    assert any(
        command.endswith(
            "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_interactive_chat.py"
        )
        for command in package["verification_commands"]
    )
    assert any(
        command.endswith(
            "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_real_desktop_chat_demo.py"
        )
        for command in package["verification_commands"]
    )
    artifact_ids = {artifact["artifact_id"] for artifact in package["tracked_artifacts"]}
    assert "interactive_chat_report" in artifact_ids
    assert "real_desktop_chat_demo_report" in artifact_ids
    assert "closure_audit_report" in artifact_ids
    assert "phase_15_real_desktop_chat_demo" in artifact_ids
    assert vc.phase15_output_bundle_size_bytes() <= 512 * 1024 * 1024

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "required-report-and-demo-surfaces-present", "result": "pass"},
            {"id": "reproducibility-artifact-count-bounded", "result": "pass"},
            {"id": "verification-command-set-recorded", "result": "pass"},
            {"id": "bundle-size-within-planning-ceiling", "result": "pass"},
        ],
        anchors={
            "reproducibility_package": package,
            "bundle_size_bytes": vc.phase15_output_bundle_size_bytes(),
            "evidence_manifest_before_refresh": vc.evidence_manifest_anchor(),
        },
        notes=[
            "reproducibility hashes the report and demo artifacts directly",
            "the evidence manifest is tracked by path because it is refreshed after the last verifier writes",
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
            blocker_message="reproducibility verifier could not import its runtime modules or found missing files",
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
