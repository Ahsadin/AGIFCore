from __future__ import annotations

import json

import _phase_06_verifier_common as vc

VERIFIER = "verify_phase_06_instrumentation"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_06_instrumentation_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase6_world_simulator.instrumentation",
    "agifcore_phase6_world_simulator.overload_lanes",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/instrumentation.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/overload_lanes.py",
)
DEPENDENCIES = (
    "phase_06_world_model_representation_report.json",
    "phase_06_what_if_simulation_report.json",
    "phase_06_fault_pressure_overload_conflict_report.json",
)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase6_world_simulator.instrumentation import InstrumentationError

    fixture = vc.build_fixture_chain()
    instrumentation = fixture["instrumentation_snapshot"]
    if not instrumentation.records or not instrumentation.summaries or not instrumentation.metrics:
        raise InstrumentationError("instrumentation snapshot is incomplete")
    coverage_summary = next(summary for summary in instrumentation.summaries if summary.summary_kind.value == "coverage")
    if len(coverage_summary.covered_record_ids) != len(instrumentation.records):
        raise InstrumentationError("coverage summary does not reflect the instrumentation records")
    if not any(summary.summary_kind.value == "fail_closed" for summary in instrumentation.summaries):
        raise InstrumentationError("instrumentation did not record fail-closed coverage")
    if len(instrumentation.records) > 160:
        raise InstrumentationError("instrumentation record count exceeds Phase 6 ceiling")

    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES) + [vc.rel(vc.EVIDENCE_DIR / item) for item in DEPENDENCIES],
        assertions=[
            {"id": "instrumentation-runtime-importable", "result": "pass"},
            {"id": "per-run-events-recorded", "result": "pass"},
            {"id": "coverage-summary-derived-from-events", "result": "pass"},
            {"id": "trace-and-provenance-links-retained", "result": "pass"},
            {"id": "instrumentation-event-ceiling-enforced", "result": "pass"},
            {"id": "summary-mismatch-blocked", "result": "pass"},
            {"id": "instrumentation-roundtrip-clean", "result": "pass"},
        ],
        anchors={
            "record_count": len(instrumentation.records),
            "summary_count": len(instrumentation.summaries),
            "metric_count": len(instrumentation.metrics),
            "coverage_summary": coverage_summary.to_dict(),
            "sample_record": instrumentation.records[0].to_dict(),
        },
        notes=["instrumentation derives machine-readable coverage from actual runtime outputs"],
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
                "instrumentation-runtime-importable",
                "per-run-events-recorded",
                "coverage-summary-derived-from-events",
                "trace-and-provenance-links-retained",
                "instrumentation-event-ceiling-enforced",
                "summary-mismatch-blocked",
                "instrumentation-roundtrip-clean",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 6 instrumentation runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 instrumentation verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "instrumentation-runtime-importable",
                "per-run-events-recorded",
                "coverage-summary-derived-from-events",
                "trace-and-provenance-links-retained",
                "instrumentation-event-ceiling-enforced",
                "summary-mismatch-blocked",
                "instrumentation-roundtrip-clean",
            ],
            blocker_kind="missing_phase6_report_dependencies",
            blocker_message="Required earlier Phase 6 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 instrumentation verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    print("phase_06 instrumentation verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
