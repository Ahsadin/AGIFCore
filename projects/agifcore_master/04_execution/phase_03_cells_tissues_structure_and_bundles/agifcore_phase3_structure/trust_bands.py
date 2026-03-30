from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from cell_contracts import (
    Phase3StructureError,
    require_mapping,
    require_non_empty_str,
)

TRUST_BAND_ORDER = ("blocked", "guarded", "standard", "elevated")
TRUST_BAND_RANK = {name: index for index, name in enumerate(TRUST_BAND_ORDER)}
REQUIRED_TRUST_BAND_FIELDS = ("band_name", "allow_activation", "max_scheduler_priority")
TRUST_SCORE_BAND_TABLE = (
    (0.00, 0.25, "blocked"),
    (0.25, 0.50, "guarded"),
    (0.50, 0.80, "standard"),
    (0.80, 1.00, "elevated"),
)


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise Phase3StructureError(f"{field_name} must be a bool")
    return value


def require_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise Phase3StructureError(f"{field_name} must be an int")
    return value


def normalize_trust_band_name(value: Any, field_name: str = "band_name") -> str:
    band_name = require_non_empty_str(value, field_name).lower()
    if band_name not in TRUST_BAND_RANK:
        raise Phase3StructureError(
            f"{field_name} must be one of {list(TRUST_BAND_ORDER)}"
        )
    return band_name


def trust_band_at_least(band_name: str, *, minimum_band: str) -> bool:
    resolved_band = normalize_trust_band_name(band_name, "band_name")
    resolved_minimum = normalize_trust_band_name(minimum_band, "minimum_band")
    return TRUST_BAND_RANK[resolved_band] >= TRUST_BAND_RANK[resolved_minimum]


def normalize_trust_score(score: Any, *, field_name: str = "trust_score") -> float:
    if not isinstance(score, (int, float)):
        raise Phase3StructureError(f"{field_name} must be a float in [0.0, 1.0]")
    normalized = float(score)
    if normalized < 0.0 or normalized > 1.0:
        raise Phase3StructureError(f"{field_name} must be a float in [0.0, 1.0]")
    return normalized


def trust_band_for_score(score: Any) -> str:
    normalized = normalize_trust_score(score)
    for minimum, maximum, band_name in TRUST_SCORE_BAND_TABLE:
        if normalized >= minimum and normalized < maximum:
            return band_name
    return "elevated"


def validate_trust_band_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    for field_name in REQUIRED_TRUST_BAND_FIELDS:
        if field_name not in normalized:
            raise Phase3StructureError(
                f"missing required trust band field: {field_name}"
            )
    max_scheduler_priority = require_int(
        normalized["max_scheduler_priority"], "max_scheduler_priority"
    )
    if max_scheduler_priority < 0:
        raise Phase3StructureError("max_scheduler_priority must be >= 0")
    return {
        "band_name": normalize_trust_band_name(normalized["band_name"]),
        "allow_activation": require_bool(normalized["allow_activation"], "allow_activation"),
        "allow_split_merge": require_bool(
            normalized.get("allow_split_merge", False), "allow_split_merge"
        ),
        "require_manual_review": require_bool(
            normalized.get("require_manual_review", False), "require_manual_review"
        ),
        "max_scheduler_priority": max_scheduler_priority,
        "policy_envelope": require_mapping(
            normalized.get("policy_envelope", {}), "policy_envelope"
        ),
    }


@dataclass(frozen=True, slots=True)
class TrustBand:
    """Slice-2 trust controls with explicit enforcement behavior."""

    band_name: str
    allow_activation: bool
    allow_split_merge: bool
    require_manual_review: bool
    max_scheduler_priority: int
    policy_envelope: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "TrustBand":
        normalized = validate_trust_band_payload(payload)
        return cls(**normalized)

    @classmethod
    def from_trust_score(
        cls, score: float, *, policy_envelope: Mapping[str, Any] | None = None
    ) -> "TrustBand":
        band_name = trust_band_for_score(score)
        defaults = default_trust_band_policy(band_name)
        defaults["policy_envelope"] = dict(policy_envelope or {})
        return cls(**defaults)

    def to_dict(self) -> dict[str, Any]:
        return {
            "band_name": self.band_name,
            "allow_activation": self.allow_activation,
            "allow_split_merge": self.allow_split_merge,
            "require_manual_review": self.require_manual_review,
            "max_scheduler_priority": self.max_scheduler_priority,
            "policy_envelope": dict(self.policy_envelope),
        }

    def validate(self) -> None:
        validate_trust_band_payload(self.to_dict())

    def enforce_activation(self) -> None:
        if not self.allow_activation:
            raise Phase3StructureError(
                f"trust band {self.band_name} blocks activation"
            )

    def enforce_scheduler_priority(self, priority: int) -> None:
        if priority > self.max_scheduler_priority:
            raise Phase3StructureError(
                f"priority {priority} exceeds trust-band max {self.max_scheduler_priority}"
            )

    def enforce_minimum_band(self, minimum_band: str) -> None:
        if not trust_band_at_least(self.band_name, minimum_band=minimum_band):
            raise Phase3StructureError(
                f"trust band {self.band_name} is below minimum required band {minimum_band}"
            )


def default_trust_band_policy(band_name: str) -> dict[str, Any]:
    resolved = normalize_trust_band_name(band_name)
    if resolved == "blocked":
        return {
            "band_name": resolved,
            "allow_activation": False,
            "allow_split_merge": False,
            "require_manual_review": True,
            "max_scheduler_priority": 0,
            "policy_envelope": {},
        }
    if resolved == "guarded":
        return {
            "band_name": resolved,
            "allow_activation": True,
            "allow_split_merge": False,
            "require_manual_review": True,
            "max_scheduler_priority": 3,
            "policy_envelope": {},
        }
    if resolved == "standard":
        return {
            "band_name": resolved,
            "allow_activation": True,
            "allow_split_merge": True,
            "require_manual_review": False,
            "max_scheduler_priority": 6,
            "policy_envelope": {},
        }
    return {
        "band_name": resolved,
        "allow_activation": True,
        "allow_split_merge": True,
        "require_manual_review": False,
        "max_scheduler_priority": 10,
        "policy_envelope": {},
    }
