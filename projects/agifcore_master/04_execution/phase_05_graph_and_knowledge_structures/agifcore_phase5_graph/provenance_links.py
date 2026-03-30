from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Mapping

MAX_PROVENANCE_LINKS = 16
ALLOWED_ENTITY_KINDS = ("descriptor", "skill", "concept", "transfer", "edge", "selection")
ALLOWED_ORIGIN_KINDS = ("inherited", "constructed")
ALLOWED_REFERENCE_ROLES = (
    "source_memory",
    "review",
    "rollback",
    "replay",
    "workspace",
    "artifact",
    "source",
    "correction",
    "compression",
    "retirement",
)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clamp_score(value: float) -> float:
    return round(min(1.0, max(0.0, float(value))), 6)


def stable_hash_payload(payload: Mapping[str, Any]) -> str:
    return sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class ProvenanceLinksError(ValueError):
    """Raised when Phase 5 provenance links are missing or malformed."""


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProvenanceLinksError(f"{field_name} must be a non-empty string")
    return value


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ProvenanceLinksError(f"{field_name} must be a mapping")
    return dict(value)


def require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ProvenanceLinksError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        text = require_non_empty_str(item, f"{field_name}[]")
        if text in seen:
            raise ProvenanceLinksError(f"{field_name} contains duplicate entries")
        seen.add(text)
        result.append(text)
    return result


@dataclass(slots=True)
class ProvenanceLink:
    role: str
    ref_id: str
    ref_kind: str
    source_path: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "ref_id": self.ref_id,
            "ref_kind": self.ref_kind,
            "source_path": self.source_path,
            "metadata": deepcopy(self.metadata),
        }


@dataclass(slots=True)
class ProvenanceBundle:
    entity_kind: str
    entity_id: str
    origin_kind: str
    links: list[ProvenanceLink]
    inherited_from: list[str]
    created_at: str
    provenance_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_kind": self.entity_kind,
            "entity_id": self.entity_id,
            "origin_kind": self.origin_kind,
            "links": [link.to_dict() for link in self.links],
            "inherited_from": list(self.inherited_from),
            "created_at": self.created_at,
            "provenance_hash": self.provenance_hash,
        }


def _normalize_link(link: ProvenanceLink | Mapping[str, Any]) -> ProvenanceLink:
    if isinstance(link, ProvenanceLink):
        normalized = link
    else:
        link_map = require_mapping(link, "provenance_link")
        normalized = ProvenanceLink(
            role=require_non_empty_str(link_map.get("role"), "role"),
            ref_id=require_non_empty_str(link_map.get("ref_id"), "ref_id"),
            ref_kind=require_non_empty_str(link_map.get("ref_kind"), "ref_kind"),
            source_path=require_non_empty_str(link_map.get("source_path"), "source_path"),
            metadata=require_mapping(link_map.get("metadata", {}), "metadata"),
        )
    if normalized.role not in ALLOWED_REFERENCE_ROLES:
        raise ProvenanceLinksError(f"role must be one of {ALLOWED_REFERENCE_ROLES}")
    return normalized


def build_provenance_bundle(
    *,
    entity_kind: str,
    entity_id: str,
    origin_kind: str,
    links: list[ProvenanceLink | Mapping[str, Any]],
    inherited_from: list[str] | None = None,
) -> ProvenanceBundle:
    normalized_kind = require_non_empty_str(entity_kind, "entity_kind")
    if normalized_kind not in ALLOWED_ENTITY_KINDS:
        raise ProvenanceLinksError(f"entity_kind must be one of {ALLOWED_ENTITY_KINDS}")
    normalized_origin = require_non_empty_str(origin_kind, "origin_kind")
    if normalized_origin not in ALLOWED_ORIGIN_KINDS:
        raise ProvenanceLinksError(f"origin_kind must be one of {ALLOWED_ORIGIN_KINDS}")
    normalized_links = [_normalize_link(link) for link in links]
    if not normalized_links:
        raise ProvenanceLinksError("links must contain at least one provenance link")
    if len(normalized_links) > MAX_PROVENANCE_LINKS:
        raise ProvenanceLinksError("provenance link fanout exceeds Phase 5 ceiling")
    role_ref_pairs: set[tuple[str, str]] = set()
    for link in normalized_links:
        pair = (link.role, link.ref_id)
        if pair in role_ref_pairs:
            raise ProvenanceLinksError("duplicate provenance role/ref_id pair")
        role_ref_pairs.add(pair)
    normalized_inherited_from = require_unique_str_list(inherited_from or [], "inherited_from")
    payload = {
        "entity_kind": normalized_kind,
        "entity_id": require_non_empty_str(entity_id, "entity_id"),
        "origin_kind": normalized_origin,
        "links": [link.to_dict() for link in normalized_links],
        "inherited_from": list(normalized_inherited_from),
    }
    return ProvenanceBundle(
        entity_kind=payload["entity_kind"],
        entity_id=payload["entity_id"],
        origin_kind=payload["origin_kind"],
        links=normalized_links,
        inherited_from=normalized_inherited_from,
        created_at=utc_timestamp(),
        provenance_hash=stable_hash_payload(payload),
    )


def bundle_from_dict(payload: Mapping[str, Any]) -> ProvenanceBundle:
    payload_map = require_mapping(payload, "provenance_bundle")
    bundle = build_provenance_bundle(
        entity_kind=payload_map.get("entity_kind"),
        entity_id=payload_map.get("entity_id"),
        origin_kind=payload_map.get("origin_kind"),
        links=payload_map.get("links", []),
        inherited_from=payload_map.get("inherited_from", []),
    )
    created_at = payload_map.get("created_at")
    if created_at is not None:
        bundle.created_at = require_non_empty_str(created_at, "created_at")
    provenance_hash = payload_map.get("provenance_hash")
    if provenance_hash is not None:
        bundle.provenance_hash = require_non_empty_str(provenance_hash, "provenance_hash")
    return bundle


def require_roles(bundle: ProvenanceBundle, required_roles: tuple[str, ...]) -> None:
    present = {link.role for link in bundle.links}
    missing = [role for role in required_roles if role not in present]
    if missing:
        raise ProvenanceLinksError(f"missing required provenance roles: {missing}")


def provenance_score(bundle: ProvenanceBundle) -> float:
    roles = {link.role for link in bundle.links}
    score = 0.0
    if "source_memory" in roles:
        score += 0.35
    if "review" in roles:
        score += 0.35
    if "rollback" in roles or "workspace" in roles:
        score += 0.15
    if bundle.origin_kind == "inherited" and bundle.inherited_from:
        score += 0.1
    if "artifact" in roles or "source" in roles:
        score += 0.05
    return clamp_score(score)
