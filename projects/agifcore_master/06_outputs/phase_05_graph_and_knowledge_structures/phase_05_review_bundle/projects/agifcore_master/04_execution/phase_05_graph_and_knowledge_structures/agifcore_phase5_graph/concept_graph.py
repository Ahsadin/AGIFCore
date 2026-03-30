from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Mapping

from .provenance_links import (
    ProvenanceBundle,
    ProvenanceLinksError,
    build_provenance_bundle,
    bundle_from_dict,
    canonical_size_bytes,
    require_mapping,
    require_non_empty_str,
    require_roles,
    require_unique_str_list,
    stable_hash_payload,
    utc_timestamp,
)
from .supersession_rules import SupersessionLedger, SupersessionRulesError

MAX_CONCEPT_NODES = 512
MAX_CONCEPT_BYTES = 4 * 1024 * 1024


class ConceptGraphError(ValueError):
    """Raised when the concept graph violates the Phase 5 abstraction boundary."""


@dataclass(slots=True)
class ConceptNode:
    concept_id: str
    concept_type: str
    statement: str
    theory_fragments: list[str]
    descriptor_refs: list[str]
    tags: list[str]
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
            "concept_id": self.concept_id,
            "concept_type": self.concept_type,
            "statement": self.statement,
            "theory_fragments": list(self.theory_fragments),
            "descriptor_refs": list(self.descriptor_refs),
            "tags": list(self.tags),
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
class ConceptEdge:
    edge_id: str
    source_concept_id: str
    target_concept_id: str
    relation: str
    provenance: ProvenanceBundle
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_concept_id": self.source_concept_id,
            "target_concept_id": self.target_concept_id,
            "relation": self.relation,
            "provenance": self.provenance.to_dict(),
            "created_at": self.created_at,
        }


