from __future__ import annotations

from .contracts import (
    MAX_PROFILE_MANIFEST_COUNT,
    PROFILE_ACTIVE_BANDS,
    PROFILE_NAMES,
    PROFILE_MANIFEST_SCHEMA,
    PROFILE_TARGET_ACTIVE_CELLS,
    require_mapping,
    require_profile_name,
    stable_hash_payload,
)


PROFILE_ROLE_DESCRIPTIONS = {
    "mobile": "constrained product runtime",
    "laptop": "reference product runtime",
    "builder": "diagnostic and instrumentation runtime",
}

PROFILE_DIAGNOSTICS_SCOPE = {
    "mobile": "bounded local diagnostics only",
    "laptop": "reference evidence capture",
    "builder": "deeper diagnostics without correctness privilege",
}


def build_profile_manifest(
    *,
    profile: str,
    phase13_session_open: dict[str, object],
    phase13_shell_snapshot: dict[str, object],
) -> dict[str, object]:
    resolved_profile = require_profile_name(profile, "profile")
    session_open = require_mapping(phase13_session_open, "phase13_session_open")
    shell_snapshot = require_mapping(phase13_shell_snapshot, "phase13_shell_snapshot")
    public_surfaces = list(session_open["available_surfaces"])
    blocked_surface_names = list(shell_snapshot["blocked_surface_names"])
    contract_fingerprint = {
        "public_surfaces": public_surfaces,
        "blocked_surface_names": blocked_surface_names,
        "allowlisted_routes": list(shell_snapshot["allowlisted_routes"]),
        "gateway_route_count": shell_snapshot["gateway_surface_count"],
        "ui_view_count": shell_snapshot["ui_view_count"],
    }
    payload = {
        "schema": PROFILE_MANIFEST_SCHEMA,
        "profile": resolved_profile,
        "profile_role": PROFILE_ROLE_DESCRIPTIONS[resolved_profile],
        "same_architecture_preserved": True,
        "same_public_surfaces": public_surfaces,
        "same_blocked_surface_names": blocked_surface_names,
        "same_gateway_route_count": len(shell_snapshot["allowlisted_routes"]),
        "same_ui_view_count": shell_snapshot["ui_view_count"],
        "same_contract_hash": stable_hash_payload(contract_fingerprint),
        "active_cell_band": dict(PROFILE_ACTIVE_BANDS[resolved_profile]),
        "target_active_cells": PROFILE_TARGET_ACTIVE_CELLS[resolved_profile],
        "diagnostics_scope": PROFILE_DIAGNOSTICS_SCOPE[resolved_profile],
        "correctness_privilege": False,
    }
    return {
        **payload,
        "profile_hash": stable_hash_payload(payload),
    }


def build_all_profile_manifests(
    *,
    phase13_session_open: dict[str, object],
    phase13_shell_snapshot: dict[str, object],
) -> dict[str, object]:
    manifests = [
        build_profile_manifest(
            profile=profile,
            phase13_session_open=phase13_session_open,
            phase13_shell_snapshot=phase13_shell_snapshot,
        )
        for profile in PROFILE_NAMES
    ]
    if len(manifests) > MAX_PROFILE_MANIFEST_COUNT:
        raise ValueError("profile manifest count exceeds planning ceiling")
    payload = {
        "schema": PROFILE_MANIFEST_SCHEMA,
        "manifest_count": len(manifests),
        "profiles": manifests,
    }
    return {
        **payload,
        "manifest_hash": stable_hash_payload(payload),
    }

