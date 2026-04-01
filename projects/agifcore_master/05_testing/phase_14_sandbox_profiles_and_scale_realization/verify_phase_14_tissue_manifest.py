from __future__ import annotations

import json

import _phase_14_verifier_common as vc
from agifcore_phase14_sandbox.contracts import CELL_FAMILY_IDS, tissue_variant_spec

VERIFIER = "verify_phase_14_tissue_manifest"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_tissue_manifest.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_14_tissue_manifest_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase14_sandbox.contracts",
    "agifcore_phase14_sandbox.tissue_manifest",
    "agifcore_phase14_sandbox.sandbox_profile_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "tissue-count-within-locked-band",
    "exact-tissue-count",
    "tissue-specialization-unique",
    "profile-cap-diversity-stable",
]


def _tissue_signature(tissue: dict[str, object]) -> tuple[object, ...]:
    return (
        str(tissue["tissue_variant_id"]),
        str(tissue["specialization_tag"]),
        str(tissue["tissue_focus"]),
        str(tissue["evidence_lane"]),
        str(tissue["continuity_handling_class"]),
        str(tissue["escalation_handling_class"]),
        tuple(sorted(tissue["allowed_family_mix"])),
        tuple(tissue["exemplar_class_ids"]),
        tuple(sorted(tissue["active_cell_cap_by_profile"].items())),
        tuple(sorted(tissue["activation_priority_boost_by_profile"].items())),
    )


def build_pass_report() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    manifest = result["shell"].tissue_manifest()
    tissue_signatures: dict[str, tuple[object, ...]] = {}
    variant_occurrences: dict[str, int] = {"primary_path": 0, "continuity_backstop": 0}
    for tissue in manifest["tissues"]:
        tissue_id = str(tissue["tissue_id"])
        signature = _tissue_signature(tissue)
        variant_spec = tissue_variant_spec(str(tissue["tissue_variant_id"]))
        variant_occurrences[str(tissue["tissue_variant_id"])] += 1
        if tissue_id in tissue_signatures:
            assert tissue_signatures[tissue_id] == signature
        else:
            tissue_signatures[tissue_id] = signature
        assert str(tissue["specialization_tag"]) == str(variant_spec["specialization_tag"])
        assert str(tissue["tissue_focus"]) == str(variant_spec["tissue_focus"])
        assert str(tissue["evidence_lane"]) == str(variant_spec["evidence_lane"])
        assert str(tissue["continuity_handling_class"]) == str(variant_spec["continuity_handling_class"])
        assert str(tissue["escalation_handling_class"]) == str(variant_spec["escalation_handling_class"])
        assert list(tissue["exemplar_class_ids"]) == list(variant_spec["exemplar_class_ids"])
        assert tissue["active_cell_cap_by_profile"] == variant_spec["active_cell_cap_by_profile"]
        assert tissue["activation_priority_boost_by_profile"] == variant_spec["activation_priority_boost_by_profile"]
        assert tissue["logical_cell_count"] == 32
        assert set(tissue["allowed_family_mix"]).issubset(set(CELL_FAMILY_IDS))
        assert str(tissue["focus_family"]) in tissue["allowed_family_mix"]
    assert 24 <= manifest["tissue_count"] <= 40
    assert manifest["tissue_count"] == 32
    assert manifest["tissue_variant_count"] == 2
    assert manifest["tissue_variant_counts"] == {
        "continuity_backstop": 16,
        "primary_path": 16,
    }
    assert variant_occurrences == {
        "primary_path": 16,
        "continuity_backstop": 16,
    }
    assert manifest["focus_family_tissue_counts"] == {
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
    assert all(
        tissue["active_cell_cap_by_profile"]
        == tissue_variant_spec(str(tissue["tissue_variant_id"]))["active_cell_cap_by_profile"]
        for tissue in manifest["tissues"]
    )
    assert all(
        tissue["activation_priority_boost_by_profile"]
        == tissue_variant_spec(str(tissue["tissue_variant_id"]))["activation_priority_boost_by_profile"]
        for tissue in manifest["tissues"]
    )
    assert manifest["continuity_handling_class_counts"] == {
        "checkpoint_guard": 16,
        "inline_handoff": 16,
    }
    assert manifest["escalation_handling_class_counts"] == {
        "forward_escalation": 16,
        "stabilize_then_escalate": 16,
    }
    assert manifest["per_profile_total_active_cap"] == {
        "builder": 256,
        "laptop": 128,
        "mobile": 48,
    }
    assert len(tissue_signatures) == 32
    assert len(set(tissue_signatures.values())) == 32
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "tissue-count-within-locked-band", "result": "pass"},
            {"id": "exact-tissue-count", "result": "pass"},
            {"id": "tissue-specialization-unique", "result": "pass"},
            {"id": "profile-cap-diversity-stable", "result": "pass"},
        ],
        anchors={
            "tissue_manifest": manifest,
            "tissue_signatures": tissue_signatures,
        },
        notes=[
            "the tissue manifest preserves a literal 32-tissue realization inside the locked 24-40 band",
            "tissue specialization is machine-checkable through stable tissue signatures and profile caps",
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
            blocker_message="tissue manifest verifier could not import its runtime modules or found missing files",
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
