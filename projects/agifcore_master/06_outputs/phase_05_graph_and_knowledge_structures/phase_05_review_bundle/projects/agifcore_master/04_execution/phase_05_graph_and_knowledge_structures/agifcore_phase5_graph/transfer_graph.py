from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .conflict_rules import ConflictCandidate, ConflictRuleEngine, trust_band_score
from .provenance_links import (
    ProvenanceBundle,
    ProvenanceLinksError,
    build_provenance_bundle,
    bundle_from_dict,
    canonical_size_bytes,
    clamp_score,
    provenance_score,
    require_mapping,
    require_non_empty_str,
    require_roles,
    require_unique_str_list,
    stable_hash_payload,
    utc_timestamp,
)

MAX_TRANSFER_LINKS = 128
MAX_TRANSFER_BYTES = 2 * 1024 * 1024
CROSS_DOMAIN_PROVENANCE_FLOOR = 0.45
TRANSFER_ABSTAIN_FLOOR = 0.48


class TransferGraphError(ValueError):
    """Raised when governed transfer behavior exceeds the bounded Phase 5 scope."""


@dataclass(slots=True)
class TransferRecord:
    transfer_id: str
    source_graph: str
    source_id: str
    source_domain: str
    target_graph: str
    target_id: str
    target_domain: str
    explicit_transfer_approval: bool
    requested_policy_requirements: list[str]
    source_policy_requirements: list[str]
    trust_band: str
    provenance: ProvenanceBundle
    baseline_support_score: float
    target_support_score: float
    quality_score: float
    decision: str
    decision_reason: str
    conflict_status: str
    authority_review_ref: str | None
    created_at: str
    materialized_transfer_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "transfer_id": self.transfer_id,
            "source_graph": self.source_graph,
            "source_id": self.source_id,
            "source_domain": self.source_domain,
            "target_graph": self.target_graph,
            "target_id": self.target_id,
            "target_domain": self.target_domain,
            "explicit_transfer_approval": self.explicit_transfer_approval,
            "requested_policy_requirements": list(self.requested_policy_requirements),
            "source_policy_requirements": list(self.source_policy_requirements),
            "trust_band": self.trust_band,
            "provenance": self.provenance.to_dict(),
            "baseline_support_score": self.baseline_support_score,
            "target_support_score": self.target_support_score,
            "quality_score": self.quality_score,
            "decision": self.decision,
            "decision_reason": self.decision_reason,
            "conflict_status": self.conflict_status,
            "authority_review_ref": self.authority_review_ref,
            "created_at": self.created_at,
            "materialized_transfer_id": self.materialized_transfer_id,
            "metadata": dict(self.metadata),
        }


