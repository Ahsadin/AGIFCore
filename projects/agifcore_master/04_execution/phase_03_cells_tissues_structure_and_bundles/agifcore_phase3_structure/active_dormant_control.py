from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from activation_policies import (
    ActivationPolicy,
    PHASE3_DORMANT_BLUEPRINT_CEILING,
    require_profile_name,
)
from cell_contracts import Phase3StructureError, require_non_empty_str
from trust_bands import TrustBand

PHASE2_LIFECYCLE_STATES = frozenset(
    {
        "dormant",
        "active",
        "quarantined",
        "retired",
        "split_pending",
        "consolidating",
    }
)


def require_non_negative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise Phase3StructureError(f"{field_name} must be an int")
    if value < 0:
        raise Phase3StructureError(f"{field_name} must be >= 0")
    return value


def validate_phase2_lifecycle_state(state: Any) -> str:
    normalized = require_non_empty_str(state, "lifecycle_state")
    if normalized not in PHASE2_LIFECYCLE_STATES:
        raise Phase3StructureError(
            f"lifecycle_state must be one of {sorted(PHASE2_LIFECYCLE_STATES)}"
        )
    return normalized


@dataclass(frozen=True, slots=True)
class ActiveDormantDecision:
    """Bounded recommendation surface; does not mutate lifecycle state directly."""

    action: str
    allowed: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "allowed": self.allowed,
            "reason": self.reason,
        }


def evaluate_activation_readiness(
    *,
    policy: ActivationPolicy,
    lifecycle_state: str,
    need_score: float,
    estimated_cost: float,
    active_cell_count: int,
    trust_band: TrustBand,
) -> ActiveDormantDecision:
    resolved_state = validate_phase2_lifecycle_state(lifecycle_state)
    evaluation = policy.evaluate_activation(
        lifecycle_state=resolved_state,
        need_score=need_score,
        estimated_cost=estimated_cost,
        active_cell_count=active_cell_count,
        trust_band=trust_band,
    )
    return ActiveDormantDecision(
        action="activate",
        allowed=bool(evaluation["allow"]),
        reason=str(evaluation["reason"]),
    )


def evaluate_dormant_pressure(
    *,
    dormant_blueprint_count: int,
    lifecycle_state: str,
) -> ActiveDormantDecision:
    resolved_state = validate_phase2_lifecycle_state(lifecycle_state)
    dormant_count = require_non_negative_int(
        dormant_blueprint_count, "dormant_blueprint_count"
    )
    if resolved_state != "dormant":
        return ActiveDormantDecision(
            action="none",
            allowed=True,
            reason="dormant pressure check applies to dormant lifecycle_state only",
        )
    if dormant_count > PHASE3_DORMANT_BLUEPRINT_CEILING:
        return ActiveDormantDecision(
            action="review_required",
            allowed=False,
            reason="dormant blueprint ceiling exceeded",
        )
    return ActiveDormantDecision(
        action="none",
        allowed=True,
        reason="dormant blueprint pressure within phase-3 ceiling",
    )


def build_lifecycle_transition_request(
    *,
    cell_id: str,
    from_state: str,
    to_state: str,
    reason: str,
    actor: str = "kernel",
) -> dict[str, str]:
    resolved_from = validate_phase2_lifecycle_state(from_state)
    resolved_to = validate_phase2_lifecycle_state(to_state)
    if (resolved_from, resolved_to) not in {
        ("dormant", "active"),
        ("active", "dormant"),
    }:
        raise Phase3StructureError(
            "active-dormant control only allows dormant<->active requests"
        )
    return {
        "cell_id": require_non_empty_str(cell_id, "cell_id"),
        "from_state": resolved_from,
        "to_state": resolved_to,
        "reason": require_non_empty_str(reason, "reason"),
        "actor": require_non_empty_str(actor, "actor"),
        "transition_action": "activate"
        if resolved_to == "active"
        else "hibernate",
    }


def validate_profile_context(profile: str, context: Mapping[str, Any]) -> dict[str, Any]:
    resolved_profile = require_profile_name(profile, "profile")
    normalized_context = dict(context)
    normalized_context["profile"] = resolved_profile
    return normalized_context
