from __future__ import annotations

import json

import _phase_06_verifier_common as vc

OUTPUT_PATH = vc.DEMO_DIR / "phase_06_stress_conflict_demo.json"


def main() -> int:
    from agifcore_phase6_world_simulator.conflict_lanes import ConflictLaneEngine
    from agifcore_phase6_world_simulator.fault_lanes import FaultLaneEngine
    from agifcore_phase6_world_simulator.overload_lanes import OverloadLaneEngine
    from agifcore_phase6_world_simulator.pressure_lanes import PressureLaneEngine
    from agifcore_phase6_world_simulator.what_if_simulation import WhatIfSimulationEngine

    fixture = vc.build_fixture_chain()
    manifest = vc.refresh_evidence_manifest()
    if manifest["status"] != "phase_6_verifier_family_pass":
        raise SystemExit("Phase 6 evidence manifest is not fully passing; stress/conflict demo cannot be exported truthfully")

    fault = fixture["fault_lane_snapshot"]
    pressure = fixture["pressure_lane_snapshot"]
    conflict = fixture["conflict_lane_snapshot"]
    overload = fixture["overload_lane_snapshot"]
    instrumentation = fixture["instrumentation_snapshot"]
    usefulness = fixture["usefulness_snapshot"]

    forced_future_state = fixture["candidate_future_snapshot"].to_dict()
    forced_future_state["futures"][0]["projected_outcome"] = "abstain"
    forced_simulation = WhatIfSimulationEngine().build_snapshot(
        world_model_state=fixture["world_model_snapshot"].to_dict(),
        candidate_future_state=forced_future_state,
    )
    forced_fault = FaultLaneEngine().build_snapshot(
        world_model_state=fixture["world_model_snapshot"].to_dict(),
        what_if_simulation_state=forced_simulation.to_dict(),
    )
    forced_pressure = PressureLaneEngine().build_snapshot(
        what_if_simulation_state=forced_simulation.to_dict(),
        fault_lane_state=forced_fault.to_dict(),
        working_memory_state=fixture["working_memory_state"],
    )
    forced_conflict = ConflictLaneEngine().build_snapshot(
        what_if_simulation_state=forced_simulation.to_dict(),
        pressure_lane_state=forced_pressure.to_dict(),
        transfer_graph_state=fixture["transfer_graph_state"],
    )
    forced_overload = OverloadLaneEngine().build_snapshot(
        pressure_lane_state=forced_pressure.to_dict(),
        conflict_lane_state=forced_conflict.to_dict(),
    )

    payload = {
        "phase": "6",
        "demo_id": "phase_06_stress_conflict_demo",
        "status": "pass",
        "phase_remains_open": True,
        "manifest_status": manifest["status"],
        "review_order": [
            vc.rel(vc.PROJECT_ROOT / "01_plan" / "PHASE_06_WORLD_MODEL_AND_SIMULATOR.md"),
            vc.rel(vc.EVIDENCE_DIR / "phase_06_fault_pressure_overload_conflict_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_06_instrumentation_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_06_usefulness_scoring_report.json"),
        ],
        "runnable_command": (
            "python3 projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/"
            "run_phase_06_stress_conflict_demo.py"
        ),
        "anchors": {
            "fault_entry_count": len(fault.entries),
            "pressure_entry_count": len(pressure.entries),
            "conflict_entry_count": len(conflict.entries),
            "overload_entry_count": len(overload.entries),
            "instrumentation_record_count": len(instrumentation.records),
            "instrumentation_summary_count": len(instrumentation.summaries),
            "instrumentation_metric_count": len(instrumentation.metrics),
            "qualified_domain_count": usefulness.qualified_domain_count,
            "overall_usefulness_outcome": usefulness.overall_outcome.value,
            "forced_fault_case_count": sum(len(entry.fault_cases) for entry in forced_fault.entries),
            "forced_pressure_fail_closed_count": sum(
                1 for entry in forced_pressure.entries if entry.outcome.value == "fail_closed"
            ),
            "forced_conflict_hold_or_abstain_count": sum(
                1 for entry in forced_conflict.entries if entry.outcome.value in {"hold", "abstain"}
            ),
            "forced_overload_non_clear_count": sum(
                1 for entry in forced_overload.entries if entry.outcome.value != "clear"
            ),
            "sample_fault_entry": fault.entries[0].to_dict(),
            "sample_pressure_entry": pressure.entries[0].to_dict(),
            "sample_conflict_entry": conflict.entries[0].to_dict(),
            "sample_overload_entry": overload.entries[0].to_dict(),
            "sample_instrumentation_record": instrumentation.records[0].to_dict(),
            "sample_usefulness_domain_score": usefulness.domain_scores[0].to_dict(),
        },
        "evidence_paths": {
            "manifest": vc.rel(vc.MANIFEST_PATH),
            "lane_chain": vc.rel(vc.EVIDENCE_DIR / "phase_06_fault_pressure_overload_conflict_report.json"),
            "instrumentation": vc.rel(vc.EVIDENCE_DIR / "phase_06_instrumentation_report.json"),
            "usefulness": vc.rel(vc.EVIDENCE_DIR / "phase_06_usefulness_scoring_report.json"),
        },
        "notes": [
            "This demo is generated from a real Phase 6 fixture chain.",
            "The forced degraded path proves fault, pressure, conflict, and overload reactions.",
            "Instrumentation remains machine-readable and evidence-linked.",
            "Usefulness scoring remains evidence-bound.",
            "No approval is implied by this demo export.",
        ],
    }
    vc.dump_json(OUTPUT_PATH, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
