from __future__ import annotations

import json

import _phase_11_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase11_cycle(scenario="weak")
    fixture = result["fixture"]
    phase10_turn = result["phase10_turn"]
    cycle = result["cycle"].to_dict()
    inquiry = cycle["self_initiated_inquiry_engine"]
    return {
        "phase": "11",
        "demo_id": "bounded_self_initiated_inquiry",
        "status": "open",
        "original_prompt": fixture["intake"]["raw_text"],
        "phase10_inputs": {
            "support_state": phase10_turn["overlay_contract"]["support_state"],
            "missing_needs": phase10_turn["meta_cognition_observer"]["missing_needs"],
            "redirect_refs": phase10_turn["overlay_contract"]["redirect_refs"],
        },
        "phase11_outputs": {
            "idle_reflection": cycle["idle_reflection"],
            "offline_reflection_and_consolidation": cycle["offline_reflection_and_consolidation"],
            "self_initiated_inquiry_engine": inquiry,
        },
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_11_idle_reflection_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_offline_reflection_and_consolidation_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_11_self_initiated_inquiry_engine_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only bounded inquiry demo",
            "Phase 11 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    inquiry = payload["phase11_outputs"]["self_initiated_inquiry_engine"]
    first = inquiry["inquiries"][0]
    return [
        "# Phase 11 Demo: Bounded Self-Initiated Inquiry",
        "",
        "Phase 11 remains `open`. This demo is inspectable review material only.",
        "",
        "## Input Trigger",
        "",
        f"- support state: `{payload['phase10_inputs']['support_state']}`",
        f"- missing needs: `{payload['phase10_inputs']['missing_needs']}`",
        f"- inquiry count: `{inquiry['inquiry_count']}`",
        "",
        "## Inquiry Record",
        "",
        f"- trigger kind: `{first['trigger_kind']}`",
        f"- goal: `{first['goal']}`",
        f"- budget limit: `{first['budget_limit']}`",
        f"- allowed local inputs: `{first['allowed_local_inputs']}`",
        f"- stop condition: `{first['stop_condition']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- inquiry stays local, bounded, and single-shot",
        "- the demo does not imply approval or phase completion",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_11_bounded_self_initiated_inquiry_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_11_bounded_self_initiated_inquiry_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
