from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    FAIL_CLOSED_CATALOG_SCHEMA,
    MAX_FAIL_CLOSED_STATES,
    bounded_unique,
    build_blocked_surface_record,
    normalize_support_state,
    stable_hash_payload,
)


def build_fail_closed_catalog(
    *,
    phase10_turn_state: Mapping[str, Any],
    phase11_cycle_state: Mapping[str, Any],
    phase12_cycle_state: Mapping[str, Any],
) -> dict[str, Any]:
    phase10_overlay = dict(phase10_turn_state.get("overlay_contract", {}))
    phase11_overlay = dict(phase11_cycle_state.get("overlay_contract", {}))
    phase12_overlay = dict(phase12_cycle_state.get("overlay_contract", {}))
    support_state = normalize_support_state(str(phase12_overlay.get("support_state", "unknown")))
    evidence_refs = bounded_unique(
        [
            *list(phase10_overlay.get("evidence_refs", [])),
            *list(phase11_overlay.get("evidence_refs", [])),
            *list(phase12_overlay.get("evidence_refs", [])),
        ],
        ceiling=12,
        field_name="catalog_evidence_refs",
    )
    states = [
        build_blocked_surface_record(
            surface_name="task_submit",
            reason_code="reserved_surface_fail_closed",
            user_guidance="Task submission stays blocked in the first Phase 13 slice. Use conversation_turn instead.",
            evidence_refs=evidence_refs,
            next_steps=("use conversation_turn", "inspect trace_export"),
        ),
        build_blocked_surface_record(
            surface_name="policy_update",
            reason_code="reserved_surface_fail_closed",
            user_guidance="Policy updates stay blocked in Phase 13 so the product shell cannot self-widen runtime policy.",
            evidence_refs=evidence_refs,
            next_steps=("inspect fail_closed_help", "re-run through a later approved phase only"),
        ),
        build_blocked_surface_record(
            surface_name="gateway_route",
            reason_code="unknown_route",
            user_guidance="The requested local route is not allowlisted for this product shell.",
            evidence_refs=evidence_refs,
            next_steps=("retry with an allowlisted route", "inspect session_open"),
        ),
        build_blocked_surface_record(
            surface_name="gateway_policy",
            reason_code="policy_hash_mismatch",
            user_guidance="The request policy hash does not match the live shell policy, so the gateway fails closed.",
            evidence_refs=evidence_refs,
            next_steps=("refresh session_open", "retry with the returned policy hash"),
        ),
        build_blocked_surface_record(
            surface_name="installer_distribution",
            reason_code="integrity_manifest_required",
            user_guidance="Local distribution stays blocked until the integrity manifest is present and matches the bundle.",
            evidence_refs=evidence_refs,
            next_steps=("inspect installer_status", "inspect local bundle manifest"),
        ),
        build_blocked_surface_record(
            surface_name="conversation_turn",
            reason_code="runner_bypass_blocked",
            user_guidance=(
                "Conversation turns must pass through the local gateway and runner path together. "
                "Direct runner bypass is blocked."
            ),
            evidence_refs=evidence_refs,
            next_steps=("use the embeddable runtime API", "inspect gateway envelope"),
        ),
    ]
    if len(states) > MAX_FAIL_CLOSED_STATES:
        raise ValueError("fail-closed state catalog exceeds planning ceiling")
    payload = {
        "schema": FAIL_CLOSED_CATALOG_SCHEMA,
        "support_state": support_state,
        "state_count": len(states),
        "states": states,
    }
    return {
        **payload,
        "snapshot_hash": stable_hash_payload(payload),
    }


def select_fail_closed_state(
    *,
    catalog: Mapping[str, Any],
    surface_name: str,
    reason_code: str,
) -> dict[str, Any]:
    for state in catalog.get("states", []):
        if state.get("surface_name") == surface_name and state.get("reason_code") == reason_code:
            return dict(state)
    return build_blocked_surface_record(
        surface_name=surface_name,
        reason_code=reason_code,
        user_guidance="The product shell blocked the request because it could not prove a safe path.",
        evidence_refs=list(catalog.get("states", [{}])[0].get("evidence_refs", [])) if catalog.get("states") else [],
        next_steps=("inspect fail_closed_help",),
    )
