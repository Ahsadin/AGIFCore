from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .provenance_links import clamp_score, require_non_empty_str, utc_timestamp

MAX_CONFLICT_SET = 8
TRUST_BAND_SCORES = {
    "policy": 0.95,
    "bounded_local": 0.76,
    "reviewed": 0.72,
    "experimental": 0.35,
    "unknown": 0.6,
}


class ConflictRulesError(ValueError):
    """Raised when Phase 5 conflict evaluation is malformed or out of bounds."""


def trust_band_score(trust_band: str) -> float:
    normalized = require_non_empty_str(trust_band, "trust_band")
    return clamp_score(TRUST_BAND_SCORES.get(normalized, TRUST_BAND_SCORES["unknown"]))


@dataclass(slots=True)
class ConflictCandidate:
    candidate_id: str
    active: bool
    trust_band: str
    provenance_score: float
    utility_score: float
    policy_requirements_met: bool
    target_domains: list[str] = field(default_factory=list)
    retired: bool = False
    superseded: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "active": self.active,
            "trust_band": self.trust_band,
            "provenance_score": clamp_score(self.provenance_score),
            "utility_score": clamp_score(self.utility_score),
            "policy_requirements_met": self.policy_requirements_met,
            "target_domains": list(self.target_domains),
            "retired": self.retired,
            "superseded": self.superseded,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ConflictDecision:
    status: str
    chosen_candidate_id: str | None
    reason_code: str
    competing_candidate_ids: list[str]
    blocked_candidate_ids: list[str]
    scored_candidates: list[dict[str, Any]]
    decided_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "chosen_candidate_id": self.chosen_candidate_id,
            "reason_code": self.reason_code,
            "competing_candidate_ids": list(self.competing_candidate_ids),
            "blocked_candidate_ids": list(self.blocked_candidate_ids),
            "scored_candidates": [dict(item) for item in self.scored_candidates],
            "decided_at": self.decided_at,
        }


class ConflictRuleEngine:
    """Conflict evaluator for support choice and governed transfer decisions."""

    def __init__(self, *, max_conflict_size: int = MAX_CONFLICT_SET) -> None:
        self.max_conflict_size = max_conflict_size

    def evaluate_candidates(
        self,
        *,
        candidates: list[ConflictCandidate],
        requested_domain: str | None = None,
    ) -> ConflictDecision:
        if not candidates:
            raise ConflictRulesError("candidates must not be empty")
        if len(candidates) > self.max_conflict_size:
            raise ConflictRulesError("candidate count exceeds Phase 5 conflict-set ceiling")

        scored_candidates: list[dict[str, Any]] = []
        allowed_candidates: list[tuple[ConflictCandidate, float]] = []
        blocked_candidate_ids: list[str] = []

        for candidate in candidates:
            reason_code = "clear"
            if not candidate.active:
                reason_code = "inactive_source"
            elif candidate.retired:
                reason_code = "retired_source"
            elif candidate.superseded:
                reason_code = "superseded_source"
            elif not candidate.policy_requirements_met:
                reason_code = "missing_required_policy"
            elif requested_domain and candidate.target_domains and requested_domain not in candidate.target_domains:
                reason_code = "target_domain_mismatch"
            elif clamp_score(candidate.provenance_score) < 0.3:
                reason_code = "provenance_gap"

            trust_score = trust_band_score(candidate.trust_band)
            total_score = clamp_score(
                (0.45 * clamp_score(candidate.utility_score))
                + (0.35 * trust_score)
                + (0.20 * clamp_score(candidate.provenance_score))
            )
            candidate_report = candidate.to_dict()
            candidate_report["trust_score"] = trust_score
            candidate_report["total_score"] = total_score
            candidate_report["blocked_reason"] = None if reason_code == "clear" else reason_code
            scored_candidates.append(candidate_report)

            if reason_code == "clear":
                allowed_candidates.append((candidate, total_score))
            else:
                blocked_candidate_ids.append(candidate.candidate_id)

        if not allowed_candidates:
            return ConflictDecision(
                status="blocked",
                chosen_candidate_id=None,
                reason_code="all_candidates_blocked",
                competing_candidate_ids=[candidate.candidate_id for candidate in candidates],
                blocked_candidate_ids=blocked_candidate_ids,
                scored_candidates=scored_candidates,
                decided_at=utc_timestamp(),
            )

        allowed_candidates.sort(key=lambda item: item[1], reverse=True)
        winner, winner_score = allowed_candidates[0]
        competing_ids = [candidate.candidate_id for candidate, _ in allowed_candidates]
        if len(allowed_candidates) > 1:
            runner_up_score = allowed_candidates[1][1]
            if winner_score - runner_up_score < 0.08:
                return ConflictDecision(
                    status="defer",
                    chosen_candidate_id=None,
                    reason_code="insufficient_separation",
                    competing_candidate_ids=competing_ids,
                    blocked_candidate_ids=blocked_candidate_ids,
                    scored_candidates=scored_candidates,
                    decided_at=utc_timestamp(),
                )

        return ConflictDecision(
            status="clear",
            chosen_candidate_id=winner.candidate_id,
            reason_code="highest_governed_score",
            competing_candidate_ids=competing_ids,
            blocked_candidate_ids=blocked_candidate_ids,
            scored_candidates=scored_candidates,
            decided_at=utc_timestamp(),
        )
