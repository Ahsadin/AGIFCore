from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping

from .entity_classes import (
    MAX_ENTITY_COUNT,
    StateValueType,
    WorldEntity,
    WorldEntityKind,
    WorldEntityStatus,
    WorldModelSnapshot,
    WorldOperatorKind,
    WorldOperatorStatus,
    WorldRelation,
    WorldRelationKind,
    build_provenance_bundle,
    build_state_value,
    build_world_operator,
    canonical_size_bytes,
    clamp_score,
    provenance_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    require_unique_str_list,
    stable_hash_payload,
    trust_band_confidence,
)
from .target_domains import TargetDomainRegistry, build_default_registry

MAX_WORLD_RELATIONS = 512
MAX_WORLD_MODEL_BYTES = 4 * 1024 * 1024


class WorldModelError(ValueError):
    """Raised when the Phase 6 world model violates the approved boundary or budget."""


def _first_link_ref(links: list[Mapping[str, Any]], role: str) -> Mapping[str, Any] | None:
    for link in links:
        if link.get("role") == role:
            return link
    return None


def _entity_status_from_flags(status: str, trust_band: str, quality_score: float | None = None) -> WorldEntityStatus:
    normalized = require_non_empty_str(status, "status")
    if normalized in {"retired", "superseded", "denied", "blocked"}:
        return WorldEntityStatus.BLOCKED
    if normalized in {"held", "abstained", "defer"}:
        return WorldEntityStatus.HELD
    if trust_band == "experimental" or (quality_score is not None and quality_score < 0.45):
        return WorldEntityStatus.HELD
    return WorldEntityStatus.REVIEW_ONLY


def _relation_strength(base: float, provenance_score_value: float, trust_band: str) -> float:
    return clamp_score(
        (0.45 * base) + (0.30 * provenance_score_value) + (0.25 * trust_band_confidence(trust_band))
    )


