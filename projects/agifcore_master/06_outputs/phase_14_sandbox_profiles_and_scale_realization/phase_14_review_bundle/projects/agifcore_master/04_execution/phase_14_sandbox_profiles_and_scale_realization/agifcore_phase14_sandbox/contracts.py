from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Mapping


class Phase14SandboxError(ValueError):
    """Raised when the Phase 14 sandbox/profile contract is violated."""


SANDBOX_PROFILE_RUNTIME_SCHEMA = "agifcore.phase_14.sandbox_profile_runtime.v1"
SANDBOX_POLICY_SCHEMA = "agifcore.phase_14.sandbox_policy.v1"
SANDBOX_EXECUTION_RECEIPT_SCHEMA = "agifcore.phase_14.sandbox_execution_receipt.v1"
PACKAGE_MANIFEST_SCHEMA = "agifcore.phase_14.sample_wasm_package.v1"
WASMTIME_FUEL_LIMITS_SCHEMA = "agifcore.phase_14.wasmtime_fuel_limits.v1"
WASMTIME_MEMORY_LIMITS_SCHEMA = "agifcore.phase_14.wasmtime_memory_limits.v1"
WASMTIME_WALL_TIME_LIMITS_SCHEMA = "agifcore.phase_14.wasmtime_wall_time_limits.v1"
CELL_MANIFEST_SCHEMA = "agifcore.phase_14.cell_manifest.v1"
TISSUE_MANIFEST_SCHEMA = "agifcore.phase_14.tissue_manifest.v1"
PROFILE_MANIFEST_SCHEMA = "agifcore.phase_14.profile_manifest.v1"
ACTIVE_CELL_BUDGET_SCHEMA = "agifcore.phase_14.active_cell_budget.v1"
DORMANT_SURVIVAL_PROOF_SCHEMA = "agifcore.phase_14.dormant_survival_proof.v1"
MANIFEST_AUDIT_SCHEMA = "agifcore.phase_14.manifest_audit.v1"

PROFILE_NAMES = ("mobile", "laptop", "builder")
LOCKED_LOGICAL_CELL_COUNT = 1024
LOCKED_TISSUE_COUNT = 32
LOCKED_TISSUE_BAND = (24, 40)

MAX_SANDBOX_POLICY_COUNT = 12
MAX_WASMTIME_LIMIT_CLASSES = 4
MAX_PROFILE_MANIFEST_COUNT = 3
MAX_ACTIVE_BUDGET_STATES = 5
MAX_DORMANT_SURVIVAL_CASES = 12
MAX_PHASE14_DEMO_BUNDLE_BYTES = 224 * 1024 * 1024

PROFILE_ACTIVE_BANDS = {
    "mobile": {"min": 8, "max": 24},
    "laptop": {"min": 64, "max": 128},
    "builder": {"min": 128, "max": 256},
}

PROFILE_TARGET_ACTIVE_CELLS = {
    "mobile": 16,
    "laptop": 96,
    "builder": 160,
}

PROFILE_ACTIVE_TISSUE_COUNTS = {
    "mobile": 16,
    "laptop": 32,
    "builder": 32,
}

PROFILE_CELLS_PER_ACTIVE_TISSUE = {
    "mobile": 2,
    "laptop": 4,
    "builder": 8,
}

ACTIVE_BUDGET_STATE_IDS = (
    "within_budget",
    "near_ceiling",
    "ceiling_blocked",
    "hibernate_required",
    "profile_mismatch",
)

CELL_FAMILY_IDS = (
    "intake_router",
    "attention",
    "working_memory",
    "episodic_memory",
    "semantic_abstraction",
    "procedural_skill",
    "world_model_simulator",
    "planner",
    "critic_error_monitor",
    "governance_authority",
    "transfer_broker",
    "scheduler_resource",
    "continuity_self_history",
    "language_realizer",
    "compression_retirement",
    "audit_replay",
)

SANDBOX_REQUIRED_FAMILIES = frozenset(
    {
        "procedural_skill",
        "world_model_simulator",
        "transfer_broker",
        "audit_replay",
    }
)

POLICY_IDS = (
    "mobile_constrained_policy",
    "laptop_default_policy",
    "builder_diagnostic_policy",
    "strict_fail_closed_policy",
)

