from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Mapping


class Phase13ProductRuntimeError(ValueError):
    """Raised when Phase 13 product-runtime state breaks the governed contract."""


PRODUCT_RUNTIME_SHELL_SCHEMA = "agifcore.phase_13.product_runtime_shell.v1"
EMBEDDABLE_RUNTIME_API_SCHEMA = "agifcore.phase_13.embeddable_runtime_api.v1"
GATEWAY_ENVELOPE_SCHEMA = "agifcore.phase_13.gateway_envelope.v1"
GATEWAY_RESPONSE_SCHEMA = "agifcore.phase_13.gateway_response.v1"
SESSION_OPEN_SCHEMA = "agifcore.phase_13.session_open.v1"
CONVERSATION_TURN_SCHEMA = "agifcore.phase_13.conversation_turn.v1"
LOCAL_DESKTOP_UI_SCHEMA = "agifcore.phase_13.local_desktop_ui.v1"
STATE_EXPORT_SCHEMA = "agifcore.phase_13.state_export.v1"
TRACE_EXPORT_SCHEMA = "agifcore.phase_13.trace_export.v1"
MEMORY_REVIEW_EXPORT_SCHEMA = "agifcore.phase_13.memory_review_export.v1"
SAFE_SHUTDOWN_SCHEMA = "agifcore.phase_13.safe_shutdown.v1"
FAIL_CLOSED_UX_SCHEMA = "agifcore.phase_13.fail_closed_ux.v1"
FAIL_CLOSED_CATALOG_SCHEMA = "agifcore.phase_13.fail_closed_ux_catalog.v1"
INSTALLER_DISTRIBUTION_SCHEMA = "agifcore.phase_13.installer_distribution.v1"

PHASE10_SCHEMA = "agifcore.phase_10.meta_cognition_turn.v1"
PHASE11_SCHEMA = "agifcore.phase_11.self_improvement_cycle.v1"
PHASE12_SCHEMA = "agifcore.phase_12.structural_growth_cycle.v1"
PHASE2_STATE_EXPORT_SCHEMA = "agifcore.phase_02.state_export.v1"
PHASE2_MEMORY_REVIEW_EXPORT_SCHEMA = "agifcore.phase_02.memory_review_export.v1"

MAX_EVIDENCE_REFS = 24
MAX_PUBLIC_SURFACES = 8
MAX_LOCAL_GATEWAY_ROUTES = 10
MAX_DESKTOP_UI_VIEWS = 7
MAX_STATE_EXPORT_BYTES = 8 * 1024 * 1024
MAX_TRACE_EXPORT_BYTES = 16 * 1024 * 1024
MAX_MEMORY_REVIEW_EXPORT_BYTES = 8 * 1024 * 1024
MAX_FAIL_CLOSED_STATES = 10
MAX_INSTALLER_ARTIFACTS = 6
MAX_DEMO_BUNDLE_BYTES = 192 * 1024 * 1024
MAX_GATEWAY_PAYLOAD_BYTES = 32 * 1024
MAX_GATEWAY_REQUESTS_PER_SESSION = 12

PUBLIC_SURFACES = (
    "session_open",
    "conversation_turn",
    "state_export",
    "trace_export",
    "memory_review_export",
    "safe_shutdown",
)
BLOCKED_SURFACES = ("task_submit", "policy_update")
SUPPORT_SURFACES = ("fail_closed_help", "installer_status")
ALL_SURFACES = (*PUBLIC_SURFACES, *BLOCKED_SURFACES)
ALL_GATEWAY_SURFACES = (*PUBLIC_SURFACES, *BLOCKED_SURFACES, *SUPPORT_SURFACES)

ROUTE_TO_SURFACE = {
    "/api/session-open": "session_open",
    "/api/conversation-turn": "conversation_turn",
    "/api/state-export": "state_export",
    "/api/trace-export": "trace_export",
    "/api/memory-review-export": "memory_review_export",
    "/api/safe-shutdown": "safe_shutdown",
    "/api/task-submit": "task_submit",
    "/api/policy-update": "policy_update",
    "/api/fail-closed-help": "fail_closed_help",
    "/api/installer-status": "installer_status",
}
SURFACE_TO_ROUTE = {surface: route for route, surface in ROUTE_TO_SURFACE.items()}

DESKTOP_UI_VIEWS = (
    "session_overview",
    "conversation_result",
    "trace_export_view",
    "state_export_view",
    "memory_review_view",
    "fail_closed_help_view",
    "installer_distribution_view",
)

