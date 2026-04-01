from __future__ import annotations

import json

import _phase_14_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    allowed_receipt = shell.sandbox_execute(
        profile="laptop",
        function_name="add",
        function_args=[1, 2],
        output_dir=vc.DEMO_DIR,
    )
    tampered_receipt = shell.sandbox_execute(
        profile="laptop",
        function_name="add",
        function_args=[1, 2],
        variant="tampered",
        output_dir=vc.DEMO_DIR,
    )
    fuel_receipt = shell.sandbox_execute(
        profile="mobile",
        function_name="spin",
        output_dir=vc.DEMO_DIR,
    )
    memory_receipt = shell.sandbox_execute(
        profile="mobile",
        policy_id="strict_fail_closed_policy",
        function_name="grow_to_pages",
        function_args=[600],
        output_dir=vc.DEMO_DIR,
    )
    timeout_receipt = shell.sandbox_execute(
        profile="mobile",
        policy_id="strict_fail_closed_policy",
        function_name="spin",
        output_dir=vc.DEMO_DIR,
    )
    return {
        "phase": "14",
        "demo_id": "sandbox_enforcement",
        "status": "open",
        "phase14_shell": shell.shell_snapshot(),
        "sandbox_policies": shell.sandbox_policies(),
        "allowed_receipt": allowed_receipt,
        "tampered_receipt": tampered_receipt,
        "fuel_receipt": fuel_receipt,
        "memory_receipt": memory_receipt,
        "timeout_receipt": timeout_receipt,
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_14_sandbox_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_wasmtime_fuel_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_wasmtime_memory_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_wasmtime_wall_time_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only sandbox enforcement demo",
            "Phase 14 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    return [
        "# Phase 14 Demo: Sandbox Enforcement",
        "",
        "Phase 14 remains `open`. This demo is inspectable review material only.",
        "",
        "## Runtime Snapshot",
        "",
        f"- phase13 shell hash: `{payload['phase14_shell']['phase13_shell_hash']}`",
        f"- wasmtime available: `{payload['phase14_shell']['wasmtime_available']}`",
        f"- sandbox policy count: `{payload['phase14_shell']['sandbox_policy_count']}`",
        "",
        "## Enforcement Receipts",
        "",
        f"- allowed packaged execution: `{payload['allowed_receipt']['status']}` with stdout `{payload['allowed_receipt']['stdout']}`",
        f"- tampered package: `{payload['tampered_receipt']['reason_code']}`",
        f"- fuel limit: `{payload['fuel_receipt']['reason_code']}`",
        f"- memory limit: `{payload['memory_receipt']['reason_code']}`",
        f"- wall timeout: `{payload['timeout_receipt']['reason_code']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- sandbox enforcement is explicit and fail-closed",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_14_sandbox_enforcement_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_14_sandbox_enforcement_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
