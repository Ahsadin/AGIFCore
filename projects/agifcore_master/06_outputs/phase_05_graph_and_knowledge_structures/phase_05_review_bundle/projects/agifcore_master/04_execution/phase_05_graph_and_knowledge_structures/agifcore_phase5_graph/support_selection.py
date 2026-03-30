from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .conflict_rules import trust_band_score
from .provenance_links import clamp_score, require_non_empty_str, require_unique_str_list, utc_timestamp

MAX_SUPPORT_CANDIDATES = 24


class SupportSelectionError(ValueError):
    """Raised when reusable support selection exceeds Phase 5 bounds."""


def _tokenize(value: str) -> set[str]:
    return {token for token in value.lower().replace("_", " ").replace("-", " ").split() if token}


@dataclass(slots=True)
class SupportSelectionQuery:
    query_id: str
    query_text: str
    target_domain: str
    required_policy_requirements: list[str]
    requested_layers: list[str]
    max_candidates: int = MAX_SUPPORT_CANDIDATES


@dataclass(slots=True)
class SupportCandidate:
    candidate_id: str
    graph_layer: str
    entity_id: str
    label: str
    trust_band: str
    provenance_score: float
    utility_score: float
    matched_terms: list[str]
    policy_requirements: list[str]
    status: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "graph_layer": self.graph_layer,
            "entity_id": self.entity_id,
            "label": self.label,
            "trust_band": self.trust_band,
            "provenance_score": clamp_score(self.provenance_score),
            "utility_score": clamp_score(self.utility_score),
            "matched_terms": list(self.matched_terms),
            "policy_requirements": list(self.policy_requirements),
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class SupportSelectionResult:
    query_id: str
    status: str
    reason: str
    selected_candidate_ids: list[str]
    ranked_candidates: list[dict[str, Any]]
    blocked_candidate_ids: list[str]
    evaluated_candidate_count: int
    generated_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_id": self.query_id,
            "status": self.status,
            "reason": self.reason,
            "selected_candidate_ids": list(self.selected_candidate_ids),
            "ranked_candidates": [dict(item) for item in self.ranked_candidates],
            "blocked_candidate_ids": list(self.blocked_candidate_ids),
            "evaluated_candidate_count": self.evaluated_candidate_count,
            "generated_at": self.generated_at,
        }


