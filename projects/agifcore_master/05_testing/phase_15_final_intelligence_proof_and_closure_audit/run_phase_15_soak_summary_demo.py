from __future__ import annotations

import json

import _phase_15_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    from agifcore_phase15_proof.soak_harness import run_soak_harness

    shells = vc.run_phase15_shells()
    weak_shell = shells["proof_shells"]["weak"]
    contract = weak_shell.soak_contract()
    result = run_soak_harness(proof_shells=shells["proof_shells"])
    return {
        "phase": "15",
        "demo_id": "soak_summary",
        "status": "open",
        "soak_contract": contract,
        "soak_result": result,
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_15_soak_summary.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_15_hardening_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only soak summary demo",
            "Phase 15 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    result = payload["soak_result"]
    return [
        "# Phase 15 Demo: Soak Summary",
        "",
        "Phase 15 remains `open`. This demo is inspectable review material only.",
        "",
        "## Soak Summary",
        "",
        f"- duration classes: `{result['duration_class_count']}`",
        f"- total iterations: `{result['total_iterations']}`",
        f"- total failures: `{result['total_failures']}`",
        f"- status: `{result['status']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- the soak harness stays bounded to local duration classes",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_15_soak_summary_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_15_soak_summary_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
