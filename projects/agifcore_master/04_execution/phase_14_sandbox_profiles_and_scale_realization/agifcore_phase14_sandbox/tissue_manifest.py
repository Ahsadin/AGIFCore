from __future__ import annotations

from collections import defaultdict

from .contracts import (
    LOCKED_TISSUE_BAND,
    LOCKED_TISSUE_COUNT,
    PROFILE_NAMES,
    TISSUE_MANIFEST_SCHEMA,
    stable_hash_payload,
    tissue_variant_spec,
)


def build_tissue_manifest(*, cell_manifest: dict[str, object]) -> dict[str, object]:
    cells = list(cell_manifest["cells"])
    cells_by_tissue: dict[str, list[dict[str, object]]] = defaultdict(list)
    for cell in cells:
        cells_by_tissue[str(cell["primary_tissue_id"])].append(cell)
    tissue_ids = sorted(cells_by_tissue)
    if len(tissue_ids) != LOCKED_TISSUE_COUNT:
        raise ValueError("tissue count does not match locked phase-14 tissue count")
    if not (LOCKED_TISSUE_BAND[0] <= len(tissue_ids) <= LOCKED_TISSUE_BAND[1]):
        raise ValueError("tissue count is outside the locked 24-40 band")

    focus_family_by_tissue = {
        tissue_id: str(cells_by_tissue[tissue_id][0]["role_family"]) for tissue_id in tissue_ids
    }
    tissue_variant_counts: dict[str, int] = defaultdict(int)
    focus_family_counts: dict[str, int] = defaultdict(int)
    continuity_handling_counts: dict[str, int] = defaultdict(int)
    escalation_handling_counts: dict[str, int] = defaultdict(int)
    per_profile_total_active_cap = {profile: 0 for profile in PROFILE_NAMES}
    tissues: list[dict[str, object]] = []
    for index, tissue_id in enumerate(tissue_ids):
        member_cells = cells_by_tissue[tissue_id]
        focus_family = str(member_cells[0]["role_family"])
        if any(str(cell["role_family"]) != focus_family for cell in member_cells):
            raise ValueError("tissue contains mixed role families")
        variant_ids = {str(cell["tissue_variant_id"]) for cell in member_cells}
        if len(variant_ids) != 1:
            raise ValueError("tissue contains mixed variant ids")
        tissue_variant_id = next(iter(variant_ids))
        variant_spec = tissue_variant_spec(tissue_variant_id)
        sibling_index = index + 1 if index % 2 == 0 else index - 1
        routing_targets = [
            tissue_ids[sibling_index],
            tissue_ids[(index - 1) % len(tissue_ids)],
            tissue_ids[(index + 1) % len(tissue_ids)],
        ]
        allowed_family_mix = sorted(
            {
                focus_family,
                *(focus_family_by_tissue[item] for item in routing_targets),
            }
        )
        exemplar_class_distribution: dict[str, int] = defaultdict(int)
        dormancy_behavior_distribution: dict[str, int] = defaultdict(int)
        continuity_requirement_distribution: dict[str, int] = defaultdict(int)
        evidence_requirement_distribution: dict[str, int] = defaultdict(int)
        profile_eligibility_patterns: set[str] = set()
        activation_priority_min_by_profile: dict[str, int] = {}
        activation_priority_max_by_profile: dict[str, int] = {}
        for profile in PROFILE_NAMES:
            priorities = [
                int(cell["activation_priority_by_profile"][profile]) for cell in member_cells
            ]
            activation_priority_min_by_profile[profile] = min(priorities)
            activation_priority_max_by_profile[profile] = max(priorities)
        for cell in member_cells:
            exemplar_class_distribution[str(cell["exemplar_class_id"])] += 1
            dormancy_behavior_distribution[str(cell["dormancy_behavior_class"])] += 1
            continuity_requirement_distribution[str(cell["continuity_requirement_class"])] += 1
            evidence_requirement_distribution[str(cell["evidence_requirement_class"])] += 1
            profile_eligibility_patterns.add("+".join(cell["allowed_profiles"]))
        active_caps = {
            profile: int(variant_spec["active_cell_cap_by_profile"][profile]) for profile in PROFILE_NAMES
        }
        for profile, cap in active_caps.items():
            per_profile_total_active_cap[profile] += cap
        payload = {
            "tissue_id": tissue_id,
            "tissue_name": f"{focus_family}_tissue_{(index % 2) + 1}",
            "focus_family": focus_family,
            "logical_cell_count": len(member_cells),
            "cell_ids": [str(cell["cell_id"]) for cell in member_cells],
            "routing_targets": routing_targets,
            "preferred_routing_targets": routing_targets[:2],
            "failover_routing_target": routing_targets[2],
            "allowed_family_mix": allowed_family_mix,
            "tissue_variant_id": tissue_variant_id,
            "specialization_tag": str(variant_spec["specialization_tag"]),
            "tissue_focus": str(variant_spec["tissue_focus"]),
            "evidence_lane": str(variant_spec["evidence_lane"]),
            "continuity_handling_class": str(variant_spec["continuity_handling_class"]),
            "escalation_handling_class": str(variant_spec["escalation_handling_class"]),
            "active_cell_cap_by_profile": active_caps,
            "activation_priority_boost_by_profile": dict(variant_spec["activation_priority_boost_by_profile"]),
            "exemplar_class_ids": [str(item) for item in variant_spec["exemplar_class_ids"]],
            "exemplar_class_distribution": {
                key: exemplar_class_distribution[key] for key in sorted(exemplar_class_distribution)
            },
            "dormancy_behavior_distribution": {
                key: dormancy_behavior_distribution[key] for key in sorted(dormancy_behavior_distribution)
            },
            "continuity_requirement_distribution": {
                key: continuity_requirement_distribution[key]
                for key in sorted(continuity_requirement_distribution)
            },
            "evidence_requirement_distribution": {
                key: evidence_requirement_distribution[key] for key in sorted(evidence_requirement_distribution)
            },
            "profile_eligibility_patterns": sorted(profile_eligibility_patterns),
            "activation_priority_min_by_profile": activation_priority_min_by_profile,
            "activation_priority_max_by_profile": activation_priority_max_by_profile,
            "policy_envelope": {
                "profile_bounded": True,
                "supports_same_public_contract": True,
                "tissue_variant_id": tissue_variant_id,
                "specialization_tag": str(variant_spec["specialization_tag"]),
                "continuity_handling_class": str(variant_spec["continuity_handling_class"]),
                "escalation_handling_class": str(variant_spec["escalation_handling_class"]),
            },
        }
        tissues.append({**payload, "tissue_hash": stable_hash_payload(payload)})
        tissue_variant_counts[tissue_variant_id] += 1
        focus_family_counts[focus_family] += 1
        continuity_handling_counts[str(variant_spec["continuity_handling_class"])] += 1
        escalation_handling_counts[str(variant_spec["escalation_handling_class"])] += 1
    payload = {
        "schema": TISSUE_MANIFEST_SCHEMA,
        "tissue_count": len(tissues),
        "tissue_band": {"min": LOCKED_TISSUE_BAND[0], "max": LOCKED_TISSUE_BAND[1]},
        "total_logical_cell_count": len(cells),
        "tissue_variant_count": len(tissue_variant_counts),
        "tissue_variant_counts": {key: tissue_variant_counts[key] for key in sorted(tissue_variant_counts)},
        "focus_family_tissue_counts": {key: focus_family_counts[key] for key in sorted(focus_family_counts)},
        "continuity_handling_class_counts": {
            key: continuity_handling_counts[key] for key in sorted(continuity_handling_counts)
        },
        "escalation_handling_class_counts": {
            key: escalation_handling_counts[key] for key in sorted(escalation_handling_counts)
        },
        "per_profile_total_active_cap": per_profile_total_active_cap,
        "tissues": tissues,
    }
    return {
        **payload,
        "manifest_hash": stable_hash_payload(payload),
    }
