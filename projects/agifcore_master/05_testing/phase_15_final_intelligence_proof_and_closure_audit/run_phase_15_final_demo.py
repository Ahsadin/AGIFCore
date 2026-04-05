from __future__ import annotations

import json

import _phase_15_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    from agifcore_phase15_proof.live_demo_pack import run_live_demo_pack
    from run_phase_15_real_desktop_chat_demo import build_demo_payload as build_real_desktop_chat_demo

    shells = vc.run_phase15_shells()
    weak_shell = shells["proof_shells"]["weak"]
    catalog = weak_shell.live_demo_pack()
    result = run_live_demo_pack(
        pack_catalog=catalog,
        proof_shells=shells["proof_shells"],
        output_dir=vc.DEMO_DIR,
    )
    real_desktop_demo = build_real_desktop_chat_demo()
    return {
        "phase": "15",
        "demo_id": "final_demo",
        "status": "open",
        "live_demo_catalog": catalog,
        "live_demo_result": result,
        "real_desktop_chat_demo": real_desktop_demo,
        "weak_shell_snapshot": shells["weak"]["snapshot"],
        "contradiction_shell_snapshot": shells["contradiction"]["snapshot"],
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_15_live_demo_pack_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_15_real_desktop_chat_demo_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_15_blind_pack_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_15_hidden_pack_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only final demo",
            "Phase 15 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    result = payload["live_demo_result"]
    desktop_demo = payload["real_desktop_chat_demo"]
    return [
        "# Phase 15 Demo: Final AGIFCore Demo",
        "",
        "Phase 15 remains `open`. This demo is inspectable review material only.",
        "",
        "## Demo Summary",
        "",
        f"- session count: `{result['session_count']}`",
        f"- coverage types: `{', '.join(result['coverage_types'])}`",
        f"- status: `{result['status']}`",
        "",
        "## Primary Chat Host",
        "",
        f"- host kind: `{desktop_demo['host_kind']}`",
        f"- runtime host: `{desktop_demo['runtime_host']}`",
        f"- ui selected view: `{desktop_demo['ui_snapshot']['selected_view']}`",
        f"- ui message count: `{desktop_demo['ui_snapshot']['message_count']}`",
        f"- launcher: `{desktop_demo['launch_command']}`",
        "",
        "## Runtime Snapshots",
        "",
        f"- weak shell hash: `{payload['weak_shell_snapshot']['snapshot_hash']}`",
        f"- contradiction shell hash: `{payload['contradiction_shell_snapshot']['snapshot_hash']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- the final demo stays separate from blind and hidden packs",
        "- the primary non-terminal chat host is the desktop UI demo and the terminal path is secondary debug only",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_15_final_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_15_final_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
