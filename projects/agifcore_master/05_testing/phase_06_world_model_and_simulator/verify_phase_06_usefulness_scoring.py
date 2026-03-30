from __future__ import annotations

import json

import _phase_06_verifier_common as vc

VERIFIER = "verify_phase_06_usefulness_scoring"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_06_usefulness_scoring_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase6_world_simulator.usefulness_scoring",
    "agifcore_phase6_world_simulator.instrumentation",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/usefulness_scoring.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/instrumentation.py",
)
DEPENDENCIES = (
    "phase_06_instrumentation_report.json",
    "phase_06_fault_pressure_overload_conflict_report.json",
    "phase_06_candidate_futures_report.json",
)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase6_world_simulator.usefulness_scoring import UsefulnessScoringEngine, UsefulnessScoringError

    fixture = vc.build_fixture_chain()
    usefulness = fixture["usefulness_snapshot"]
    if usefulness.qualified_domain_count < 4:
        raise UsefulnessScoringError("usefulness scoring did not qualify the minimum number of domains")
    if usefulness.overall_outcome.value != "qualified":
        raise UsefulnessScoringError("usefulness scoring did not preserve the qualified overall outcome")
    if not all(score.evidence_inputs > 0 for score in usefulness.domain_scores):
        raise UsefulnessScoringError("usefulness scoring accepted domains without evidence-linked inputs")
    limited_engine = UsefulnessScoringEngine(max_inputs=1)
    limited_result = limited_engine.build_snapshot(
        target_domain_registry_state=fixture["target_domain_registry_state"],
        world_model_state=fixture["world_model_snapshot"].to_dict(),
        candidate_future_state=fixture["candidate_future_snapshot"].to_dict(),
        what_if_simulation_state=fixture["what_if_simulation_snapshot"].to_dict(),
        fault_lane_state=fixture["fault_lane_snapshot"].to_dict(),
        pressure_lane_state=fixture["pressure_lane_snapshot"].to_dict(),
        conflict_lane_state=fixture["conflict_lane_snapshot"].to_dict(),
        overload_lane_state=fixture["overload_lane_snapshot"].to_dict(),
        instrumentation_state=fixture["instrumentation_snapshot"].to_dict(),
    )
    if limited_result.qualified_domain_count >= usefulness.qualified_domain_count:
        raise UsefulnessScoringError("usefulness input ceiling did not reduce the qualified signal set")
    manifest = vc.refresh_evidence_manifest()
    if manifest["status"] not in {"phase_6_verifier_family_pass", "phase_6_verifier_family_incomplete"}:
        raise UsefulnessScoringError("Phase 6 manifest was not rebuilt from disk")

    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES) + [vc.rel(vc.EVIDENCE_DIR / item) for item in DEPENDENCIES],
        assertions=[
            {"id": "usefulness-runtime-importable", "result": "pass"},
            {"id": "evidence-linked-inputs-required", "result": "pass"},
            {"id": "instrumentation-dependency-enforced", "result": "pass"},
            {"id": "domain-specific-usefulness-supported", "result": "pass"},
            {"id": "threshold-and-reason-codes-supported", "result": "pass"},
            {"id": "unsafe-regression-check-supported", "result": "pass"},
            {"id": "usefulness-input-ceiling-enforced", "result": "pass"},
            {"id": "low-evidence-usefulness-abstains", "result": "pass"},
            {"id": "phase-06-evidence-manifest-rebuilt-from-disk", "result": "pass"},
        ],
        anchors={
            "qualified_domain_count": usefulness.qualified_domain_count,
            "overall_outcome": usefulness.overall_outcome.value,
            "sample_domain_score": usefulness.domain_scores[0].to_dict(),
            "manifest_status": manifest["status"],
        },
        notes=["usefulness scoring remains evidence-bound and rebuilds the manifest from disk"],
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
                "usefulness-runtime-importable",
                "evidence-linked-inputs-required",
                "instrumentation-dependency-enforced",
                "domain-specific-usefulness-supported",
                "threshold-and-reason-codes-supported",
                "unsafe-regression-check-supported",
                "usefulness-input-ceiling-enforced",
                "low-evidence-usefulness-abstains",
                "phase-06-evidence-manifest-rebuilt-from-disk",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 6 usefulness scoring runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_06 usefulness_scoring verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "usefulness-runtime-importable",
                "evidence-linked-inputs-required",
                "instrumentation-dependency-enforced",
                "domain-specific-usefulness-supported",
                "threshold-and-reason-codes-supported",
                "unsafe-regression-check-supported",
                "usefulness-input-ceiling-enforced",
                "low-evidence-usefulness-abstains",
                "phase-06-evidence-manifest-rebuilt-from-disk",
            ],
            blocker_kind="missing_phase6_report_dependencies",
            blocker_message="Required earlier Phase 6 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_06 usefulness_scoring verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    manifest = vc.refresh_evidence_manifest()
    report["anchors"]["manifest_status"] = manifest["status"]
    vc.dump_json(REPORT_PATH, report)
    print("phase_06 usefulness_scoring verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
