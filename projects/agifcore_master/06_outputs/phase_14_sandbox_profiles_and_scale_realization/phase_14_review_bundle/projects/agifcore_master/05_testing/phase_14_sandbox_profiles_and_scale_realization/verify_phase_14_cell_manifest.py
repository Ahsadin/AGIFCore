from __future__ import annotations

import json

import _phase_14_verifier_common as vc
from agifcore_phase14_sandbox.contracts import (
    CELL_FAMILY_IDS,
    exemplar_class_spec,
    family_behavior_spec,
    operation_set_for_exemplar,
    tissue_variant_spec,
)

VERIFIER = "verify_phase_14_cell_manifest"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_cell_manifest.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_14_cell_manifest_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase14_sandbox.contracts",
    "agifcore_phase14_sandbox.cell_manifest",
    "agifcore_phase14_sandbox.sandbox_profile_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "exact-logical-cell-count",
    "family-differentiation-unique",
    "constraint-diversity-bounded",
    "exemplar-structure-bounded",
]


def _family_core_signature(family_spec: dict[str, object]) -> tuple[object, ...]:
    return (
        tuple(family_spec["allowed_profiles"]),
        tuple(family_spec["backstop_profiles"]),
        tuple(family_spec["allowed_actions"]),
        tuple(family_spec["forbidden_actions"]),
        str(family_spec["routing_responsibility"]),
        str(family_spec["activation_budget_class"]),
        str(family_spec["export_visibility_class"]),
        str(family_spec["dormancy_behavior_class"]),
        str(family_spec["continuity_requirement_class"]),
        str(family_spec["evidence_requirement_class"]),
        bool(family_spec["audit_replay_required"]),
    )


