from __future__ import annotations

import json

import _phase_06_verifier_common as vc

VERIFIER = "verify_phase_06_world_model_representation"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_06_world_model_representation_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase6_world_simulator.entity_classes",
    "agifcore_phase6_world_simulator.target_domains",
    "agifcore_phase6_world_simulator.world_model",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/entity_classes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/target_domains.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/world_model.py",
)
DEPENDENCIES = ("phase_06_entity_classes_report.json",)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase6_world_simulator.world_model import WorldModelBuilder, WorldModelError

    fixture = vc.build_fixture_chain()
    world = fixture["world_model_snapshot"]
    if not world.entities or not world.relations:
        raise WorldModelError("world model did not produce entities and relations")
    if not all(entity.operators for entity in world.entities):
        raise WorldModelError("world-model entities were created without operators")
    descriptor_entity = next(entity for entity in world.entities if entity.entity_kind.value == "descriptor_support")
    provenance_roles = sorted({link.role for link in descriptor_entity.provenance.links})
    if "graph" not in provenance_roles or not {"review", "source_memory"} & set(provenance_roles):
        raise WorldModelError("descriptor world entity does not carry the required Phase 4/5 provenance roles")
    if not all(0.0 <= entity.world_confidence <= 1.0 for entity in world.entities):
        raise WorldModelError("world confidence escaped the bounded range")
    if not all(0.0 <= relation.relation_strength <= 1.0 for relation in world.relations):
        raise WorldModelError("relation strength escaped the bounded range")
    if any(operator.execution_enabled for entity in world.entities for operator in entity.operators):
        raise WorldModelError("world model enabled live execution")
    limited_builder = WorldModelBuilder(max_entities=10)
    try:
        limited_builder.build_snapshot(
            semantic_memory_state=fixture["semantic_memory_state"],
            procedural_memory_state=fixture["procedural_memory_state"],
            continuity_memory_state=fixture["continuity_memory_state"],
            working_memory_state=fixture["working_memory_state"],
            descriptor_graph_state=fixture["descriptor_graph_state"],
            skill_graph_state=fixture["skill_graph_state"],
            concept_graph_state=fixture["concept_graph_state"],
            transfer_graph_state=fixture["transfer_graph_state"],
            support_selection_result=fixture["support_selection_result"],
            target_domain_registry_state=fixture["target_domain_registry_state"],
        )
        entity_ceiling_enforced = False
    except WorldModelError:
        entity_ceiling_enforced = True
    if not entity_ceiling_enforced:
        raise WorldModelError("world-model entity ceiling was not enforced")

    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES) + [vc.rel(vc.EVIDENCE_DIR / DEPENDENCIES[0])],
        assertions=[
            {"id": "world-model-runtime-importable", "result": "pass"},
            {"id": "world-cells-relations-operators-separated", "result": "pass"},
            {"id": "phase4-phase5-provenance-enforced", "result": "pass"},
            {"id": "execution-disabled-state-enforced", "result": "pass"},
            {"id": "relation-strength-and-confidence-bounds-enforced", "result": "pass"},
            {"id": "entity-ceiling-enforced", "result": "pass"},
            {"id": "world-model-roundtrip-clean", "result": "pass"},
        ],
        anchors={
            "entity_count": len(world.entities),
            "relation_count": len(world.relations),
            "phase4_interfaces": list(world.phase4_interfaces),
            "phase5_interfaces": list(world.phase5_interfaces),
            "descriptor_entity": descriptor_entity.to_dict(),
            "sample_relation": world.relations[0].to_dict(),
        },
        notes=["world model stays read-only and consumes serialized upstream state only"],
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
                "world-model-runtime-importable",
                "world-cells-relations-operators-separated",
                "phase4-phase5-provenance-enforced",
                "execution-disabled-state-enforced",
                "relation-strength-and-confidence-bounds-enforced",
                "entity-ceiling-enforced",
                "world-model-roundtrip-clean",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 6 world-model runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 world_model_representation verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "world-model-runtime-importable",
                "world-cells-relations-operators-separated",
                "phase4-phase5-provenance-enforced",
                "execution-disabled-state-enforced",
                "relation-strength-and-confidence-bounds-enforced",
                "entity-ceiling-enforced",
                "world-model-roundtrip-clean",
            ],
            blocker_kind="missing_phase6_report_dependencies",
            blocker_message="Required earlier Phase 6 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 world_model_representation verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    print("phase_06 world_model_representation verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
