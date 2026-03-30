from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from bundle_manifest import REQUIRED_SCHEMA_KEYS, validate_bundle_manifest_payload
from cell_contracts import Phase3StructureError, validate_cell_contract_payload
from tissue_manifests import validate_tissue_manifest_payload


def runtime_root() -> Path:
    return Path(__file__).resolve().parent


def schema_root() -> Path:
    return runtime_root() / "schemas"


def resolve_schema_path(schema_ref: str, *, base_dir: Path | None = None) -> Path:
    if not isinstance(schema_ref, str) or not schema_ref.strip():
        raise Phase3StructureError("schema reference must be a non-empty string")
    root = base_dir or runtime_root()
    candidate = Path(schema_ref)
    path = candidate if candidate.is_absolute() else root / candidate
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise Phase3StructureError(
            f"schema reference escapes runtime root: {schema_ref}"
        ) from exc
    if not resolved.exists():
        raise Phase3StructureError(f"schema reference does not exist: {schema_ref}")
    return resolved


def load_schema_document(schema_ref: str, *, base_dir: Path | None = None) -> dict[str, Any]:
    resolved = resolve_schema_path(schema_ref, base_dir=base_dir)
    try:
        payload = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise Phase3StructureError(
            f"schema file is not valid JSON: {resolved}"
        ) from exc
    if not isinstance(payload, dict):
        raise Phase3StructureError(f"schema document must be a JSON object: {resolved}")
    return payload


def validate_bundle_schema_foundation(
    payload: Mapping[str, Any],
    *,
    base_dir: Path | None = None,
) -> dict[str, Any]:
    bundle_manifest = validate_bundle_manifest_payload(payload)
    schema_paths: dict[str, str] = {}
    for schema_key in REQUIRED_SCHEMA_KEYS:
        schema_ref = bundle_manifest["schema_refs"][schema_key]
        document = load_schema_document(schema_ref, base_dir=base_dir)
        title = document.get("title")
        if not isinstance(title, str) or not title.strip():
            raise Phase3StructureError(
                f"schema document missing title: {schema_ref}"
            )
        schema_paths[schema_key] = str(
            resolve_schema_path(schema_ref, base_dir=base_dir)
        )

    cell_contract = validate_cell_contract_payload(
        bundle_manifest["payload_inventory"]["cell_contract"]
    )
    tissue_manifest = validate_tissue_manifest_payload(
        bundle_manifest["payload_inventory"]["tissue_manifest"],
        cell_contracts_by_id={cell_contract["cell_id"]: cell_contract},
    )
    return {
        "bundle_manifest": bundle_manifest,
        "cell_contract": cell_contract,
        "tissue_manifest": tissue_manifest,
        "schema_paths": schema_paths,
    }
