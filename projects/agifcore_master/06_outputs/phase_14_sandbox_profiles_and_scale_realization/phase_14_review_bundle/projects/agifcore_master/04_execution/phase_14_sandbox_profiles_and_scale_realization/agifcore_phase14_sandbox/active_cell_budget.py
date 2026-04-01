from __future__ import annotations

from collections import defaultdict
import math
from typing import Any, Mapping

from .contracts import (
    ACTIVE_BUDGET_STATE_IDS,
    ACTIVE_CELL_BUDGET_SCHEMA,
    MAX_ACTIVE_BUDGET_STATES,
    PROFILE_ACTIVE_BANDS,
    PROFILE_CELLS_PER_ACTIVE_TISSUE,
    PROFILE_ACTIVE_TISSUE_COUNTS,
    PROFILE_TARGET_ACTIVE_CELLS,
    require_mapping,
    require_non_negative_int,
    require_profile_name,
    stable_hash_payload,
)


def _cells_by_id(cell_manifest: Mapping[str, Any]) -> dict[str, dict[str, object]]:
    return {
        str(cell["cell_id"]): dict(cell)
        for cell in list(require_mapping(cell_manifest, "cell_manifest")["cells"])
    }


def _eligible_cells_by_tissue(
    *,
    profile: str,
    cell_manifest: Mapping[str, Any],
    tissue_manifest: Mapping[str, Any],
) -> dict[str, list[dict[str, object]]]:
    resolved_profile = require_profile_name(profile, "profile")
    cells = list(require_mapping(cell_manifest, "cell_manifest")["cells"])
    tissues = list(require_mapping(tissue_manifest, "tissue_manifest")["tissues"])
    tissue_ids = {str(tissue["tissue_id"]) for tissue in tissues}
    result = {tissue_id: [] for tissue_id in tissue_ids}
    for cell in cells:
        if resolved_profile not in set(cell["allowed_profiles"]):
            continue
        result[str(cell["primary_tissue_id"])].append(dict(cell))
    for values in result.values():
        values.sort(key=lambda item: str(item["cell_id"]))
    return result


def _default_requested_tissues(profile: str, requested_active_cells: int) -> int:
    per_tissue_target = PROFILE_CELLS_PER_ACTIVE_TISSUE[profile]
    return min(
        PROFILE_ACTIVE_TISSUE_COUNTS[profile],
        max(1, math.ceil(requested_active_cells / per_tissue_target)),
    )


def _cell_priority(cell: Mapping[str, Any], *, profile: str) -> int:
    by_profile = cell.get("activation_priority_by_profile", {})
    if isinstance(by_profile, Mapping) and profile in by_profile:
        return int(by_profile[profile])
    return int(cell.get("activation_priority", 0))


def _select_active_cells(
    *,
    profile: str,
    tissue_manifest: Mapping[str, Any],
    eligible_cells_by_tissue: Mapping[str, list[dict[str, object]]],
    requested_active_cells: int,
    requested_active_tissues: int,
) -> tuple[list[str], list[str], list[dict[str, object]]]:
    selected_cell_ids: list[str] = []
    selected_tissue_ids: list[str] = []
    selection_trace: list[dict[str, object]] = []
    tissues = list(require_mapping(tissue_manifest, "tissue_manifest")["tissues"])
    ordered_tissues = sorted(
        tissues,
        key=lambda tissue: (
            -int(tissue["activation_priority_boost_by_profile"][profile]),
            str(tissue["tissue_id"]),
        ),
    )
    for tissue in ordered_tissues:
        tissue_id = str(tissue["tissue_id"])
        candidates = list(eligible_cells_by_tissue.get(tissue_id, []))
        if not candidates:
            continue
        candidates.sort(
            key=lambda item: (
                -_cell_priority(item, profile=profile),
                -int(bool(item.get("audit_replay_required"))),
                str(item["cell_id"]),
            )
        )
        if len(selected_tissue_ids) >= requested_active_tissues:
            break
        available_slots = min(
            int(tissue["active_cell_cap_by_profile"][profile]),
            requested_active_cells - len(selected_cell_ids),
        )
        if available_slots <= 0:
            break
        selected_tissue_ids.append(tissue_id)
        selected_slice = [str(item["cell_id"]) for item in candidates[:available_slots]]
        selected_cell_ids.extend(selected_slice)
        selection_trace.append(
            {
                "tissue_id": tissue_id,
                "tissue_variant_id": tissue["tissue_variant_id"],
                "specialization_tag": tissue["specialization_tag"],
                "activation_priority_boost": int(tissue["activation_priority_boost_by_profile"][profile]),
                "available_candidate_count": len(candidates),
                "selected_cell_ids": selected_slice,
            }
        )
        if len(selected_cell_ids) >= requested_active_cells:
            break
    return selected_cell_ids, selected_tissue_ids, selection_trace


