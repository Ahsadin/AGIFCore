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

MAX_SKILL_NODES = 256
MAX_SKILL_BYTES = 2 * 1024 * 1024


class SkillGraphError(ValueError):
    """Raised when the skill graph violates the Phase 5 procedural boundary."""


@dataclass(slots=True)
class SkillNode:
    skill_id: str
    skill_name: str
    objective: str
    descriptor_refs: list[str]
    preconditions: list[str]
    postconditions: list[str]
    constraints: list[str]
    allowed_target_domains: list[str]
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
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "objective": self.objective,
            "descriptor_refs": list(self.descriptor_refs),
            "preconditions": list(self.preconditions),
            "postconditions": list(self.postconditions),
            "constraints": list(self.constraints),
            "allowed_target_domains": list(self.allowed_target_domains),
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
class SkillGroundingEdge:
    edge_id: str
    skill_id: str
    descriptor_id: str
    relation: str
    provenance: ProvenanceBundle
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "skill_id": self.skill_id,
            "descriptor_id": self.descriptor_id,
            "relation": self.relation,
            "provenance": self.provenance.to_dict(),
            "created_at": self.created_at,
        }


class SkillGraphStore:
    """Procedural graph distinct from descriptor and concept layers."""

    def __init__(
        self,
        *,
        store_id: str = "phase-05-skill-graph",
        max_nodes: int = MAX_SKILL_NODES,
        max_state_bytes: int = MAX_SKILL_BYTES,
    ) -> None:
        self.store_id = store_id
        self.max_nodes = max_nodes
        self.max_state_bytes = max_state_bytes
        self._nodes: dict[str, SkillNode] = {}
        self._edges: dict[str, SkillGroundingEdge] = {}
        self._order: list[str] = []
        self._supersession = SupersessionLedger()

    def add_skill(
        self,
        *,
        skill_id: str,
        skill_name: str,
        objective: str,
        descriptor_refs: list[str],
        preconditions: list[str],
        postconditions: list[str],
        constraints: list[str],
        allowed_target_domains: list[str],
        trust_band: str,
        policy_requirements: list[str],
        provenance_links: list[Mapping[str, Any]],
        origin_kind: str = "constructed",
        inherited_from: list[str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        normalized_id = require_non_empty_str(skill_id, "skill_id")
        if normalized_id in self._nodes:
            raise SkillGraphError(f"duplicate skill_id: {normalized_id}")
        try:
            provenance = build_provenance_bundle(
                entity_kind="skill",
                entity_id=normalized_id,
                origin_kind=origin_kind,
                links=provenance_links,
                inherited_from=inherited_from,
            )
            require_roles(provenance, ("source_memory", "review"))
        except ProvenanceLinksError as error:
            raise SkillGraphError(str(error)) from error
        timestamp = utc_timestamp()
        node = SkillNode(
            skill_id=normalized_id,
            skill_name=require_non_empty_str(skill_name, "skill_name"),
            objective=require_non_empty_str(objective, "objective"),
            descriptor_refs=require_unique_str_list(descriptor_refs, "descriptor_refs"),
            preconditions=require_unique_str_list(preconditions, "preconditions"),
            postconditions=require_unique_str_list(postconditions, "postconditions"),
            constraints=require_unique_str_list(constraints, "constraints"),
            allowed_target_domains=require_unique_str_list(
                allowed_target_domains, "allowed_target_domains"
            ),
            trust_band=require_non_empty_str(trust_band, "trust_band"),
            policy_requirements=require_unique_str_list(policy_requirements, "policy_requirements"),
            provenance=provenance,
            created_at=timestamp,
            updated_at=timestamp,
            metadata=require_mapping(metadata or {}, "metadata"),
        )
        self._nodes[node.skill_id] = node
        self._order.append(node.skill_id)
        self._ensure_size()
        return node.skill_id

    def add_grounding(
        self,
        *,
        edge_id: str,
        skill_id: str,
        descriptor_id: str,
        provenance_links: list[Mapping[str, Any]],
        relation: str = "grounded_by",
    ) -> str:
        normalized_edge_id = require_non_empty_str(edge_id, "edge_id")
        if normalized_edge_id in self._edges:
            raise SkillGraphError(f"duplicate edge_id: {normalized_edge_id}")
        node = self._get_node(skill_id)
        descriptor_ref = require_non_empty_str(descriptor_id, "descriptor_id")
        if descriptor_ref not in node.descriptor_refs:
            node.descriptor_refs.append(descriptor_ref)
            node.updated_at = utc_timestamp()
        try:
            provenance = build_provenance_bundle(
                entity_kind="edge",
                entity_id=normalized_edge_id,
                origin_kind="constructed",
                links=provenance_links,
            )
            require_roles(provenance, ("review",))
        except ProvenanceLinksError as error:
            raise SkillGraphError(str(error)) from error
        edge = SkillGroundingEdge(
            edge_id=normalized_edge_id,
            skill_id=node.skill_id,
            descriptor_id=descriptor_ref,
            relation=require_non_empty_str(relation, "relation"),
            provenance=provenance,
            created_at=utc_timestamp(),
        )
        self._edges[edge.edge_id] = edge
        self._ensure_size()
        return edge.edge_id

    def mark_retired(self, *, skill_id: str, retirement_ref: str) -> None:
        node = self._get_node(skill_id)
        node.status = "retired"
        node.retirement_ref = require_non_empty_str(retirement_ref, "retirement_ref")
        node.updated_at = utc_timestamp()

    def mark_superseded(
        self,
        *,
        skill_id: str,
        successor_id: str,
        review_ref: str,
        reason: str = "superseded",
    ) -> None:
        node = self._get_node(skill_id)
        self._get_node(successor_id)
        try:
            self._supersession.register(
                entity_kind="skill",
                predecessor_id=node.skill_id,
                successor_id=require_non_empty_str(successor_id, "successor_id"),
                review_ref=review_ref,
                reason=reason,
            )
        except SupersessionRulesError as error:
            raise SkillGraphError(str(error)) from error
        node.status = "superseded"
        node.superseded_by = successor_id
        node.updated_at = utc_timestamp()

    def skill_state(self, skill_id: str) -> dict[str, Any]:
        return self._get_node(skill_id).to_dict()

    def active_skill_ids(self) -> list[str]:
        return [skill_id for skill_id in self._order if self._nodes[skill_id].status == "active"]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_05.skill_graph.v1",
            "store_id": self.store_id,
            "max_nodes": self.max_nodes,
            "nodes": [self._nodes[skill_id].to_dict() for skill_id in self._order],
            "edges": [edge.to_dict() for edge in self._edges.values()],
            "supersession": self._supersession.export_state(),
            "state_hash": stable_hash_payload(
                {
                    "nodes": [self._nodes[skill_id].to_dict() for skill_id in self._order],
                    "edges": [edge.to_dict() for edge in self._edges.values()],
                }
            ),
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        payload_map = require_mapping(payload, "skill_graph_state")
        if payload_map.get("schema") != "agifcore.phase_05.skill_graph.v1":
            raise SkillGraphError("skill graph schema mismatch")
        self.store_id = require_non_empty_str(payload_map.get("store_id"), "store_id")
        max_nodes = payload_map.get("max_nodes", self.max_nodes)
        if not isinstance(max_nodes, int) or max_nodes <= 0:
            raise SkillGraphError("max_nodes must be a positive integer")
        self.max_nodes = max_nodes
        self._nodes = {}
        self._edges = {}
        self._order = []
        for node_payload in payload_map.get("nodes", []):
            node_map = require_mapping(node_payload, "node")
            node = SkillNode(
                skill_id=require_non_empty_str(node_map.get("skill_id"), "skill_id"),
                skill_name=require_non_empty_str(node_map.get("skill_name"), "skill_name"),
                objective=require_non_empty_str(node_map.get("objective"), "objective"),
                descriptor_refs=require_unique_str_list(node_map.get("descriptor_refs", []), "descriptor_refs"),
                preconditions=require_unique_str_list(node_map.get("preconditions", []), "preconditions"),
                postconditions=require_unique_str_list(node_map.get("postconditions", []), "postconditions"),
                constraints=require_unique_str_list(node_map.get("constraints", []), "constraints"),
                allowed_target_domains=require_unique_str_list(
                    node_map.get("allowed_target_domains", []), "allowed_target_domains"
                ),
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
            self._nodes[node.skill_id] = node
            self._order.append(node.skill_id)
        for edge_payload in payload_map.get("edges", []):
            edge_map = require_mapping(edge_payload, "edge")
            edge = SkillGroundingEdge(
                edge_id=require_non_empty_str(edge_map.get("edge_id"), "edge_id"),
                skill_id=require_non_empty_str(edge_map.get("skill_id"), "skill_id"),
                descriptor_id=require_non_empty_str(edge_map.get("descriptor_id"), "descriptor_id"),
                relation=require_non_empty_str(edge_map.get("relation"), "relation"),
                provenance=bundle_from_dict(edge_map.get("provenance", {})),
                created_at=require_non_empty_str(edge_map.get("created_at"), "created_at"),
            )
            self._edges[edge.edge_id] = edge
        self._supersession = SupersessionLedger()
        self._supersession.load_state(payload_map.get("supersession", {}))
        self._ensure_size()

    def _get_node(self, skill_id: str) -> SkillNode:
        normalized = require_non_empty_str(skill_id, "skill_id")
        node = self._nodes.get(normalized)
        if node is None:
            raise SkillGraphError(f"unknown skill_id: {normalized}")
        return node

    def _ensure_size(self) -> None:
        if len(self._order) > self.max_nodes:
            raise SkillGraphError("skill graph exceeds max node count")
        if canonical_size_bytes(self.export_state()) > self.max_state_bytes:
            raise SkillGraphError("skill graph exceeds max state bytes")