FAIL_CLOSED_STATE_IDS = (
    "fail_closed::task_submit::reserved_surface_fail_closed",
    "fail_closed::policy_update::reserved_surface_fail_closed",
    "fail_closed::gateway_route::unknown_route",
    "fail_closed::gateway_policy::policy_hash_mismatch",
    "fail_closed::installer_distribution::integrity_manifest_required",
    "fail_closed::conversation_turn::runner_bypass_blocked",
)

PHASE2_OPERATOR_COMMANDS = [
    "inspect_state",
    "plan_governed_action",
    "verify_or_replay",
    "rollback_or_quarantine",
    "export_evidence",
]


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_hash_payload(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


def canonical_size_bytes(payload: Mapping[str, Any] | list[Any]) -> int:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return len(encoded)


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase13ProductRuntimeError(f"{field_name} must be a non-empty string")
    return value.strip()


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase13ProductRuntimeError(f"{field_name} must be a mapping")
    return dict(value)


def require_schema(payload: Any, expected_schema: str, field_name: str) -> dict[str, Any]:
    payload_map = require_mapping(payload, field_name)
    if payload_map.get("schema") != expected_schema:
        raise Phase13ProductRuntimeError(
            f"{field_name} schema mismatch: expected {expected_schema}"
        )
    return payload_map


def deep_copy_jsonable(value: Any) -> Any:
    return deepcopy(value)


def bounded_unique(
    values: list[str],
    *,
    ceiling: int,
    field_name: str,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in values:
        cleaned = " ".join(str(raw).split()).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
        if len(result) >= ceiling:
            break
    if not result and not allow_empty:
        raise Phase13ProductRuntimeError(f"{field_name} must include at least one value")
    return tuple(result)


def make_ref(prefix: str, payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    clean_prefix = require_non_empty_str(prefix, "prefix").replace(" ", "_")
    return f"{clean_prefix}::{stable_hash_payload(payload)[:12]}"


def normalize_support_state(value: str) -> str:
    candidate = value.strip().lower()
    if candidate in {"grounded", "inferred", "search_needed", "unknown"}:
        return candidate
    return "unknown"


def infer_knowledge_gap_reason(*, support_state: str, selected_outcome: str) -> str:
    clean_support = normalize_support_state(support_state)
    outcome = str(selected_outcome).strip().lower()
    if clean_support == "grounded":
        return "none"
    if clean_support == "search_needed":
        return "needs_fresh_information"
    if outcome == "clarify":
        return "ambiguous_request"
    if clean_support == "inferred":
        return "conflicting_state"
    return "missing_local_evidence"


def infer_next_action(*, support_state: str, selected_outcome: str) -> str:
    clean_support = normalize_support_state(support_state)
    outcome = str(selected_outcome).strip().lower()
    if clean_support == "grounded":
        return "answer"
    if outcome == "clarify":
        return "clarify"
    if clean_support == "search_needed":
        return "search_local"
    if clean_support == "inferred":
        return "clarify"
    return "abstain"


def infer_final_answer_mode(*, support_state: str, selected_outcome: str) -> str:
    clean_support = normalize_support_state(support_state)
    outcome = str(selected_outcome).strip().lower()
    if clean_support == "grounded":
        return "grounded_fact"
    if outcome == "clarify":
        return "clarify"
    if clean_support == "search_needed":
        return "search_needed"
    if clean_support == "inferred":
        return "derived_explanation"
    return "unknown"


def build_blocked_surface_record(
    *,
    surface_name: str,
    reason_code: str,
    user_guidance: str,
    evidence_refs: list[str] | tuple[str, ...],
    next_steps: list[str] | tuple[str, ...] = (),
) -> dict[str, Any]:
    clean_surface = require_non_empty_str(surface_name, "surface_name")
    clean_reason = require_non_empty_str(reason_code, "reason_code")
    clean_guidance = require_non_empty_str(user_guidance, "user_guidance")
    bounded_evidence = bounded_unique(
        [str(item) for item in evidence_refs],
        ceiling=MAX_EVIDENCE_REFS,
        field_name="evidence_refs",
        allow_empty=True,
    )
    bounded_steps = bounded_unique(
        [str(item) for item in next_steps],
        ceiling=4,
        field_name="next_steps",
        allow_empty=True,
    )
    state_id = f"fail_closed::{clean_surface}::{clean_reason}"
    payload = {
        "schema": FAIL_CLOSED_UX_SCHEMA,
        "state_id": state_id,
        "surface_name": clean_surface,
        "reason_code": clean_reason,
        "headline": clean_surface.replace("_", " ").title(),
        "user_guidance": clean_guidance,
        "next_steps": list(bounded_steps),
        "evidence_refs": list(bounded_evidence),
        "transfer_execution_enabled": False,
    }
    return {
        **payload,
        "state_hash": stable_hash_payload(payload),
    }
