from __future__ import annotations

import json

import _phase_14_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    manifests = shell.profile_manifests()
    laptop_manifest = next(item for item in manifests["profiles"] if item["profile"] == "laptop")
    budget = shell.active_cell_budget(profile="laptop", requested_active_cells=96)
    sandbox_receipt = shell.sandbox_execute(
        profile="laptop",
        function_name="add",
        function_args=[2, 5],
        output_dir=vc.DEMO_DIR,
    )
    return {
        "phase": "14",
        "demo_id": "laptop_profile",
        "status": "open",
        "phase14_shell": shell.shell_snapshot(),
        "laptop_profile_manifest": laptop_manifest,
        "active_cell_budget": budget,
        "sandbox_receipt": sandbox_receipt,
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_14_profile_manifest_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_active_cell_budget_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_sandbox_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only laptop profile demo",
            "Phase 14 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    manifest = payload["laptop_profile_manifest"]
    budget = payload["active_cell_budget"]
    return [
        "# Phase 14 Demo: Laptop Profile",
        "",
        "Phase 14 remains `open`. This demo is inspectable review material only.",
        "",
        "## Laptop Profile Manifest",
        "",
        f"- same contract hash: `{manifest['same_contract_hash']}`",
        f"- active cell band: `{manifest['active_cell_band']}`",
        f"- target active cells: `{manifest['target_active_cells']}`",
        f"- correctness privilege: `{manifest['correctness_privilege']}`",
        "",
        "## Laptop Budget Result",
        "",
        f"- budget state: `{budget['budget_state']}`",
        f"- selected active cells: `{budget['selected_active_cell_count']}`",
        f"- selected active tissues: `{budget['selected_active_tissue_count']}`",
        "",
        "## Sandbox Smoke Test",
        "",
        f"- packaged execution status: `{payload['sandbox_receipt']['status']}`",
        f"- packaged execution stdout: `{payload['sandbox_receipt']['stdout']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- the laptop profile is the reference runtime profile, not a correctness exception",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_14_laptop_profile_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_14_laptop_profile_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
