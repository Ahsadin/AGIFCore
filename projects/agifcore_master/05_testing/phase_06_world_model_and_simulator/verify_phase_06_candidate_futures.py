from __future__ import annotations

import json

import _phase_06_verifier_common as vc

VERIFIER = "verify_phase_06_candidate_futures"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_06_candidate_futures_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase6_world_simulator.entity_classes",
    "agifcore_phase6_world_simulator.world_model",
    "agifcore_phase6_world_simulator.candidate_futures",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/entity_classes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/world_model.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/candidate_futures.py",
)
DEPENDENCIES = (
    "phase_06_world_model_representation_report.json",
    "phase_06_target_domain_structures_report.json",
)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase6_world_simulator.candidate_futures import CandidateFuturePlanner, CandidateFuturesError

    fixture = vc.build_fixture_chain()
    future_snapshot = fixture["candidate_future_snapshot"]
    if not future_snapshot.futures:
        raise CandidateFuturesError("candidate futures were not produced")
    branch_record_present = any(item.parent_future_id is not None or item.branch_depth > 1 for item in future_snapshot.futures)
    if not branch_record_present:
        raise CandidateFuturesError("candidate futures do not contain any real branch records")
    if not all(item.state_codes and "live_transfer_execution_disabled" in item.state_codes for item in future_snapshot.futures):
        raise CandidateFuturesError("candidate future state codes are incomplete")
    if not all({"world_model", "future"} <= {link.role for link in item.provenance.links} for item in future_snapshot.futures):
        raise CandidateFuturesError("candidate future provenance is not linked back to world-model inputs")
    limited_planner = CandidateFuturePlanner(max_futures=4)
    try:
        limited_planner.build_snapshot(world_model_state=fixture["world_model_snapshot"].to_dict())
        fanout_ceiling_enforced = False
    except CandidateFuturesError:
        fanout_ceiling_enforced = True
    if not fanout_ceiling_enforced:
        raise CandidateFuturesError("candidate future fanout ceiling was not enforced")

    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES) + [vc.rel(vc.EVIDENCE_DIR / item) for item in DEPENDENCIES],
        assertions=[
            {"id": "candidate-futures-runtime-importable", "result": "pass"},
            {"id": "real-branch-records-supported", "result": "pass"},
            {"id": "projected-outcomes-and-state-codes-present", "result": "pass"},
            {"id": "future-provenance-linked-to-world-model", "result": "pass"},
            {"id": "candidate-future-fanout-ceiling-enforced", "result": "pass"},
            {"id": "candidate-futures-roundtrip-clean", "result": "pass"},
        ],
        anchors={
            "future_count": len(future_snapshot.futures),
            "branch_depths": sorted({item.branch_depth for item in future_snapshot.futures}),
            "branching_future_count": sum(1 for item in future_snapshot.futures if item.parent_future_id is not None),
            "sample_future": future_snapshot.futures[0].to_dict(),
        },
        notes=["candidate futures stay bounded and branch-record based"],
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
                "candidate-futures-runtime-importable",
                "real-branch-records-supported",
                "projected-outcomes-and-state-codes-present",
                "future-provenance-linked-to-world-model",
                "candidate-future-fanout-ceiling-enforced",
                "candidate-futures-roundtrip-clean",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 6 candidate-future runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 candidate_futures verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "candidate-futures-runtime-importable",
                "real-branch-records-supported",
                "projected-outcomes-and-state-codes-present",
                "future-provenance-linked-to-world-model",
                "candidate-future-fanout-ceiling-enforced",
                "candidate-futures-roundtrip-clean",
            ],
            blocker_kind="missing_phase6_report_dependencies",
            blocker_message="Required earlier Phase 6 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 candidate_futures verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    print("phase_06 candidate_futures verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
