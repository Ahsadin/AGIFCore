from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

MAX_REVIEW_CANDIDATES = 256
ALLOWED_TIERS = ("hot", "warm", "cold", "ephemeral")
ALLOWED_DECISIONS = ("approve", "reject", "hold")


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class MemoryReviewError(ValueError):
    """Raised when review candidates or decisions violate the Phase 4 boundary."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MemoryReviewError(f"{field_name} must be a non-empty string")
    return value


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise MemoryReviewError(f"{field_name} must be a mapping")
    return dict(value)


def _require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise MemoryReviewError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        text = _require_non_empty_str(item, f"{field_name}[]")
        if text in seen:
            raise MemoryReviewError(f"{field_name} contains duplicate entries")
        seen.add(text)
        result.append(text)
    return result


@dataclass(slots=True)
class ReviewCandidate:
    review_ref: str
    candidate_id: str
    source_plane: str
    target_plane: str
    candidate_kind: str
    proposed_tier: str
    payload: dict[str, Any]
    provenance_refs: list[str]
    submitted_at: str
    status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_ref": self.review_ref,
            "candidate_id": self.candidate_id,
            "source_plane": self.source_plane,
            "target_plane": self.target_plane,
            "candidate_kind": self.candidate_kind,
            "proposed_tier": self.proposed_tier,
            "payload": deepcopy(self.payload),
            "provenance_refs": list(self.provenance_refs),
            "submitted_at": self.submitted_at,
            "status": self.status,
        }


@dataclass(slots=True)
class ReviewDecision:
    decision_ref: str
    review_ref: str
    decision: str
    assigned_tier: str
    rationale: str
    reviewer: str
    decided_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_ref": self.decision_ref,
            "review_ref": self.review_ref,
            "decision": self.decision,
            "assigned_tier": self.assigned_tier,
            "rationale": self.rationale,
            "reviewer": self.reviewer,
            "decided_at": self.decided_at,
        }


class MemoryReviewQueue:
    """Explicit review queue with tiered decisions that affect candidate readiness."""

    def __init__(self, *, queue_id: str = "phase-04-memory-review", max_candidates: int = MAX_REVIEW_CANDIDATES) -> None:
        self.queue_id = queue_id
        self.max_candidates = max_candidates
        self._candidate_counter = 0
        self._decision_counter = 0
        self._candidates: dict[str, ReviewCandidate] = {}
        self._decisions: list[ReviewDecision] = []

    def submit_candidate(
        self,
        *,
        candidate_id: str,
        source_plane: str,
        target_plane: str,
        candidate_kind: str,
        proposed_tier: str,
        payload: Mapping[str, Any],
        provenance_refs: list[str],
    ) -> str:
        if len(self._candidates) >= self.max_candidates:
            raise MemoryReviewError("memory review queue exceeds max candidate count")
        normalized_tier = _require_non_empty_str(proposed_tier, "proposed_tier")
        if normalized_tier not in ALLOWED_TIERS:
            raise MemoryReviewError(f"proposed_tier must be one of {ALLOWED_TIERS}")
        self._candidate_counter += 1
        review_ref = f"memory-review-{self._candidate_counter:08d}"
        candidate = ReviewCandidate(
            review_ref=review_ref,
            candidate_id=_require_non_empty_str(candidate_id, "candidate_id"),
            source_plane=_require_non_empty_str(source_plane, "source_plane"),
            target_plane=_require_non_empty_str(target_plane, "target_plane"),
            candidate_kind=_require_non_empty_str(candidate_kind, "candidate_kind"),
            proposed_tier=normalized_tier,
            payload=_require_mapping(payload, "payload"),
            provenance_refs=_require_unique_str_list(provenance_refs, "provenance_refs"),
            submitted_at=utc_timestamp(),
        )
        self._candidates[review_ref] = candidate
        return review_ref

    def decide(
        self,
        *,
        review_ref: str,
        decision: str,
        assigned_tier: str,
        rationale: str,
        reviewer: str = "phase-04-reviewer",
    ) -> dict[str, Any]:
        candidate = self._get_candidate(review_ref)
        normalized_decision = _require_non_empty_str(decision, "decision")
        if normalized_decision not in ALLOWED_DECISIONS:
            raise MemoryReviewError(f"decision must be one of {ALLOWED_DECISIONS}")
        normalized_tier = _require_non_empty_str(assigned_tier, "assigned_tier")
        if normalized_tier not in ALLOWED_TIERS:
            raise MemoryReviewError(f"assigned_tier must be one of {ALLOWED_TIERS}")
        self._decision_counter += 1
        decision_ref = f"memory-review-decision-{self._decision_counter:08d}"
        candidate.status = {
            "approve": "approved",
            "reject": "rejected",
            "hold": "held",
        }[normalized_decision]
        record = ReviewDecision(
            decision_ref=decision_ref,
            review_ref=review_ref,
            decision=normalized_decision,
            assigned_tier=normalized_tier,
            rationale=_require_non_empty_str(rationale, "rationale"),
            reviewer=_require_non_empty_str(reviewer, "reviewer"),
            decided_at=utc_timestamp(),
        )
        self._decisions.append(record)
        return {
            "review_ref": review_ref,
            "candidate_id": candidate.candidate_id,
            "status": candidate.status,
            "assigned_tier": normalized_tier,
            "decision_ref": decision_ref,
        }

    def approved_candidates(self, *, target_plane: str | None = None) -> list[dict[str, Any]]:
        approved = [item for item in self._candidates.values() if item.status == "approved"]
        if target_plane is not None:
            approved = [item for item in approved if item.target_plane == target_plane]
        return [item.to_dict() for item in approved]

    def tier_summary(self) -> dict[str, int]:
        counts = {tier: 0 for tier in ALLOWED_TIERS}
        for candidate in self._candidates.values():
            counts[candidate.proposed_tier] += 1
        return counts

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_04.memory_review.v1",
            "queue_id": self.queue_id,
            "max_candidates": self.max_candidates,
            "tier_summary": self.tier_summary(),
            "candidates": [item.to_dict() for item in self._candidates.values()],
            "decisions": [item.to_dict() for item in self._decisions],
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_04.memory_review.v1":
            raise MemoryReviewError("memory review schema mismatch")
        self.queue_id = _require_non_empty_str(payload.get("queue_id"), "queue_id")
        max_candidates = payload.get("max_candidates", self.max_candidates)
        if not isinstance(max_candidates, int) or max_candidates <= 0:
            raise MemoryReviewError("max_candidates must be a positive integer")
        self.max_candidates = max_candidates
        candidates = payload.get("candidates", [])
        decisions = payload.get("decisions", [])
        if not isinstance(candidates, list) or not isinstance(decisions, list):
            raise MemoryReviewError("candidates and decisions must be lists")
        self._candidates = {}
        self._candidate_counter = 0
        for candidate_payload in candidates:
            candidate_map = _require_mapping(candidate_payload, "candidate")
            candidate = ReviewCandidate(
                review_ref=_require_non_empty_str(candidate_map.get("review_ref"), "review_ref"),
                candidate_id=_require_non_empty_str(candidate_map.get("candidate_id"), "candidate_id"),
                source_plane=_require_non_empty_str(candidate_map.get("source_plane"), "source_plane"),
                target_plane=_require_non_empty_str(candidate_map.get("target_plane"), "target_plane"),
                candidate_kind=_require_non_empty_str(candidate_map.get("candidate_kind"), "candidate_kind"),
                proposed_tier=_require_non_empty_str(candidate_map.get("proposed_tier"), "proposed_tier"),
                payload=_require_mapping(candidate_map.get("payload", {}), "payload"),
                provenance_refs=_require_unique_str_list(candidate_map.get("provenance_refs", []), "provenance_refs"),
                submitted_at=_require_non_empty_str(candidate_map.get("submitted_at"), "submitted_at"),
                status=_require_non_empty_str(candidate_map.get("status", "pending"), "status"),
            )
            self._candidates[candidate.review_ref] = candidate
            suffix = candidate.review_ref.split("-")[-1]
            if suffix.isdigit():
                self._candidate_counter = max(self._candidate_counter, int(suffix))
        self._decisions = []
        self._decision_counter = 0
        for decision_payload in decisions:
            decision_map = _require_mapping(decision_payload, "decision")
            decision = ReviewDecision(
                decision_ref=_require_non_empty_str(decision_map.get("decision_ref"), "decision_ref"),
                review_ref=_require_non_empty_str(decision_map.get("review_ref"), "review_ref"),
                decision=_require_non_empty_str(decision_map.get("decision"), "decision"),
                assigned_tier=_require_non_empty_str(decision_map.get("assigned_tier"), "assigned_tier"),
                rationale=_require_non_empty_str(decision_map.get("rationale"), "rationale"),
                reviewer=_require_non_empty_str(decision_map.get("reviewer"), "reviewer"),
                decided_at=_require_non_empty_str(decision_map.get("decided_at"), "decided_at"),
            )
            self._decisions.append(decision)
            suffix = decision.decision_ref.split("-")[-1]
            if suffix.isdigit():
                self._decision_counter = max(self._decision_counter, int(suffix))

    def _get_candidate(self, review_ref: str) -> ReviewCandidate:
        normalized = _require_non_empty_str(review_ref, "review_ref")
        candidate = self._candidates.get(normalized)
        if candidate is None:
            raise MemoryReviewError(f"unknown review_ref: {normalized}")
        return candidate
