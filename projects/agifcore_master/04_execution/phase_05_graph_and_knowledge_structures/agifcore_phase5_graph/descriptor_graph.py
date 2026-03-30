from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Mapping

from .provenance_links import (
    ProvenanceBundle,
    ProvenanceLinksError,
    bundle_from_dict,
    canonical_size_bytes,
    build_provenance_bundle,
    require_mapping,
    require_non_empty_str,
    require_roles,
    require_unique_str_list,
    stable_hash_payload,
    utc_timestamp,
)
from .supersession_rules import SupersessionLedger, SupersessionRulesError

MAX_DESCRIPTOR_NODES = 768
MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024


class DescriptorGraphError(ValueError):
    """Raised when descriptor graph behavior violates Phase 5 boundaries."""


def _map_error(error: Exception) -> DescriptorGraphError:
    return DescriptorGraphError(str(error))


@dataclass(slots=True)
class DescriptorNode:
    descriptor_id: str
    descriptor_type: str
    label: str
    alias_tags: list[str]
    domain_tags: list[str]
    concept_tags: list[str]
    support_refs: list[str]
    trust_band: str
    policy_requirements: list[str]
    provenance: ProvenanceBundle
    created_at: str
    updated_at: str
    status: str = "active"
    superseded_by: str | None = None
    retirement_ref: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "descriptor_id": self.descriptor_id,
            "descriptor_type": self.descriptor_type,
            "label": self.label,
            "alias_tags": list(self.alias_tags),
            "domain_tags": list(self.domain_tags),
            "concept_tags": list(self.concept_tags),
            "support_refs": list(self.support_refs),
            "trust_band": self.trust_band,
            "policy_requirements": list(self.policy_requirements),
            "provenance": self.provenance.to_dict(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "superseded_by": self.superseded_by,
            "retirement_ref": self.retirement_ref,
            "metadata": deepcopy(self.metadata),
        }


@dataclass(slots=True)
class DescriptorEdge:
    edge_id: str
    source_descriptor_id: str
    target_descriptor_id: str
    relation: str
    weight: float
    provenance: ProvenanceBundle
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_descriptor_id": self.source_descriptor_id,
            "target_descriptor_id": self.target_descriptor_id,
            "relation": self.relation,
            "weight": self.weight,
            "provenance": self.provenance.to_dict(),
            "created_at": self.created_at,
        }


