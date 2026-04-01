from __future__ import annotations

import json

import _phase_14_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    manifests = shell.profile_manifests()
    mobile_manifest = next(item for item in manifests["profiles"] if item["profile"] == "mobile")
    laptop_manifest = next(item for item in manifests["profiles"] if item["profile"] == "laptop")
    within_budget = shell.active_cell_budget(profile="mobile", requested_active_cells=16)
    blocked_budget = shell.active_cell_budget(profile="mobile", requested_active_cells=30)
    fuel_receipt = shell.sandbox_execute(
        profile="mobile",
        function_name="spin",
        output_dir=vc.DEMO_DIR,
    )
    return {
        "phase": "14",
        "demo_id": "mobile_constrained",
        "status": "open",
        "phase14_shell": shell.shell_snapshot(),
        "mobile_profile_manifest": mobile_manifest,
        "laptop_contract_hash": laptop_manifest["same_contract_hash"],
        "within_budget": within_budget,
        "blocked_budget": blocked_budget,
        "fuel_receipt": fuel_receipt,
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_14_profile_manifest_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_active_cell_budget_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_wasmtime_fuel_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only mobile constrained demo",
            "Phase 14 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    manifest = payload["mobile_profile_manifest"]
    return [
        "# Phase 14 Demo: Mobile Constrained Profile",
        "",
        "Phase 14 remains `open`. This demo is inspectable review material only.",
        "",
        "## Mobile Profile Manifest",
        "",
        f"- same contract hash: `{manifest['same_contract_hash']}`",
        f"- laptop contract hash: `{payload['laptop_contract_hash']}`",
        f"- active cell band: `{manifest['active_cell_band']}`",
        f"- diagnostics scope: `{manifest['diagnostics_scope']}`",
        "",
        "## Budget Outcomes",
        "",
        f"- within-budget state: `{payload['within_budget']['budget_state']}`",
        f"- blocked state: `{payload['blocked_budget']['budget_state']}`",
        f"- blocked reason: `{payload['blocked_budget']['reason_code']}`",
        "",
        "## Constrained Fail-Closed Path",
        "",
        f"- mobile fuel receipt: `{payload['fuel_receipt']['reason_code']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- mobile stays on the same public runtime contract while using tighter bounded resources",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_14_mobile_constrained_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_14_mobile_constrained_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
