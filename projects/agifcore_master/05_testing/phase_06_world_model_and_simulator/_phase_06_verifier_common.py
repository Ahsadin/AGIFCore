from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

PHASE = "6"
PHASE_NAME = "phase_06_world_model_and_simulator"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
TEST_ROOT_NAME = "05_testing"
RUNTIME_PACKAGE = "agifcore_phase6_world_simulator"
PHASE_04_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_04_memory_planes"
PHASE_05_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures"
PHASE_06_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator"
PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/01_plan/DEMO_PROTOCOL.md",
    "projects/agifcore_master/03_design/SIMULATOR_MODEL.md",
    "projects/agifcore_master/03_design/CONVERSATION_MODEL.md",
    "projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/__init__.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/entity_classes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/target_domains.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/world_model.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/candidate_futures.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/what_if_simulation.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/fault_lanes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/pressure_lanes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/conflict_lanes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/overload_lanes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/instrumentation.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/usefulness_scoring.py",
)
REQUIRED_REPORT_FILES = (
    "phase_06_entity_classes_report.json",
    "phase_06_target_domain_structures_report.json",
    "phase_06_world_model_representation_report.json",
    "phase_06_candidate_futures_report.json",
    "phase_06_what_if_simulation_report.json",
    "phase_06_fault_pressure_overload_conflict_report.json",
    "phase_06_instrumentation_report.json",
    "phase_06_usefulness_scoring_report.json",
)
EXPECTED_REPORT_VERIFIERS = {
    "phase_06_entity_classes_report.json": "verify_phase_06_entity_classes",
    "phase_06_target_domain_structures_report.json": "verify_phase_06_target_domain_structures",
    "phase_06_world_model_representation_report.json": "verify_phase_06_world_model_representation",
    "phase_06_candidate_futures_report.json": "verify_phase_06_candidate_futures",
    "phase_06_what_if_simulation_report.json": "verify_phase_06_what_if_simulation",
    "phase_06_fault_pressure_overload_conflict_report.json": "verify_phase_06_fault_pressure_overload_conflict_lanes",
    "phase_06_instrumentation_report.json": "verify_phase_06_instrumentation",
    "phase_06_usefulness_scoring_report.json": "verify_phase_06_usefulness_scoring",
}


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
TEST_ROOT = PROJECT_ROOT / TEST_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_06_evidence"
DEMO_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_06_demo_bundle"
MANIFEST_PATH = EVIDENCE_DIR / "phase_06_evidence_manifest.json"


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_path() -> None:
    runtime_roots = (
        REPO_ROOT / PHASE_04_RUNTIME_PARENT,
        REPO_ROOT / PHASE_05_RUNTIME_PARENT,
        REPO_ROOT / PHASE_06_RUNTIME_PARENT,
    )
    for root in runtime_roots:
        runtime_path = str(root)
        if runtime_path not in sys.path:
            sys.path.insert(0, runtime_path)


ensure_runtime_import_path()


def dump_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[str]) -> list[str]:
    return [path for path in paths if not (REPO_ROOT / path).exists()]


def runtime_modules_available(module_names: tuple[str, ...]) -> bool:
    try:
        for module_name in module_names:
            importlib.import_module(module_name)
    except Exception:
        return False
    return True


def report_dependency_failures(required_reports: tuple[str, ...]) -> list[str]:
    failures: list[str] = []
    for filename in required_reports:
        report_path = EVIDENCE_DIR / filename
        if not report_path.exists():
            failures.append(filename)
            continue
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        if payload.get("status") != "pass":
            failures.append(filename)
    return failures


def build_blocked_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertion_ids: list[str],
    blocker_kind: str,
    blocker_message: str,
    missing: list[str] | None = None,
    dependency_reports: list[str] | None = None,
) -> dict[str, Any]:
    blocker: dict[str, Any] = {"kind": blocker_kind, "message": blocker_message}
    if missing:
        blocker["missing_files"] = missing
    if dependency_reports:
        blocker["dependency_reports"] = dependency_reports
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "blocked",
        "blocker": blocker,
        "checked_files": checked_files,
        "assertions": [{"id": assertion_id, "result": "blocked"} for assertion_id in assertion_ids],
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "notes": ["Phase 6 remains open", "no approval implied"],
    }