POLICY_CLASS_IDS = {
    "mobile_constrained_policy": "mobile_constrained",
    "laptop_default_policy": "laptop_default",
    "builder_diagnostic_policy": "builder_diagnostic",
    "strict_fail_closed_policy": "strict_fail_closed",
}

DEFAULT_POLICY_BY_PROFILE = {
    "mobile": "mobile_constrained_policy",
    "laptop": "laptop_default_policy",
    "builder": "builder_diagnostic_policy",
}

WASM_FALLBACK_CODES = (
    "WASMTIME_UNAVAILABLE",
    "INVALID_WASM_MODULE",
    "BUNDLE_INTEGRITY_REQUIRED",
    "PROFILE_NOT_ALLOWED",
    "FUEL_LIMIT_EXCEEDED",
    "MEMORY_LIMIT_EXCEEDED",
    "WALL_TIMEOUT_EXCEEDED",
)

PROFILE_ALL = PROFILE_NAMES
PROFILE_LAPTOP_BUILDER = ("laptop", "builder")
PROFILE_BUILDER_ONLY = ("builder",)

ACTIVATION_BUDGET_CLASS_PRIORITY = {
    "frontline": 90,
    "coordination": 80,
    "retentive": 65,
    "sandboxed": 75,
    "governance": 85,
    "diagnostic": 55,
}

