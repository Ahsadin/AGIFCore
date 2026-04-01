from __future__ import annotations

import json

import _phase_12_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase12_cycle(scenario="weak")
    fixture = result["fixture"]
    phase11_cycle = result["phase11_cycle"]
    cycle = result["cycle"].to_dict()
    theories = cycle["theory_formation"]["candidates"]
    return {
        "phase": "12",
        "demo_id": "theory_growth",
        "status": "open",
        "original_prompt": fixture["intake"]["raw_text"],
        "phase11_inputs": {
            "support_state": phase11_cycle["overlay_contract"]["support_state"],
            "held_proposal_ids": phase11_cycle["overlay_contract"]["held_proposal_ids"],
            "read_only_phase10_refs": phase11_cycle["overlay_contract"]["read_only_phase10_refs"],
        },
        "phase12_outputs": {
            "self_model_feedback": cycle["self_model_feedback"],
            "theory_formation": cycle["theory_formation"],
            "procedure_tool_invention": cycle["procedure_tool_invention"],
            "overlay_contract": cycle["overlay_contract"],
        },
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_12_self_model_feedback_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_12_theory_formation_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_12_procedure_tool_invention_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_12_structural_growth_cycle_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only theory-growth demo",
            "Phase 12 remains open",
            "no approval implied",
        ],
        "theory_candidate_ids": [item["candidate_id"] for item in theories],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    phase11 = payload["phase11_inputs"]
    phase12 = payload["phase12_outputs"]
    candidate = phase12["theory_formation"]["candidates"][0]
    procedure = phase12["procedure_tool_invention"]["candidates"][0]
    return [
        "# Phase 12 Demo: Theory Growth",
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
        f"- held proposal ids: `{phase11['held_proposal_ids']}`",
        f"- read-only Phase 10 ref count: `{len(phase11['read_only_phase10_refs'])}`",
        "",
        "## Phase 12 Theory Growth Path",
        "",
        f"- theory candidate count: `{phase12['theory_formation']['candidate_count']}`",
        f"- theory label: `{candidate['theory_label']}`",
        f"- theory confidence band: `{candidate['theory_confidence_band']}`",
        f"- falsifier refs: `{candidate['falsifier_refs']}`",
        f"- next verification step: `{candidate['verification_next_step']}`",
        "",
        "## Bounded Procedure Candidate",
        "",
        f"- skill anchor ref: `{procedure['skill_anchor_ref']}`",
        f"- non-auto-execute: `{procedure['non_auto_execute']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- theory growth remains falsifiable and candidate-bound",
        "- the demo does not imply approval or phase completion",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_12_theory_growth_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_12_theory_growth_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
