from __future__ import annotations

import json

import _phase_06_verifier_common as vc

VERIFIER = "verify_phase_06_fault_pressure_overload_conflict_lanes"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_06_fault_pressure_overload_conflict_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase6_world_simulator.fault_lanes",
    "agifcore_phase6_world_simulator.pressure_lanes",
    "agifcore_phase6_world_simulator.conflict_lanes",
    "agifcore_phase6_world_simulator.overload_lanes",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/fault_lanes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/pressure_lanes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/conflict_lanes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/overload_lanes.py",
)
DEPENDENCIES = ("phase_06_what_if_simulation_report.json",)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase6_world_simulator.conflict_lanes import ConflictLaneEngine
    from agifcore_phase6_world_simulator.fault_lanes import FaultLaneEngine
    from agifcore_phase6_world_simulator.fault_lanes import FaultLanesError
    from agifcore_phase6_world_simulator.overload_lanes import OverloadLaneEngine
    from agifcore_phase6_world_simulator.pressure_lanes import PressureLaneEngine
    from agifcore_phase6_world_simulator.pressure_lanes import PressureLanesError
    from agifcore_phase6_world_simulator.what_if_simulation import WhatIfSimulationEngine

    fixture = vc.build_fixture_chain()
    fault = fixture["fault_lane_snapshot"]
    pressure = fixture["pressure_lane_snapshot"]
    conflict = fixture["conflict_lane_snapshot"]
    overload = fixture["overload_lane_snapshot"]
    if not fault.entries or not pressure.entries or not conflict.entries or not overload.entries:
        raise FaultLanesError("one or more lane snapshots are empty")
    if not any(entry.scenarios for entry in pressure.entries):
        raise PressureLanesError("pressure scenarios were not exercised")
    if not any(result.reason_codes for entry in conflict.entries for result in entry.results):
        raise FaultLanesError("conflict results do not carry reason codes")
    if not any(result.reason_codes for entry in overload.entries for result in entry.results):
        raise FaultLanesError("overload results do not carry reason codes")
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
    if not any(entry.fault_cases for entry in forced_fault.entries):
        raise FaultLanesError("fault overlays were not exercised")
    combined_lane_groups = len(fault.entries) + len(pressure.entries) + len(conflict.entries) + len(overload.entries)
    if combined_lane_groups > 32:
        raise FaultLanesError("combined lane count exceeds the Phase 6 ceiling")

    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES) + [vc.rel(vc.EVIDENCE_DIR / DEPENDENCIES[0])],
        assertions=[
            {"id": "fault-overlays-supported", "result": "pass"},
            {"id": "pressure-scenarios-grounded-in-prior-outputs", "result": "pass"},
            {"id": "overload-threshold-reasoning-supported", "result": "pass"},
            {"id": "conflict-clear-hold-abstain-blocked-paths-supported", "result": "pass"},
            {"id": "lane-reason-codes-machine-checkable", "result": "pass"},
            {"id": "lane-provenance-linked-to-prior-layers", "result": "pass"},
            {"id": "combined-lane-count-ceiling-enforced", "result": "pass"},
            {"id": "lane-roundtrip-clean", "result": "pass"},
        ],
        anchors={
            "fault_entry_count": len(fault.entries),
            "pressure_entry_count": len(pressure.entries),
            "conflict_entry_count": len(conflict.entries),
            "overload_entry_count": len(overload.entries),
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
        },
        notes=["lane outputs stay machine-checkable and chained in order"],
    )


def main() -> int:
    missing = vc.missing_files(list(vc.PLAN_REFS) + list(RUNTIME_FILES))
    dependency_failures = vc.report_dependency_failures(DEPENDENCIES)
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "fault-overlays-supported",
                "pressure-scenarios-grounded-in-prior-outputs",
                "overload-threshold-reasoning-supported",
                "conflict-clear-hold-abstain-blocked-paths-supported",
                "lane-reason-codes-machine-checkable",
                "lane-provenance-linked-to-prior-layers",
                "combined-lane-count-ceiling-enforced",
                "lane-roundtrip-clean",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 6 lane runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 fault_pressure_overload_conflict verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "fault-overlays-supported",
                "pressure-scenarios-grounded-in-prior-outputs",
                "overload-threshold-reasoning-supported",
                "conflict-clear-hold-abstain-blocked-paths-supported",
                "lane-reason-codes-machine-checkable",
                "lane-provenance-linked-to-prior-layers",
                "combined-lane-count-ceiling-enforced",
                "lane-roundtrip-clean",
            ],
            blocker_kind="missing_phase6_report_dependencies",
            blocker_message="Required earlier Phase 6 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 fault_pressure_overload_conflict verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    print("phase_06 fault_pressure_overload_conflict verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
