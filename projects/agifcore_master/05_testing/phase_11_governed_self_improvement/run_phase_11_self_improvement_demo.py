from __future__ import annotations

import json

import _phase_11_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase11_cycle(scenario="contradiction")
    fixture = result["fixture"]
    phase10_turn = result["phase10_turn"]
    cycle = result["cycle"].to_dict()
    overlay = cycle["overlay_contract"]
    return {
        "phase": "11",
        "demo_id": "self_improvement",
        "status": "open",
        "original_prompt": fixture["intake"]["raw_text"],
        "phase10_inputs": {
            "support_state": phase10_turn["overlay_contract"]["support_state"],
            "selected_outcome": phase10_turn["overlay_contract"]["selected_outcome"],
            "diagnosis_items": phase10_turn["weak_answer_diagnosis"]["items"],
            "theory_fragments": phase10_turn["theory_fragments"]["fragments"],
        },
        "phase11_outputs": {
            "offline_reflection_and_consolidation": cycle["offline_reflection_and_consolidation"],
            "proposal_generation": cycle["proposal_generation"],
            "self_experiment_lab": cycle["self_experiment_lab"],
            "shadow_evaluation": cycle["shadow_evaluation"],
            "before_after_measurement": cycle["before_after_measurement"],
            "adoption_or_rejection_pipeline": cycle["adoption_or_rejection_pipeline"],
            "post_adoption_monitoring": cycle["post_adoption_monitoring"],
            "overlay_contract": overlay,
        },
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_11_offline_reflection_and_consolidation_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_proposal_generation_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_self_experiment_lab_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_shadow_evaluation_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_before_after_measurement_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_adoption_or_rejection_pipeline_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_post_adoption_monitoring_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_self_improvement_cycle_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only self-improvement demo",
            "Phase 11 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    phase10 = payload["phase10_inputs"]
    phase11 = payload["phase11_outputs"]
    return [
        "# Phase 11 Demo: Self-Improvement",
        "",
        "Phase 11 remains `open`. This demo is inspectable review material only.",
        "",
        "## Original Prompt",
        "",
        f"- `{payload['original_prompt']}`",
        "",
        "## Phase 10 Input Surface",
        "",
        f"- support state: `{phase10['support_state']}`",
        f"- selected outcome: `{phase10['selected_outcome']}`",
        f"- diagnosis item count: `{len(phase10['diagnosis_items'])}`",
        f"- theory fragment count: `{len(phase10['theory_fragments'])}`",
        "",
        "## Phase 11 Improvement Path",
        "",
        f"- reflection item count: `{phase11['offline_reflection_and_consolidation']['item_count']}`",
        f"- proposal count: `{phase11['proposal_generation']['proposal_count']}`",
        f"- experiment count: `{phase11['self_experiment_lab']['experiment_count']}`",
        f"- adopted proposals: `{phase11['overlay_contract']['adopted_proposal_ids']}`",
        f"- monitoring refs: `{phase11['overlay_contract']['monitoring_refs']}`",
        "",
        "## Before/After Measurement",
        "",
        *[
            f"- proposal `{item['proposal_id']}`: baseline `{item['baseline_metric']}` -> adopted `{item['adopted_metric']}` -> rollback `{item['rollback_metric']}`"
            for item in phase11["before_after_measurement"]["measurements"]
        ],
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- the demo remains bounded to local replayable state",
        "- the demo does not imply approval or phase completion",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_11_self_improvement_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_11_self_improvement_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