class TransferGraphStore:
    """Governed transfer graph with explicit approve, deny, abstain, and blocked outcomes."""

    def __init__(
        self,
        *,
        store_id: str = "phase-05-transfer-graph",
        max_links: int = MAX_TRANSFER_LINKS,
        max_state_bytes: int = MAX_TRANSFER_BYTES,
    ) -> None:
        self.store_id = store_id
        self.max_links = max_links
        self.max_state_bytes = max_state_bytes
        self._records: dict[str, TransferRecord] = {}
        self._order: list[str] = []
        self._conflicts = ConflictRuleEngine()

    def record_transfer(
        self,
        *,
        transfer_id: str,
        source_graph: str,
        source_id: str,
        source_domain: str,
        target_graph: str,
        target_id: str,
        target_domain: str,
        source_status: str,
        trust_band: str,
        source_policy_requirements: list[str],
        requested_policy_requirements: list[str],
        allowed_target_domains: list[str],
        explicit_transfer_approval: bool,
        provenance_links: list[Mapping[str, Any]],
        baseline_support_score: float,
        target_support_score: float,
        authority_review_ref: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        normalized_id = require_non_empty_str(transfer_id, "transfer_id")
        if normalized_id in self._records:
            raise TransferGraphError(f"duplicate transfer_id: {normalized_id}")
        normalized_authority_review_ref: str | None = None
        if authority_review_ref is not None:
            normalized_authority_review_ref = require_non_empty_str(
                authority_review_ref,
                "authority_review_ref",
            )
        try:
            provenance = build_provenance_bundle(
                entity_kind="transfer",
                entity_id=normalized_id,
                origin_kind="constructed",
                links=provenance_links,
            )
            require_roles(provenance, ("source_memory", "review"))
        except ProvenanceLinksError as error:
            raise TransferGraphError(str(error)) from error

        source_is_active = require_non_empty_str(source_status, "source_status") == "active"
        prov_score = provenance_score(provenance)
        trust_score = trust_band_score(trust_band)
        quality_score = clamp_score(
            (0.4 * trust_score)
            + (0.3 * prov_score)
            + (0.15 * clamp_score(baseline_support_score))
            + (0.15 * clamp_score(target_support_score))
        )
        policy_set = set(require_unique_str_list(source_policy_requirements, "source_policy_requirements"))
        requested_policy_set = set(
            require_unique_str_list(requested_policy_requirements, "requested_policy_requirements")
        )
        conflict = self._conflicts.evaluate_candidates(
            candidates=[
                ConflictCandidate(
                    candidate_id=source_id,
                    active=source_is_active,
                    retired=source_status == "retired",
                    superseded=source_status == "superseded",
                    trust_band=require_non_empty_str(trust_band, "trust_band"),
                    provenance_score=prov_score,
                    utility_score=quality_score,
                    policy_requirements_met=policy_set.issubset(requested_policy_set),
                    target_domains=require_unique_str_list(allowed_target_domains, "allowed_target_domains"),
                )
            ],
            requested_domain=require_non_empty_str(target_domain, "target_domain"),
        )

        decision = "approved"
        reason = "approved"
        materialized_transfer_id: str | None = None
        cross_domain = require_non_empty_str(source_domain, "source_domain") != require_non_empty_str(
            target_domain, "target_domain"
        )
        if conflict.status == "blocked":
            decision = "blocked"
            reason = conflict.reason_code
        elif conflict.status == "defer":
            decision = "abstained"
            reason = conflict.reason_code
        elif cross_domain and not explicit_transfer_approval:
            decision = "denied"
            reason = "missing_explicit_transfer_approval"
        elif cross_domain and normalized_authority_review_ref is None:
            decision = "denied"
            reason = "missing_authority_review_ref"
        elif cross_domain and prov_score < CROSS_DOMAIN_PROVENANCE_FLOOR:
            decision = "denied"
            reason = "cross_domain_provenance_below_floor"
        elif quality_score < TRANSFER_ABSTAIN_FLOOR:
            decision = "abstained"
            reason = "transfer_quality_below_abstain_floor"
        else:
            materialized_transfer_id = f"materialized::{normalized_id}"

        record = TransferRecord(
            transfer_id=normalized_id,
            source_graph=require_non_empty_str(source_graph, "source_graph"),
            source_id=require_non_empty_str(source_id, "source_id"),
            source_domain=require_non_empty_str(source_domain, "source_domain"),
            target_graph=require_non_empty_str(target_graph, "target_graph"),
            target_id=require_non_empty_str(target_id, "target_id"),
            target_domain=require_non_empty_str(target_domain, "target_domain"),
            explicit_transfer_approval=bool(explicit_transfer_approval),
            requested_policy_requirements=sorted(requested_policy_set),
            source_policy_requirements=sorted(policy_set),
            trust_band=require_non_empty_str(trust_band, "trust_band"),
            provenance=provenance,
            baseline_support_score=clamp_score(baseline_support_score),
            target_support_score=clamp_score(target_support_score),
            quality_score=quality_score,
            decision=decision,
            decision_reason=reason,
            conflict_status=conflict.status,
            authority_review_ref=normalized_authority_review_ref,
            created_at=utc_timestamp(),
            materialized_transfer_id=materialized_transfer_id,
            metadata=require_mapping(metadata or {}, "metadata"),
        )
        self._records[record.transfer_id] = record
        self._order.append(record.transfer_id)
        self._ensure_size()
        return record.transfer_id

    def transfer_state(self, transfer_id: str) -> dict[str, Any]:
        record = self._records.get(require_non_empty_str(transfer_id, "transfer_id"))
        if record is None:
            raise TransferGraphError(f"unknown transfer_id: {transfer_id}")
        return record.to_dict()

    def active_link_ids(self) -> list[str]:
        return [
            transfer_id
            for transfer_id in self._order
            if self._records[transfer_id].decision == "approved"
        ]

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_05.transfer_graph.v1",
            "store_id": self.store_id,
            "max_links": self.max_links,
            "records": [self._records[transfer_id].to_dict() for transfer_id in self._order],
            "state_hash": stable_hash_payload(
                {"records": [self._records[transfer_id].to_dict() for transfer_id in self._order]}
            ),
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        payload_map = require_mapping(payload, "transfer_graph_state")
        if payload_map.get("schema") != "agifcore.phase_05.transfer_graph.v1":
            raise TransferGraphError("transfer graph schema mismatch")
        self.store_id = require_non_empty_str(payload_map.get("store_id"), "store_id")
        max_links = payload_map.get("max_links", self.max_links)
        if not isinstance(max_links, int) or max_links <= 0:
            raise TransferGraphError("max_links must be a positive integer")
        self.max_links = max_links
        self._records = {}
        self._order = []
        for record_payload in payload_map.get("records", []):
            record_map = require_mapping(record_payload, "record")
            authority_review_ref = record_map.get("authority_review_ref")
            normalized_authority_review_ref: str | None = None
            if authority_review_ref is not None:
                normalized_authority_review_ref = require_non_empty_str(
                    authority_review_ref,
                    "authority_review_ref",
                )
            record = TransferRecord(
                transfer_id=require_non_empty_str(record_map.get("transfer_id"), "transfer_id"),
                source_graph=require_non_empty_str(record_map.get("source_graph"), "source_graph"),
                source_id=require_non_empty_str(record_map.get("source_id"), "source_id"),
                source_domain=require_non_empty_str(record_map.get("source_domain"), "source_domain"),
                target_graph=require_non_empty_str(record_map.get("target_graph"), "target_graph"),
                target_id=require_non_empty_str(record_map.get("target_id"), "target_id"),
                target_domain=require_non_empty_str(record_map.get("target_domain"), "target_domain"),
                explicit_transfer_approval=bool(record_map.get("explicit_transfer_approval")),
                requested_policy_requirements=require_unique_str_list(
                    record_map.get("requested_policy_requirements", []),
                    "requested_policy_requirements",
                ),
                source_policy_requirements=require_unique_str_list(
                    record_map.get("source_policy_requirements", []),
                    "source_policy_requirements",
                ),
                trust_band=require_non_empty_str(record_map.get("trust_band"), "trust_band"),
                provenance=bundle_from_dict(record_map.get("provenance", {})),
                baseline_support_score=clamp_score(record_map.get("baseline_support_score", 0.0)),
                target_support_score=clamp_score(record_map.get("target_support_score", 0.0)),
                quality_score=clamp_score(record_map.get("quality_score", 0.0)),
                decision=require_non_empty_str(record_map.get("decision"), "decision"),
                decision_reason=require_non_empty_str(record_map.get("decision_reason"), "decision_reason"),
                conflict_status=require_non_empty_str(record_map.get("conflict_status"), "conflict_status"),
                authority_review_ref=normalized_authority_review_ref,
                created_at=require_non_empty_str(record_map.get("created_at"), "created_at"),
                materialized_transfer_id=record_map.get("materialized_transfer_id"),
                metadata=require_mapping(record_map.get("metadata", {}), "metadata"),
            )
            cross_domain = record.source_domain != record.target_domain
            if cross_domain and record.explicit_transfer_approval and record.decision == "approved":
                if record.authority_review_ref is None:
                    raise TransferGraphError("approved cross-domain transfer missing authority_review_ref")
            self._records[record.transfer_id] = record
            self._order.append(record.transfer_id)
        self._ensure_size()

    def _ensure_size(self) -> None:
        if len(self.active_link_ids()) > self.max_links:
            raise TransferGraphError("transfer graph exceeds max active-link count")
        if canonical_size_bytes(self.export_state()) > self.max_state_bytes:
            raise TransferGraphError("transfer graph exceeds max state bytes")
