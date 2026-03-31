from __future__ import annotations

import json

import _phase_10_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase10_turn(scenario="weak")
    fixture = result["fixture"]
    turn = result["turn"].to_dict()
    overlay = turn["overlay_contract"]
    diagnosis = turn["weak_answer_diagnosis"]
    observer = turn["meta_cognition_observer"]
    redirect = turn["attention_redirect"]
    journal = turn["strategy_journal"]

    return {
        "phase": "10",
        "demo_id": "why_was_this_weak",
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
            "what_would_verify": fixture["science_world_turn"]["visible_reasoning_summary"]["what_would_verify"],
            "science_reflection_records": fixture["science_world_turn"]["science_reflection"]["records"],
        },
        "phase9_inputs": {
            "selected_lane": fixture["rich_expression_turn"]["selected_lane"],
            "public_response_text": fixture["rich_expression_turn"]["overlay_contract"]["public_response_text"],
            "uncertainty_statements": fixture["rich_expression_turn"]["overlay_contract"]["uncertainty_statements"],
        },
        "phase10_outputs": {
            "selected_outcome": overlay["selected_outcome"],
            "public_explanation": overlay["public_explanation"],
            "diagnosis": diagnosis,
            "observer": observer,
            "redirect": redirect,
            "strategy_journal": journal,
            "trace_refs": {
                "self_model_ref": overlay["self_model_ref"],
                "observer_ref": overlay["observer_ref"],
                "strategy_journal_ref": overlay["strategy_journal_ref"],
                "diagnosis_ref": overlay["diagnosis_ref"],
                "redirect_refs": overlay["redirect_refs"],
            },
        },
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_10_self_model_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_10_meta_cognition_layer_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_10_meta_cognition_observer_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_10_attention_redirect_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_10_strategy_journal_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_10_weak_answer_diagnosis_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only demo surface",
            "Phase 10 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    phase10 = payload["phase10_outputs"]
    diagnosis = phase10["diagnosis"]
    redirect = phase10["redirect"]
    journal = phase10["strategy_journal"]
    return [
        "# Phase 10 Demo: Why Was This Weak",
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
        f"- final answer mode: `{payload['phase7_inputs']['final_answer_mode']}`",
        f"- Phase 9 selected lane: `{payload['phase9_inputs']['selected_lane']}`",
        f"- visible uncertainty: `{payload['phase8_inputs']['uncertainty'][0]}`",
        "",
        "## Phase 10 Result",
        "",
        f"- selected outcome: `{phase10['selected_outcome']}`",
        f"- public explanation: `{phase10['public_explanation']}`",
        f"- diagnosis count: `{diagnosis['item_count']}`",
        f"- redirect count: `{redirect['redirect_count']}`",
        f"- journal entry count: `{journal['entry_count']}`",
        "",
        "## Why It Was Weak",
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
        "- the diagnosis stays bounded to visible support gaps and uncertainty",
        "- the demo does not imply approval or phase completion",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_10_why_was_this_weak_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_10_why_was_this_weak_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
