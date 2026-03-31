from __future__ import annotations

import json

import _phase_07_verifier_common as vc

OUTPUT_PATH = vc.DEMO_DIR / "phase_07_self_knowledge_demo.json"


def main() -> int:
    manifest = vc.refresh_evidence_manifest()
    if manifest["status"] != "phase_7_verifier_family_pass":
        raise SystemExit("Phase 7 evidence manifest is not fully passing; self-knowledge demo cannot be exported truthfully")

    prompt = "what can you do in this agifcore repo?"
    turn = vc.build_conversation_fixture(raw_text=prompt)["conversation_turn_snapshot"]
    payload = {
        "phase": "7",
        "demo_id": "phase_07_self_knowledge_demo",
        "status": "pass",
        "phase_remains_open": True,
        "manifest_status": manifest["status"],
        "prompt": prompt,
        "review_order": [
            vc.rel(vc.PROJECT_ROOT / "01_plan" / "PHASE_07_CONVERSATION_CORE.md"),
            vc.rel(vc.EVIDENCE_DIR / "phase_07_self_knowledge_surface_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_07_utterance_planner_and_surface_realizer_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_07_answer_contract_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_07_anti_generic_filler_report.json"),
        ],
        "runnable_command": (
            "python3 projects/agifcore_master/05_testing/phase_07_conversation_core/"
            "run_phase_07_self_knowledge_demo.py"
        ),
        "anchors": {
            "interpretation": turn.interpretation.to_dict(),
            "support_resolution": turn.support_resolution.to_dict(),
            "self_knowledge": turn.self_knowledge.to_dict(),
            "utterance_plan": turn.utterance_plan.to_dict(),
            "response_surface": turn.response_surface.to_dict(),
            "guardrail_result": turn.guardrail_result.to_dict(),
            "answer_contract": turn.answer_contract.to_dict(),
        },
        "evidence_paths": {
            "manifest": vc.rel(vc.MANIFEST_PATH),
            "self_knowledge_surface": vc.rel(vc.EVIDENCE_DIR / "phase_07_self_knowledge_surface_report.json"),
            "utterance_planner_and_surface_realizer": vc.rel(
                vc.EVIDENCE_DIR / "phase_07_utterance_planner_and_surface_realizer_report.json"
            ),
            "answer_contract": vc.rel(vc.EVIDENCE_DIR / "phase_07_answer_contract_report.json"),
            "anti_generic_filler": vc.rel(vc.EVIDENCE_DIR / "phase_07_anti_generic_filler_report.json"),
        },
        "notes": [
            "This demo exposes only continuity-backed self-knowledge.",
            "The response keeps local limits explicit instead of inventing unsupported self-assertion.",
            "No approval is implied by this demo export.",
        ],
    }
    vc.dump_json(OUTPUT_PATH, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