class DescriptorGraphStore:
    """Distinct descriptor graph with explicit retirement and supersession visibility."""

    def __init__(
        self,
        *,
        store_id: str = "phase-05-descriptor-graph",
        max_nodes: int = MAX_DESCRIPTOR_NODES,
        max_state_bytes: int = MAX_DESCRIPTOR_BYTES,
    ) -> None:
        self.store_id = store_id
        self.max_nodes = max_nodes
        self.max_state_bytes = max_state_bytes
        self._nodes: dict[str, DescriptorNode] = {}
        self._edges: dict[str, DescriptorEdge] = {}
        self._order: list[str] = []
        self._supersession = SupersessionLedger()

    def add_node(
        self,
        *,
        descriptor_id: str,
        descriptor_type: str,
        label: str,
        alias_tags: list[str],
        domain_tags: list[str],
        concept_tags: list[str],
        support_refs: list[str],
        trust_band: str,
        policy_requirements: list[str],
        provenance_links: list[Mapping[str, Any]],
        origin_kind: str = "constructed",
        inherited_from: list[str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        normalized_id = require_non_empty_str(descriptor_id, "descriptor_id")
        if normalized_id in self._nodes:
            raise DescriptorGraphError(f"duplicate descriptor_id: {normalized_id}")
        try:
            provenance = build_provenance_bundle(
                entity_kind="descriptor",
                entity_id=normalized_id,
                origin_kind=origin_kind,
                links=provenance_links,
                inherited_from=inherited_from,
            )
            require_roles(provenance, ("source_memory", "review"))
        except ProvenanceLinksError as error:
            raise _map_error(error) from error
        timestamp = utc_timestamp()
        node = DescriptorNode(
            descriptor_id=normalized_id,
            descriptor_type=require_non_empty_str(descriptor_type, "descriptor_type"),
            label=require_non_empty_str(label, "label"),
            alias_tags=require_unique_str_list(alias_tags, "alias_tags"),
            domain_tags=require_unique_str_list(domain_tags, "domain_tags"),
            concept_tags=require_unique_str_list(concept_tags, "concept_tags"),
            support_refs=require_unique_str_list(support_refs, "support_refs"),
            trust_band=require_non_empty_str(trust_band, "trust_band"),
            policy_requirements=require_unique_str_list(policy_requirements, "policy_requirements"),
            provenance=provenance,
            created_at=timestamp,
            updated_at=timestamp,
            metadata=require_mapping(metadata or {}, "metadata"),
        )
        self._nodes[node.descriptor_id] = node
        self._order.append(node.descriptor_id)
        self._ensure_size()
        return node.descriptor_id

    def relate(
        self,
        *,
        edge_id: str,
        source_descriptor_id: str,
        target_descriptor_id: str,
        relation: str,
        weight: float,
        provenance_links: list[Mapping[str, Any]],
    ) -> str:
        normalized_edge_id = require_non_empty_str(edge_id, "edge_id")
        if normalized_edge_id in self._edges:
            raise DescriptorGraphError(f"duplicate edge_id: {normalized_edge_id}")
        source = self._get_node(source_descriptor_id)
        target = self._get_node(target_descriptor_id)
        try:
            provenance = build_provenance_bundle(
                entity_kind="edge",
                entity_id=normalized_edge_id,
                origin_kind="constructed",
                links=provenance_links,
            )
            require_roles(provenance, ("review",))
        except ProvenanceLinksError as error:
            raise _map_error(error) from error
        edge = DescriptorEdge(
            edge_id=normalized_edge_id,
            source_descriptor_id=source.descriptor_id,
            target_descriptor_id=target.descriptor_id,
            relation=require_non_empty_str(relation, "relation"),
            weight=round(float(weight), 6),
            provenance=provenance,
            created_at=utc_timestamp(),
        )
        self._edges[edge.edge_id] = edge
        self._ensure_size()
        return edge.edge_id

    def mark_retired(self, *, descriptor_id: str, retirement_ref: str) -> None:
        node = self._get_node(descriptor_id)
        node.status = "retired"
        node.retirement_ref = require_non_empty_str(retirement_ref, "retirement_ref")
        node.updated_at = utc_timestamp()
        self._ensure_size()

    def mark_superseded(
        self,
        *,
        descriptor_id: str,
        successor_id: str,
        review_ref: str,
        reason: str = "superseded",
    ) -> None:
        node = self._get_node(descriptor_id)
        self._get_node(successor_id)
        try:
            self._supersession.register(
                entity_kind="descriptor",
                predecessor_id=node.descriptor_id,
                successor_id=require_non_empty_str(successor_id, "successor_id"),
                review_ref=review_ref,
                reason=reason,
            )
        except SupersessionRulesError as error:
            raise DescriptorGraphError(str(error)) from error
        node.status = "superseded"
        node.superseded_by = successor_id
        node.updated_at = utc_timestamp()

    def node_state(self, descriptor_id: str) -> dict[str, Any]:
        return self._get_node(descriptor_id).to_dict()

    def edge_state(self, edge_id: str) -> dict[str, Any]:
        edge = self._edges.get(require_non_empty_str(edge_id, "edge_id"))
        if edge is None:
            raise DescriptorGraphError(f"unknown edge_id: {edge_id}")
        return edge.to_dict()

    def active_node_ids(self) -> list[str]:
        return [node_id for node_id in self._order if self._nodes[node_id].status == "active"]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_05.descriptor_graph.v1",
            "store_id": self.store_id,
            "max_nodes": self.max_nodes,
            "nodes": [self._nodes[node_id].to_dict() for node_id in self._order],
            "edges": [edge.to_dict() for edge in self._edges.values()],
            "supersession": self._supersession.export_state(),
            "state_hash": stable_hash_payload(
                {
                    "nodes": [self._nodes[node_id].to_dict() for node_id in self._order],
                    "edges": [edge.to_dict() for edge in self._edges.values()],
                }
            ),
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        payload_map = require_mapping(payload, "descriptor_graph_state")
        if payload_map.get("schema") != "agifcore.phase_05.descriptor_graph.v1":
            raise DescriptorGraphError("descriptor graph schema mismatch")
        self.store_id = require_non_empty_str(payload_map.get("store_id"), "store_id")
        max_nodes = payload_map.get("max_nodes", self.max_nodes)
        if not isinstance(max_nodes, int) or max_nodes <= 0:
            raise DescriptorGraphError("max_nodes must be a positive integer")
        self.max_nodes = max_nodes
        self._nodes = {}
        self._edges = {}
        self._order = []
        for node_payload in payload_map.get("nodes", []):
            node_map = require_mapping(node_payload, "node")
            node = DescriptorNode(
                descriptor_id=require_non_empty_str(node_map.get("descriptor_id"), "descriptor_id"),
                descriptor_type=require_non_empty_str(node_map.get("descriptor_type"), "descriptor_type"),
                label=require_non_empty_str(node_map.get("label"), "label"),
                alias_tags=require_unique_str_list(node_map.get("alias_tags", []), "alias_tags"),
                domain_tags=require_unique_str_list(node_map.get("domain_tags", []), "domain_tags"),
                concept_tags=require_unique_str_list(node_map.get("concept_tags", []), "concept_tags"),
                support_refs=require_unique_str_list(node_map.get("support_refs", []), "support_refs"),
                trust_band=require_non_empty_str(node_map.get("trust_band"), "trust_band"),
                policy_requirements=require_unique_str_list(
                    node_map.get("policy_requirements", []), "policy_requirements"
                ),
                provenance=bundle_from_dict(node_map.get("provenance", {})),
                created_at=require_non_empty_str(node_map.get("created_at"), "created_at"),
                updated_at=require_non_empty_str(node_map.get("updated_at"), "updated_at"),
                status=require_non_empty_str(node_map.get("status", "active"), "status"),
                superseded_by=node_map.get("superseded_by"),
                retirement_ref=node_map.get("retirement_ref"),
                metadata=require_mapping(node_map.get("metadata", {}), "metadata"),
            )
            self._nodes[node.descriptor_id] = node
            self._order.append(node.descriptor_id)
        for edge_payload in payload_map.get("edges", []):
            edge_map = require_mapping(edge_payload, "edge")
            edge = DescriptorEdge(
                edge_id=require_non_empty_str(edge_map.get("edge_id"), "edge_id"),
                source_descriptor_id=require_non_empty_str(
                    edge_map.get("source_descriptor_id"), "source_descriptor_id"
                ),
                target_descriptor_id=require_non_empty_str(
                    edge_map.get("target_descriptor_id"), "target_descriptor_id"
                ),
                relation=require_non_empty_str(edge_map.get("relation"), "relation"),
                weight=round(float(edge_map.get("weight", 0.0)), 6),
                provenance=bundle_from_dict(edge_map.get("provenance", {})),
                created_at=require_non_empty_str(edge_map.get("created_at"), "created_at"),
            )
            self._edges[edge.edge_id] = edge
        self._supersession = SupersessionLedger()
        self._supersession.load_state(payload_map.get("supersession", {}))
        self._ensure_size()

    def _get_node(self, descriptor_id: str) -> DescriptorNode:
        normalized = require_non_empty_str(descriptor_id, "descriptor_id")
        node = self._nodes.get(normalized)
        if node is None:
            raise DescriptorGraphError(f"unknown descriptor_id: {normalized}")
        return node

    def _ensure_size(self) -> None:
        if len(self._order) > self.max_nodes:
            raise DescriptorGraphError("descriptor graph exceeds max node count")
        size_bytes = canonical_size_bytes(self.export_state())
        if size_bytes > self.max_state_bytes:
            raise DescriptorGraphError("descriptor graph exceeds max state bytes")
