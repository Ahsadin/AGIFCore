from __future__ import annotations

from typing import Any, Mapping

from .entity_classes import (
    MAX_TARGET_DOMAIN_OBJECTS,
    Phase6EntityError,
    TargetDomainObject,
    TargetDomainStructure,
    bundle_from_dict,
    build_provenance_bundle,
    canonical_size_bytes,
    require_mapping,
    require_non_empty_str,
    require_schema,
    require_unique_str_list,
    stable_hash_payload,
)

MAX_TARGET_DOMAIN_BYTES = 2 * 1024 * 1024


class TargetDomainError(ValueError):
    """Raised when target-domain structures violate Phase 6 bounds or contracts."""


_RECOMMENDED_STRUCTURES: tuple[dict[str, Any], ...] = (
    {
        "domain_id": "finance_document_workflows",
        "domain_name": "finance document workflows",
        "prefixes": ["finance.", "document.", "invoice."],
        "descriptor_tokens": ["invoice", "ledger", "approval"],
        "object_templates": ["finance.queue", "document.packet", "invoice.record"],
        "requires_target_match": True,
        "minimum_signal_groups": 3,
    },
    {
        "domain_id": "pos_store_operations",
        "domain_name": "POS/store operations",
        "prefixes": ["pos.", "store.", "inventory."],
        "descriptor_tokens": ["store", "inventory", "restock"],
        "object_templates": ["store.queue", "inventory.item", "restock.route"],
        "requires_target_match": True,
        "minimum_signal_groups": 3,
    },
    {
        "domain_id": "procurement_work_order_processing",
        "domain_name": "procurement/work-order processing",
        "prefixes": ["procurement.", "work_order."],
        "descriptor_tokens": ["procurement", "work", "route"],
        "object_templates": ["procurement.ticket", "work_order.packet", "vendor.route"],
        "requires_target_match": True,
        "minimum_signal_groups": 3,
    },
    {
        "domain_id": "claims_case_handling",
        "domain_name": "claims/case handling",
        "prefixes": ["claims.", "case."],
        "descriptor_tokens": ["claim", "case", "evidence"],
        "object_templates": ["claims.packet", "case.timeline", "evidence.bundle"],
        "requires_target_match": True,
        "minimum_signal_groups": 3,
    },
    {
        "domain_id": "maintenance_diagnostics",
        "domain_name": "maintenance/diagnostics",
        "prefixes": ["maintenance.", "diagnostics.", "ops.field_execution."],
        "descriptor_tokens": ["maintenance", "diagnostic", "route"],
        "object_templates": ["maintenance.alert", "diagnostic.trace", "field.route"],
        "requires_target_match": True,
        "minimum_signal_groups": 3,
    },
    {
        "domain_id": "building_home_infrastructure_events",
        "domain_name": "building/home infrastructure events",
        "prefixes": ["building.", "home.", "ops.local_dispatch."],
        "descriptor_tokens": ["building", "home", "dispatch"],
        "object_templates": ["building.event", "home.alert", "dispatch.route"],
        "requires_target_match": True,
        "minimum_signal_groups": 3,
    },
    {
        "domain_id": "planning_coordination_workflows",
        "domain_name": "planning/coordination workflows",
        "prefixes": ["planning.", "coordination.", "ops."],
        "descriptor_tokens": ["plan", "coordination", "route"],
        "object_templates": ["planning.packet", "coordination.event", "ops.route"],
        "requires_target_match": False,
        "minimum_signal_groups": 3,
    },
    {
        "domain_id": "compliance_support_triage",
        "domain_name": "compliance/support triage",
        "prefixes": ["compliance.", "support."],
        "descriptor_tokens": ["compliance", "support", "policy"],
        "object_templates": ["compliance.rule", "support.ticket", "policy.response"],
        "requires_target_match": True,
        "minimum_signal_groups": 3,
    },
)