def build_pass_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertions: list[dict[str, Any]],
    anchors: Mapping[str, Any],
    notes: list[str],
) -> dict[str, Any]:
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "pass",
        "checked_files": checked_files,
        "assertions": assertions,
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "anchors": dict(anchors),
        "notes": [*notes, "Phase 6 remains open", "no approval implied"],
    }


def refresh_evidence_manifest() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    missing_reports: list[str] = []
    invalid_reports: list[str] = []
    for filename in REQUIRED_REPORT_FILES:
        report_path = EVIDENCE_DIR / filename
        if not report_path.exists():
            missing_reports.append(filename)
            continue
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        status = str(payload.get("status", "unknown"))
        if status not in {"pass", "blocked"}:
            invalid_reports.append(filename)
        if payload.get("phase") != PHASE:
            invalid_reports.append(filename)
        if payload.get("verifier") != EXPECTED_REPORT_VERIFIERS[filename]:
            invalid_reports.append(filename)
        if payload.get("outputs", {}).get("report") != rel(report_path):
            invalid_reports.append(filename)
        assertions = payload.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            invalid_reports.append(filename)
        reports.append(
            {
                "report_id": filename.removeprefix("phase_06_").removesuffix("_report.json"),
                "path": rel(report_path),
                "status": status,
            }
        )
    invalid_reports = sorted(set(invalid_reports))
    overall_pass = (
        not missing_reports
        and not invalid_reports
        and len(reports) == len(REQUIRED_REPORT_FILES)
        and all(report["status"] == "pass" for report in reports)
    )
    manifest = {
        "phase": PHASE,
        "phase_remains_open": True,
        "required_report_count": len(REQUIRED_REPORT_FILES),
        "available_report_count": len(reports),
        "missing_reports": missing_reports,
        "invalid_reports": invalid_reports,
        "reports": reports,
        "status": "phase_6_verifier_family_pass" if overall_pass else "phase_6_verifier_family_incomplete",
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 6 remains open",
            "manifest is rebuilt from actual report files on disk",
            "no approval implied",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def build_fixture_chain() -> dict[str, Any]:
    from agifcore_phase4_memory.continuity_memory import ContinuityMemoryStore
    from agifcore_phase4_memory.procedural_memory import ProceduralMemoryStore
    from agifcore_phase4_memory.semantic_memory import SemanticMemoryStore
    from agifcore_phase4_memory.working_memory import WorkingMemoryStore
    from agifcore_phase5_graph.concept_graph import ConceptGraphStore
    from agifcore_phase5_graph.descriptor_graph import DescriptorGraphStore
    from agifcore_phase5_graph.skill_graph import SkillGraphStore
    from agifcore_phase5_graph.support_selection import SupportSelectionEngine
    from agifcore_phase5_graph.transfer_graph import TransferGraphStore
    from agifcore_phase6_world_simulator import (
        CandidateFuturePlanner,
        ConflictLaneEngine,
        FaultLaneEngine,
        InstrumentationEngine,
        OverloadLaneEngine,
        PressureLaneEngine,
        UsefulnessScoringEngine,
        WhatIfSimulationEngine,
        WorldModelBuilder,
        build_default_registry,
    )

    links = [
        {"role": "source_memory", "ref_id": "source-1", "ref_kind": "memory_entry", "source_path": "phase4/source"},
        {"role": "review", "ref_id": "review-1", "ref_kind": "review", "source_path": "phase4/review"},
    ]
    edge_links = [{"role": "review", "ref_id": "review-2", "ref_kind": "review", "source_path": "phase4/review"}]
    domains = [
        ("finance_document_workflows", "invoice extraction", "Extract invoice fields", "Invoices share stable field structure"),
        ("pos_store_operations", "store restock", "Route store restock", "Store restock depends on inventory signals"),
        ("claims_case_handling", "claims evidence", "Prepare claims evidence", "Claims evidence must stay ordered"),
        ("planning_coordination_workflows", "planning route", "Coordinate planning route", "Planning routes need explicit sequencing"),
    ]

    semantic_memory = SemanticMemoryStore()
    procedural_memory = ProceduralMemoryStore()
    continuity_memory = ContinuityMemoryStore()
    working_memory = WorkingMemoryStore()
    working_memory.bind_turn(
        conversation_id="conv-1",
        turn_id="turn-1",
        task_id="phase6-smoke",
        support_refs=["descriptor::desc-1"],
    )
    working_memory.add_support_ref("descriptor::desc-2")

    for index, (domain_id, abstraction, objective, statement) in enumerate(domains, start=1):
        semantic_memory.add_entry(
            entry_id=f"sem-{index}",
            concept_type="theory_fragment",
            abstraction=statement,
            provenance_refs=[f"prov-sem-{index}"],
            review_ref=f"review-sem-{index}",
            source_candidate_id=f"candidate-sem-{index}",
            supporting_refs=[f"support-sem-{index}"],
            graph_refs=[f"desc-{index}", f"concept-{index}"],
        )
        procedural_memory.add_procedure(
            procedure_id=f"proc-{index}",
            procedure_name=objective,
            objective=objective,
            steps=["step one", "step two"],
            preconditions=["reviewed support available"],
            postconditions=["projection ready"],
            constraints=["read only"],
            provenance_refs=[f"prov-proc-{index}"],
            review_ref=f"review-proc-{index}",
            source_candidate_id=f"candidate-proc-{index}",
            graph_refs=[f"skill-{index}"],
        )
        continuity_memory.record_anchor(
            anchor_id=f"cont-{index}",
            subject=domain_id,
            continuity_kind="domain_anchor",
            statement=f"{domain_id} continuity preserved",
            provenance_refs=[f"prov-cont-{index}"],
        )

    descriptor_graph = DescriptorGraphStore()
    skill_graph = SkillGraphStore()
    concept_graph = ConceptGraphStore()
    transfer_graph = TransferGraphStore()
    for index, (domain_id, abstraction, objective, statement) in enumerate(domains, start=1):
        descriptor_graph.add_node(
            descriptor_id=f"desc-{index}",
            descriptor_type="workflow_pattern",
            label=abstraction,
            alias_tags=abstraction.split(),
            domain_tags=[domain_id],
            concept_tags=["workflow"],
            support_refs=[f"support://desc/{index}"],
            trust_band="reviewed",
            policy_requirements=["route"],
            provenance_links=links,
            origin_kind="inherited",
            inherited_from=["agif_fabric_v1"],
        )
        if index > 1:
            descriptor_graph.relate(
                edge_id=f"desc-edge-{index}",
                source_descriptor_id=f"desc-{index-1}",
                target_descriptor_id=f"desc-{index}",
                relation="supports",
                weight=0.7,
                provenance_links=edge_links,
            )
        skill_graph.add_skill(
            skill_id=f"skill-{index}",
            skill_name=objective,
            objective=objective,
            descriptor_refs=[f"desc-{index}"],
            preconditions=["reviewed support available"],
            postconditions=["projection ready"],
            constraints=["read only"],
            allowed_target_domains=[domain_id],
            trust_band="bounded_local",
            policy_requirements=["route"],
            provenance_links=links,
        )
        concept_graph.add_concept(
            concept_id=f"concept-{index}",
            concept_type="theory_fragment",
            statement=statement,
            theory_fragments=[statement],
            descriptor_refs=[f"desc-{index}"],
            tags=domain_id.split("_"),
            trust_band="reviewed",
            policy_requirements=["route"],
            provenance_links=links,
        )
        transfer_graph.record_transfer(
            transfer_id=f"transfer-{index}",
            source_graph="descriptor",
            source_id=f"desc-{index}",
            source_domain=domain_id,
            target_graph="target_domain",
            target_id=domain_id,
            target_domain=domain_id,
            source_status="active",
            trust_band="reviewed",
            source_policy_requirements=["route"],
            requested_policy_requirements=["route"],
            allowed_target_domains=[domain_id],
            explicit_transfer_approval=True,
            provenance_links=links,
            baseline_support_score=0.75,
            target_support_score=0.8,
            authority_review_ref=f"authority-{index}",
        )

    support_selection = SupportSelectionEngine().select_from_graphs(
        query_id="phase6-query-1",
        query_text="invoice store claims planning workflow route evidence extraction",
        target_domain="finance_document_workflows",
        required_policy_requirements=["route"],
        descriptor_graph=descriptor_graph,
        skill_graph=skill_graph,
        concept_graph=concept_graph,
    )
    target_domain_registry = build_default_registry()
    world_model = WorldModelBuilder().build_snapshot(
        semantic_memory_state=semantic_memory.export_state(),
        procedural_memory_state=procedural_memory.export_state(),
        continuity_memory_state=continuity_memory.export_state(),
        working_memory_state=working_memory.export_state(),
        descriptor_graph_state=descriptor_graph.export_state(),
        skill_graph_state=skill_graph.export_state(),
        concept_graph_state=concept_graph.export_state(),
        transfer_graph_state=transfer_graph.export_state(),
        support_selection_result=support_selection.to_dict(),
        target_domain_registry_state=target_domain_registry.export_state(),
    )
    candidate_futures = CandidateFuturePlanner().build_snapshot(world_model_state=world_model.to_dict())
    what_if_simulation = WhatIfSimulationEngine().build_snapshot(
        world_model_state=world_model.to_dict(),
        candidate_future_state=candidate_futures.to_dict(),
    )
    fault_lanes = FaultLaneEngine().build_snapshot(
        world_model_state=world_model.to_dict(),
        what_if_simulation_state=what_if_simulation.to_dict(),
    )
    pressure_lanes = PressureLaneEngine().build_snapshot(
        what_if_simulation_state=what_if_simulation.to_dict(),
        fault_lane_state=fault_lanes.to_dict(),
        working_memory_state=working_memory.export_state(),
    )
    conflict_lanes = ConflictLaneEngine().build_snapshot(
        what_if_simulation_state=what_if_simulation.to_dict(),
        pressure_lane_state=pressure_lanes.to_dict(),
        transfer_graph_state=transfer_graph.export_state(),
    )
    overload_lanes = OverloadLaneEngine().build_snapshot(
        pressure_lane_state=pressure_lanes.to_dict(),
        conflict_lane_state=conflict_lanes.to_dict(),
    )
    instrumentation = InstrumentationEngine().build_snapshot(
        world_model_state=world_model.to_dict(),
        candidate_future_state=candidate_futures.to_dict(),
        what_if_simulation_state=what_if_simulation.to_dict(),
        fault_lane_state=fault_lanes.to_dict(),
        pressure_lane_state=pressure_lanes.to_dict(),
        conflict_lane_state=conflict_lanes.to_dict(),
        overload_lane_state=overload_lanes.to_dict(),
    )
    usefulness = UsefulnessScoringEngine().build_snapshot(
        target_domain_registry_state=target_domain_registry.export_state(),
        world_model_state=world_model.to_dict(),
        candidate_future_state=candidate_futures.to_dict(),
        what_if_simulation_state=what_if_simulation.to_dict(),
        fault_lane_state=fault_lanes.to_dict(),
        pressure_lane_state=pressure_lanes.to_dict(),
        conflict_lane_state=conflict_lanes.to_dict(),
        overload_lane_state=overload_lanes.to_dict(),
        instrumentation_state=instrumentation.to_dict(),
    )
    return {
        "semantic_memory_state": semantic_memory.export_state(),
        "procedural_memory_state": procedural_memory.export_state(),
        "continuity_memory_state": continuity_memory.export_state(),
        "working_memory_state": working_memory.export_state(),
        "descriptor_graph_state": descriptor_graph.export_state(),
        "skill_graph_state": skill_graph.export_state(),
        "concept_graph_state": concept_graph.export_state(),
        "transfer_graph_state": transfer_graph.export_state(),
        "support_selection_result": support_selection.to_dict(),
        "target_domain_registry_state": target_domain_registry.export_state(),
        "world_model_snapshot": world_model,
        "candidate_future_snapshot": candidate_futures,
        "what_if_simulation_snapshot": what_if_simulation,
        "fault_lane_snapshot": fault_lanes,
        "pressure_lane_snapshot": pressure_lanes,
        "conflict_lane_snapshot": conflict_lanes,
        "overload_lane_snapshot": overload_lanes,
        "instrumentation_snapshot": instrumentation,
        "usefulness_snapshot": usefulness,
    }
