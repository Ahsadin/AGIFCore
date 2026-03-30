from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from .continuity_memory import ContinuityMemoryStore
from .procedural_memory import ProceduralMemoryStore
from .semantic_memory import SemanticMemoryStore


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class PromotionPipelineError(ValueError):
    """Raised when promotion bypasses review or targets the wrong plane."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PromotionPipelineError(f"{field_name} must be a non-empty string")
    return value


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise PromotionPipelineError(f"{field_name} must be a mapping")
    return dict(value)


def _require_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise PromotionPipelineError(f"{field_name} must be a list")
    result: list[str] = []
    for item in value:
        result.append(_require_non_empty_str(item, f"{field_name}[]"))
    return result


@dataclass(frozen=True, slots=True)
class PromotionRecord:
    promotion_id: str
    target_plane: str
    created_id: str
    review_ref: str
    source_candidate_id: str
    promoted_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "promotion_id": self.promotion_id,
            "target_plane": self.target_plane,
            "created_id": self.created_id,
            "review_ref": self.review_ref,
            "source_candidate_id": self.source_candidate_id,
            "promoted_at": self.promoted_at,
        }


class PromotionPipeline:
    """Review-gated promotion into semantic, procedural, or continuity memory."""

    def __init__(self) -> None:
        self._counter = 0
        self._records: list[PromotionRecord] = []

    def promote_review_candidate(
        self,
        *,
        review_ref: str,
        review_queue: Any,
        source_candidate: Mapping[str, Any],
        semantic_store: SemanticMemoryStore | None = None,
        procedural_store: ProceduralMemoryStore | None = None,
        continuity_store: ContinuityMemoryStore | None = None,
    ) -> dict[str, Any]:
        normalized_review_ref = _require_non_empty_str(review_ref, "review_ref")
        if not hasattr(review_queue, "export_state"):
            raise PromotionPipelineError("review_queue must expose export_state()")
        queue_state = _require_mapping(review_queue.export_state(), "review_queue_state")
        queue_candidates = queue_state.get("candidates", [])
        if not isinstance(queue_candidates, list):
            raise PromotionPipelineError("review_queue export must contain a candidates list")
        review: dict[str, Any] | None = None
        for item in queue_candidates:
            candidate_map = _require_mapping(item, "review_candidate")
            if candidate_map.get("review_ref") == normalized_review_ref:
                review = candidate_map
                break
        if review is None:
            raise PromotionPipelineError(f"review_ref not found in review queue: {normalized_review_ref}")
        candidate = _require_mapping(source_candidate, "source_candidate")
        if _require_non_empty_str(review.get("status"), "status") != "approved":
            raise PromotionPipelineError("promotion requires an approved review candidate")
        target_plane = _require_non_empty_str(review.get("target_plane"), "target_plane")
        review_ref = normalized_review_ref
        source_candidate_id = _require_non_empty_str(
            candidate.get("candidate_id"), "candidate_id"
        )
        if _require_non_empty_str(review.get("candidate_id"), "candidate_id") != source_candidate_id:
            raise PromotionPipelineError("review candidate and source candidate must reference the same candidate_id")
        payload = _require_mapping(candidate.get("payload", {}), "payload")
        provenance_refs = _require_str_list(
            candidate.get("provenance_refs", []), "provenance_refs"
        )
        self._counter += 1
        promotion_id = f"phase4-promotion-{self._counter:08d}"

        if target_plane == "semantic":
            if semantic_store is None:
                raise PromotionPipelineError("semantic_store is required for semantic promotion")
            created_id = f"semantic-entry-{self._counter:08d}"
            semantic_store.add_entry(
                entry_id=created_id,
                concept_type=_require_non_empty_str(
                    candidate.get("candidate_kind"), "candidate_kind"
                ),
                abstraction=_require_non_empty_str(
                    payload.get("summary") or payload.get("abstraction") or str(payload),
                    "abstraction",
                ),
                provenance_refs=provenance_refs,
                review_ref=review_ref,
                source_candidate_id=source_candidate_id,
                supporting_refs=_require_str_list(payload.get("supporting_refs", []), "supporting_refs"),
                graph_refs=_require_str_list(payload.get("graph_refs", []), "graph_refs"),
                metadata={"promotion_id": promotion_id},
            )
        elif target_plane == "procedural":
            if procedural_store is None:
                raise PromotionPipelineError("procedural_store is required for procedural promotion")
            created_id = f"procedure-entry-{self._counter:08d}"
            steps = payload.get("steps", [])
            if not steps:
                steps = [payload.get("summary") or "reviewed procedure step"]
            procedural_store.add_procedure(
                procedure_id=created_id,
                procedure_name=_require_non_empty_str(
                    payload.get("procedure_name") or source_candidate_id, "procedure_name"
                ),
                objective=_require_non_empty_str(
                    payload.get("objective") or payload.get("summary") or "reviewed procedure",
                    "objective",
                ),
                steps=_require_str_list(steps, "steps"),
                preconditions=_require_str_list(payload.get("preconditions", []), "preconditions"),
                postconditions=_require_str_list(payload.get("postconditions", []), "postconditions"),
                constraints=_require_str_list(payload.get("constraints", []), "constraints"),
                provenance_refs=provenance_refs,
                review_ref=review_ref,
                source_candidate_id=source_candidate_id,
                graph_refs=_require_str_list(payload.get("graph_refs", []), "graph_refs"),
                metadata={"promotion_id": promotion_id},
            )
        elif target_plane == "continuity":
            if continuity_store is None:
                raise PromotionPipelineError("continuity_store is required for continuity promotion")
            created_id = f"continuity-anchor-{self._counter:08d}"
            continuity_store.record_anchor(
                anchor_id=created_id,
                subject=_require_non_empty_str(payload.get("subject") or "self", "subject"),
                continuity_kind=_require_non_empty_str(
                    payload.get("continuity_kind") or "self_history",
                    "continuity_kind",
                ),
                statement=_require_non_empty_str(
                    payload.get("statement") or payload.get("summary") or str(payload),
                    "statement",
                ),
                provenance_refs=provenance_refs,
                metadata={"promotion_id": promotion_id, "review_ref": review_ref},
            )
        else:
            raise PromotionPipelineError("target_plane must be semantic, procedural, or continuity")

        record = PromotionRecord(
            promotion_id=promotion_id,
            target_plane=target_plane,
            created_id=created_id,
            review_ref=review_ref,
            source_candidate_id=source_candidate_id,
            promoted_at=utc_timestamp(),
        )
        self._records.append(record)
        return record.to_dict()

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_04.promotion_pipeline.v1",
            "promotion_records": [item.to_dict() for item in self._records],
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_04.promotion_pipeline.v1":
            raise PromotionPipelineError("promotion pipeline schema mismatch")
        records = payload.get("promotion_records", [])
        if not isinstance(records, list):
            raise PromotionPipelineError("promotion_records must be a list")
        self._records = []
        self._counter = 0
        for record_payload in records:
            record_map = _require_mapping(record_payload, "promotion_record")
            record = PromotionRecord(
                promotion_id=_require_non_empty_str(record_map.get("promotion_id"), "promotion_id"),
                target_plane=_require_non_empty_str(record_map.get("target_plane"), "target_plane"),
                created_id=_require_non_empty_str(record_map.get("created_id"), "created_id"),
                review_ref=_require_non_empty_str(record_map.get("review_ref"), "review_ref"),
                source_candidate_id=_require_non_empty_str(
                    record_map.get("source_candidate_id"), "source_candidate_id"
                ),
                promoted_at=_require_non_empty_str(record_map.get("promoted_at"), "promoted_at"),
            )
            self._records.append(record)
            suffix = record.promotion_id.split("-")[-1]
            if suffix.isdigit():
                self._counter = max(self._counter, int(suffix))
