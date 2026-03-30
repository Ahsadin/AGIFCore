from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from cell_contracts import (
    Phase3StructureError,
    canonical_size_bytes,
    require_mapping,
    require_non_empty_str,
    require_unique_string_list,
)

MAX_BUNDLE_PAYLOAD_BYTES = 8 * 1024 * 1024
REQUIRED_BUNDLE_MANIFEST_FIELDS = (
    "bundle_id",
    "bundle_version",
    "bundle_type",
    "entry_contracts",
    "schema_refs",
    "payload_inventory",
    "provenance_fields",
)
REQUIRED_SCHEMA_KEYS = ("cell_contract", "tissue_manifest", "bundle_manifest")


def validate_bundle_manifest_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    for field_name in REQUIRED_BUNDLE_MANIFEST_FIELDS:
        if field_name not in normalized:
            raise Phase3StructureError(
                f"missing required bundle manifest field: {field_name}"
            )

    entry_contracts = require_unique_string_list(
        normalized["entry_contracts"], "entry_contracts"
    )
    schema_refs = require_mapping(normalized["schema_refs"], "schema_refs")
    payload_inventory = require_mapping(
        normalized["payload_inventory"], "payload_inventory"
    )
    provenance_fields = require_mapping(
        normalized["provenance_fields"], "provenance_fields"
    )

    for schema_key in REQUIRED_SCHEMA_KEYS:
        require_non_empty_str(schema_refs.get(schema_key), f"schema_refs.{schema_key}")
    if "cell_contract" not in payload_inventory or "tissue_manifest" not in payload_inventory:
        raise Phase3StructureError(
            "payload_inventory must include cell_contract and tissue_manifest"
        )
    require_mapping(payload_inventory["cell_contract"], "payload_inventory.cell_contract")
    require_mapping(
        payload_inventory["tissue_manifest"], "payload_inventory.tissue_manifest"
    )

    normalized_manifest = {
        "bundle_id": require_non_empty_str(normalized["bundle_id"], "bundle_id"),
        "bundle_version": require_non_empty_str(
            normalized["bundle_version"], "bundle_version"
        ),
        "bundle_type": require_non_empty_str(normalized["bundle_type"], "bundle_type"),
        "entry_contracts": entry_contracts,
        "schema_refs": schema_refs,
        "payload_inventory": payload_inventory,
        "provenance_fields": provenance_fields,
    }
    if canonical_size_bytes(normalized_manifest) > MAX_BUNDLE_PAYLOAD_BYTES:
        raise Phase3StructureError("bundle manifest exceeds max bundle payload size")
    return normalized_manifest


@dataclass(frozen=True, slots=True)
class BundleManifest:
    """Slice-1 bundle metadata and schema-linkage surface."""

    bundle_id: str
    bundle_version: str
    bundle_type: str
    entry_contracts: list[str]
    schema_refs: dict[str, Any]
    payload_inventory: dict[str, Any]
    provenance_fields: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "BundleManifest":
        normalized = validate_bundle_manifest_payload(payload)
        return cls(**normalized)

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "bundle_version": self.bundle_version,
            "bundle_type": self.bundle_type,
            "entry_contracts": list(self.entry_contracts),
            "schema_refs": dict(self.schema_refs),
            "payload_inventory": dict(self.payload_inventory),
            "provenance_fields": dict(self.provenance_fields),
        }

    def validate(self) -> None:
        validate_bundle_manifest_payload(self.to_dict())