class TargetDomainRegistry:
    """Canonical Phase 6 target-domain registry with bounded object counts."""

    def __init__(
        self,
        *,
        store_id: str = "phase-06-target-domains",
        max_objects: int = MAX_TARGET_DOMAIN_OBJECTS,
        max_state_bytes: int = MAX_TARGET_DOMAIN_BYTES,
    ) -> None:
        self.store_id = store_id
        self.max_objects = max_objects
        self.max_state_bytes = max_state_bytes
        self._structures: dict[str, TargetDomainStructure] = {}
        self._order: list[str] = []

    def register_structure(
        self,
        *,
        domain_id: str,
        domain_name: str,
        prefixes: list[str],
        descriptor_tokens: list[str],
        object_templates: list[str],
        requires_target_match: bool,
        minimum_signal_groups: int,
        provenance_links: list[Mapping[str, Any]],
        origin_kind: str = "inherited",
        inherited_from: list[str] | None = None,
    ) -> str:
        normalized_id = require_non_empty_str(domain_id, "domain_id")
        if normalized_id in self._structures:
            raise TargetDomainError(f"duplicate domain_id: {normalized_id}")
        if not isinstance(minimum_signal_groups, int) or minimum_signal_groups <= 0:
            raise TargetDomainError("minimum_signal_groups must be a positive integer")
        provenance = build_provenance_bundle(
            entity_kind="target_domain_structure",
            entity_id=normalized_id,
            origin_kind=origin_kind,
            links=provenance_links,
            inherited_from=inherited_from,
        )
        objects: list[TargetDomainObject] = []
        for template in require_unique_str_list(object_templates, "object_templates"):
            payload = {
                "domain_id": normalized_id,
                "label": template,
                "category": template.split(".")[0],
            }
            object_id = f"{normalized_id}::{template}"
            object_provenance = build_provenance_bundle(
                entity_kind="target_domain_object",
                entity_id=object_id,
                origin_kind=origin_kind,
                links=provenance_links,
                inherited_from=inherited_from,
            )
            objects.append(
                TargetDomainObject(
                    object_id=object_id,
                    domain_id=normalized_id,
                    label=template,
                    category=payload["category"],
                    provenance=object_provenance,
                    object_hash=stable_hash_payload(payload),
                )
            )
        structure_payload = {
            "domain_id": normalized_id,
            "domain_name": require_non_empty_str(domain_name, "domain_name"),
            "prefixes": require_unique_str_list(prefixes, "prefixes"),
            "descriptor_tokens": require_unique_str_list(descriptor_tokens, "descriptor_tokens"),
            "minimum_signal_groups": minimum_signal_groups,
            "object_templates": require_unique_str_list(object_templates, "object_templates"),
            "requires_target_match": bool(requires_target_match),
        }
        structure = TargetDomainStructure(
            domain_id=normalized_id,
            domain_name=structure_payload["domain_name"],
            prefixes=tuple(structure_payload["prefixes"]),
            descriptor_tokens=tuple(structure_payload["descriptor_tokens"]),
            minimum_signal_groups=minimum_signal_groups,
            object_templates=tuple(structure_payload["object_templates"]),
            objects=tuple(objects),
            requires_target_match=bool(requires_target_match),
            provenance=provenance,
            structure_hash=stable_hash_payload(structure_payload),
        )
        self._structures[normalized_id] = structure
        self._order.append(normalized_id)
        self._ensure_size()
        return normalized_id

    def structure_state(self, domain_id: str) -> dict[str, Any]:
        structure = self._structures.get(require_non_empty_str(domain_id, "domain_id"))
        if structure is None:
            raise TargetDomainError(f"unknown domain_id: {domain_id}")
        return structure.to_dict()

    def domain_ids(self) -> list[str]:
        return list(self._order)

    def match_domains(
        self,
        *,
        labels: list[str],
        allowed_domains: list[str] | None = None,
    ) -> list[str]:
        allowed = set(allowed_domains or self._order)
        normalized_labels = [label.lower() for label in require_unique_str_list(labels, "labels")]
        joined = " ".join(normalized_labels)
        matches: list[str] = []
        for domain_id in self._order:
            if domain_id not in allowed:
                continue
            structure = self._structures[domain_id]
            if any(prefix.lower() in joined for prefix in structure.prefixes):
                matches.append(domain_id)
                continue
            if any(token.lower() in joined for token in structure.descriptor_tokens):
                matches.append(domain_id)
        return matches

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_06.target_domains.v1",
            "store_id": self.store_id,
            "max_objects": self.max_objects,
            "structures": [self._structures[domain_id].to_dict() for domain_id in self._order],
            "state_hash": stable_hash_payload(
                {"structures": [self._structures[domain_id].to_dict() for domain_id in self._order]}
            ),
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        payload_map = require_schema(payload, "agifcore.phase_06.target_domains.v1", "target_domain_state")
        self.store_id = require_non_empty_str(payload_map.get("store_id"), "store_id")
        max_objects = payload_map.get("max_objects", self.max_objects)
        if not isinstance(max_objects, int) or max_objects <= 0:
            raise TargetDomainError("max_objects must be a positive integer")
        self.max_objects = max_objects
        self._structures = {}
        self._order = []
        for structure_payload in payload_map.get("structures", []):
            structure_map = require_mapping(structure_payload, "structure")
            objects: list[TargetDomainObject] = []
            for object_payload in structure_map.get("objects", []):
                object_map = require_mapping(object_payload, "object")
                object_provenance = bundle_from_dict(require_mapping(object_map.get("provenance"), "provenance"))
                objects.append(
                    TargetDomainObject(
                        object_id=require_non_empty_str(object_map.get("object_id"), "object_id"),
                        domain_id=require_non_empty_str(object_map.get("domain_id"), "domain_id"),
                        label=require_non_empty_str(object_map.get("label"), "label"),
                        category=require_non_empty_str(object_map.get("category"), "category"),
                        provenance=object_provenance,
                        object_hash=require_non_empty_str(object_map.get("object_hash"), "object_hash"),
                    )
                )
            provenance = bundle_from_dict(require_mapping(structure_map.get("provenance"), "provenance"))
            structure = TargetDomainStructure(
                domain_id=require_non_empty_str(structure_map.get("domain_id"), "domain_id"),
                domain_name=require_non_empty_str(structure_map.get("domain_name"), "domain_name"),
                prefixes=tuple(require_unique_str_list(structure_map.get("prefixes", []), "prefixes")),
                descriptor_tokens=tuple(
                    require_unique_str_list(structure_map.get("descriptor_tokens", []), "descriptor_tokens")
                ),
                minimum_signal_groups=int(structure_map.get("minimum_signal_groups")),
                object_templates=tuple(
                    require_unique_str_list(structure_map.get("object_templates", []), "object_templates")
                ),
                objects=tuple(objects),
                requires_target_match=bool(structure_map.get("requires_target_match", True)),
                provenance=provenance,
                structure_hash=require_non_empty_str(structure_map.get("structure_hash"), "structure_hash"),
            )
            self._structures[structure.domain_id] = structure
            self._order.append(structure.domain_id)
        self._ensure_size()

    def _ensure_size(self) -> None:
        object_count = sum(len(self._structures[domain_id].objects) for domain_id in self._order)
        if object_count > self.max_objects:
            raise TargetDomainError("target-domain object count exceeds Phase 6 ceiling")
        if canonical_size_bytes(self.export_state()) > self.max_state_bytes:
            raise TargetDomainError("target-domain state exceeds Phase 6 byte ceiling")


def build_default_registry() -> TargetDomainRegistry:
    registry = TargetDomainRegistry()
    links = [
        {
            "role": "source",
            "ref_id": "phase-06-target-domain-port",
            "ref_kind": "target_domain_contract",
            "source_path": "agif_fabric_v1/intelligence/fabric/domain",
        },
        {
            "role": "review",
            "ref_id": "phase-06-target-domain-review",
            "ref_kind": "governor_review",
            "source_path": "projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md",
        },
    ]
    for structure in _RECOMMENDED_STRUCTURES:
        registry.register_structure(
            domain_id=structure["domain_id"],
            domain_name=structure["domain_name"],
            prefixes=list(structure["prefixes"]),
            descriptor_tokens=list(structure["descriptor_tokens"]),
            object_templates=list(structure["object_templates"]),
            requires_target_match=bool(structure["requires_target_match"]),
            minimum_signal_groups=int(structure["minimum_signal_groups"]),
            provenance_links=links,
            inherited_from=["agif_fabric_v1", "agif_v2_master"],
        )
    return registry
