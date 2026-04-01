from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Mapping

from bundle_manifest import validate_bundle_manifest_payload
from cell_contracts import Phase3StructureError, require_mapping, require_non_empty_str

DIGEST_PREFIX = "sha256:"
_SHA256_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def canonical_payload_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_sha256_digest(payload: Any) -> str:
    return f"{DIGEST_PREFIX}{hashlib.sha256(canonical_payload_bytes(payload)).hexdigest()}"


def validate_digest_format(digest_value: Any, field_name: str) -> str:
    digest = require_non_empty_str(digest_value, field_name)
    if not _SHA256_DIGEST_RE.match(digest):
        raise Phase3StructureError(
            f"{field_name} must be a sha256 digest in format sha256:<64 lowercase hex>"
        )
    return digest


def _normalize_integrity_record(entry_name: str, value: Any) -> dict[str, Any]:
    record = require_mapping(value, f"integrity_inventory.{entry_name}")
    if "payload" not in record:
        raise Phase3StructureError(
            f"integrity inventory entry missing payload: {entry_name}"
        )
    if "digest" not in record:
        raise Phase3StructureError(
            f"integrity inventory entry missing digest: {entry_name}"
        )
    digest = validate_digest_format(
        record["digest"], f"integrity_inventory.{entry_name}.digest"
    )
    return {"payload": record["payload"], "digest": digest}


@dataclass(frozen=True, slots=True)
class BundleIntegrityResult:
    bundle_id: str
    checked_entries: list[str]
    entry_digests: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "status": "pass",
            "digest_algorithm": "sha256",
            "checked_entries": list(self.checked_entries),
            "entry_digests": dict(self.entry_digests),
        }


def validate_bundle_integrity(
    bundle_manifest_payload: Mapping[str, Any],
    integrity_inventory: Mapping[str, Any],
) -> dict[str, Any]:
    bundle_manifest = validate_bundle_manifest_payload(bundle_manifest_payload)
    records = require_mapping(integrity_inventory, "integrity_inventory")
    manifest_inventory = require_mapping(
        bundle_manifest["payload_inventory"], "bundle_manifest.payload_inventory"
    )

    manifest_entry_names = sorted(manifest_inventory.keys())
    record_entry_names = sorted(records.keys())

    for entry_name in manifest_entry_names:
        if entry_name not in records:
            raise Phase3StructureError(
                f"missing integrity inventory entry for manifest payload: {entry_name}"
            )
    for entry_name in record_entry_names:
        if entry_name not in manifest_inventory:
            raise Phase3StructureError(
                f"integrity inventory has unknown entry not present in manifest: {entry_name}"
            )

    entry_digests: dict[str, str] = {}
    for entry_name in manifest_entry_names:
        record = _normalize_integrity_record(entry_name, records[entry_name])
        manifest_payload = manifest_inventory[entry_name]
        if record["payload"] != manifest_payload:
            raise Phase3StructureError(
                f"manifest/inventory payload mismatch for entry: {entry_name}"
            )

        expected_digest = record["digest"]
        actual_digest = compute_sha256_digest(record["payload"])
        if expected_digest != actual_digest:
            raise Phase3StructureError(
                f"hash mismatch for payload inventory entry: {entry_name}"
            )
        entry_digests[entry_name] = actual_digest

    result = BundleIntegrityResult(
        bundle_id=require_non_empty_str(bundle_manifest["bundle_id"], "bundle_id"),
        checked_entries=manifest_entry_names,
        entry_digests=entry_digests,
    )
    return result.to_dict()
