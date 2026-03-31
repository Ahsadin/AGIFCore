from __future__ import annotations

import json

import _phase_10_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase10_turn(scenario="contradiction")
    fixture = result["fixture"]
    turn = result["turn"].to_dict()
    overlay = turn["overlay_contract"]
    skeptic = turn["skeptic_counterexample"]
    surprise = turn["surprise_engine"]
    fragments = turn["theory_fragments"]
    diagnosis = turn["weak_answer_diagnosis"]

    return {
        "phase": "10",
        "demo_id": "contradiction",
        "status": "open",
        "original_prompt": fixture["intake"]["raw_text"],
        "phase7_inputs": {
            "support_state": fixture["support"]["support_state"],
            "knowledge_gap_reason": fixture["support"]["knowledge_gap_reason"],
            "next_action": fixture["support"]["next_action"],
            "final_answer_mode": fixture["answer_contract"]["final_answer_mode"],
        },
        "phase8_inputs": {
            "uncertainty": fixture["science_world_turn"]["visible_reasoning_summary"]["uncertainty"],
            "science_reflection_records": fixture["science_world_turn"]["science_reflection"]["records"],
        },
        "phase9_inputs": {
            "selected_lane": fixture["rich_expression_turn"]["selected_lane"],
            "public_response_text": fixture["rich_expression_turn"]["overlay_contract"]["public_response_text"],
            "comparison_axes": fixture["rich_expression_turn"]["comparison"]["axes"],
        },
        "phase10_outputs": {
            "selected_outcome": overlay["selected_outcome"],
            "public_explanation": overlay["public_explanation"],
            "skeptic_counterexample": skeptic,
            "surprise_engine": surprise,
            "theory_fragments": fragments,
            "weak_answer_diagnosis": diagnosis,
            "trace_refs": {
                "skeptic_ref": overlay["skeptic_ref"],
                "surprise_ref": overlay["surprise_ref"],
                "theory_fragment_refs": overlay["theory_fragment_refs"],
                "diagnosis_ref": overlay["diagnosis_ref"],
            },
        },
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_10_meta_cognition_layer_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_10_skeptic_counterexample_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_10_surprise_engine_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_10_theory_fragments_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_10_weak_answer_diagnosis_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only contradiction demo",
            "Phase 10 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    phase10 = payload["phase10_outputs"]
    skeptic = phase10["skeptic_counterexample"]
    surprise = phase10["surprise_engine"]
    fragments = phase10["theory_fragments"]
    diagnosis = phase10["weak_answer_diagnosis"]
    return [
        "# Phase 10 Demo: Contradiction",
        "",
        "Phase 10 remains `open`. This demo is inspectable review material only.",
        "",
        "## Original Prompt",
        "",
        f"- `{payload['original_prompt']}`",
        "",
        "## Lower-Phase Inputs",
        "",
        f"- support state: `{payload['phase7_inputs']['support_state']}`",
        f"- Phase 9 selected lane: `{payload['phase9_inputs']['selected_lane']}`",
        f"- first uncertainty cue: `{payload['phase8_inputs']['uncertainty'][0]}`",
        "",
        "## Contradiction Result",
        "",
        f"- selected outcome: `{phase10['selected_outcome']}`",
        f"- public explanation: `{phase10['public_explanation']}`",
        f"- skeptic branch count: `{skeptic['branch_count']}`",
        f"- surprise event count: `{surprise['event_count']}`",
        f"- theory fragment count: `{fragments['fragment_count']}`",
        "",
        "## Skeptic Branches",
        "",
        *[
            f"- variable flip: `{item['what_variable_could_flip_the_answer']}` | changed answer: `{item['changed_answer_after_skeptic']}`"
            for item in skeptic["branches"]
        ],
        "",
        "## Surprise And Fragment",
        "",
        f"- triggered action: `{surprise['events'][0]['triggered_action']}`",
        f"- trigger reason: {surprise['events'][0]['trigger_reason']}",
        f"- fragment statement: {fragments['fragments'][0]['fragment_statement']}",
        f"- falsifier: {fragments['fragments'][0]['falsifier']}",
        f"- next verification step: {fragments['fragments'][0]['next_verification_step']}",
        "",
        "## Diagnosis",
        "",
        *[
            f"- `{item['kind']}`: {item['why_weak']} Next step: {item['next_step']}"
            for item in diagnosis["items"]
        ],
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- the contradiction path stays bounded and evidence-linked",
        "- the demo does not imply approval or phase completion",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_10_contradiction_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_10_contradiction_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
