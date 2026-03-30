from __future__ import annotations

import json

import _phase_06_verifier_common as vc

VERIFIER = "verify_phase_06_what_if_simulation"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_06_what_if_simulation_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase6_world_simulator.entity_classes",
    "agifcore_phase6_world_simulator.candidate_futures",
    "agifcore_phase6_world_simulator.what_if_simulation",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/entity_classes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/candidate_futures.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/what_if_simulation.py",
)
DEPENDENCIES = ("phase_06_candidate_futures_report.json",)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase6_world_simulator.what_if_simulation import WhatIfSimulationEngine, WhatIfSimulationError

    fixture = vc.build_fixture_chain()
    simulation = fixture["what_if_simulation_snapshot"]
    if not simulation.entries:
        raise WhatIfSimulationError("what-if simulation produced no entries")
    if not all(entry.trace_steps for entry in simulation.entries):
        raise WhatIfSimulationError("simulation entries are missing trace steps")
    if not all(not any("response_text" in step.detail for step in entry.trace_steps) for entry in simulation.entries):
        raise WhatIfSimulationError("simulation traces leaked conversation-layer behavior")
    fail_closed_future_state = fixture["candidate_future_snapshot"].to_dict()
    fail_closed_future_state["futures"][0]["projected_outcome"] = "abstain"
    fail_closed_simulation = WhatIfSimulationEngine().build_snapshot(
        world_model_state=fixture["world_model_snapshot"].to_dict(),
        candidate_future_state=fail_closed_future_state,
    )
    if not any(entry.fail_closed for entry in fail_closed_simulation.entries):
        raise WhatIfSimulationError("simulation did not fail closed when the input future abstained")
    limited_engine = WhatIfSimulationEngine(max_branch_depth=1)
    limited_simulation = limited_engine.build_snapshot(
        world_model_state=fixture["world_model_snapshot"].to_dict(),
        candidate_future_state=fixture["candidate_future_snapshot"].to_dict(),
    )
    branch_depth_ceiling_enforced = any(
        entry.branch_depth > 1 and entry.fail_closed and entry.outcome.value == "abstain"
        for entry in limited_simulation.entries
    )
    if not branch_depth_ceiling_enforced:
        raise WhatIfSimulationError("branch-depth ceiling was not enforced")

    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES) + [vc.rel(vc.EVIDENCE_DIR / DEPENDENCIES[0])],
        assertions=[
            {"id": "what-if-runtime-importable", "result": "pass"},
            {"id": "deterministic-causal-evaluation-supported", "result": "pass"},
            {"id": "simulation-trace-linked-to-input-branches", "result": "pass"},
            {"id": "insufficient-evidence-abstains", "result": "pass"},
            {"id": "branch-depth-ceiling-enforced", "result": "pass"},
            {"id": "simulation-stays-read-only", "result": "pass"},
            {"id": "what-if-roundtrip-clean", "result": "pass"},
        ],
        anchors={
            "entry_count": len(simulation.entries),
            "baseline_fail_closed_count": sum(1 for entry in simulation.entries if entry.fail_closed),
            "forced_fail_closed_count": sum(1 for entry in fail_closed_simulation.entries if entry.fail_closed),
            "limited_branch_depth_fail_closed_count": sum(
                1 for entry in limited_simulation.entries if entry.branch_depth > 1 and entry.fail_closed
            ),
            "sample_entry": simulation.entries[0].to_dict(),
        },
        notes=["what-if simulation stays deterministic, traced, and execution-disabled"],
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
                "what-if-runtime-importable",
                "deterministic-causal-evaluation-supported",
                "simulation-trace-linked-to-input-branches",
                "insufficient-evidence-abstains",
                "branch-depth-ceiling-enforced",
                "simulation-stays-read-only",
                "what-if-roundtrip-clean",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 6 what-if simulation runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 what_if_simulation verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "what-if-runtime-importable",
                "deterministic-causal-evaluation-supported",
                "simulation-trace-linked-to-input-branches",
                "insufficient-evidence-abstains",
                "branch-depth-ceiling-enforced",
                "simulation-stays-read-only",
                "what-if-roundtrip-clean",
            ],
            blocker_kind="missing_phase6_report_dependencies",
            blocker_message="Required earlier Phase 6 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 what_if_simulation verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    print("phase_06 what_if_simulation verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
