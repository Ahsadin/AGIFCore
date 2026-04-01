from __future__ import annotations

import json
import subprocess

import _phase_13_verifier_common as vc

VERIFIER = "verify_phase_13_installer_distribution"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_installer_distribution.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_13_installer_distribution_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.installer_distribution",
    "agifcore_phase13_product_runtime.product_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "installer-schema-correct",
    "artifact-count-bounded",
    "local-bundle-files-exist",
    "launcher-smoke-test-passes",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase13_shell(scenario="weak", build_distribution_bundle=True)
    shell = weak_case["shell"]
    installer = shell.installer_distribution(output_dir=vc.DEMO_DIR)
    bundle_dir = vc.DEMO_DIR / "local_distribution_bundle"
    runner_out = subprocess.run(
        ["sh", str(bundle_dir / "launch_phase_13_local_runner.sh")],
        cwd=vc.REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    gateway_out = subprocess.run(
        ["sh", str(bundle_dir / "launch_phase_13_local_gateway.sh")],
        cwd=vc.REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    ui_out = subprocess.run(
        ["sh", str(bundle_dir / "launch_phase_13_local_desktop_ui.sh")],
        cwd=vc.REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert installer["schema"] == "agifcore.phase_13.installer_distribution.v1"
    assert installer["artifact_count"] <= 6
    for item in installer["artifacts"]:
        assert vc.REPO_ROOT.joinpath(item["path"]).exists()
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "installer-schema-correct", "result": "pass"},
            {"id": "artifact-count-bounded", "result": "pass"},
            {"id": "local-bundle-files-exist", "result": "pass"},
            {"id": "launcher-smoke-test-passes", "result": "pass"},
        ],
        anchors={
            "installer_distribution": installer,
            "runner_launcher_output": json.loads(runner_out.stdout),
            "gateway_launcher_output": json.loads(gateway_out.stdout),
            "ui_launcher_output": json.loads(ui_out.stdout),
        },
        notes=["installer distribution stays local-only and proves the bundle launchers can run without public-release flow"],
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
            blocker_message="installer distribution verifier could not import its runtime modules or found missing files",
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
