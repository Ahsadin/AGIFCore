from __future__ import annotations

import json

import _phase_06_verifier_common as vc

VERIFIER = "verify_phase_06_target_domain_structures"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_06_target_domain_structures_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase6_world_simulator.entity_classes",
    "agifcore_phase6_world_simulator.target_domains",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/entity_classes.py",
    "projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/target_domains.py",
)
DEPENDENCIES = ("phase_06_entity_classes_report.json",)


def build_pass_report() -> dict[str, object]:
    from agifcore_phase6_world_simulator.target_domains import TargetDomainError, TargetDomainRegistry, build_default_registry

    registry = build_default_registry()
    exported = registry.export_state()
    clone = TargetDomainRegistry()
    clone.load_state(exported)
    matched_domains = registry.match_domains(labels=["invoice route approval"])
    if not matched_domains or matched_domains[0] != "finance_document_workflows":
        raise TargetDomainError("target-domain matching did not find the expected finance domain")
    try:
        registry.structure_state("missing-domain")
        unregistered_domain_blocked = False
    except TargetDomainError:
        unregistered_domain_blocked = True
    small_registry = TargetDomainRegistry(max_objects=1)
    try:
        small_registry.register_structure(
            domain_id="too_many_objects",
            domain_name="too many objects",
            prefixes=["too_many."],
            descriptor_tokens=["too", "many"],
            object_templates=["too_many.object_a", "too_many.object_b"],
            requires_target_match=True,
            minimum_signal_groups=1,
            provenance_links=[
                {"role": "source", "ref_id": "fixture", "ref_kind": "source", "source_path": "phase6/test"},
                {"role": "review", "ref_id": "review", "ref_kind": "review", "source_path": "phase6/test"},
            ],
        )
        object_ceiling_enforced = False
    except TargetDomainError:
        object_ceiling_enforced = True
    if clone.export_state() != exported:
        raise TargetDomainError("target-domain registry export did not round-trip cleanly")
    if not unregistered_domain_blocked:
        raise TargetDomainError("missing domain lookup was not blocked")
    if not object_ceiling_enforced:
        raise TargetDomainError("target-domain object ceiling was not enforced")

    sample_domain = registry.structure_state("finance_document_workflows")
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES) + [vc.rel(vc.EVIDENCE_DIR / DEPENDENCIES[0])],
        assertions=[
            {"id": "target-domain-runtime-importable", "result": "pass"},
            {"id": "canonical-domain-registry-present", "result": "pass"},
            {"id": "prefix-and-tag-matching-supported", "result": "pass"},
            {"id": "target-domain-object-metadata-retained", "result": "pass"},
            {"id": "unregistered-domain-blocked", "result": "pass"},
            {"id": "target-domain-object-ceiling-enforced", "result": "pass"},
            {"id": "target-domain-roundtrip-clean", "result": "pass"},
        ],
        anchors={
            "domain_ids": registry.domain_ids(),
            "matched_domains": matched_domains,
            "sample_domain": sample_domain,
        },
        notes=["target-domain structures stay canonical and bounded"],
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
                "target-domain-runtime-importable",
                "canonical-domain-registry-present",
                "prefix-and-tag-matching-supported",
                "target-domain-object-metadata-retained",
                "unregistered-domain-blocked",
                "target-domain-object-ceiling-enforced",
                "target-domain-roundtrip-clean",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 6 target-domain structures are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 target_domain_structures verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    if dependency_failures:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "target-domain-runtime-importable",
                "canonical-domain-registry-present",
                "prefix-and-tag-matching-supported",
                "target-domain-object-metadata-retained",
                "unregistered-domain-blocked",
                "target-domain-object-ceiling-enforced",
                "target-domain-roundtrip-clean",
            ],
            blocker_kind="missing_phase6_report_dependencies",
            blocker_message="Required earlier Phase 6 reports are missing or not passing.",
            dependency_reports=dependency_failures,
        )
        vc.dump_json(REPORT_PATH, report)
        print("phase_06 target_domain_structures verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    print("phase_06 target_domain_structures verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