FAMILY_BEHAVIOR_SPECS = {
    "intake_router": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_ALL,
        "allowed_actions": ("accept_input", "route_turn", "stage_handoff"),
        "forbidden_actions": ("mutate_policy", "run_unsandboxed_wasm"),
        "routing_responsibility": "ingress_distribution",
        "activation_budget_class": "frontline",
        "export_visibility_class": "support_visible",
        "dormancy_behavior_class": "warm_standby",
        "continuity_requirement_class": "strict",
        "evidence_requirement_class": "request_receipt",
        "audit_replay_required": False,
    },
    "attention": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_ALL,
        "allowed_actions": ("prioritize_signal", "suppress_noise", "route_attention"),
        "forbidden_actions": ("mutate_policy", "emit_public_claim"),
        "routing_responsibility": "salience_filtering",
        "activation_budget_class": "frontline",
        "export_visibility_class": "internal_only",
        "dormancy_behavior_class": "warm_standby",
        "continuity_requirement_class": "strict",
        "evidence_requirement_class": "decision_trace",
        "audit_replay_required": False,
    },
    "working_memory": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_ALL,
        "allowed_actions": ("hold_context", "evict_stale_context", "serve_context_window"),
        "forbidden_actions": ("retire_memory", "publish_trace"),
        "routing_responsibility": "context_window_management",
        "activation_budget_class": "coordination",
        "export_visibility_class": "internal_only",
        "dormancy_behavior_class": "checkpoint_restore",
        "continuity_requirement_class": "strict",
        "evidence_requirement_class": "decision_trace",
        "audit_replay_required": False,
    },
    "episodic_memory": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_ALL,
        "allowed_actions": ("write_episode_index", "retrieve_episode", "link_episode_context"),
        "forbidden_actions": ("emit_public_claim", "run_unsandboxed_wasm"),
        "routing_responsibility": "episode_recall",
        "activation_budget_class": "retentive",
        "export_visibility_class": "support_visible",
        "dormancy_behavior_class": "cold_retention",
        "continuity_requirement_class": "journaled",
        "evidence_requirement_class": "retention_receipt",
        "audit_replay_required": False,
    },
    "semantic_abstraction": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_ALL,
        "allowed_actions": ("derive_schema", "compress_pattern", "merge_concepts"),
        "forbidden_actions": ("accept_input", "mutate_policy"),
        "routing_responsibility": "concept_synthesis",
        "activation_budget_class": "coordination",
        "export_visibility_class": "support_visible",
        "dormancy_behavior_class": "checkpoint_restore",
        "continuity_requirement_class": "journaled",
        "evidence_requirement_class": "decision_trace",
        "audit_replay_required": False,
    },
    "procedural_skill": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_LAPTOP_BUILDER,
        "allowed_actions": ("run_skill_recipe", "invoke_tool_adapter", "emit_skill_receipt"),
        "forbidden_actions": ("run_unsandboxed_wasm", "mutate_phase_truth"),
        "routing_responsibility": "tool_execution_handoff",
        "activation_budget_class": "sandboxed",
        "export_visibility_class": "support_visible",
        "dormancy_behavior_class": "checkpoint_restore",
        "continuity_requirement_class": "checkpointed",
        "evidence_requirement_class": "sandbox_receipt",
        "audit_replay_required": True,
    },
    "world_model_simulator": {
        "allowed_profiles": PROFILE_LAPTOP_BUILDER,
        "backstop_profiles": PROFILE_BUILDER_ONLY,
        "allowed_actions": ("run_simulation", "evaluate_counterfactual", "score_world_branch"),
        "forbidden_actions": ("emit_public_claim", "run_unsandboxed_wasm"),
        "routing_responsibility": "simulation_branching",
        "activation_budget_class": "sandboxed",
        "export_visibility_class": "internal_only",
        "dormancy_behavior_class": "checkpoint_restore",
        "continuity_requirement_class": "checkpointed",
        "evidence_requirement_class": "sandbox_receipt",
        "audit_replay_required": True,
    },
    "planner": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_LAPTOP_BUILDER,
        "allowed_actions": ("propose_plan", "stage_next_action", "rank_plan_options"),
        "forbidden_actions": ("mutate_policy", "run_unsandboxed_wasm"),
        "routing_responsibility": "plan_selection",
        "activation_budget_class": "coordination",
        "export_visibility_class": "support_visible",
        "dormancy_behavior_class": "warm_standby",
        "continuity_requirement_class": "strict",
        "evidence_requirement_class": "decision_trace",
        "audit_replay_required": False,
    },
    "critic_error_monitor": {
        "allowed_profiles": PROFILE_LAPTOP_BUILDER,
        "backstop_profiles": PROFILE_BUILDER_ONLY,
        "allowed_actions": ("check_support_gaps", "flag_risk", "emit_block_reason"),
        "forbidden_actions": ("accept_input", "emit_public_claim"),
        "routing_responsibility": "critique_and_blocking",
        "activation_budget_class": "diagnostic",
        "export_visibility_class": "audit_only",
        "dormancy_behavior_class": "cold_retention",
        "continuity_requirement_class": "checkpointed",
        "evidence_requirement_class": "audit_receipt",
        "audit_replay_required": True,
    },
    "governance_authority": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_LAPTOP_BUILDER,
        "allowed_actions": ("enforce_policy", "block_forbidden_action", "issue_governance_receipt"),
        "forbidden_actions": ("run_unsandboxed_wasm", "widen_public_surface"),
        "routing_responsibility": "policy_governance",
        "activation_budget_class": "governance",
        "export_visibility_class": "audit_only",
        "dormancy_behavior_class": "warm_standby",
        "continuity_requirement_class": "strict",
        "evidence_requirement_class": "policy_receipt",
        "audit_replay_required": True,
    },
    "transfer_broker": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_LAPTOP_BUILDER,
        "allowed_actions": ("broker_handoff", "normalize_payload", "stage_transfer_receipt"),
        "forbidden_actions": ("emit_public_claim", "mutate_phase_truth"),
        "routing_responsibility": "cross_family_transfer",
        "activation_budget_class": "sandboxed",
        "export_visibility_class": "support_visible",
        "dormancy_behavior_class": "checkpoint_restore",
        "continuity_requirement_class": "checkpointed",
        "evidence_requirement_class": "handoff_trace",
        "audit_replay_required": True,
    },
    "scheduler_resource": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_ALL,
        "allowed_actions": ("allocate_budget", "defer_work", "schedule_activation"),
        "forbidden_actions": ("emit_public_claim", "run_unsandboxed_wasm"),
        "routing_responsibility": "resource_scheduling",
        "activation_budget_class": "coordination",
        "export_visibility_class": "internal_only",
        "dormancy_behavior_class": "warm_standby",
        "continuity_requirement_class": "journaled",
        "evidence_requirement_class": "decision_trace",
        "audit_replay_required": False,
    },
    "continuity_self_history": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_ALL,
        "allowed_actions": ("anchor_self_state", "recover_identity", "stamp_continuity"),
        "forbidden_actions": ("emit_public_claim", "run_unsandboxed_wasm"),
        "routing_responsibility": "continuity_anchoring",
        "activation_budget_class": "retentive",
        "export_visibility_class": "audit_only",
        "dormancy_behavior_class": "cold_retention",
        "continuity_requirement_class": "strict",
        "evidence_requirement_class": "audit_receipt",
        "audit_replay_required": True,
    },
    "language_realizer": {
        "allowed_profiles": PROFILE_ALL,
        "backstop_profiles": PROFILE_ALL,
        "allowed_actions": ("compose_reply", "format_output", "preserve_truth_markers"),
        "forbidden_actions": ("mutate_policy", "run_unsandboxed_wasm"),
        "routing_responsibility": "response_realization",
        "activation_budget_class": "frontline",
        "export_visibility_class": "public_visible",
        "dormancy_behavior_class": "warm_standby",
        "continuity_requirement_class": "strict",
        "evidence_requirement_class": "request_receipt",
        "audit_replay_required": False,
    },
    "compression_retirement": {
        "allowed_profiles": PROFILE_LAPTOP_BUILDER,
        "backstop_profiles": PROFILE_BUILDER_ONLY,
        "allowed_actions": ("retire_memory", "compress_trace", "emit_retention_receipt"),
        "forbidden_actions": ("accept_input", "emit_public_claim"),
        "routing_responsibility": "retention_and_compression",
        "activation_budget_class": "diagnostic",
        "export_visibility_class": "audit_only",
        "dormancy_behavior_class": "cold_retention",
        "continuity_requirement_class": "journaled",
        "evidence_requirement_class": "retention_receipt",
        "audit_replay_required": True,
    },
    "audit_replay": {
        "allowed_profiles": PROFILE_LAPTOP_BUILDER,
        "backstop_profiles": PROFILE_BUILDER_ONLY,
        "allowed_actions": ("replay_trace", "rebuild_evidence", "verify_audit_path"),
        "forbidden_actions": ("accept_input", "emit_public_claim"),
        "routing_responsibility": "audit_reconstruction",
        "activation_budget_class": "diagnostic",
        "export_visibility_class": "audit_only",
        "dormancy_behavior_class": "cold_retention",
        "continuity_requirement_class": "checkpointed",
        "evidence_requirement_class": "audit_receipt",
        "audit_replay_required": True,
    },
}

