from __future__ import annotations

import json

import _phase_12_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase12_cycle(scenario="contradiction")
    fixture = result["fixture"]
    phase11_cycle = result["phase11_cycle"]
    cycle = result["cycle"].to_dict()
    overlay = cycle["overlay_contract"]
    return {
        "phase": "12",
        "demo_id": "structural_growth",
        "status": "open",
        "original_prompt": fixture["intake"]["raw_text"],
        "phase11_inputs": {
            "support_state": phase11_cycle["overlay_contract"]["support_state"],
            "adopted_proposal_ids": phase11_cycle["overlay_contract"]["adopted_proposal_ids"],
            "monitoring_refs": phase11_cycle["overlay_contract"]["monitoring_refs"],
        },
        "phase12_outputs": {
            "self_model_feedback": cycle["self_model_feedback"],
            "reflection_control": cycle["reflection_control"],
            "curiosity_gap_selection": cycle["curiosity_gap_selection"],
            "self_reorganization": cycle["self_reorganization"],
            "domain_genesis": cycle["domain_genesis"],
            "overlay_contract": overlay,
        },
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_12_self_model_feedback_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_12_reflection_control_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_12_self_reorganization_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_12_domain_genesis_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_12_curiosity_gap_selection_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_12_structural_growth_cycle_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only structural-growth demo",
            "Phase 12 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    phase11 = payload["phase11_inputs"]
    phase12 = payload["phase12_outputs"]
    candidate = phase12["self_reorganization"]["candidates"][0]
    domain_candidate = phase12["domain_genesis"]["candidates"][0]
    return [
        "# Phase 12 Demo: Structural Growth",
        "",
        "Phase 12 remains `open`. This demo is inspectable review material only.",
        "",
        "## Original Prompt",
        "",
        f"- `{payload['original_prompt']}`",
        "",
        "## Phase 11 Input Surface",
        "",
        f"- support state: `{phase11['support_state']}`",
        f"- adopted proposal ids: `{phase11['adopted_proposal_ids']}`",
        f"- monitoring ref count: `{len(phase11['monitoring_refs'])}`",
        "",
        "## Phase 12 Structural Path",
        "",
        f"- feedback item count: `{phase12['self_model_feedback']['item_count']}`",
        f"- reflection action count: `{phase12['reflection_control']['action_count']}`",
        f"- selected gap ids: `{phase12['overlay_contract']['selected_gap_ids']}`",
        f"- reorganization candidate state: `{candidate['candidate_state']}`",
        f"- reorganization target: `{candidate['target_structure_ref']}`",
        f"- domain candidate state: `{domain_candidate['candidate_state']}`",
        f"- domain candidate label: `{domain_candidate['domain_label']}`",
        "",
        "## Rollback Discipline",
        "",
        f"- rollback target: `{candidate['rollback_target']}`",
        f"- rejected alternative: `{candidate['rejected_alternative_ref']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- structural growth remains candidate-bound",
        "- the demo does not imply approval or phase completion",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_12_structural_growth_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_12_structural_growth_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
