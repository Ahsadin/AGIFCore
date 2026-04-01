from __future__ import annotations

from collections import defaultdict

from .contracts import (
    ACTIVATION_BUDGET_CLASS_PRIORITY,
    CELL_FAMILY_IDS,
    CELL_MANIFEST_SCHEMA,
    CONTINUITY_CLASS_PRIORITY,
    DORMANCY_CLASS_PRIORITY,
    LOCKED_LOGICAL_CELL_COUNT,
    LOCKED_TISSUE_COUNT,
    PROFILE_NAMES,
    SANDBOX_REQUIRED_FAMILIES,
    exemplar_class_spec,
    family_behavior_spec,
    operation_set_for_exemplar,
    stable_hash_payload,
    tissue_variant_for_tissue_index,
    tissue_variant_spec,
)


CELLS_PER_TISSUE = LOCKED_LOGICAL_CELL_COUNT // LOCKED_TISSUE_COUNT
EXEMPLAR_CLASSES_PER_TISSUE = 4
CELLS_PER_EXEMPLAR = CELLS_PER_TISSUE // EXEMPLAR_CLASSES_PER_TISSUE


def _family_for_tissue(tissue_index: int) -> str:
    return CELL_FAMILY_IDS[tissue_index // 2]


def _tissue_id_for_index(tissue_index: int) -> str:
    return f"tissue_{tissue_index + 1:02d}"


def _allowed_profiles_for_cell(*, family_spec: dict[str, object], tissue_variant_id: str) -> tuple[str, ...]:
    if tissue_variant_id == "continuity_backstop":
        return tuple(family_spec.get("backstop_profiles", family_spec["allowed_profiles"]))
    return tuple(family_spec["allowed_profiles"])


def _exemplar_class_id(*, tissue_variant_id: str, tissue_slot: int) -> str:
    variant_spec = tissue_variant_spec(tissue_variant_id)
    exemplar_ids = tuple(variant_spec["exemplar_class_ids"])
    exemplar_index = min(len(exemplar_ids) - 1, tissue_slot // CELLS_PER_EXEMPLAR)
    return str(exemplar_ids[exemplar_index])


def _resolved_allowed_actions(
    *,
    family_spec: dict[str, object],
    exemplar_spec: dict[str, object],
) -> tuple[str, ...]:
    family_actions = tuple(str(item) for item in family_spec["allowed_actions"])
    selected = [
        family_actions[index]
        for index in exemplar_spec["allowed_action_indexes"]
        if 0 <= index < len(family_actions)
    ]
    return tuple(selected or family_actions[:1])


def build_cell_manifest() -> dict[str, object]:
    cells: list[dict[str, object]] = []
    family_counts = {family: 0 for family in CELL_FAMILY_IDS}
    sandbox_required_count = 0
    audit_replay_required_count = 0
    contract_variants: dict[str, int] = defaultdict(int)
    exemplar_class_counts: dict[str, int] = defaultdict(int)
    allowed_profile_pattern_counts: dict[str, int] = defaultdict(int)
    activation_budget_class_counts: dict[str, int] = defaultdict(int)
    export_visibility_class_counts: dict[str, int] = defaultdict(int)
    dormancy_behavior_class_counts: dict[str, int] = defaultdict(int)
    continuity_requirement_class_counts: dict[str, int] = defaultdict(int)
    evidence_requirement_class_counts: dict[str, int] = defaultdict(int)
    tissue_variant_counts: dict[str, int] = defaultdict(int)
    operation_set_signature_counts: dict[str, int] = defaultdict(int)
    cell_number = 0
    for tissue_index in range(LOCKED_TISSUE_COUNT):
        tissue_id = _tissue_id_for_index(tissue_index)
        role_family = _family_for_tissue(tissue_index)
        family_spec = family_behavior_spec(role_family)
        tissue_variant_id = tissue_variant_for_tissue_index(tissue_index)
        tissue_spec = tissue_variant_spec(tissue_variant_id)
        requires_sandbox = role_family in SANDBOX_REQUIRED_FAMILIES
        for tissue_slot in range(CELLS_PER_TISSUE):
            cell_number += 1
            lineage_number = ((cell_number - 1) // 4) + 1
            exemplar_class_id = _exemplar_class_id(
                tissue_variant_id=tissue_variant_id,
                tissue_slot=tissue_slot,
            )
            exemplar_spec = exemplar_class_spec(exemplar_class_id)
            allowed_profiles = _allowed_profiles_for_cell(
                family_spec=family_spec,
                tissue_variant_id=tissue_variant_id,
            )
            allowed_actions = _resolved_allowed_actions(
                family_spec=family_spec,
                exemplar_spec=exemplar_spec,
            )
            allowed_operation_set = operation_set_for_exemplar(
                role_family=role_family,
                exemplar_class_id=exemplar_class_id,
            )
            export_visibility_class = str(
                exemplar_spec["export_visibility_override"] or family_spec["export_visibility_class"]
            )
            dormancy_behavior_class = str(
                exemplar_spec["dormancy_behavior_override"] or family_spec["dormancy_behavior_class"]
            )
            continuity_requirement_class = str(
                exemplar_spec["continuity_requirement_override"]
                or family_spec["continuity_requirement_class"]
            )
            evidence_requirement_class = str(
                exemplar_spec["evidence_requirement_override"]
                or family_spec["evidence_requirement_class"]
            )
            activation_priority_base = (
                ACTIVATION_BUDGET_CLASS_PRIORITY[str(family_spec["activation_budget_class"])]
                + int(exemplar_spec["activation_priority_offset"])
            )
            slot_penalty = tissue_slot // CELLS_PER_EXEMPLAR
            activation_priority_by_profile = {
                profile: activation_priority_base
                + int(tissue_spec["activation_priority_boost_by_profile"][profile])
                - slot_penalty
                for profile in PROFILE_NAMES
            }
            contract_variant = f"{role_family}:{tissue_variant_id}:{exemplar_class_id}"
            allowed_profile_pattern = "+".join(allowed_profiles)
            operation_signature = "|".join(allowed_operation_set)
            constraint_tags = [
                f"variant:{tissue_variant_id}",
                f"dormancy:{dormancy_behavior_class}",
                f"continuity:{continuity_requirement_class}",
                f"evidence:{evidence_requirement_class}",
                "sandbox_required" if requires_sandbox else "sandbox_optional",
                "audit_replay_required" if bool(family_spec["audit_replay_required"]) else "audit_replay_optional",
            ]
            payload = {
                "cell_id": f"cell_{cell_number:04d}",
                "lineage_id": f"lineage_{lineage_number:04d}",
                "role_family": role_family,
                "role_name": f"{role_family}_{tissue_slot + 1:02d}",
                "primary_tissue_id": tissue_id,
                "allowed_profiles": list(allowed_profiles),
                "backstop_profiles": list(family_spec["backstop_profiles"]),
                "default_lifecycle_state": "dormant",
                "bundle_ref": f"bundle::{role_family}::{cell_number:04d}",
                "continuity_ref": f"continuity::{lineage_number:04d}::{cell_number:04d}",
                "memory_anchor_ref": f"memory::{lineage_number:04d}",
                "requires_wasm_sandbox": requires_sandbox,
                "allowed_actions": list(allowed_actions),
                "allowed_operation_set": list(allowed_operation_set),
                "forbidden_actions": list(family_spec["forbidden_actions"]),
                "blocked_operation_set": list(family_spec["forbidden_actions"]),
                "routing_responsibility": family_spec["routing_responsibility"],
                "activation_budget_class": family_spec["activation_budget_class"],
                "activation_priority": max(activation_priority_by_profile.values()),
                "activation_priority_by_profile": activation_priority_by_profile,
                "export_visibility_class": export_visibility_class,
                "dormancy_behavior_class": dormancy_behavior_class,
                "continuity_requirement_class": continuity_requirement_class,
                "evidence_requirement_class": evidence_requirement_class,
                "audit_replay_required": bool(family_spec["audit_replay_required"]),
                "sandbox_policy_class": "required" if requires_sandbox else "not_required",
                "exemplar_class_id": exemplar_class_id,
                "contract_variant": contract_variant,
                "tissue_variant_id": tissue_variant_id,
                "tissue_specialization_tag": str(tissue_spec["specialization_tag"]),
                "constraint_tags": constraint_tags,
                "policy_envelope": {
                    "activation_mode": "profile_bounded",
                    "requires_wasm_sandbox": requires_sandbox,
                    "role_family": role_family,
                    "export_visibility_class": export_visibility_class,
                    "dormancy_behavior_class": dormancy_behavior_class,
                    "continuity_requirement_class": continuity_requirement_class,
                    "evidence_requirement_class": evidence_requirement_class,
                    "routing_responsibility": str(family_spec["routing_responsibility"]),
                    "activation_priority_floor": min(activation_priority_by_profile.values()),
                    "activation_priority_ceiling": max(activation_priority_by_profile.values()),
                    "dormancy_priority": int(DORMANCY_CLASS_PRIORITY[dormancy_behavior_class]),
                    "continuity_priority": int(CONTINUITY_CLASS_PRIORITY[continuity_requirement_class]),
                    "allowed_profile_pattern": allowed_profile_pattern,
                },
            }
            cells.append({**payload, "cell_hash": stable_hash_payload(payload)})
            family_counts[role_family] += 1
            if requires_sandbox:
                sandbox_required_count += 1
            if bool(family_spec["audit_replay_required"]):
                audit_replay_required_count += 1
            contract_variants[contract_variant] += 1
            exemplar_class_counts[exemplar_class_id] += 1
            allowed_profile_pattern_counts[allowed_profile_pattern] += 1
            activation_budget_class_counts[str(family_spec["activation_budget_class"])] += 1
            export_visibility_class_counts[export_visibility_class] += 1
            dormancy_behavior_class_counts[dormancy_behavior_class] += 1
            continuity_requirement_class_counts[continuity_requirement_class] += 1
            evidence_requirement_class_counts[evidence_requirement_class] += 1
            tissue_variant_counts[tissue_variant_id] += 1
            operation_set_signature_counts[operation_signature] += 1
    payload = {
        "schema": CELL_MANIFEST_SCHEMA,
        "cell_count": len(cells),
        "tissue_count": LOCKED_TISSUE_COUNT,
        "family_count": len(CELL_FAMILY_IDS),
        "family_counts": family_counts,
        "sandbox_required_family_ids": list(SANDBOX_REQUIRED_FAMILIES),
        "sandbox_required_cell_count": sandbox_required_count,
        "audit_replay_required_cell_count": audit_replay_required_count,
        "contract_variant_count": len(contract_variants),
        "contract_variant_counts": {key: contract_variants[key] for key in sorted(contract_variants)},
        "exemplar_class_ids": sorted(exemplar_class_counts),
        "exemplar_class_counts": {
            key: exemplar_class_counts[key] for key in sorted(exemplar_class_counts)
        },
        "allowed_profile_pattern_count": len(allowed_profile_pattern_counts),
        "allowed_profile_pattern_counts": {
            key: allowed_profile_pattern_counts[key] for key in sorted(allowed_profile_pattern_counts)
        },
        "activation_budget_class_count": len(activation_budget_class_counts),
        "activation_budget_class_counts": {
            key: activation_budget_class_counts[key] for key in sorted(activation_budget_class_counts)
        },
        "export_visibility_class_count": len(export_visibility_class_counts),
        "export_visibility_class_counts": {
            key: export_visibility_class_counts[key] for key in sorted(export_visibility_class_counts)
        },
        "dormancy_behavior_class_count": len(dormancy_behavior_class_counts),
        "dormancy_behavior_class_counts": {
            key: dormancy_behavior_class_counts[key] for key in sorted(dormancy_behavior_class_counts)
        },
        "continuity_requirement_class_count": len(continuity_requirement_class_counts),
        "continuity_requirement_class_counts": {
            key: continuity_requirement_class_counts[key]
            for key in sorted(continuity_requirement_class_counts)
        },
        "evidence_requirement_class_count": len(evidence_requirement_class_counts),
        "evidence_requirement_class_counts": {
            key: evidence_requirement_class_counts[key] for key in sorted(evidence_requirement_class_counts)
        },
        "tissue_variant_count": len(tissue_variant_counts),
        "tissue_variant_counts": {key: tissue_variant_counts[key] for key in sorted(tissue_variant_counts)},
        "operation_set_signature_count": len(operation_set_signature_counts),
        "operation_set_signature_counts": {
            key: operation_set_signature_counts[key] for key in sorted(operation_set_signature_counts)
        },
        "cells": cells,
    }
    return {
        **payload,
        "manifest_hash": stable_hash_payload(payload),
    }