def build_active_cell_budget(
    *,
    profile: str,
    cell_manifest: Mapping[str, Any],
    tissue_manifest: Mapping[str, Any],
    profile_manifest: Mapping[str, Any],
    requested_active_cells: int | None = None,
    requested_active_tissues: int | None = None,
    requested_cell_ids: list[str] | tuple[str, ...] | None = None,
    current_active_cells: int | None = None,
    current_active_tissues: int | None = None,
) -> dict[str, object]:
    if len(ACTIVE_BUDGET_STATE_IDS) > MAX_ACTIVE_BUDGET_STATES:
        raise ValueError("active budget state count exceeds planning ceiling")
    resolved_profile = require_profile_name(profile, "profile")
    resolved_profile_manifest = require_mapping(profile_manifest, "profile_manifest")
    resolved_cell_manifest = require_mapping(cell_manifest, "cell_manifest")
    resolved_tissue_manifest = require_mapping(tissue_manifest, "tissue_manifest")
    active_band = dict(PROFILE_ACTIVE_BANDS[resolved_profile])
    target_active_cells = PROFILE_TARGET_ACTIVE_CELLS[resolved_profile]
    max_active_cells = active_band["max"]
    min_active_cells = active_band["min"]
    max_active_tissues = PROFILE_ACTIVE_TISSUE_COUNTS[resolved_profile]
    requested_cells = require_non_negative_int(
        requested_active_cells if requested_active_cells is not None else target_active_cells,
        "requested_active_cells",
    )
    requested_tissues = require_non_negative_int(
        requested_active_tissues
        if requested_active_tissues is not None
        else _default_requested_tissues(resolved_profile, requested_cells),
        "requested_active_tissues",
    )
    current_cells = require_non_negative_int(current_active_cells or 0, "current_active_cells")
    current_tissues = require_non_negative_int(current_active_tissues or 0, "current_active_tissues")
    cells_lookup = _cells_by_id(resolved_cell_manifest)
    eligible_cells_by_tissue = _eligible_cells_by_tissue(
        profile=resolved_profile,
        cell_manifest=resolved_cell_manifest,
        tissue_manifest=resolved_tissue_manifest,
    )
    requested_ids = [str(item) for item in (requested_cell_ids or [])]
    invalid_requested_ids = [
        item
        for item in requested_ids
        if item not in cells_lookup or resolved_profile not in set(cells_lookup[item]["allowed_profiles"])
    ]
    selected_active_cell_ids, selected_active_tissue_ids, selection_trace = _select_active_cells(
        profile=resolved_profile,
        tissue_manifest=resolved_tissue_manifest,
        eligible_cells_by_tissue=eligible_cells_by_tissue,
        requested_active_cells=min(requested_cells, max_active_cells),
        requested_active_tissues=min(requested_tissues, max_active_tissues),
    )
    dormant_cell_ids = [
        str(cell["cell_id"])
        for cell in resolved_cell_manifest["cells"]
        if str(cell["cell_id"]) not in set(selected_active_cell_ids)
    ]
    selected_active_cells = [cells_lookup[item] for item in selected_active_cell_ids if item in cells_lookup]
    selected_family_counts: dict[str, int] = defaultdict(int)
    selected_exemplar_class_counts: dict[str, int] = defaultdict(int)
    selected_tissue_variant_counts: dict[str, int] = defaultdict(int)
    selected_dormancy_behavior_counts: dict[str, int] = defaultdict(int)
    selected_continuity_requirement_counts: dict[str, int] = defaultdict(int)
    selected_priority_values: list[int] = []
    selected_audit_replay_required_count = 0
    selected_sandbox_required_count = 0
    for cell in selected_active_cells:
        selected_family_counts[str(cell["role_family"])] += 1
        selected_exemplar_class_counts[str(cell["exemplar_class_id"])] += 1
        selected_tissue_variant_counts[str(cell["tissue_variant_id"])] += 1
        selected_dormancy_behavior_counts[str(cell["dormancy_behavior_class"])] += 1
        selected_continuity_requirement_counts[str(cell["continuity_requirement_class"])] += 1
        selected_priority_values.append(_cell_priority(cell, profile=resolved_profile))
        if bool(cell.get("audit_replay_required")):
            selected_audit_replay_required_count += 1
        if bool(cell.get("requires_wasm_sandbox")):
            selected_sandbox_required_count += 1
    hibernate_candidate_ids: list[str] = []
    if current_cells > max_active_cells or current_tissues > max_active_tissues:
        hibernate_count = max(current_cells - max_active_cells, 0)
        low_priority_first = sorted(
            selected_active_cells,
            key=lambda cell: (
                _cell_priority(cell, profile=resolved_profile),
                str(cell["cell_id"]),
            ),
        )
        hibernate_candidate_ids = [
            str(cell["cell_id"]) for cell in low_priority_first[:hibernate_count]
        ]
        budget_state = "hibernate_required"
        allowed = False
        enforcement_action = "hibernate"
        reason_code = "ACTIVE_CELL_BUDGET_HIBERNATE_REQUIRED"
    elif invalid_requested_ids:
        budget_state = "profile_mismatch"
        allowed = False
        enforcement_action = "deny"
        reason_code = "PROFILE_NOT_ALLOWED"
    elif requested_cells > max_active_cells or requested_tissues > max_active_tissues:
        budget_state = "ceiling_blocked"
        allowed = False
        enforcement_action = "deny"
        reason_code = "ACTIVE_CELL_BUDGET_EXCEEDED"
    elif requested_cells > target_active_cells or requested_tissues > _default_requested_tissues(
        resolved_profile, target_active_cells
    ):
        budget_state = "near_ceiling"
        allowed = True
        enforcement_action = "admit_with_warning"
        reason_code = "ACTIVE_CELL_BUDGET_NEAR_CEILING"
    else:
        budget_state = "within_budget"
        allowed = True
        enforcement_action = "admit"
        reason_code = "ACTIVE_CELL_BUDGET_WITHIN_LIMITS"
    payload = {
        "schema": ACTIVE_CELL_BUDGET_SCHEMA,
        "profile": resolved_profile,
        "profile_manifest_hash": resolved_profile_manifest["profile_hash"],
        "cell_manifest_hash": resolved_cell_manifest["manifest_hash"],
        "tissue_manifest_hash": resolved_tissue_manifest["manifest_hash"],
        "budget_state_catalog": list(ACTIVE_BUDGET_STATE_IDS),
        "budget_state": budget_state,
        "allowed": allowed,
        "enforcement_action": enforcement_action,
        "reason_code": reason_code,
        "target_active_cells": target_active_cells,
        "requested_active_cells": requested_cells,
        "requested_active_tissues": requested_tissues,
        "current_active_cells": current_cells,
        "current_active_tissues": current_tissues,
        "min_active_cells": min_active_cells,
        "max_active_cells": max_active_cells,
        "max_active_tissues": max_active_tissues,
        "eligible_cell_count": sum(len(items) for items in eligible_cells_by_tissue.values()),
        "selected_active_cell_count": len(selected_active_cell_ids),
        "selected_active_tissue_count": len(selected_active_tissue_ids),
        "selected_active_cell_ids": selected_active_cell_ids,
        "selected_active_tissue_ids": selected_active_tissue_ids,
        "selected_family_counts": {
            key: selected_family_counts[key] for key in sorted(selected_family_counts)
        },
        "selected_exemplar_class_counts": {
            key: selected_exemplar_class_counts[key] for key in sorted(selected_exemplar_class_counts)
        },
        "selected_tissue_variant_counts": {
            key: selected_tissue_variant_counts[key] for key in sorted(selected_tissue_variant_counts)
        },
        "selected_dormancy_behavior_counts": {
            key: selected_dormancy_behavior_counts[key] for key in sorted(selected_dormancy_behavior_counts)
        },
        "selected_continuity_requirement_counts": {
            key: selected_continuity_requirement_counts[key]
            for key in sorted(selected_continuity_requirement_counts)
        },
        "selected_audit_replay_required_count": selected_audit_replay_required_count,
        "selected_sandbox_required_count": selected_sandbox_required_count,
        "selected_activation_priority_min": min(selected_priority_values) if selected_priority_values else 0,
        "selected_activation_priority_max": max(selected_priority_values) if selected_priority_values else 0,
        "selected_activation_priority_total": sum(selected_priority_values),
        "tissue_selection_trace": selection_trace,
        "invalid_requested_cell_ids": invalid_requested_ids,
        "hibernate_candidate_ids": hibernate_candidate_ids,
        "dormant_cell_count": len(dormant_cell_ids),
        "dormant_cell_preview_ids": dormant_cell_ids[:32],
    }
    return {**payload, "receipt_hash": stable_hash_payload(payload)}
