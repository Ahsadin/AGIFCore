from __future__ import annotations

import json

import _phase_14_verifier_common as vc

VERIFIER = "verify_phase_14_manifest_differentiation"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_manifest_differentiation.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_14_manifest_differentiation_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase14_sandbox.cell_manifest",
    "agifcore_phase14_sandbox.tissue_manifest",
    "agifcore_phase14_sandbox.active_cell_budget",
    "agifcore_phase14_sandbox.dormant_cell_survival",
    "agifcore_phase14_sandbox.profile_manifests",
    "agifcore_phase14_sandbox.sandbox_profile_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "family-differentiation-real",
    "tissue-specialization-real",
    "constraint-diversity-real",
    "exemplar-structure-bounded",
    "budget-selection-uses-priority",
    "dormant-proof-covers-differentiated-classes",
    "manifest-audit-remains-consistent",
]


def build_pass_report() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    summary = vc.build_manifest_differentiation_summary(shell=shell, profile="laptop")
    audit = shell.manifest_audit()

    assert summary["family_count"] == 16
    assert summary["family_signature_count"] == 16
    assert summary["contract_variant_count"] == 128
    assert summary["exemplar_class_count"] == 8
    assert summary["constraint_diversity"] == {
        "allowed_profile_pattern_count": 3,
        "activation_budget_class_count": 6,
        "export_visibility_class_count": 4,
        "dormancy_behavior_class_count": 3,
        "continuity_requirement_class_count": 3,
        "evidence_requirement_class_count": 7,
        "tissue_variant_count": 2,
        "operation_set_signature_count": 80,
        "sandbox_required_cell_count": 256,
        "audit_replay_required_cell_count": 512,
    }
    assert summary["tissue_count"] == 32
    assert summary["tissue_variant_count"] == 2
    assert summary["tissue_signature_count"] == 32
    assert summary["focus_family_tissue_counts"] == {
        "attention": 2,
        "audit_replay": 2,
        "compression_retirement": 2,
        "continuity_self_history": 2,
        "critic_error_monitor": 2,
        "episodic_memory": 2,
        "governance_authority": 2,
        "intake_router": 2,
        "language_realizer": 2,
        "planner": 2,
        "procedural_skill": 2,
        "scheduler_resource": 2,
        "semantic_abstraction": 2,
        "transfer_broker": 2,
        "working_memory": 2,
        "world_model_simulator": 2,
    }
    assert summary["continuity_handling_class_counts"] == {
        "checkpoint_guard": 16,
        "inline_handoff": 16,
    }
    assert summary["escalation_handling_class_counts"] == {
        "forward_escalation": 16,
        "stabilize_then_escalate": 16,
    }
    assert summary["per_profile_total_active_cap"] == {
        "builder": 256,
        "laptop": 128,
        "mobile": 48,
    }

    budget = summary["budget"]
    assert budget["selected_active_cell_count"] == 96
    assert budget["selected_active_tissue_count"] == 22
    assert budget["budget_state"] == "within_budget"
    assert budget["selected_activation_priority_min"] < budget["selected_activation_priority_max"]
    assert len(budget["selected_family_counts"]) > 1
    assert len(budget["selected_exemplar_class_counts"]) > 1
    assert len(budget["selected_tissue_variant_counts"]) == 2
    assert budget["selected_audit_replay_required_count"] > 0
    assert budget["selected_sandbox_required_count"] > 0

    proof = summary["proof"]
    assert proof["case_count"] == 8
    assert proof["dormancy_behavior_class_count"] == 3
    assert proof["continuity_requirement_class_count"] == 3
    assert proof["tissue_variant_count"] == 2
    assert proof["exemplar_class_count"] == 8
    assert len(proof["covered_dormancy_behavior_classes"]) == 3
    assert len(proof["covered_continuity_requirement_classes"]) == 3
    assert len(proof["covered_evidence_requirement_classes"]) == 7
    assert len(proof["covered_tissue_variant_ids"]) == 2
    assert len(proof["covered_exemplar_class_ids"]) == 7

    assert audit["audit_status"] == "pass"
    assert audit["logical_cell_count"] == 1024
    assert audit["tissue_count"] == 32
    assert audit["profile_count"] == 3
    assert audit["same_contract_hash_count"] == 1

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "family-differentiation-real", "result": "pass"},
            {"id": "tissue-specialization-real", "result": "pass"},
            {"id": "constraint-diversity-real", "result": "pass"},
            {"id": "exemplar-structure-bounded", "result": "pass"},
            {"id": "budget-selection-uses-priority", "result": "pass"},
            {"id": "dormant-proof-covers-differentiated-classes", "result": "pass"},
            {"id": "manifest-audit-remains-consistent", "result": "pass"},
        ],
        anchors={
            "manifest_differentiation": summary,
            "manifest_audit": audit,
        },
        notes=[
            "family differentiation is proven through stable family signatures and per-family structural counts",
            "tissue specialization is proven through variant counts, focus counts, and profile caps",
            "budget and dormant proofs consume the differentiated structure and remain bounded",
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
            blocker_message="manifest differentiation verifier could not import its runtime modules or found missing files",
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
