from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from cell_contracts import Phase3StructureError, require_mapping, require_non_empty_str
from trust_bands import TrustBand, normalize_trust_band_name, trust_band_at_least

PHASE3_PROFILE_ACTIVE_CELL_CEILINGS = {
    "mobile": 8,
    "laptop": 32,
}
PHASE3_TISSUE_CEILING = 12
PHASE3_DORMANT_BLUEPRINT_CEILING = 128
REQUIRED_ACTIVATION_POLICY_FIELDS = (
    "policy_id",
    "cell_id",
    "tissue_id",
    "profile",
    "minimum_need_score",
    "maximum_estimated_cost",
    "minimum_trust_band",
    "policy_envelope",
)


def require_float(value: Any, field_name: str) -> float:
    if not isinstance(value, (int, float)):
        raise Phase3StructureError(f"{field_name} must be a float")
    return float(value)


def require_non_negative_float(value: Any, field_name: str) -> float:
    normalized = require_float(value, field_name)
    if normalized < 0.0:
        raise Phase3StructureError(f"{field_name} must be >= 0.0")
    return normalized


def require_profile_name(value: Any, field_name: str = "profile") -> str:
    profile = require_non_empty_str(value, field_name).lower()
    if profile not in PHASE3_PROFILE_ACTIVE_CELL_CEILINGS:
        raise Phase3StructureError(
            f"{field_name} must be one of {list(PHASE3_PROFILE_ACTIVE_CELL_CEILINGS)}"
        )
    return profile


def profile_active_cell_ceiling(profile: str) -> int:
    resolved = require_profile_name(profile)
    return PHASE3_PROFILE_ACTIVE_CELL_CEILINGS[resolved]


def validate_activation_policy_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    for field_name in REQUIRED_ACTIVATION_POLICY_FIELDS:
        if field_name not in normalized:
            raise Phase3StructureError(
                f"missing required activation policy field: {field_name}"
            )
    minimum_need_score = require_float(
        normalized["minimum_need_score"], "minimum_need_score"
    )
    if minimum_need_score < 0.0 or minimum_need_score > 1.0:
        raise Phase3StructureError("minimum_need_score must be in [0.0, 1.0]")
    return {
        "policy_id": require_non_empty_str(normalized["policy_id"], "policy_id"),
        "cell_id": require_non_empty_str(normalized["cell_id"], "cell_id"),
        "tissue_id": require_non_empty_str(normalized["tissue_id"], "tissue_id"),
        "profile": require_profile_name(normalized["profile"], "profile"),
        "minimum_need_score": minimum_need_score,
        "maximum_estimated_cost": require_non_negative_float(
            normalized["maximum_estimated_cost"], "maximum_estimated_cost"
        ),
        "minimum_trust_band": normalize_trust_band_name(
            normalized["minimum_trust_band"], "minimum_trust_band"
        ),
        "policy_envelope": require_mapping(
            normalized["policy_envelope"], "policy_envelope"
        ),
    }


@dataclass(frozen=True, slots=True)
class ActivationPolicy:
    """Slice-2 activation guardrails above Phase 2 lifecycle + scheduler surfaces."""

    policy_id: str
    cell_id: str
    tissue_id: str
    profile: str
    minimum_need_score: float
    maximum_estimated_cost: float
    minimum_trust_band: str
    policy_envelope: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ActivationPolicy":
        normalized = validate_activation_policy_payload(payload)
        return cls(**normalized)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "cell_id": self.cell_id,
            "tissue_id": self.tissue_id,
            "profile": self.profile,
            "minimum_need_score": self.minimum_need_score,
            "maximum_estimated_cost": self.maximum_estimated_cost,
            "minimum_trust_band": self.minimum_trust_band,
            "policy_envelope": dict(self.policy_envelope),
        }

    def validate(self) -> None:
        validate_activation_policy_payload(self.to_dict())

    def evaluate_activation(
        self,
        *,
        lifecycle_state: str,
        need_score: float,
        estimated_cost: float,
        active_cell_count: int,
        trust_band: TrustBand | str,
    ) -> dict[str, Any]:
        if lifecycle_state != "dormant":
            return {
                "allow": False,
                "reason": "activation requires lifecycle_state=dormant",
            }
        if need_score < self.minimum_need_score:
            return {
                "allow": False,
                "reason": "need_score below minimum_need_score",
            }
        if estimated_cost > self.maximum_estimated_cost:
            return {
                "allow": False,
                "reason": "estimated_cost exceeds maximum_estimated_cost",
            }
        if active_cell_count >= profile_active_cell_ceiling(self.profile):
            return {
                "allow": False,
                "reason": "active cell ceiling reached for profile",
            }
        trust_band_name = (
            trust_band.band_name if isinstance(trust_band, TrustBand) else trust_band
        )
        if isinstance(trust_band, TrustBand) and not trust_band.allow_activation:
            return {
                "allow": False,
                "reason": "trust band blocks activation",
            }
        if not trust_band_at_least(
            trust_band_name, minimum_band=self.minimum_trust_band
        ):
            return {
                "allow": False,
                "reason": "trust band below policy minimum",
            }
        return {"allow": True, "reason": "activation allowed"}
