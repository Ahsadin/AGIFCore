from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from activation_policies import (
    PHASE3_DORMANT_BLUEPRINT_CEILING,
    PHASE3_PROFILE_ACTIVE_CELL_CEILINGS,
    PHASE3_TISSUE_CEILING,
)
from cell_contracts import (
    MAX_MANIFEST_SIZE_BYTES,
    Phase3StructureError,
    require_mapping,
    require_non_empty_str,
)
from tissue_manifests import SPLIT_PRESSURE_MEMBER_COUNT

PHASE3_BUNDLE_PAYLOAD_CEILING_BYTES = 8 * 1024 * 1024
PROFILE_NAMES = ("mobile", "laptop", "builder")
BUILDER_ACTIVE_CELL_CEILING = 64

PROFILE_ACTIVE_CELL_CEILINGS = {
    "mobile": PHASE3_PROFILE_ACTIVE_CELL_CEILINGS["mobile"],
    "laptop": PHASE3_PROFILE_ACTIVE_CELL_CEILINGS["laptop"],
    "builder": BUILDER_ACTIVE_CELL_CEILING,
}

REQUIRED_PROFILE_BUDGET_FIELDS = (
    "profile",
    "max_active_cells",
    "max_tissues",
    "max_members_per_tissue_before_review",
    "max_dormant_blueprints",
    "max_manifest_size_bytes",
    "max_bundle_payload_size_bytes",
    "policy_envelope",
)

REQUIRED_PROFILE_BUDGET_CONTEXT_FIELDS = (
    "active_cell_count",
    "tissue_count",
    "largest_tissue_member_count",
    "dormant_blueprint_count",
    "manifest_size_bytes",
    "bundle_payload_size_bytes",
)


def require_non_negative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise Phase3StructureError(f"{field_name} must be an int")
    if value < 0:
        raise Phase3StructureError(f"{field_name} must be >= 0")
    return value


def require_profile_name(value: Any, field_name: str = "profile") -> str:
    profile = require_non_empty_str(value, field_name).lower()
    if profile not in PROFILE_ACTIVE_CELL_CEILINGS:
        raise Phase3StructureError(f"{field_name} must be one of {list(PROFILE_NAMES)}")
    return profile


def validate_profile_budget_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    for field_name in REQUIRED_PROFILE_BUDGET_FIELDS:
        if field_name not in normalized:
            raise Phase3StructureError(
                f"missing required profile budget field: {field_name}"
            )
    profile = require_profile_name(normalized["profile"], "profile")
    max_active_cells = require_non_negative_int(
        normalized["max_active_cells"], "max_active_cells"
    )
    if max_active_cells > PROFILE_ACTIVE_CELL_CEILINGS[profile]:
        raise Phase3StructureError(
            f"max_active_cells exceeds phase-3 ceiling for profile {profile}"
        )

    max_tissues = require_non_negative_int(normalized["max_tissues"], "max_tissues")
    if max_tissues > PHASE3_TISSUE_CEILING:
        raise Phase3StructureError("max_tissues exceeds phase-3 tissue ceiling")

    max_members_per_tissue_before_review = require_non_negative_int(
        normalized["max_members_per_tissue_before_review"],
        "max_members_per_tissue_before_review",
    )
    if max_members_per_tissue_before_review > SPLIT_PRESSURE_MEMBER_COUNT:
        raise Phase3StructureError(
            "max_members_per_tissue_before_review exceeds split-pressure ceiling"
        )

    max_dormant_blueprints = require_non_negative_int(
        normalized["max_dormant_blueprints"], "max_dormant_blueprints"
    )
    if max_dormant_blueprints > PHASE3_DORMANT_BLUEPRINT_CEILING:
        raise Phase3StructureError(
            "max_dormant_blueprints exceeds phase-3 dormant blueprint ceiling"
        )

    max_manifest_size_bytes = require_non_negative_int(
        normalized["max_manifest_size_bytes"], "max_manifest_size_bytes"
    )
    if max_manifest_size_bytes > MAX_MANIFEST_SIZE_BYTES:
        raise Phase3StructureError("max_manifest_size_bytes exceeds manifest-size ceiling")

    max_bundle_payload_size_bytes = require_non_negative_int(
        normalized["max_bundle_payload_size_bytes"], "max_bundle_payload_size_bytes"
    )
    if max_bundle_payload_size_bytes > PHASE3_BUNDLE_PAYLOAD_CEILING_BYTES:
        raise Phase3StructureError(
            "max_bundle_payload_size_bytes exceeds bundle-payload ceiling"
        )

    return {
        "profile": profile,
        "max_active_cells": max_active_cells,
        "max_tissues": max_tissues,
        "max_members_per_tissue_before_review": max_members_per_tissue_before_review,
        "max_dormant_blueprints": max_dormant_blueprints,
        "max_manifest_size_bytes": max_manifest_size_bytes,
        "max_bundle_payload_size_bytes": max_bundle_payload_size_bytes,
        "policy_envelope": require_mapping(
            normalized["policy_envelope"], "policy_envelope"
        ),
    }


