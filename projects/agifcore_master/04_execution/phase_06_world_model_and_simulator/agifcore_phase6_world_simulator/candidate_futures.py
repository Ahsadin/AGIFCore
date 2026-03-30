from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping

from .entity_classes import (
    MAX_BRANCH_DEPTH,
    MAX_CANDIDATE_FUTURES,
    CandidateFuture,
    CandidateFutureSnapshot,
    SimulationOutcome,
    WorldEntityKind,
    WorldEntityStatus,
    WorldOperatorStatus,
    WorldRelationKind,
    build_provenance_bundle,
    canonical_size_bytes,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

MAX_FUTURE_STATE_BYTES = 2 * 1024 * 1024


class CandidateFuturesError(ValueError):
    """Raised when candidate-future generation violates Phase 6 boundaries."""


def _sort_relations(relations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        relations,
        key=lambda item: (
            -float(item.get("relation_strength", 0.0)),
            str(item.get("relation_kind")),
            str(item.get("relation_id")),
        ),
    )


class CandidateFuturePlanner:
    """Build bounded candidate futures from a read-only Phase 6 world-model snapshot."""

    def __init__(
        self,
        *,
        max_futures: int = MAX_CANDIDATE_FUTURES,
        max_branch_depth: int = MAX_BRANCH_DEPTH,
        max_state_bytes: int = MAX_FUTURE_STATE_BYTES,
    ) -> None:
        self.max_futures = max_futures
        self.max_branch_depth = max_branch_depth
        self.max_state_bytes = max_state_bytes

    def build_snapshot(self, *, world_model_state: Mapping[str, Any]) -> CandidateFutureSnapshot:
        world_state = require_schema(world_model_state, "agifcore.phase_06.world_model.v1", "world_model_state")
        entities = [require_mapping(item, "world_entity") for item in world_state.get("entities", [])]
        relations = [require_mapping(item, "world_relation") for item in world_state.get("relations", [])]
        entity_by_id = {
            require_non_empty_str(entity.get("entity_id"), "entity_id"): entity for entity in entities
        }
        target_entities = {
            entity_id
            for entity_id, entity in entity_by_id.items()
            if entity.get("entity_kind") == WorldEntityKind.TARGET_DOMAIN_OBJECT.value
        }
        relation_by_source: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        for relation in relations:
            if relation.get("target_entity_id") not in target_entities:
                continue
            kind = relation.get("relation_kind")
            if kind not in {WorldRelationKind.PROJECTS_TO_TARGET.value, WorldRelationKind.FOCUSES_ON.value}:
                continue
            source_entity_id = require_non_empty_str(relation.get("source_entity_id"), "source_entity_id")
            relation_by_source[source_entity_id].append(relation)

        futures: list[CandidateFuture] = []
        for entity in sorted(entities, key=lambda item: str(item.get("entity_id"))):
            entity_id = require_non_empty_str(entity.get("entity_id"), "entity_id")
            if entity.get("entity_kind") == WorldEntityKind.TARGET_DOMAIN_OBJECT.value:
                continue
            if entity.get("entity_kind") not in {
                WorldEntityKind.DESCRIPTOR_SUPPORT.value,
            }:
                continue
            if entity.get("status") == WorldEntityStatus.BLOCKED.value:
                continue
            target_domain = entity.get("target_domain")
            if not target_domain:
                continue
            operators = [require_mapping(item, "operator") for item in entity.get("operators", [])]
            if not operators:
                continue
            operator = operators[0]
            source_relations = _sort_relations(relation_by_source.get(entity_id, []))
            if not source_relations:
                continue
            parent_future_id: str | None = None
            for relation_index, relation in enumerate(source_relations[:2], start=1):
                if len(futures) >= self.max_futures:
                    raise CandidateFuturesError("candidate-future count exceeds Phase 6 ceiling")
                operator_status = str(operator.get("status"))
                entity_status = str(entity.get("status"))
                if operator_status == WorldOperatorStatus.BLOCKED.value:
                    projected_outcome = SimulationOutcome.ABSTAIN
                    reason_codes = ["operator_blocked", "future_abstained"]
                elif operator_status == WorldOperatorStatus.HOLD_REQUIRED.value or entity_status == WorldEntityStatus.HELD.value:
                    projected_outcome = SimulationOutcome.HOLD_PROJECTED
                    reason_codes = ["hold_required", "review_only_execution_disabled"]
                else:
                    projected_outcome = SimulationOutcome.REVIEW_ONLY_PROJECTED
                    reason_codes = ["candidate_future_ready", "review_only_execution_disabled"]
                branch_depth = min(relation_index, self.max_branch_depth)
                payload = {
                    "source_entity_id": entity_id,
                    "target_domain": target_domain,
                    "relation_id": relation["relation_id"],
                    "branch_depth": branch_depth,
                    "parent_future_id": parent_future_id,
                    "projected_outcome": projected_outcome.value,
                }
                future_id = f"future::{stable_hash_payload(payload)[:12]}"
                relation_strength = float(relation.get("relation_strength", 0.0))
                entity_confidence = float(entity.get("world_confidence", 0.0))
                operator_confidence = float(operator.get("bounded_confidence", 0.0))
                bounded_confidence = clamp_score(
                    (0.45 * entity_confidence) + (0.35 * relation_strength) + (0.20 * operator_confidence)
                )
                state_codes = (
                    "read_only_projection",
                    f"entity_status_{entity_status}",
                    f"operator_status_{operator_status}",
                    f"relation_kind_{relation.get('relation_kind')}",
                    "live_transfer_execution_disabled",
                )
                provenance = build_provenance_bundle(
                    entity_kind="candidate_future",
                    entity_id=future_id,
                    origin_kind="constructed",
                    links=[
                        {
                            "role": "world_model",
                            "ref_id": entity_id,
                            "ref_kind": "world_entity",
                            "source_path": "phase6/world_model",
                        },
                        {
                            "role": "future",
                            "ref_id": relation["relation_id"],
                            "ref_kind": "world_relation",
                            "source_path": "phase6/candidate_futures",
                        },
                    ],
                )
                futures.append(
                    CandidateFuture(
                        future_id=future_id,
                        source_entity_id=entity_id,
                        target_domain=require_non_empty_str(target_domain, "target_domain"),
                        relation_id=require_non_empty_str(relation.get("relation_id"), "relation_id"),
                        branch_depth=branch_depth,
                        parent_future_id=parent_future_id,
                        projected_outcome=projected_outcome,
                        bounded_confidence=bounded_confidence,
                        state_codes=state_codes,
                        reason_codes=tuple(reason_codes),
                        provenance=provenance,
                        future_hash=stable_hash_payload(
                            {
                                **payload,
                                "bounded_confidence": bounded_confidence,
                                "state_codes": state_codes,
                                "reason_codes": reason_codes,
                            }
                        ),
                    )
                )
                parent_future_id = future_id

        snapshot = CandidateFutureSnapshot(
            schema="agifcore.phase_06.candidate_futures.v1",
            max_futures=self.max_futures,
            max_branch_depth=self.max_branch_depth,
            source_world_model_hash=require_non_empty_str(world_state.get("snapshot_hash"), "snapshot_hash"),
            futures=tuple(futures),
            snapshot_hash=stable_hash_payload(
                {
                    "source_world_model_hash": world_state.get("snapshot_hash"),
                    "futures": [future.to_dict() for future in futures],
                }
            ),
        )
        if canonical_size_bytes(snapshot.to_dict()) > self.max_state_bytes:
            raise CandidateFuturesError("candidate-future state exceeds Phase 6 byte ceiling")
        return snapshot
