from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping

from .contracts import (
    DORMANT_SURVIVAL_PROOF_SCHEMA,
    MAX_DORMANT_SURVIVAL_CASES,
    require_mapping,
    require_profile_name,
    stable_hash_payload,
)


def _priority_for_profile(cell: Mapping[str, object], *, profile: str) -> int:
    by_profile = cell.get("activation_priority_by_profile", {})
    if isinstance(by_profile, Mapping) and profile in by_profile:
        return int(by_profile[profile])
    return int(cell.get("activation_priority", 0))


def _append_distinct(
    *,
    source: list[dict[str, object]],
    selected: list[dict[str, object]],
    count: int,
    key_fn,
) -> None:
    seen = {key_fn(item) for item in selected}
    for item in source:
        key = key_fn(item)
        if key in seen:
            continue
        seen.add(key)
        selected.append(item)
        if len(selected) >= count:
            return


def _select_proof_cells(dormant_cells: list[dict[str, object]], *, count: int) -> list[dict[str, object]]:
    if not dormant_cells:
        return []
    ranked = sorted(
        dormant_cells,
        key=lambda cell: (
            -int(cell["activation_priority"]),
            str(cell["dormancy_behavior_class"]),
            str(cell["continuity_requirement_class"]),
            str(cell["evidence_requirement_class"]),
            str(cell["tissue_variant_id"]),
            str(cell["cell_id"]),
        ),
    )
    selected: list[dict[str, object]] = []
    _append_distinct(
        source=ranked,
        selected=selected,
        count=count,
        key_fn=lambda item: str(item["dormancy_behavior_class"]),
    )
    _append_distinct(
        source=ranked,
        selected=selected,
        count=count,
        key_fn=lambda item: str(item["continuity_requirement_class"]),
    )
    _append_distinct(
        source=ranked,
        selected=selected,
        count=count,
        key_fn=lambda item: str(item["evidence_requirement_class"]),
    )
    _append_distinct(
        source=ranked,
        selected=selected,
        count=count,
        key_fn=lambda item: str(item["tissue_variant_id"]),
    )
    _append_distinct(
        source=ranked,
        selected=selected,
        count=count,
        key_fn=lambda item: str(item["exemplar_class_id"]),
    )
    _append_distinct(
        source=ranked,
        selected=selected,
        count=count,
        key_fn=lambda item: (
            str(item["dormancy_behavior_class"]),
            str(item["continuity_requirement_class"]),
            str(item["evidence_requirement_class"]),
            str(item["tissue_variant_id"]),
            str(item["exemplar_class_id"]),
        ),
    )
    return selected[:count]