def default_profile_budget_payload(profile: str) -> dict[str, Any]:
    resolved_profile = require_profile_name(profile, "profile")
    return {
        "profile": resolved_profile,
        "max_active_cells": PROFILE_ACTIVE_CELL_CEILINGS[resolved_profile],
        "max_tissues": PHASE3_TISSUE_CEILING,
        "max_members_per_tissue_before_review": SPLIT_PRESSURE_MEMBER_COUNT,
        "max_dormant_blueprints": PHASE3_DORMANT_BLUEPRINT_CEILING,
        "max_manifest_size_bytes": MAX_MANIFEST_SIZE_BYTES,
        "max_bundle_payload_size_bytes": PHASE3_BUNDLE_PAYLOAD_CEILING_BYTES,
        "policy_envelope": {},
    }


def validate_profile_budget_context(context: Mapping[str, Any]) -> dict[str, int]:
    normalized = dict(context)
    for field_name in REQUIRED_PROFILE_BUDGET_CONTEXT_FIELDS:
        if field_name not in normalized:
            raise Phase3StructureError(
                f"missing required profile budget context field: {field_name}"
            )
    return {
        "active_cell_count": require_non_negative_int(
            normalized["active_cell_count"], "active_cell_count"
        ),
        "tissue_count": require_non_negative_int(normalized["tissue_count"], "tissue_count"),
        "largest_tissue_member_count": require_non_negative_int(
            normalized["largest_tissue_member_count"], "largest_tissue_member_count"
        ),
        "dormant_blueprint_count": require_non_negative_int(
            normalized["dormant_blueprint_count"], "dormant_blueprint_count"
        ),
        "manifest_size_bytes": require_non_negative_int(
            normalized["manifest_size_bytes"], "manifest_size_bytes"
        ),
        "bundle_payload_size_bytes": require_non_negative_int(
            normalized["bundle_payload_size_bytes"], "bundle_payload_size_bytes"
        ),
    }


@dataclass(frozen=True, slots=True)
class ProfileBudgetRule:
    profile: str
    max_active_cells: int
    max_tissues: int
    max_members_per_tissue_before_review: int
    max_dormant_blueprints: int
    max_manifest_size_bytes: int
    max_bundle_payload_size_bytes: int
    policy_envelope: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ProfileBudgetRule":
        normalized = validate_profile_budget_payload(payload)
        return cls(**normalized)

    @classmethod
    def for_profile(cls, profile: str) -> "ProfileBudgetRule":
        return cls.from_payload(default_profile_budget_payload(profile))

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "max_active_cells": self.max_active_cells,
            "max_tissues": self.max_tissues,
            "max_members_per_tissue_before_review": self.max_members_per_tissue_before_review,
            "max_dormant_blueprints": self.max_dormant_blueprints,
            "max_manifest_size_bytes": self.max_manifest_size_bytes,
            "max_bundle_payload_size_bytes": self.max_bundle_payload_size_bytes,
            "policy_envelope": dict(self.policy_envelope),
        }

    def validate(self) -> None:
        validate_profile_budget_payload(self.to_dict())

    def evaluate(self, context: Mapping[str, Any]) -> dict[str, Any]:
        normalized_context = validate_profile_budget_context(context)
        violations: list[str] = []
        if normalized_context["active_cell_count"] > self.max_active_cells:
            violations.append("active_cell_count exceeds max_active_cells")
        if normalized_context["tissue_count"] > self.max_tissues:
            violations.append("tissue_count exceeds max_tissues")
        if (
            normalized_context["largest_tissue_member_count"]
            > self.max_members_per_tissue_before_review
        ):
            violations.append(
                "largest_tissue_member_count exceeds max_members_per_tissue_before_review"
            )
        if normalized_context["dormant_blueprint_count"] > self.max_dormant_blueprints:
            violations.append("dormant_blueprint_count exceeds max_dormant_blueprints")
        if normalized_context["manifest_size_bytes"] > self.max_manifest_size_bytes:
            violations.append("manifest_size_bytes exceeds max_manifest_size_bytes")
        if (
            normalized_context["bundle_payload_size_bytes"]
            > self.max_bundle_payload_size_bytes
        ):
            violations.append(
                "bundle_payload_size_bytes exceeds max_bundle_payload_size_bytes"
            )
        return {
            "allow": len(violations) == 0,
            "profile": self.profile,
            "reason": "budget check passed"
            if len(violations) == 0
            else "budget ceiling exceeded",
            "violations": violations,
            "checked_context": normalized_context,
        }


def evaluate_profile_budget(
    *,
    profile: str,
    context: Mapping[str, Any],
    policy_envelope: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    rule = ProfileBudgetRule.from_payload(
        {
            **default_profile_budget_payload(profile),
            "policy_envelope": dict(policy_envelope or {}),
        }
    )
    return rule.evaluate(context)