class SupportSelectionEngine:
    """Bounded support selection grounded in graph evidence, trust, and utility."""

    def __init__(self, *, max_candidates: int = MAX_SUPPORT_CANDIDATES) -> None:
        self.max_candidates = max_candidates

    def select_from_graphs(
        self,
        *,
        query_id: str,
        query_text: str,
        target_domain: str,
        required_policy_requirements: list[str],
        descriptor_graph: Any,
        skill_graph: Any,
        concept_graph: Any,
        requested_layers: list[str] | None = None,
        max_candidates: int | None = None,
    ) -> SupportSelectionResult:
        effective_max = max_candidates or self.max_candidates
        if effective_max > self.max_candidates:
            raise SupportSelectionError("requested max_candidates exceeds Phase 5 ceiling")
        query = SupportSelectionQuery(
            query_id=require_non_empty_str(query_id, "query_id"),
            query_text=require_non_empty_str(query_text, "query_text"),
            target_domain=require_non_empty_str(target_domain, "target_domain"),
            required_policy_requirements=require_unique_str_list(
                required_policy_requirements, "required_policy_requirements"
            ),
            requested_layers=require_unique_str_list(
                requested_layers or ["descriptor", "skill", "concept"],
                "requested_layers",
            ),
            max_candidates=effective_max,
        )
        candidates = self._build_candidates(query, descriptor_graph, skill_graph, concept_graph)
        if len(candidates) > effective_max:
            return SupportSelectionResult(
                query_id=query.query_id,
                status="blocked",
                reason="candidate_limit_exceeded",
                selected_candidate_ids=[],
                ranked_candidates=[],
                blocked_candidate_ids=[candidate.candidate_id for candidate in candidates],
                evaluated_candidate_count=len(candidates),
                generated_at=utc_timestamp(),
            )

        ranked: list[dict[str, Any]] = []
        blocked_ids: list[str] = []
        for candidate in candidates:
            policy_ok = set(candidate.policy_requirements).issubset(set(query.required_policy_requirements))
            active = candidate.status == "active"
            if not active or not policy_ok or candidate.provenance_score < 0.3:
                blocked_ids.append(candidate.candidate_id)
                continue
            trust_score = trust_band_score(candidate.trust_band)
            score = clamp_score(
                (0.5 * candidate.utility_score)
                + (0.3 * trust_score)
                + (0.2 * clamp_score(candidate.provenance_score))
            )
            candidate_report = candidate.to_dict()
            candidate_report["trust_score"] = trust_score
            candidate_report["selection_score"] = score
            ranked.append(candidate_report)
        ranked.sort(key=lambda item: item["selection_score"], reverse=True)
        selected_ids = [item["candidate_id"] for item in ranked[:5]]
        status = "selected" if selected_ids else "abstained"
        reason = "governed_support_selected" if selected_ids else "no_candidate_passed_filters"
        return SupportSelectionResult(
            query_id=query.query_id,
            status=status,
            reason=reason,
            selected_candidate_ids=selected_ids,
            ranked_candidates=ranked,
            blocked_candidate_ids=blocked_ids,
            evaluated_candidate_count=len(candidates),
            generated_at=utc_timestamp(),
        )

    def _build_candidates(
        self,
        query: SupportSelectionQuery,
        descriptor_graph: Any,
        skill_graph: Any,
        concept_graph: Any,
    ) -> list[SupportCandidate]:
        query_tokens = _tokenize(query.query_text)
        candidates: list[SupportCandidate] = []
        if "descriptor" in query.requested_layers:
            for descriptor_id in descriptor_graph.active_node_ids():
                node = descriptor_graph.node_state(descriptor_id)
                matched = sorted(
                    query_tokens
                    & (
                        _tokenize(node["label"])
                        | set(token.lower() for token in node["alias_tags"])
                        | set(token.lower() for token in node["domain_tags"])
                        | set(token.lower() for token in node["concept_tags"])
                    )
                )
                utility = clamp_score((len(matched) / max(1, len(query_tokens))) + (0.2 if query.target_domain in node["domain_tags"] else 0.0))
                candidates.append(
                    SupportCandidate(
                        candidate_id=f"descriptor::{descriptor_id}",
                        graph_layer="descriptor",
                        entity_id=descriptor_id,
                        label=node["label"],
                        trust_band=node["trust_band"],
                        provenance_score=node["provenance"]["links"] and clamp_score(len(node["provenance"]["links"]) / 4.0) or 0.0,
                        utility_score=utility,
                        matched_terms=matched,
                        policy_requirements=node["policy_requirements"],
                        status=node["status"],
                    )
                )
        if "skill" in query.requested_layers:
            for skill_id in skill_graph.active_skill_ids():
                node = skill_graph.skill_state(skill_id)
                matched = sorted(
                    query_tokens
                    & (
                        _tokenize(node["skill_name"])
                        | _tokenize(node["objective"])
                        | set(term.lower() for term in node["descriptor_refs"])
                    )
                )
                domain_bonus = 0.2 if not node["allowed_target_domains"] or query.target_domain in node["allowed_target_domains"] else 0.0
                utility = clamp_score((len(matched) / max(1, len(query_tokens))) + domain_bonus)
                candidates.append(
                    SupportCandidate(
                        candidate_id=f"skill::{skill_id}",
                        graph_layer="skill",
                        entity_id=skill_id,
                        label=node["skill_name"],
                        trust_band=node["trust_band"],
                        provenance_score=node["provenance"]["links"] and clamp_score(len(node["provenance"]["links"]) / 4.0) or 0.0,
                        utility_score=utility,
                        matched_terms=matched,
                        policy_requirements=node["policy_requirements"],
                        status="active"
                        if node["status"] == "active" and (not node["allowed_target_domains"] or query.target_domain in node["allowed_target_domains"])
                        else "blocked",
                    )
                )
        if "concept" in query.requested_layers:
            for concept_id in concept_graph.active_concept_ids():
                node = concept_graph.concept_state(concept_id)
                matched = sorted(
                    query_tokens
                    & (
                        _tokenize(node["statement"])
                        | set(token.lower() for token in node["tags"])
                        | set(fragment.lower() for fragment in node["theory_fragments"])
                    )
                )
                utility = clamp_score(len(matched) / max(1, len(query_tokens)))
                candidates.append(
                    SupportCandidate(
                        candidate_id=f"concept::{concept_id}",
                        graph_layer="concept",
                        entity_id=concept_id,
                        label=node["statement"],
                        trust_band=node["trust_band"],
                        provenance_score=node["provenance"]["links"] and clamp_score(len(node["provenance"]["links"]) / 4.0) or 0.0,
                        utility_score=utility,
                        matched_terms=matched,
                        policy_requirements=node["policy_requirements"],
                        status=node["status"],
                    )
                )
        return candidates
