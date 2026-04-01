from __future__ import annotations

import json
import subprocess

import _phase_13_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase13_shell(scenario="weak", build_distribution_bundle=True)
    shell = result["shell"]
    installer = shell.installer_distribution(output_dir=vc.DEMO_DIR)
    bundle_dir = vc.DEMO_DIR / "local_distribution_bundle"
    runner_out = subprocess.run(
        ["sh", str(bundle_dir / "launch_phase_13_local_runner.sh")],
        cwd=vc.REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return {
        "phase": "13",
        "demo_id": "installer_distribution",
        "status": "open",
        "product_shell": shell.shell_snapshot(),
        "installer_distribution": installer,
        "runner_launcher_output": json.loads(runner_out.stdout),
        "bundle_dir": vc.rel(bundle_dir),
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_13_installer_distribution_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only installer/distribution demo",
            "Phase 13 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    installer = payload["installer_distribution"]
    return [
        "# Phase 13 Demo: Installer Distribution",
        "",
        "Phase 13 remains `open`. This demo is inspectable review material only.",
        "",
        "## Local Distribution Bundle",
        "",
        f"- bundle dir: `{payload['bundle_dir']}`",
        f"- artifact count: `{installer['artifact_count']}`",
        f"- public release blocked: `{installer['public_release_blocked']}`",
        f"- integrity hash: `{installer['integrity_manifest']['integrity_hash']}`",
        "",
        "## Launcher Proof",
        "",
        f"- runner launcher session id: `{payload['runner_launcher_output']['session_id']}`",
        f"- runner launcher support state: `{payload['runner_launcher_output']['support_state']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- distribution stays local-only and does not claim public release readiness",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_13_installer_distribution_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_13_installer_distribution_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