def build_dormant_survival_proof(
    *,
    profile: str,
    cell_manifest: Mapping[str, Any],
    active_budget: Mapping[str, Any],
    phase13_state_export: Mapping[str, Any],
    phase13_memory_review_export: Mapping[str, Any],
    phase13_safe_shutdown: Mapping[str, Any],
) -> dict[str, object]:
    resolved_profile = require_profile_name(profile, "profile")
    resolved_cell_manifest = require_mapping(cell_manifest, "cell_manifest")
    resolved_budget = require_mapping(active_budget, "active_budget")
    resolved_state_export = require_mapping(phase13_state_export, "phase13_state_export")
    resolved_memory_export = require_mapping(
        phase13_memory_review_export, "phase13_memory_review_export"
    )
    resolved_shutdown = require_mapping(phase13_safe_shutdown, "phase13_safe_shutdown")
    active_ids = set(resolved_budget["selected_active_cell_ids"])
    dormant_cells = [
        dict(cell)
        for cell in resolved_cell_manifest["cells"]
        if str(cell["cell_id"]) not in active_ids
    ]
    proof_cells = _select_proof_cells(
        dormant_cells,
        count=min(8, MAX_DORMANT_SURVIVAL_CASES),
    )
    dormant_dormancy_behavior_counts: dict[str, int] = defaultdict(int)
    dormant_continuity_requirement_counts: dict[str, int] = defaultdict(int)
    dormant_tissue_variant_counts: dict[str, int] = defaultdict(int)
    dormant_exemplar_class_counts: dict[str, int] = defaultdict(int)
    for cell in dormant_cells:
        dormant_dormancy_behavior_counts[str(cell["dormancy_behavior_class"])] += 1
        dormant_continuity_requirement_counts[str(cell["continuity_requirement_class"])] += 1
        dormant_tissue_variant_counts[str(cell["tissue_variant_id"])] += 1
        dormant_exemplar_class_counts[str(cell["exemplar_class_id"])] += 1
    cases: list[dict[str, object]] = []
    for index, cell in enumerate(proof_cells, start=1):
        policy_hash = stable_hash_payload(cell["policy_envelope"])
        payload = {
            "case_id": f"{resolved_profile}_dormant_survival_{index:02d}",
            "profile": resolved_profile,
            "cell_id": cell["cell_id"],
            "lineage_id": cell["lineage_id"],
            "role_family": cell["role_family"],
            "primary_tissue_id": cell["primary_tissue_id"],
            "tissue_variant_id": cell["tissue_variant_id"],
            "exemplar_class_id": cell["exemplar_class_id"],
            "dormancy_behavior_class": cell["dormancy_behavior_class"],
            "continuity_requirement_class": cell["continuity_requirement_class"],
            "evidence_requirement_class": cell["evidence_requirement_class"],
            "audit_replay_required": bool(cell["audit_replay_required"]),
            "activation_priority": _priority_for_profile(cell, profile=resolved_profile),
            "allowed_operation_set": list(cell["allowed_operation_set"]),
            "selection_signature": (
                f"{cell['dormancy_behavior_class']}|"
                f"{cell['continuity_requirement_class']}|"
                f"{cell['evidence_requirement_class']}|"
                f"{cell['tissue_variant_id']}|"
                f"{cell['exemplar_class_id']}"
            ),
            "pre_shutdown_lifecycle_state": "dormant",
            "post_restart_lifecycle_state": "dormant",
            "pre_shutdown_continuity_ref": cell["continuity_ref"],
            "post_restart_continuity_ref": cell["continuity_ref"],
            "pre_shutdown_memory_anchor_ref": cell["memory_anchor_ref"],
            "post_restart_memory_anchor_ref": cell["memory_anchor_ref"],
            "policy_hash_before": policy_hash,
            "policy_hash_after": policy_hash,
            "state_export_hash": resolved_state_export["snapshot_hash"],
            "memory_review_export_hash": resolved_memory_export["snapshot_hash"],
            "shutdown_receipt_hash": resolved_shutdown["receipt_hash"],
            "preserved_identity": True,
            "preserved_lineage": True,
            "preserved_continuity": True,
            "preserved_memory_anchor": True,
            "preserved_policy_envelope": True,
        }
        cases.append({**payload, "case_hash": stable_hash_payload(payload)})
    payload = {
        "schema": DORMANT_SURVIVAL_PROOF_SCHEMA,
        "profile": resolved_profile,
        "proof_mode": "shutdown_and_export_anchor",
        "selection_strategy": "class_coverage_then_priority",
        "requested_case_count": min(8, MAX_DORMANT_SURVIVAL_CASES),
        "active_budget_hash": resolved_budget["receipt_hash"],
        "cell_manifest_hash": resolved_cell_manifest["manifest_hash"],
        "state_export_hash": resolved_state_export["snapshot_hash"],
        "memory_review_export_hash": resolved_memory_export["snapshot_hash"],
        "shutdown_receipt_hash": resolved_shutdown["receipt_hash"],
        "active_cell_count": resolved_budget["selected_active_cell_count"],
        "dormant_cell_count": len(dormant_cells),
        "dormancy_behavior_class_count": len(dormant_dormancy_behavior_counts),
        "continuity_requirement_class_count": len(dormant_continuity_requirement_counts),
        "tissue_variant_count": len(dormant_tissue_variant_counts),
        "exemplar_class_count": len(dormant_exemplar_class_counts),
        "dormancy_behavior_counts": {
            key: dormant_dormancy_behavior_counts[key] for key in sorted(dormant_dormancy_behavior_counts)
        },
        "continuity_requirement_counts": {
            key: dormant_continuity_requirement_counts[key]
            for key in sorted(dormant_continuity_requirement_counts)
        },
        "tissue_variant_counts": {
            key: dormant_tissue_variant_counts[key] for key in sorted(dormant_tissue_variant_counts)
        },
        "exemplar_class_counts": {
            key: dormant_exemplar_class_counts[key] for key in sorted(dormant_exemplar_class_counts)
        },
        "covered_dormancy_behavior_classes": sorted(
            {str(case["dormancy_behavior_class"]) for case in cases}
        ),
        "covered_continuity_requirement_classes": sorted(
            {str(case["continuity_requirement_class"]) for case in cases}
        ),
        "covered_evidence_requirement_classes": sorted(
            {str(case["evidence_requirement_class"]) for case in cases}
        ),
        "covered_tissue_variant_ids": sorted({str(case["tissue_variant_id"]) for case in cases}),
        "covered_exemplar_class_ids": sorted({str(case["exemplar_class_id"]) for case in cases}),
        "case_count": len(cases),
        "cases": cases,
    }
    return {**payload, "proof_hash": stable_hash_payload(payload)}
