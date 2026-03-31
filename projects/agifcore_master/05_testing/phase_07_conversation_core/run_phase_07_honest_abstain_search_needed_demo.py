from __future__ import annotations

import json

import _phase_07_verifier_common as vc

OUTPUT_PATH = vc.DEMO_DIR / "phase_07_honest_abstain_search_needed_demo.json"


def main() -> int:
    manifest = vc.refresh_evidence_manifest()
    if manifest["status"] != "phase_7_verifier_family_pass":
        raise SystemExit(
            "Phase 7 evidence manifest is not fully passing; honest abstain/search-needed demo cannot be exported truthfully"
        )

    search_prompt = "what is the latest weather today?"
    search_turn = vc.build_conversation_fixture(raw_text=search_prompt)["conversation_turn_snapshot"]

    base = vc.PHASE6_VC.build_fixture_chain()
    blocked_support = dict(base["support_selection_result"])
    blocked_support["status"] = "blocked"
    blocked_support["selected_candidate_ids"] = []
    abstain_prompt = "explain the undocumented hidden runtime behavior"
    abstain_turn = vc.build_conversation_fixture(
        raw_text=abstain_prompt,
        support_selection_result_override=blocked_support,
    )["conversation_turn_snapshot"]

    payload = {
        "phase": "7",
        "demo_id": "phase_07_honest_abstain_search_needed_demo",
        "status": "pass",
        "phase_remains_open": True,
        "manifest_status": manifest["status"],
        "review_order": [
            vc.rel(vc.PROJECT_ROOT / "01_plan" / "PHASE_07_CONVERSATION_CORE.md"),
            vc.rel(vc.EVIDENCE_DIR / "phase_07_support_state_logic_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_07_answer_contract_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_07_anti_generic_filler_report.json"),
        ],
        "runnable_command": (
            "python3 projects/agifcore_master/05_testing/phase_07_conversation_core/"
            "run_phase_07_honest_abstain_search_needed_demo.py"
        ),
        "cases": {
            "search_needed": {
                "prompt": search_prompt,
                "interpretation": search_turn.interpretation.to_dict(),
                "support_resolution": search_turn.support_resolution.to_dict(),
                "response_surface": search_turn.response_surface.to_dict(),
                "guardrail_result": search_turn.guardrail_result.to_dict(),
                "answer_contract": search_turn.answer_contract.to_dict(),
            },
            "abstain": {
                "prompt": abstain_prompt,
                "interpretation": abstain_turn.interpretation.to_dict(),
                "support_resolution": abstain_turn.support_resolution.to_dict(),
                "response_surface": abstain_turn.response_surface.to_dict(),
                "guardrail_result": abstain_turn.guardrail_result.to_dict(),
                "answer_contract": abstain_turn.answer_contract.to_dict(),
            },
        },
        "evidence_paths": {
            "manifest": vc.rel(vc.MANIFEST_PATH),
            "support_state_logic": vc.rel(vc.EVIDENCE_DIR / "phase_07_support_state_logic_report.json"),
            "answer_contract": vc.rel(vc.EVIDENCE_DIR / "phase_07_answer_contract_report.json"),
            "anti_generic_filler": vc.rel(vc.EVIDENCE_DIR / "phase_07_anti_generic_filler_report.json"),
        },
        "notes": [
            "The search-needed case preserves fresh-information honesty instead of fabricating a current-world answer.",
            "The abstain case preserves a policy-blocked local answer path instead of bluffing.",
            "No approval is implied by this demo export.",
        ],
    }
    vc.dump_json(OUTPUT_PATH, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
