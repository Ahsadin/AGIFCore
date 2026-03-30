from __future__ import annotations

import json

import _phase_06_verifier_common as vc

OUTPUT_PATH = vc.DEMO_DIR / "phase_06_causal_simulation_demo.json"


def main() -> int:
    fixture = vc.build_fixture_chain()
    manifest = vc.refresh_evidence_manifest()
    if manifest["status"] != "phase_6_verifier_family_pass":
        raise SystemExit("Phase 6 evidence manifest is not fully passing; causal demo cannot be exported truthfully")

    world_model = fixture["world_model_snapshot"]
    futures = fixture["candidate_future_snapshot"]
    simulation = fixture["what_if_simulation_snapshot"]

    world_entities = [entity.to_dict() for entity in world_model.entities]
    relations = [relation.to_dict() for relation in world_model.relations]
    future_items = [future.to_dict() for future in futures.futures]
    simulation_entries = [entry.to_dict() for entry in simulation.entries]

    descriptor_entity = next(entity for entity in world_entities if entity["entity_kind"] == "descriptor_support")
    branching_future = next(future for future in future_items if future["parent_future_id"] is None)
    trace_linked_entry = next(
        entry for entry in simulation_entries if entry["future_id"] == branching_future["future_id"]
    )

    payload = {
        "phase": "6",
        "demo_id": "phase_06_causal_simulation_demo",
        "status": "pass",
        "phase_remains_open": True,
        "manifest_status": manifest["status"],
        "review_order": [
            vc.rel(vc.PROJECT_ROOT / "01_plan" / "PHASE_06_WORLD_MODEL_AND_SIMULATOR.md"),
            vc.rel(vc.EVIDENCE_DIR / "phase_06_world_model_representation_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_06_candidate_futures_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_06_what_if_simulation_report.json"),
        ],
        "runnable_command": (
            "python3 projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/"
            "run_phase_06_causal_simulation_demo.py"
        ),
        "anchors": {
            "world_entity_count": len(world_entities),
            "world_relation_count": len(relations),
            "candidate_future_count": len(future_items),
            "branching_future_count": sum(1 for future in future_items if future["parent_future_id"] is None),
            "simulation_entry_count": len(simulation_entries),
            "baseline_fail_closed_count": sum(1 for entry in simulation_entries if entry["fail_closed"]),
            "sample_world_entity": descriptor_entity,
            "sample_candidate_future": branching_future,
            "sample_simulation_entry": trace_linked_entry,
        },
        "evidence_paths": {
            "manifest": vc.rel(vc.MANIFEST_PATH),
            "world_model": vc.rel(vc.EVIDENCE_DIR / "phase_06_world_model_representation_report.json"),
            "candidate_futures": vc.rel(vc.EVIDENCE_DIR / "phase_06_candidate_futures_report.json"),
            "what_if_simulation": vc.rel(vc.EVIDENCE_DIR / "phase_06_what_if_simulation_report.json"),
        },
        "notes": [
            "This demo is generated from a real Phase 6 fixture chain.",
            "The world model remains read-only and execution-disabled.",
            "Candidate futures remain branch-record based.",
            "What-if simulation remains trace-linked and review-only.",
            "No approval is implied by this demo export.",
        ],
    }
    vc.dump_json(OUTPUT_PATH, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
