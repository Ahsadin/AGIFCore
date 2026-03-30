from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from .semantic_memory import SemanticMemoryStore


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class CompressionPipelineError(ValueError):
    """Raised when compression is not review-gated or loses explicit retained state."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CompressionPipelineError(f"{field_name} must be a non-empty string")
    return value


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise CompressionPipelineError(f"{field_name} must be a mapping")
    return dict(value)


def _require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise CompressionPipelineError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        text = _require_non_empty_str(item, f"{field_name}[]")
        if text in seen:
            raise CompressionPipelineError(f"{field_name} contains duplicate entries")
        seen.add(text)
        result.append(text)
    return result


def _merge_unique(values: list[list[str]]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for group in values:
        for item in group:
            if item not in seen:
                seen.add(item)
                merged.append(item)
    return merged


@dataclass(frozen=True, slots=True)
class CompressionRecord:
    compression_id: str
    review_ref: str
    target_plane: str
    source_ids: list[str]
    created_id: str
    state_bytes_before: int
    state_bytes_after: int
    compressed_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "compression_id": self.compression_id,
            "review_ref": self.review_ref,
            "target_plane": self.target_plane,
            "source_ids": list(self.source_ids),
            "created_id": self.created_id,
            "state_bytes_before": self.state_bytes_before,
            "state_bytes_after": self.state_bytes_after,
            "compressed_at": self.compressed_at,
        }


class CompressionPipeline:
    """Explicit review-gated compression that preserves a retained semantic anchor."""

    def __init__(self) -> None:
        self._counter = 0
        self._records: list[CompressionRecord] = []

    def compress_semantic_entries(
        self,
        *,
        review_ref: str,
        review_queue: Any,
        semantic_store: SemanticMemoryStore,
        entry_ids: list[str],
        summary_abstraction: str,
        concept_type: str = "compressed_abstraction",
        supporting_refs: list[str] | None = None,
        graph_refs: list[str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        normalized_review_ref = _require_non_empty_str(review_ref, "review_ref")
        normalized_entry_ids = _require_unique_str_list(entry_ids, "entry_ids")
        if len(normalized_entry_ids) < 2:
            raise CompressionPipelineError("semantic compression requires at least two entry_ids")
        review = self._approved_review(
            review_ref=normalized_review_ref,
            review_queue=review_queue,
            expected_target_plane="semantic",
            expected_candidate_kind="semantic_compression",
        )
        payload = _require_mapping(review.get("payload", {}), "review_payload")
        reviewed_entry_ids = payload.get("entry_ids")
        if reviewed_entry_ids is not None:
            expected_ids = _require_unique_str_list(reviewed_entry_ids, "review_payload.entry_ids")
            if expected_ids != normalized_entry_ids:
                raise CompressionPipelineError("reviewed entry_ids must match the requested compression entry_ids")

        state_before = semantic_store.export_state()
        entries_by_id = {entry["entry_id"]: entry for entry in state_before.get("entries", [])}
        source_entries: list[dict[str, Any]] = []
        for entry_id in normalized_entry_ids:
            entry = entries_by_id.get(entry_id)
            if entry is None:
                raise CompressionPipelineError(f"semantic entry not found: {entry_id}")
            if entry.get("status") != "active":
                raise CompressionPipelineError(f"semantic entry must be active for compression: {entry_id}")
            source_entries.append(entry)

        self._counter += 1
        compression_id = f"phase4-compression-{self._counter:08d}"
        created_id = f"semantic-compression-{self._counter:08d}"

        semantic_store.add_entry(
            entry_id=created_id,
            concept_type=_require_non_empty_str(concept_type, "concept_type"),
            abstraction=_require_non_empty_str(summary_abstraction, "summary_abstraction"),
            provenance_refs=_merge_unique([entry.get("provenance_refs", []) for entry in source_entries]),
            review_ref=normalized_review_ref,
            source_candidate_id=_require_non_empty_str(review.get("candidate_id"), "candidate_id"),
            supporting_refs=_merge_unique(
                [entry.get("supporting_refs", []) for entry in source_entries]
                + [_require_unique_str_list(supporting_refs or [], "supporting_refs")]
            ),
            graph_refs=_merge_unique(
                [entry.get("graph_refs", []) for entry in source_entries]
                + [_require_unique_str_list(graph_refs or [], "graph_refs")]
            ),
            metadata={
                **_require_mapping(metadata or {}, "metadata"),
                "compression_id": compression_id,
                "compressed_entry_ids": list(normalized_entry_ids),
            },
        )
        for entry_id in normalized_entry_ids:
            semantic_store.mark_superseded(entry_id=entry_id, superseded_by=created_id)

        state_after = semantic_store.export_state()
        record = CompressionRecord(
            compression_id=compression_id,
            review_ref=normalized_review_ref,
            target_plane="semantic",
            source_ids=list(normalized_entry_ids),
            created_id=created_id,
            state_bytes_before=canonical_size_bytes(state_before),
            state_bytes_after=canonical_size_bytes(state_after),
            compressed_at=utc_timestamp(),
        )
        self._records.append(record)
        return {
            "compression": record.to_dict(),
            "review_candidate_id": review["candidate_id"],
            "semantic_state": state_after,
        }

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_04.compression_pipeline.v1",
            "compression_records": [record.to_dict() for record in self._records],
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_04.compression_pipeline.v1":
            raise CompressionPipelineError("compression pipeline schema mismatch")
        records = payload.get("compression_records", [])
        if not isinstance(records, list):
            raise CompressionPipelineError("compression_records must be a list")
        self._records = []
        self._counter = 0
        for record_payload in records:
            record_map = _require_mapping(record_payload, "compression_record")
            record = CompressionRecord(
                compression_id=_require_non_empty_str(record_map.get("compression_id"), "compression_id"),
                review_ref=_require_non_empty_str(record_map.get("review_ref"), "review_ref"),
                target_plane=_require_non_empty_str(record_map.get("target_plane"), "target_plane"),
                source_ids=_require_unique_str_list(record_map.get("source_ids", []), "source_ids"),
                created_id=_require_non_empty_str(record_map.get("created_id"), "created_id"),
                state_bytes_before=record_map.get("state_bytes_before"),
                state_bytes_after=record_map.get("state_bytes_after"),
                compressed_at=_require_non_empty_str(record_map.get("compressed_at"), "compressed_at"),
            )
            if not isinstance(record.state_bytes_before, int) or record.state_bytes_before <= 0:
                raise CompressionPipelineError("state_bytes_before must be a positive integer")
            if not isinstance(record.state_bytes_after, int) or record.state_bytes_after <= 0:
                raise CompressionPipelineError("state_bytes_after must be a positive integer")
            self._records.append(record)
            suffix = record.compression_id.split("-")[-1]
            if suffix.isdigit():
                self._counter = max(self._counter, int(suffix))

    def _approved_review(
        self,
        *,
        review_ref: str,
        review_queue: Any,
        expected_target_plane: str,
        expected_candidate_kind: str,
    ) -> dict[str, Any]:
        if not hasattr(review_queue, "export_state"):
            raise CompressionPipelineError("review_queue must expose export_state()")
        queue_state = _require_mapping(review_queue.export_state(), "review_queue_state")
        queue_candidates = queue_state.get("candidates", [])
        if not isinstance(queue_candidates, list):
            raise CompressionPipelineError("review_queue export must contain a candidates list")
        for item in queue_candidates:
            candidate = _require_mapping(item, "review_candidate")
            if candidate.get("review_ref") != review_ref:
                continue
            if _require_non_empty_str(candidate.get("status"), "status") != "approved":
                raise CompressionPipelineError("compression requires an approved review candidate")
            if _require_non_empty_str(candidate.get("target_plane"), "target_plane") != expected_target_plane:
                raise CompressionPipelineError("review candidate target_plane does not match compression plane")
            if _require_non_empty_str(candidate.get("candidate_kind"), "candidate_kind") != expected_candidate_kind:
                raise CompressionPipelineError("review candidate kind does not match compression action")
            return candidate
        raise CompressionPipelineError(f"review_ref not found in review queue: {review_ref}")
