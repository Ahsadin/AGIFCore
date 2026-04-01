from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from cell_contracts import (
    MAX_MANIFEST_SIZE_BYTES,
    Phase3StructureError,
    canonical_size_bytes,
    require_mapping,
    require_non_empty_str,
    require_unique_string_list,
)

MAX_TISSUE_MEMBERS = 16
MAX_ROUTING_TARGETS = 8
SPLIT_PRESSURE_MEMBER_COUNT = 8
REQUIRED_TISSUE_MANIFEST_FIELDS = (
    "tissue_id",
    "tissue_name",
    "allowed_role_families",
    "member_cell_ids",
    "routing_targets",
    "policy_envelope",
)


def validate_tissue_manifest_payload(
    payload: Mapping[str, Any],
    *,
    cell_contracts_by_id: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    normalized = dict(payload)
    for field_name in REQUIRED_TISSUE_MANIFEST_FIELDS:
        if field_name not in normalized:
            raise Phase3StructureError(
                f"missing required tissue manifest field: {field_name}"
            )

    normalized_manifest = {
        "tissue_id": require_non_empty_str(normalized["tissue_id"], "tissue_id"),
        "tissue_name": require_non_empty_str(
            normalized["tissue_name"], "tissue_name"
        ),
        "allowed_role_families": require_unique_string_list(
            normalized["allowed_role_families"], "allowed_role_families"
        ),
        "member_cell_ids": require_unique_string_list(
            normalized["member_cell_ids"], "member_cell_ids"
        ),
        "routing_targets": require_unique_string_list(
            normalized["routing_targets"], "routing_targets"
        ),
        "policy_envelope": require_mapping(
            normalized["policy_envelope"], "policy_envelope"
        ),
    }

    if len(normalized_manifest["member_cell_ids"]) > MAX_TISSUE_MEMBERS:
        raise Phase3StructureError(
            "tissue manifest exceeds max tissue membership fanout"
        )
    if len(normalized_manifest["routing_targets"]) > MAX_ROUTING_TARGETS:
        raise Phase3StructureError("tissue manifest exceeds max routing targets")

    if cell_contracts_by_id:
        tissue_id = normalized_manifest["tissue_id"]
        allowed_role_families = set(normalized_manifest["allowed_role_families"])
        for cell_id in normalized_manifest["member_cell_ids"]:
            contract = cell_contracts_by_id.get(cell_id)
            if contract is None:
                raise Phase3StructureError(f"unknown tissue member cell_id: {cell_id}")
            role_family = require_non_empty_str(
                contract.get("role_family"), "role_family"
            )
            if role_family not in allowed_role_families:
                raise Phase3StructureError(
                    f"member cell {cell_id} has disallowed role_family: {role_family}"
                )
            allowed_tissues = require_unique_string_list(
                contract.get("allowed_tissues"), "allowed_tissues"
            )
            if tissue_id not in allowed_tissues:
                raise Phase3StructureError(
                    f"member cell {cell_id} does not allow tissue membership for {tissue_id}"
                )

    if canonical_size_bytes(normalized_manifest) > MAX_MANIFEST_SIZE_BYTES:
        raise Phase3StructureError("tissue manifest exceeds max manifest size")
    return normalized_manifest


@dataclass(frozen=True, slots=True)
class TissueManifest:
    """Slice-1 structural tissue manifest. No memory or graph logic allowed here."""

    tissue_id: str
    tissue_name: str
    allowed_role_families: list[str]
    member_cell_ids: list[str]
    routing_targets: list[str]
    policy_envelope: dict[str, Any]

    @classmethod
    def from_payload(
        cls,
        payload: Mapping[str, Any],
        *,
        cell_contracts_by_id: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> "TissueManifest":
        normalized = validate_tissue_manifest_payload(
            payload,
            cell_contracts_by_id=cell_contracts_by_id,
        )
        return cls(**normalized)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tissue_id": self.tissue_id,
            "tissue_name": self.tissue_name,
            "allowed_role_families": list(self.allowed_role_families),
            "member_cell_ids": list(self.member_cell_ids),
            "routing_targets": list(self.routing_targets),
            "policy_envelope": dict(self.policy_envelope),
        }

    def validate(
        self,
        *,
        cell_contracts_by_id: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> None:
        validate_tissue_manifest_payload(
            self.to_dict(),
            cell_contracts_by_id=cell_contracts_by_id,
        )

    def needs_split_review(self) -> bool:
        return len(self.member_cell_ids) > SPLIT_PRESSURE_MEMBER_COUNT