def build_pass_report() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    manifest = result["shell"].cell_manifest()
    family_counts = dict(manifest["family_counts"])
    family_signatures: dict[str, tuple[object, ...]] = {}
    family_contract_variant_counts: dict[str, dict[str, int]] = {}
    family_exemplar_counts: dict[str, dict[str, int]] = {}
    family_tissue_variant_counts: dict[str, dict[str, int]] = {}
    for family in CELL_FAMILY_IDS:
        family_signatures[family] = _family_core_signature(family_behavior_spec(family))
        family_contract_variant_counts[family] = {}
        family_exemplar_counts[family] = {}
        family_tissue_variant_counts[family] = {}
    for cell in manifest["cells"]:
        family = str(cell["role_family"])
        family_spec = family_behavior_spec(family)
        tissue_spec = tissue_variant_spec(str(cell["tissue_variant_id"]))
        exemplar_spec = exemplar_class_spec(str(cell["exemplar_class_id"]))
        expected_allowed_actions = list(
            operation_set_for_exemplar(
                role_family=family,
                exemplar_class_id=str(cell["exemplar_class_id"]),
            )
        )
        expected_allowed_profiles = list(
            family_spec["backstop_profiles"]
            if str(cell["tissue_variant_id"]) == "continuity_backstop"
            else family_spec["allowed_profiles"]
        )
        assert family in CELL_FAMILY_IDS
        assert tuple(cell["allowed_profiles"]) == tuple(expected_allowed_profiles)
        assert tuple(cell["backstop_profiles"]) == tuple(family_spec["backstop_profiles"])
        assert tuple(cell["allowed_actions"]) == tuple(expected_allowed_actions)
        assert tuple(cell["allowed_operation_set"]) == tuple(expected_allowed_actions)
        assert tuple(cell["forbidden_actions"]) == tuple(family_spec["forbidden_actions"])
        assert tuple(cell["blocked_operation_set"]) == tuple(family_spec["forbidden_actions"])
        assert cell["routing_responsibility"] == family_spec["routing_responsibility"]
        assert cell["activation_budget_class"] == family_spec["activation_budget_class"]
        assert cell["dormancy_behavior_class"] in {
            family_spec["dormancy_behavior_class"],
            exemplar_spec["dormancy_behavior_override"],
        }
        assert cell["continuity_requirement_class"] in {
            family_spec["continuity_requirement_class"],
            exemplar_spec["continuity_requirement_override"],
        }
        assert cell["evidence_requirement_class"] in {
            family_spec["evidence_requirement_class"],
            exemplar_spec["evidence_requirement_override"],
        }
        assert cell["export_visibility_class"] in {
            family_spec["export_visibility_class"],
            exemplar_spec["export_visibility_override"],
        }
        assert cell["sandbox_policy_class"] == ("required" if cell["requires_wasm_sandbox"] else "not_required")
        assert cell["tissue_specialization_tag"] == tissue_spec["specialization_tag"]
        assert cell["contract_variant"] == f"{family}:{cell['tissue_variant_id']}:{cell['exemplar_class_id']}"
        assert cell["policy_envelope"]["allowed_profile_pattern"] == "+".join(cell["allowed_profiles"])
        assert cell["policy_envelope"]["routing_responsibility"] == family_spec["routing_responsibility"]
        assert cell["policy_envelope"]["activation_mode"] == "profile_bounded"
        assert int(cell["policy_envelope"]["activation_priority_floor"]) <= int(
            cell["policy_envelope"]["activation_priority_ceiling"]
        )
        family_contract_variant_counts[family][str(cell["contract_variant"])] = (
            family_contract_variant_counts[family].get(str(cell["contract_variant"]), 0) + 1
        )
        family_exemplar_counts[family][str(cell["exemplar_class_id"])] = (
            family_exemplar_counts[family].get(str(cell["exemplar_class_id"]), 0) + 1
        )
        family_tissue_variant_counts[family][str(cell["tissue_variant_id"])] = (
            family_tissue_variant_counts[family].get(str(cell["tissue_variant_id"]), 0) + 1
        )
    assert manifest["cell_count"] == 1024
    assert manifest["family_count"] == 16
    assert all(count == 64 for count in family_counts.values())
    assert len(family_signatures) == 16
    assert len(set(family_signatures.values())) == 16
    assert all(len(counts) == 8 and all(value == 8 for value in counts.values()) for counts in family_contract_variant_counts.values())
    assert all(len(counts) == 8 and all(value == 8 for value in counts.values()) for counts in family_exemplar_counts.values())
    assert all(counts == {"primary_path": 32, "continuity_backstop": 32} for counts in family_tissue_variant_counts.values())
    assert manifest["contract_variant_count"] == 128
    assert all(count == 8 for count in manifest["contract_variant_counts"].values())
    assert manifest["allowed_profile_pattern_count"] == 3
    assert manifest["activation_budget_class_count"] == 6
    assert manifest["export_visibility_class_count"] == 4
    assert manifest["dormancy_behavior_class_count"] == 3
    assert manifest["continuity_requirement_class_count"] == 3
    assert manifest["evidence_requirement_class_count"] == 7
    assert manifest["tissue_variant_count"] == 2
    assert manifest["operation_set_signature_count"] == 80
    assert manifest["exemplar_class_counts"] == {
        "anchor": 128,
        "audit": 128,
        "bridge": 128,
        "checkpoint": 128,
        "handoff": 128,
        "operator": 128,
        "recovery": 128,
        "reserve": 128,
    }
    assert manifest["sandbox_required_cell_count"] == 256
    assert manifest["audit_replay_required_cell_count"] == 512
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "exact-logical-cell-count", "result": "pass"},
            {"id": "family-differentiation-unique", "result": "pass"},
            {"id": "constraint-diversity-bounded", "result": "pass"},
            {"id": "exemplar-structure-bounded", "result": "pass"},
        ],
        anchors={
            "cell_manifest": manifest,
            "family_signatures": family_signatures,
        },
        notes=[
            "the Phase 14 cell manifest is literal and generated from AGIFCore-owned structure rules",
            "family differentiation is machine-checkable through stable family signatures",
            "constraint diversity and exemplar structure are bounded and machine-readable",
        ],
    )


def main() -> int:
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    missing = vc.missing_files(checked_files)
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=checked_files,
            assertion_ids=ASSERTION_IDS,
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="cell manifest verifier could not import its runtime modules or found missing files",
            missing=missing,
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    try:
        report = build_pass_report()
    except Exception as exc:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=checked_files,
            assertion_ids=ASSERTION_IDS,
            blocker_kind="verification_failed",
            blocker_message=str(exc),
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    vc.write_report(REPORT_PATH, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
