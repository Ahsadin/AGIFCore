from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping

MAX_MANIFEST_SIZE_BYTES = 64 * 1024
REQUIRED_CELL_CONTRACT_FIELDS = (
    "cell_id",
    "bundle_ref",
    "role_family",
    "role_name",
    "allowed_tissues",
    "split_policy",
    "merge_policy",
    "trust_profile",
    "policy_envelope",
)


class Phase3StructureError(ValueError):
    """Raised when a Phase 3 slice-1 structure violates the governed boundary."""


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(dict(payload), sort_keys=True).encode("utf-8"))


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase3StructureError(f"{field_name} must be a non-empty string")
    return value


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase3StructureError(f"{field_name} must be a mapping")
    return dict(value)


def require_unique_string_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise Phase3StructureError(f"{field_name} must be a list")
    result: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise Phase3StructureError(
                f"{field_name} entries must be non-empty strings"
            )
        if item in seen:
            raise Phase3StructureError(f"{field_name} contains duplicate entries")
        seen.add(item)
        result.append(item)
    return result


def validate_cell_contract_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    for field_name in REQUIRED_CELL_CONTRACT_FIELDS:
        if field_name not in normalized:
            raise Phase3StructureError(
                f"missing required cell contract field: {field_name}"
            )

    normalized_contract = {
        "cell_id": require_non_empty_str(normalized["cell_id"], "cell_id"),
        "bundle_ref": require_non_empty_str(normalized["bundle_ref"], "bundle_ref"),
        "role_family": require_non_empty_str(
            normalized["role_family"], "role_family"
        ),
        "role_name": require_non_empty_str(normalized["role_name"], "role_name"),
        "allowed_tissues": require_unique_string_list(
            normalized["allowed_tissues"], "allowed_tissues"
        ),
        "split_policy": require_mapping(normalized["split_policy"], "split_policy"),
        "merge_policy": require_mapping(normalized["merge_policy"], "merge_policy"),
        "trust_profile": require_mapping(
            normalized["trust_profile"], "trust_profile"
        ),
        "policy_envelope": require_mapping(
            normalized["policy_envelope"], "policy_envelope"
        ),
    }
    if canonical_size_bytes(normalized_contract) > MAX_MANIFEST_SIZE_BYTES:
        raise Phase3StructureError("cell contract exceeds max manifest size")
    return normalized_contract


@dataclass(frozen=True, slots=True)
class CellContract:
    """Slice-1 cell contract aligned to the Phase 2 registry and lifecycle surface."""

    cell_id: str
    bundle_ref: str
    role_family: str
    role_name: str
    allowed_tissues: list[str]
    split_policy: dict[str, Any]
    merge_policy: dict[str, Any]
    trust_profile: dict[str, Any]
    policy_envelope: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "CellContract":
        normalized = validate_cell_contract_payload(payload)
        return cls(**normalized)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cell_id": self.cell_id,
            "bundle_ref": self.bundle_ref,
            "role_family": self.role_family,
            "role_name": self.role_name,
            "allowed_tissues": list(self.allowed_tissues),
            "split_policy": dict(self.split_policy),
            "merge_policy": dict(self.merge_policy),
            "trust_profile": dict(self.trust_profile),
            "policy_envelope": dict(self.policy_envelope),
        }

    def validate(self) -> None:
        validate_cell_contract_payload(self.to_dict())

    def allows_tissue(self, tissue_id: str) -> bool:
        require_non_empty_str(tissue_id, "tissue_id")
        return tissue_id in self.allowed_tissues