TISSUE_VARIANT_SPECS = {
    "primary_path": {
        "specialization_tag": "online_path",
        "tissue_focus": "serve_and_route",
        "evidence_lane": "runtime_visible",
        "continuity_handling_class": "inline_handoff",
        "escalation_handling_class": "forward_escalation",
        "active_cell_cap_by_profile": {"mobile": 2, "laptop": 5, "builder": 8},
        "activation_priority_boost_by_profile": {"mobile": 12, "laptop": 8, "builder": 4},
        "exemplar_class_ids": ("anchor", "operator", "handoff", "recovery"),
    },
    "continuity_backstop": {
        "specialization_tag": "continuity_backstop",
        "tissue_focus": "stabilize_and_audit",
        "evidence_lane": "audit_visible",
        "continuity_handling_class": "checkpoint_guard",
        "escalation_handling_class": "stabilize_then_escalate",
        "active_cell_cap_by_profile": {"mobile": 1, "laptop": 3, "builder": 8},
        "activation_priority_boost_by_profile": {"mobile": 2, "laptop": 4, "builder": 10},
        "exemplar_class_ids": ("checkpoint", "audit", "reserve", "bridge"),
    },
}

EXEMPLAR_CLASS_SPECS = {
    "anchor": {
        "allowed_action_indexes": (0, 1),
        "activation_priority_offset": 30,
        "export_visibility_override": "support_visible",
        "dormancy_behavior_override": "warm_standby",
        "continuity_requirement_override": "strict",
        "evidence_requirement_override": "request_receipt",
    },
    "operator": {
        "allowed_action_indexes": (0, 1, 2),
        "activation_priority_offset": 20,
        "export_visibility_override": None,
        "dormancy_behavior_override": None,
        "continuity_requirement_override": None,
        "evidence_requirement_override": None,
    },
    "handoff": {
        "allowed_action_indexes": (1, 2),
        "activation_priority_offset": 12,
        "export_visibility_override": "support_visible",
        "dormancy_behavior_override": "checkpoint_restore",
        "continuity_requirement_override": "journaled",
        "evidence_requirement_override": "handoff_trace",
    },
    "recovery": {
        "allowed_action_indexes": (0, 2),
        "activation_priority_offset": 6,
        "export_visibility_override": "internal_only",
        "dormancy_behavior_override": "checkpoint_restore",
        "continuity_requirement_override": "checkpointed",
        "evidence_requirement_override": "decision_trace",
    },
    "checkpoint": {
        "allowed_action_indexes": (0, 1),
        "activation_priority_offset": 26,
        "export_visibility_override": "audit_only",
        "dormancy_behavior_override": "checkpoint_restore",
        "continuity_requirement_override": "checkpointed",
        "evidence_requirement_override": "policy_receipt",
    },
    "audit": {
        "allowed_action_indexes": (1, 2),
        "activation_priority_offset": 22,
        "export_visibility_override": "audit_only",
        "dormancy_behavior_override": "cold_retention",
        "continuity_requirement_override": "checkpointed",
        "evidence_requirement_override": "audit_receipt",
    },
    "reserve": {
        "allowed_action_indexes": (0,),
        "activation_priority_offset": 10,
        "export_visibility_override": "internal_only",
        "dormancy_behavior_override": "cold_retention",
        "continuity_requirement_override": "journaled",
        "evidence_requirement_override": "retention_receipt",
    },
    "bridge": {
        "allowed_action_indexes": (0, 2),
        "activation_priority_offset": 14,
        "export_visibility_override": "support_visible",
        "dormancy_behavior_override": "checkpoint_restore",
        "continuity_requirement_override": "journaled",
        "evidence_requirement_override": "handoff_trace",
    },
}