class WorldModelBuilder:
    """Build a bounded Phase 6 world-model snapshot from exported Phase 4 and Phase 5 state."""

    def __init__(
        self,
        *,
        max_entities: int = MAX_ENTITY_COUNT,
        max_relations: int = MAX_WORLD_RELATIONS,
        max_state_bytes: int = MAX_WORLD_MODEL_BYTES,
    ) -> None:
        self.max_entities = max_entities
        self.max_relations = max_relations
        self.max_state_bytes = max_state_bytes

    def build_snapshot(
        self,
        *,
        semantic_memory_state: Mapping[str, Any],
        procedural_memory_state: Mapping[str, Any],
        descriptor_graph_state: Mapping[str, Any],
        skill_graph_state: Mapping[str, Any],
        concept_graph_state: Mapping[str, Any],
        transfer_graph_state: Mapping[str, Any],
        continuity_memory_state: Mapping[str, Any] | None = None,
        working_memory_state: Mapping[str, Any] | None = None,
        support_selection_result: Mapping[str, Any] | None = None,
        target_domain_registry_state: Mapping[str, Any] | None = None,
    ) -> WorldModelSnapshot:
        semantic_state = require_schema(
            semantic_memory_state,
            "agifcore.phase_04.semantic_memory.v1",
            "semantic_memory_state",
        )
        procedural_state = require_schema(
            procedural_memory_state,
            "agifcore.phase_04.procedural_memory.v1",
            "procedural_memory_state",
        )
        descriptor_state = require_schema(
            descriptor_graph_state,
            "agifcore.phase_05.descriptor_graph.v1",
            "descriptor_graph_state",
        )
        skill_state = require_schema(skill_graph_state, "agifcore.phase_05.skill_graph.v1", "skill_graph_state")
        concept_state = require_schema(
            concept_graph_state,
            "agifcore.phase_05.concept_graph.v1",
            "concept_graph_state",
        )
        transfer_state = require_schema(
            transfer_graph_state,
            "agifcore.phase_05.transfer_graph.v1",
            "transfer_graph_state",
        )
        continuity_state = None
        if continuity_memory_state is not None:
            continuity_state = require_schema(
                continuity_memory_state,
                "agifcore.phase_04.continuity_memory.v1",
                "continuity_memory_state",
            )
        working_memory_map = None
        if working_memory_state is not None:
            working_memory_map = require_schema(
                working_memory_state,
                "agifcore.phase_04.working_memory.v1",
                "working_memory_state",
            )
        selected_candidate_ids: set[str] = set()
        if support_selection_result is not None:
            selected_candidate_ids = set(
                require_unique_str_list(
                    list(require_mapping(support_selection_result, "support_selection_result").get("selected_candidate_ids", [])),
                    "selected_candidate_ids",
                )
            )

        registry = TargetDomainRegistry()
        if target_domain_registry_state is None:
            registry = build_default_registry()
        else:
            registry.load_state(target_domain_registry_state)
        structures = {domain_id: registry.structure_state(domain_id) for domain_id in registry.domain_ids()}

        entities: list[WorldEntity] = []
        relations: list[WorldRelation] = []
        entity_id_by_target_domain: dict[str, str] = {}
        entity_id_by_source: dict[str, str] = {}
        focused_sources: defaultdict[str, list[str]] = defaultdict(list)

        for candidate_id in selected_candidate_ids:
            try:
                layer, entity_id = candidate_id.split("::", 1)
            except ValueError:
                continue
            focused_sources[f"{layer}:{entity_id}"].append(candidate_id)

        for structure in structures.values():
            target_entity_id = f"world::target::{structure['domain_id']}"
            provenance = build_provenance_bundle(
                entity_kind="world_entity",
                entity_id=target_entity_id,
                origin_kind="constructed",
                links=[
                    {
                        "role": "domain",
                        "ref_id": structure["domain_id"],
                        "ref_kind": "target_domain_structure",
                        "source_path": "phase6/target_domains",
                    },
                    {
                        "role": "review",
                        "ref_id": "phase6-world-model-target-review",
                        "ref_kind": "governor_review",
                        "source_path": "projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md",
                    },
                ],
                inherited_from=["agif_fabric_v1"],
            )
            entity = WorldEntity(
                entity_id=target_entity_id,
                entity_kind=WorldEntityKind.TARGET_DOMAIN_OBJECT,
                label=structure["domain_name"],
                target_domain=structure["domain_id"],
                status=WorldEntityStatus.REVIEW_ONLY,
                world_confidence=0.8,
                source_refs=(structure["domain_id"],),
                state_values=(
                    build_state_value(
                        field_name="minimum_signal_groups",
                        value_type=StateValueType.COUNT,
                        value_text=str(structure["minimum_signal_groups"]),
                        numeric_value=int(structure["minimum_signal_groups"]),
                    ),
                ),
                operators=(
                    build_world_operator(
                        operator_kind=WorldOperatorKind.TARGET_PROJECTION,
                        status=WorldOperatorStatus.READY_FOR_REVIEW,
                        bounded_confidence=0.8,
                        reason_codes=["canonical_target_domain"],
                    ),
                ),
                replay_safe=True,
                provenance=provenance,
                entity_hash=stable_hash_payload(
                    {
                        "entity_kind": WorldEntityKind.TARGET_DOMAIN_OBJECT.value,
                        "label": structure["domain_name"],
                        "target_domain": structure["domain_id"],
                    }
                ),
                metadata={"object_count": len(structure.get("objects", []))},
            )
            entities.append(entity)
            entity_id_by_target_domain[structure["domain_id"]] = target_entity_id

        semantic_refs_by_graph: defaultdict[str, list[str]] = defaultdict(list)
        for entry in semantic_state.get("entries", []):
            entry_map = require_mapping(entry, "semantic_entry")
            for graph_ref in entry_map.get("graph_refs", []):
                semantic_refs_by_graph[str(graph_ref)].append(str(entry_map.get("entry_id")))

        procedural_refs_by_graph: defaultdict[str, list[str]] = defaultdict(list)
        for entry in procedural_state.get("entries", []):
            entry_map = require_mapping(entry, "procedure_entry")
            for graph_ref in entry_map.get("graph_refs", []):
                procedural_refs_by_graph[str(graph_ref)].append(str(entry_map.get("procedure_id")))

        descriptor_nodes = [require_mapping(node, "descriptor_node") for node in descriptor_state.get("nodes", [])]
        for node in descriptor_nodes:
            if node.get("status") != "active":
                continue
            provenance_links = list(require_mapping(node.get("provenance"), "descriptor_provenance").get("links", []))
            review_link = _first_link_ref(provenance_links, "review")
            graph_links = [
                {
                    "role": "graph",
                    "ref_id": node["descriptor_id"],
                    "ref_kind": "descriptor_node",
                    "source_path": "phase5/descriptor_graph",
                }
            ]
            if review_link:
                graph_links.append(
                    {
                        "role": "review",
                        "ref_id": require_non_empty_str(review_link.get("ref_id"), "review_ref"),
                        "ref_kind": "review",
                        "source_path": "phase5/descriptor_graph",
                    }
                )
            semantic_refs = semantic_refs_by_graph.get(str(node["descriptor_id"]), [])
            if semantic_refs:
                graph_links.append(
                    {
                        "role": "source_memory",
                        "ref_id": semantic_refs[0],
                        "ref_kind": "semantic_entry",
                        "source_path": "phase4/semantic_memory",
                    }
                )
            domain_tags = list(node.get("domain_tags", []))
            target_domain = domain_tags[0] if domain_tags else None
            if target_domain is None:
                inferred = registry.match_domains(
                    labels=[str(node.get("label", "")), *[str(tag) for tag in node.get("alias_tags", [])]]
                )
                target_domain = inferred[0] if inferred else None
            descriptor_provenance = build_provenance_bundle(
                entity_kind="world_entity",
                entity_id=f"world::descriptor::{node['descriptor_id']}",
                origin_kind="constructed",
                links=graph_links,
                inherited_from=["agif_v2_master"] if node.get("provenance", {}).get("origin_kind") == "inherited" else [],
            )
            confidence = clamp_score(
                (0.55 * trust_band_confidence(str(node.get("trust_band"))))
                + (0.45 * provenance_score(descriptor_provenance))
            )
            entity = WorldEntity(
                entity_id=f"world::descriptor::{node['descriptor_id']}",
                entity_kind=WorldEntityKind.DESCRIPTOR_SUPPORT,
                label=require_non_empty_str(node.get("label"), "label"),
                target_domain=target_domain,
                status=_entity_status_from_flags(str(node.get("status")), str(node.get("trust_band"))),
                world_confidence=confidence,
                source_refs=tuple([str(node["descriptor_id"]), *semantic_refs]),
                state_values=(
                    build_state_value(
                        field_name="trust_band",
                        value_type=StateValueType.LABEL,
                        value_text=str(node["trust_band"]),
                    ),
                    build_state_value(
                        field_name="support_ref_count",
                        value_type=StateValueType.COUNT,
                        value_text=str(len(node.get("support_refs", []))),
                        numeric_value=len(node.get("support_refs", [])),
                    ),
                ),
                operators=(
                    build_world_operator(
                        operator_kind=WorldOperatorKind.FUTURE_EVALUATION,
                        status=(
                            WorldOperatorStatus.READY_FOR_REVIEW
                            if confidence >= 0.55
                            else WorldOperatorStatus.HOLD_REQUIRED
                        ),
                        bounded_confidence=confidence,
                        reason_codes=["descriptor_review_only", "phase5_descriptor_graph"],
                    ),
                ),
                replay_safe=True,
                provenance=descriptor_provenance,
                entity_hash=stable_hash_payload(
                    {
                        "source": node["descriptor_id"],
                        "kind": WorldEntityKind.DESCRIPTOR_SUPPORT.value,
                        "target_domain": target_domain,
                        "confidence": confidence,
                    }
                ),
                metadata={"selected_support": f"descriptor::{node['descriptor_id']}" in selected_candidate_ids},
            )
            entities.append(entity)
            entity_id_by_source[f"descriptor:{node['descriptor_id']}"] = entity.entity_id

        for node in [require_mapping(item, "skill_node") for item in skill_state.get("nodes", [])]:
            if node.get("status") != "active":
                continue
            provenance_links = list(require_mapping(node.get("provenance"), "skill_provenance").get("links", []))
            review_link = _first_link_ref(provenance_links, "review")
            graph_links = [
                {
                    "role": "graph",
                    "ref_id": node["skill_id"],
                    "ref_kind": "skill_node",
                    "source_path": "phase5/skill_graph",
                }
            ]
            if review_link:
                graph_links.append(
                    {
                        "role": "review",
                        "ref_id": require_non_empty_str(review_link.get("ref_id"), "review_ref"),
                        "ref_kind": "review",
                        "source_path": "phase5/skill_graph",
                    }
                )
            procedural_refs = procedural_refs_by_graph.get(str(node["skill_id"]), [])
            if procedural_refs:
                graph_links.append(
                    {
                        "role": "source_memory",
                        "ref_id": procedural_refs[0],
                        "ref_kind": "procedure_entry",
                        "source_path": "phase4/procedural_memory",
                    }
                )
            allowed_domains = list(node.get("allowed_target_domains", []))
            target_domain = allowed_domains[0] if allowed_domains else None
            confidence = clamp_score(0.6 * trust_band_confidence(str(node.get("trust_band"))) + 0.4)
            entity = WorldEntity(
                entity_id=f"world::skill::{node['skill_id']}",
                entity_kind=WorldEntityKind.PROCEDURAL_SKILL,
                label=require_non_empty_str(node.get("skill_name"), "skill_name"),
                target_domain=target_domain,
                status=_entity_status_from_flags(str(node.get("status")), str(node.get("trust_band"))),
                world_confidence=confidence,
                source_refs=tuple([str(node["skill_id"]), *procedural_refs]),
                state_values=(
                    build_state_value(
                        field_name="constraint_count",
                        value_type=StateValueType.COUNT,
                        value_text=str(len(node.get("constraints", []))),
                        numeric_value=len(node.get("constraints", [])),
                    ),
                ),
                operators=(
                    build_world_operator(
                        operator_kind=WorldOperatorKind.FUTURE_EVALUATION,
                        status=(
                            WorldOperatorStatus.READY_FOR_REVIEW
                            if confidence >= 0.55
                            else WorldOperatorStatus.HOLD_REQUIRED
                        ),
                        bounded_confidence=confidence,
                        reason_codes=["procedural_reuse_review_only", "phase5_skill_graph"],
                    ),
                ),
                replay_safe=True,
                provenance=build_provenance_bundle(
                    entity_kind="world_entity",
                    entity_id=f"world::skill::{node['skill_id']}",
                    origin_kind="constructed",
                    links=graph_links,
                ),
                entity_hash=stable_hash_payload(
                    {
                        "source": node["skill_id"],
                        "kind": WorldEntityKind.PROCEDURAL_SKILL.value,
                        "target_domain": target_domain,
                        "confidence": confidence,
                    }
                ),
                metadata={"selected_support": f"skill::{node['skill_id']}" in selected_candidate_ids},
            )
            entities.append(entity)
            entity_id_by_source[f"skill:{node['skill_id']}"] = entity.entity_id

        for node in [require_mapping(item, "concept_node") for item in concept_state.get("nodes", [])]:
            if node.get("status") != "active":
                continue
            provenance_links = list(require_mapping(node.get("provenance"), "concept_provenance").get("links", []))
            review_link = _first_link_ref(provenance_links, "review")
            graph_links = [
                {
                    "role": "graph",
                    "ref_id": node["concept_id"],
                    "ref_kind": "concept_node",
                    "source_path": "phase5/concept_graph",
                }
            ]
            if review_link:
                graph_links.append(
                    {
                        "role": "review",
                        "ref_id": require_non_empty_str(review_link.get("ref_id"), "review_ref"),
                        "ref_kind": "review",
                        "source_path": "phase5/concept_graph",
                    }
                )
            target_domain = next(
                (
                    require_mapping(descriptor, "descriptor_node").get("domain_tags", [None])[0]
                    for descriptor in descriptor_nodes
                    if descriptor.get("descriptor_id") in node.get("descriptor_refs", [])
                    and descriptor.get("domain_tags")
                ),
                None,
            )
            confidence = clamp_score(0.5 * trust_band_confidence(str(node.get("trust_band"))) + 0.35)
            entity = WorldEntity(
                entity_id=f"world::concept::{node['concept_id']}",
                entity_kind=WorldEntityKind.CONCEPT_SUPPORT,
                label=require_non_empty_str(node.get("statement"), "statement"),
                target_domain=target_domain,
                status=WorldEntityStatus.REVIEW_ONLY,
                world_confidence=confidence,
                source_refs=(str(node["concept_id"]),),
                state_values=(
                    build_state_value(
                        field_name="theory_fragment_count",
                        value_type=StateValueType.COUNT,
                        value_text=str(len(node.get("theory_fragments", []))),
                        numeric_value=len(node.get("theory_fragments", [])),
                    ),
                ),
                operators=(
                    build_world_operator(
                        operator_kind=WorldOperatorKind.FUTURE_EVALUATION,
                        status=(
                            WorldOperatorStatus.READY_FOR_REVIEW
                            if confidence >= 0.5
                            else WorldOperatorStatus.HOLD_REQUIRED
                        ),
                        bounded_confidence=confidence,
                        reason_codes=["concept_support_only", "phase5_concept_graph"],
                    ),
                ),
                replay_safe=True,
                provenance=build_provenance_bundle(
                    entity_kind="world_entity",
                    entity_id=f"world::concept::{node['concept_id']}",
                    origin_kind="constructed",
                    links=graph_links,
                ),
                entity_hash=stable_hash_payload(
                    {
                        "source": node["concept_id"],
                        "kind": WorldEntityKind.CONCEPT_SUPPORT.value,
                        "target_domain": target_domain,
                        "confidence": confidence,
                    }
                ),
                metadata={"selected_support": f"concept::{node['concept_id']}" in selected_candidate_ids},
            )
            entities.append(entity)
            entity_id_by_source[f"concept:{node['concept_id']}"] = entity.entity_id

        for record in [require_mapping(item, "transfer_record") for item in transfer_state.get("records", [])]:
            if record.get("decision") not in {"approved", "abstained", "blocked", "denied"}:
                continue
            provenance_links = list(require_mapping(record.get("provenance"), "transfer_provenance").get("links", []))
            review_link = _first_link_ref(provenance_links, "review")
            transfer_links = [
                {
                    "role": "transfer",
                    "ref_id": record["transfer_id"],
                    "ref_kind": "transfer_record",
                    "source_path": "phase5/transfer_graph",
                }
            ]
            if review_link:
                transfer_links.append(
                    {
                        "role": "review",
                        "ref_id": require_non_empty_str(review_link.get("ref_id"), "review_ref"),
                        "ref_kind": "review",
                        "source_path": "phase5/transfer_graph",
                    }
                )
            quality_score = float(record.get("quality_score", 0.0))
            confidence = clamp_score(0.55 * trust_band_confidence(str(record.get("trust_band"))) + 0.45 * quality_score)
            entity = WorldEntity(
                entity_id=f"world::transfer::{record['transfer_id']}",
                entity_kind=WorldEntityKind.TRANSFER_PROJECTION,
                label=f"{record['source_id']} -> {record['target_domain']}",
                target_domain=require_non_empty_str(record.get("target_domain"), "target_domain"),
                status=_entity_status_from_flags(str(record.get("decision")), str(record.get("trust_band")), quality_score),
                world_confidence=confidence,
                source_refs=tuple([str(record["transfer_id"]), str(record["source_id"])]),
                state_values=(
                    build_state_value(
                        field_name="quality_score",
                        value_type=StateValueType.SCORE,
                        value_text=str(quality_score),
                        numeric_value=quality_score,
                    ),
                ),
                operators=(
                    build_world_operator(
                        operator_kind=WorldOperatorKind.TARGET_PROJECTION,
                        status=(
                            WorldOperatorStatus.READY_FOR_REVIEW
                            if record.get("decision") == "approved"
                            else WorldOperatorStatus.HOLD_REQUIRED
                            if record.get("decision") == "abstained"
                            else WorldOperatorStatus.BLOCKED
                        ),
                        bounded_confidence=confidence,
                        reason_codes=[str(record.get("decision_reason", "transfer_decision"))],
                    ),
                ),
                replay_safe=True,
                provenance=build_provenance_bundle(
                    entity_kind="world_entity",
                    entity_id=f"world::transfer::{record['transfer_id']}",
                    origin_kind="constructed",
                    links=transfer_links,
                ),
                entity_hash=stable_hash_payload(
                    {
                        "source": record["transfer_id"],
                        "kind": WorldEntityKind.TRANSFER_PROJECTION.value,
                        "target_domain": record["target_domain"],
                        "confidence": confidence,
                    }
                ),
                metadata={"conflict_status": record.get("conflict_status"), "decision": record.get("decision")},
            )
            entities.append(entity)
            entity_id_by_source[f"transfer:{record['transfer_id']}"] = entity.entity_id

        if continuity_state is not None:
            for entry in [require_mapping(item, "continuity_anchor") for item in continuity_state.get("anchors", [])]:
                if entry.get("status") != "active":
                    continue
                candidate_domains = registry.match_domains(
                    labels=[
                        str(entry.get("subject", "")),
                        str(entry.get("continuity_kind", "")),
                        str(entry.get("statement", "")),
                    ]
                )
                target_domain = candidate_domains[0] if candidate_domains else None
                confidence = 0.55
                entity = WorldEntity(
                    entity_id=f"world::continuity::{entry['anchor_id']}",
                    entity_kind=WorldEntityKind.REVIEW_SIGNAL,
                    label=require_non_empty_str(entry.get("statement"), "statement"),
                    target_domain=target_domain,
                    status=WorldEntityStatus.REVIEW_ONLY,
                    world_confidence=confidence,
                    source_refs=(str(entry["anchor_id"]),),
                    state_values=(
                        build_state_value(
                            field_name="continuity_kind",
                            value_type=StateValueType.LABEL,
                            value_text=str(entry.get("continuity_kind")),
                        ),
                    ),
                    operators=(
                        build_world_operator(
                            operator_kind=WorldOperatorKind.FUTURE_EVALUATION,
                            status=WorldOperatorStatus.READY_FOR_REVIEW,
                            bounded_confidence=confidence,
                            reason_codes=["continuity_anchor_signal"],
                        ),
                    ),
                    replay_safe=True,
                    provenance=build_provenance_bundle(
                        entity_kind="world_entity",
                        entity_id=f"world::continuity::{entry['anchor_id']}",
                        origin_kind="constructed",
                        links=[
                            {
                                "role": "source_memory",
                                "ref_id": str(entry["anchor_id"]),
                                "ref_kind": "continuity_anchor",
                                "source_path": "phase4/continuity_memory",
                            }
                        ],
                    ),
                    entity_hash=stable_hash_payload(
                        {
                            "source": entry["anchor_id"],
                            "kind": WorldEntityKind.REVIEW_SIGNAL.value,
                            "target_domain": target_domain,
                            "confidence": confidence,
                        }
                    ),
                    metadata={"subject": entry.get("subject")},
                )
                entities.append(entity)
                entity_id_by_source[f"continuity:{entry['anchor_id']}"] = entity.entity_id

        if len(entities) > self.max_entities:
            raise WorldModelError("world-model entity count exceeds Phase 6 ceiling")

        for entity in entities:
            if entity.target_domain and entity.target_domain in entity_id_by_target_domain:
                relation_provenance_score = provenance_score(entity.provenance)
                relations.append(
                    WorldRelation(
                        relation_id=f"relation::{entity.entity_id}::{entity.target_domain}",
                        relation_kind=WorldRelationKind.PROJECTS_TO_TARGET,
                        source_entity_id=entity.entity_id,
                        target_entity_id=entity_id_by_target_domain[entity.target_domain],
                        relation_strength=_relation_strength(entity.world_confidence, relation_provenance_score, "reviewed"),
                        reason_codes=("projects_to_target_domain",),
                        replay_safe=True,
                        provenance=build_provenance_bundle(
                            entity_kind="world_relation",
                            entity_id=f"relation::{entity.entity_id}::{entity.target_domain}",
                            origin_kind="constructed",
                            links=[
                                {
                                    "role": "world_model",
                                    "ref_id": entity.entity_id,
                                    "ref_kind": "world_entity",
                                    "source_path": "phase6/world_model",
                                },
                                {
                                    "role": "domain",
                                    "ref_id": entity.target_domain,
                                    "ref_kind": "target_domain_structure",
                                    "source_path": "phase6/target_domains",
                                },
                            ],
                        ),
                        relation_hash=stable_hash_payload(
                            {
                                "kind": WorldRelationKind.PROJECTS_TO_TARGET.value,
                                "source": entity.entity_id,
                                "target": entity_id_by_target_domain[entity.target_domain],
                            }
                        ),
                    )
                )

        descriptor_entity_ids = {
            key.removeprefix("descriptor:"): value
            for key, value in entity_id_by_source.items()
            if key.startswith("descriptor:")
        }
        for node in [require_mapping(item, "concept_node") for item in concept_state.get("nodes", [])]:
            source_entity_id = entity_id_by_source.get(f"concept:{node.get('concept_id')}")
            if source_entity_id is None:
                continue
            for descriptor_ref in node.get("descriptor_refs", []):
                target_entity_id = descriptor_entity_ids.get(str(descriptor_ref))
                if target_entity_id is None:
                    continue
                relations.append(
                    WorldRelation(
                        relation_id=f"relation::{source_entity_id}::{target_entity_id}",
                        relation_kind=WorldRelationKind.SUPPORTED_BY_MEMORY,
                        source_entity_id=source_entity_id,
                        target_entity_id=target_entity_id,
                        relation_strength=_relation_strength(0.68, 0.8, "reviewed"),
                        reason_codes=("concept_descriptor_support",),
                        replay_safe=True,
                        provenance=build_provenance_bundle(
                            entity_kind="world_relation",
                            entity_id=f"relation::{source_entity_id}::{target_entity_id}",
                            origin_kind="constructed",
                            links=[
                                {
                                    "role": "graph",
                                    "ref_id": node["concept_id"],
                                    "ref_kind": "concept_node",
                                    "source_path": "phase5/concept_graph",
                                },
                                {
                                    "role": "world_model",
                                    "ref_id": target_entity_id,
                                    "ref_kind": "world_entity",
                                    "source_path": "phase6/world_model",
                                },
                            ],
                        ),
                        relation_hash=stable_hash_payload(
                            {
                                "kind": WorldRelationKind.SUPPORTED_BY_MEMORY.value,
                                "source": source_entity_id,
                                "target": target_entity_id,
                                "descriptor_ref": descriptor_ref,
                            }
                        ),
                    )
                )

        for source_key, candidate_ids in focused_sources.items():
            source_entity_id = entity_id_by_source.get(source_key)
            if source_entity_id is None:
                continue
            source_entity = next(item for item in entities if item.entity_id == source_entity_id)
            if source_entity.target_domain is None or source_entity.target_domain not in entity_id_by_target_domain:
                continue
            relations.append(
                WorldRelation(
                    relation_id=f"focus::{source_entity_id}",
                    relation_kind=WorldRelationKind.FOCUSES_ON,
                    source_entity_id=source_entity_id,
                    target_entity_id=entity_id_by_target_domain[source_entity.target_domain],
                    relation_strength=_relation_strength(0.74, 0.8, "reviewed"),
                    reason_codes=("phase5_support_selection_focus",),
                    replay_safe=True,
                    provenance=build_provenance_bundle(
                        entity_kind="world_relation",
                        entity_id=f"focus::{source_entity_id}",
                        origin_kind="constructed",
                        links=[
                            {
                                "role": "support_selection",
                                "ref_id": candidate_ids[0],
                                "ref_kind": "selected_candidate",
                                "source_path": "phase5/support_selection",
                            },
                            {
                                "role": "world_model",
                                "ref_id": source_entity_id,
                                "ref_kind": "world_entity",
                                "source_path": "phase6/world_model",
                            },
                        ],
                    ),
                    relation_hash=stable_hash_payload(
                        {
                            "kind": WorldRelationKind.FOCUSES_ON.value,
                            "source": source_entity_id,
                            "target": entity_id_by_target_domain[source_entity.target_domain],
                            "candidate_ids": sorted(candidate_ids),
                        }
                    ),
                )
            )

        if len(relations) > self.max_relations:
            raise WorldModelError("world-model relation count exceeds Phase 6 ceiling")

        snapshot = WorldModelSnapshot(
            schema="agifcore.phase_06.world_model.v1",
            entity_capacity=self.max_entities,
            relation_capacity=self.max_relations,
            phase4_interfaces=(
                "semantic_memory.export_state",
                "procedural_memory.export_state",
                "continuity_memory.export_state" if continuity_state is not None else "continuity_memory_unused",
                "working_memory.memory_pressure" if working_memory_map is not None else "working_memory_unused",
            ),
            phase5_interfaces=(
                "descriptor_graph.export_state",
                "skill_graph.export_state",
                "concept_graph.export_state",
                "transfer_graph.export_state",
                "support_selection.read_only" if support_selection_result is not None else "support_selection_unused",
            ),
            entities=tuple(entities),
            relations=tuple(relations),
            snapshot_hash=stable_hash_payload(
                {
                    "entities": [entity.to_dict() for entity in entities],
                    "relations": [relation.to_dict() for relation in relations],
                }
            ),
        )
        if canonical_size_bytes(snapshot.to_dict()) > self.max_state_bytes:
            raise WorldModelError("world-model state exceeds Phase 6 byte ceiling")
        return snapshot
