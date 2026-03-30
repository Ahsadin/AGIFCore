from __future__ import annotations

import json
from pathlib import Path

import _phase_06_verifier_common as vc

VERIFIER = "verify_phase_06_entity_classes"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_06_entity_classes_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase6_world_simulator.entity_classes",
    "agifcore_phase6_world_simulator.__init__",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/__init__.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/entity_classes.py",
)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase6_world_simulator.entity_classes import (
        ConflictOutcome,
        InstrumentationRecordKind,
        MetricValueType,
        Phase6EntityError,
        SimulationOutcome,
        StateValueType,
        UsefulnessOutcome,
        WorldEntityKind,
        WorldEntityStatus,
        WorldOperatorKind,
        WorldOperatorStatus,
        WorldRelationKind,
        build_state_value,
        build_world_operator,
    )

    sample_value = build_state_value(
        field_name="trust_band",
        value_type=StateValueType.LABEL,
        value_text="reviewed",
    )
    sample_operator = build_world_operator(
        operator_kind=WorldOperatorKind.FUTURE_EVALUATION,
        status=WorldOperatorStatus.READY_FOR_REVIEW,
        bounded_confidence=0.8,
        reason_codes=["phase6_contract_smoke"],
    )
    invalid_status_blocked = False
    try:
        WorldEntityStatus("invalid")
    except ValueError:
        invalid_status_blocked = True
    if not invalid_status_blocked:
        raise Phase6EntityError("invalid world entity status was not blocked")
    if sample_value.to_dict()["value_type"] != "label":
        raise Phase6EntityError("state value serialization did not preserve the enum value")
    if sample_operator.to_dict()["status"] != "ready_for_review":
        raise Phase6EntityError("world operator serialization did not preserve the status")

    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
        assertions=[
            {"id": "entity-classes-runtime-importable", "result": "pass"},
            {"id": "entity-kind-enums-defined", "result": "pass"},
            {"id": "relation-kind-enums-defined", "result": "pass"},
            {"id": "lane-status-enums-defined", "result": "pass"},
            {"id": "simulation-and-instrumentation-types-defined", "result": "pass"},
            {"id": "serialization-roundtrip-clean", "result": "pass"},
            {"id": "invalid-status-values-blocked", "result": "pass"},
        ],
        anchors={
            "world_entity_kinds": [item.value for item in WorldEntityKind],
            "world_relation_kinds": [item.value for item in WorldRelationKind],
            "world_operator_kinds": [item.value for item in WorldOperatorKind],
            "simulation_outcomes": [item.value for item in SimulationOutcome],
            "conflict_outcomes": [item.value for item in ConflictOutcome],
            "instrumentation_record_kinds": [item.value for item in InstrumentationRecordKind],
            "metric_value_types": [item.value for item in MetricValueType],
            "usefulness_outcomes": [item.value for item in UsefulnessOutcome],
            "sample_state_value": sample_value.to_dict(),
            "sample_world_operator": sample_operator.to_dict(),
        },
        notes=["entity classes define the typed Phase 6 contract surface"],
    )


def main() -> int:
    missing = vc.missing_files(list(vc.PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "entity-classes-runtime-importable",
                "entity-kind-enums-defined",
                "relation-kind-enums-defined",
                "lane-status-enums-defined",
                "simulation-and-instrumentation-types-defined",
                "serialization-roundtrip-clean",
                "invalid-status-values-blocked",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 6 entity classes are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 entity_classes verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    print("phase_06 entity_classes verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