TISSUE_VARIANT_ORDER = ("primary_path", "continuity_backstop")

DORMANCY_CLASS_PRIORITY = {
    "warm_standby": 3,
    "checkpoint_restore": 2,
    "cold_retention": 1,
}

CONTINUITY_CLASS_PRIORITY = {
    "strict": 3,
    "checkpointed": 2,
    "journaled": 1,
}


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_hash_payload(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


def canonical_size_bytes(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> int:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return len(encoded)


def family_behavior_spec(role_family: str) -> dict[str, Any]:
    return deep_copy_jsonable(FAMILY_BEHAVIOR_SPECS[role_family])


def tissue_variant_spec(variant_id: str) -> dict[str, Any]:
    return deep_copy_jsonable(TISSUE_VARIANT_SPECS[variant_id])


def exemplar_class_spec(class_id: str) -> dict[str, Any]:
    return deep_copy_jsonable(EXEMPLAR_CLASS_SPECS[class_id])


def tissue_variant_for_tissue_index(tissue_index: int) -> str:
    return TISSUE_VARIANT_ORDER[tissue_index % len(TISSUE_VARIANT_ORDER)]


def operation_set_for_exemplar(*, role_family: str, exemplar_class_id: str) -> tuple[str, ...]:
    family_spec = FAMILY_BEHAVIOR_SPECS[role_family]
    exemplar_spec = EXEMPLAR_CLASS_SPECS[exemplar_class_id]
    actions = tuple(family_spec["allowed_actions"])
    indexes = tuple(exemplar_spec["allowed_action_indexes"])
    selected = tuple(actions[index] for index in indexes if 0 <= index < len(actions))
    if selected:
        return selected
    return actions[:1]


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase14SandboxError(f"{field_name} must be a non-empty string")
    return value.strip()


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase14SandboxError(f"{field_name} must be a mapping")
    return dict(value)


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise Phase14SandboxError(f"{field_name} must be a bool")
    return value


def require_non_negative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise Phase14SandboxError(f"{field_name} must be an int")
    if value < 0:
        raise Phase14SandboxError(f"{field_name} must be >= 0")
    return value


def require_profile_name(value: Any, field_name: str = "profile") -> str:
    profile = require_non_empty_str(value, field_name).lower()
    if profile not in PROFILE_NAMES:
        raise Phase14SandboxError(f"{field_name} must be one of {list(PROFILE_NAMES)}")
    return profile


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
        raise Phase14SandboxError(f"{field_name} must include at least one value")
    return tuple(result)


def deep_copy_jsonable(value: Any) -> Any:
    return deepcopy(value)