class ConceptGraphStore:
    """Concept graph for reviewed abstractions and theory fragments."""

    def __init__(
        self,
        *,
        store_id: str = "phase-05-concept-graph",
        max_nodes: int = MAX_CONCEPT_NODES,
        max_state_bytes: int = MAX_CONCEPT_BYTES,
    ) -> None:
        self.store_id = store_id
        self.max_nodes = max_nodes
        self.max_state_bytes = max_state_bytes
        self._nodes: dict[str, ConceptNode] = {}
        self._edges: dict[str, ConceptEdge] = {}
        self._order: list[str] = []
        self._supersession = SupersessionLedger()

    def add_concept(
        self,
        *,
        concept_id: str,
        concept_type: str,
        statement: str,
        theory_fragments: list[str],
        descriptor_refs: list[str],
        tags: list[str],
        trust_band: str,
        policy_requirements: list[str],
        provenance_links: list[Mapping[str, Any]],
        origin_kind: str = "constructed",
        inherited_from: list[str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        normalized_id = require_non_empty_str(concept_id, "concept_id")
        if normalized_id in self._nodes:
            raise ConceptGraphError(f"duplicate concept_id: {normalized_id}")
        try:
            provenance = build_provenance_bundle(
                entity_kind="concept",
                entity_id=normalized_id,
                origin_kind=origin_kind,
                links=provenance_links,
                inherited_from=inherited_from,
            )
            require_roles(provenance, ("source_memory", "review"))
        except ProvenanceLinksError as error:
            raise ConceptGraphError(str(error)) from error
        timestamp = utc_timestamp()
        node = ConceptNode(
            concept_id=normalized_id,
            concept_type=require_non_empty_str(concept_type, "concept_type"),
            statement=require_non_empty_str(statement, "statement"),
            theory_fragments=require_unique_str_list(theory_fragments, "theory_fragments"),
            descriptor_refs=require_unique_str_list(descriptor_refs, "descriptor_refs"),
            tags=require_unique_str_list(tags, "tags"),
            trust_band=require_non_empty_str(trust_band, "trust_band"),
            policy_requirements=require_unique_str_list(policy_requirements, "policy_requirements"),
            provenance=provenance,
            created_at=timestamp,
            updated_at=timestamp,
            metadata=require_mapping(metadata or {}, "metadata"),
        )
        self._nodes[node.concept_id] = node
        self._order.append(node.concept_id)
        self._ensure_size()
        return node.concept_id

    def relate(
        self,
        *,
        edge_id: str,
        source_concept_id: str,
        target_concept_id: str,
        relation: str,
        provenance_links: list[Mapping[str, Any]],
    ) -> str:
        normalized_edge_id = require_non_empty_str(edge_id, "edge_id")
        if normalized_edge_id in self._edges:
            raise ConceptGraphError(f"duplicate edge_id: {normalized_edge_id}")
        self._get_node(source_concept_id)
        self._get_node(target_concept_id)
        try:
            provenance = build_provenance_bundle(
                entity_kind="edge",
                entity_id=normalized_edge_id,
                origin_kind="constructed",
                links=provenance_links,
            )
            require_roles(provenance, ("review",))
        except ProvenanceLinksError as error:
            raise ConceptGraphError(str(error)) from error
        edge = ConceptEdge(
            edge_id=normalized_edge_id,
            source_concept_id=require_non_empty_str(source_concept_id, "source_concept_id"),
            target_concept_id=require_non_empty_str(target_concept_id, "target_concept_id"),
            relation=require_non_empty_str(relation, "relation"),
            provenance=provenance,
            created_at=utc_timestamp(),
        )
        self._edges[edge.edge_id] = edge
        self._ensure_size()
        return edge.edge_id

    def mark_retired(self, *, concept_id: str, retirement_ref: str) -> None:
        node = self._get_node(concept_id)
        node.status = "retired"
        node.retirement_ref = require_non_empty_str(retirement_ref, "retirement_ref")
        node.updated_at = utc_timestamp()

    def mark_superseded(
        self,
        *,
        concept_id: str,
        successor_id: str,
        review_ref: str,
        reason: str = "superseded",
    ) -> None:
        node = self._get_node(concept_id)
        self._get_node(successor_id)
        try:
            self._supersession.register(
                entity_kind="concept",
                predecessor_id=node.concept_id,
                successor_id=require_non_empty_str(successor_id, "successor_id"),
                review_ref=review_ref,
                reason=reason,
            )
        except SupersessionRulesError as error:
            raise ConceptGraphError(str(error)) from error
        node.status = "superseded"
        node.superseded_by = successor_id
        node.updated_at = utc_timestamp()

    def concept_state(self, concept_id: str) -> dict[str, Any]:
        return self._get_node(concept_id).to_dict()

    def active_concept_ids(self) -> list[str]:
        return [concept_id for concept_id in self._order if self._nodes[concept_id].status == "active"]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_05.concept_graph.v1",
            "store_id": self.store_id,
            "max_nodes": self.max_nodes,
            "nodes": [self._nodes[concept_id].to_dict() for concept_id in self._order],
            "edges": [edge.to_dict() for edge in self._edges.values()],
            "supersession": self._supersession.export_state(),
            "state_hash": stable_hash_payload(
                {
                    "nodes": [self._nodes[concept_id].to_dict() for concept_id in self._order],
                    "edges": [edge.to_dict() for edge in self._edges.values()],
                }
            ),
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        payload_map = require_mapping(payload, "concept_graph_state")
        if payload_map.get("schema") != "agifcore.phase_05.concept_graph.v1":
            raise ConceptGraphError("concept graph schema mismatch")
        self.store_id = require_non_empty_str(payload_map.get("store_id"), "store_id")
        max_nodes = payload_map.get("max_nodes", self.max_nodes)
        if not isinstance(max_nodes, int) or max_nodes <= 0:
            raise ConceptGraphError("max_nodes must be a positive integer")
        self.max_nodes = max_nodes
        self._nodes = {}
        self._edges = {}
        self._order = []
        for node_payload in payload_map.get("nodes", []):
            node_map = require_mapping(node_payload, "node")
            node = ConceptNode(
                concept_id=require_non_empty_str(node_map.get("concept_id"), "concept_id"),
                concept_type=require_non_empty_str(node_map.get("concept_type"), "concept_type"),
                statement=require_non_empty_str(node_map.get("statement"), "statement"),
                theory_fragments=require_unique_str_list(
                    node_map.get("theory_fragments", []), "theory_fragments"
                ),
                descriptor_refs=require_unique_str_list(node_map.get("descriptor_refs", []), "descriptor_refs"),
                tags=require_unique_str_list(node_map.get("tags", []), "tags"),
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
            self._nodes[node.concept_id] = node
            self._order.append(node.concept_id)
        for edge_payload in payload_map.get("edges", []):
            edge_map = require_mapping(edge_payload, "edge")
            edge = ConceptEdge(
                edge_id=require_non_empty_str(edge_map.get("edge_id"), "edge_id"),
                source_concept_id=require_non_empty_str(
                    edge_map.get("source_concept_id"), "source_concept_id"
                ),
                target_concept_id=require_non_empty_str(
                    edge_map.get("target_concept_id"), "target_concept_id"
                ),
                relation=require_non_empty_str(edge_map.get("relation"), "relation"),
                provenance=bundle_from_dict(edge_map.get("provenance", {})),
                created_at=require_non_empty_str(edge_map.get("created_at"), "created_at"),
            )
            self._edges[edge.edge_id] = edge
        self._supersession = SupersessionLedger()
        self._supersession.load_state(payload_map.get("supersession", {}))
        self._ensure_size()

    def _get_node(self, concept_id: str) -> ConceptNode:
        normalized = require_non_empty_str(concept_id, "concept_id")
        node = self._nodes.get(normalized)
        if node is None:
            raise ConceptGraphError(f"unknown concept_id: {normalized}")
        return node

    def _ensure_size(self) -> None:
        if len(self._order) > self.max_nodes:
            raise ConceptGraphError("concept graph exceeds max node count")
        if canonical_size_bytes(self.export_state()) > self.max_state_bytes:
            raise ConceptGraphError("concept graph exceeds max state bytes")
