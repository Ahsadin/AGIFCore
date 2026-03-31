from __future__ import annotations

import json

import _phase_11_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase11_cycle(scenario="contradiction")
    fixture = result["fixture"]
    cycle = result["cycle"].to_dict()
    rollback = cycle["rollback_proof"]
    measurements = cycle["before_after_measurement"]
    return {
        "phase": "11",
        "demo_id": "rollback",
        "status": "open",
        "original_prompt": fixture["intake"]["raw_text"],
        "phase11_outputs": {
            "adoption_or_rejection_pipeline": cycle["adoption_or_rejection_pipeline"],
            "before_after_measurement": measurements,
            "rollback_proof": rollback,
        },
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_11_before_after_measurement_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_adoption_or_rejection_pipeline_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_rollback_proof_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only rollback demo",
            "Phase 11 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    rollback = payload["phase11_outputs"]["rollback_proof"]
    measurements = payload["phase11_outputs"]["before_after_measurement"]
    return [
        "# Phase 11 Demo: Rollback",
        "",
        "Phase 11 remains `open`. This demo is inspectable review material only.",
        "",
        "## Rollback Summary",
        "",
        f"- rollback proof count: `{rollback['rollback_count']}`",
        f"- measurement pair count: `{measurements['pair_count']}`",
        "",
        "## Roundtrip Proof",
        "",
        *[
            f"- proposal `{item['proposal_id']}`: baseline `{item['baseline_metric']}` -> adopted `{item['adopted_metric']}` -> restored `{measurements['measurements'][index]['rollback_metric']}`"
            for index, item in enumerate(measurements["measurements"])
        ],
        "",
        "## Rollback Records",
        "",
        *[
            f"- `{item['rollback_id']}` preserved baseline: `{item['roundtrip_preserved']}`"
            for item in rollback["rollbacks"]
        ],
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- rollback proof is same-pack and machine-checkable",
        "- the demo does not imply approval or phase completion",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_11_rollback_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_11_rollback_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
