from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from .episodic_memory import EpisodicMemoryStore
from .procedural_memory import ProceduralMemoryStore
from .rollback_safe_updates import RollbackSafeUpdater


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_size_bytes(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True).encode("utf-8"))


class ForgettingRetirementError(ValueError):
    """Raised when forgetting or retirement is not review-gated and explicit."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ForgettingRetirementError(f"{field_name} must be a non-empty string")
    return value


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ForgettingRetirementError(f"{field_name} must be a mapping")
    return dict(value)


def _require_unique_str_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ForgettingRetirementError(f"{field_name} must be a list")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        text = _require_non_empty_str(item, f"{field_name}[]")
        if text in seen:
            raise ForgettingRetirementError(f"{field_name} contains duplicate entries")
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
class ForgettingRecord:
    forgetting_id: str
    review_ref: str
    forgotten_event_ids: list[str]
    summary_event_id: str
    rollback_ref: str
    replay_id: str | None
    state_bytes_before: int
    state_bytes_after: int
    forgotten_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "forgetting_id": self.forgetting_id,
            "review_ref": self.review_ref,
            "forgotten_event_ids": list(self.forgotten_event_ids),
            "summary_event_id": self.summary_event_id,
            "rollback_ref": self.rollback_ref,
            "replay_id": self.replay_id,
            "state_bytes_before": self.state_bytes_before,
            "state_bytes_after": self.state_bytes_after,
            "forgotten_at": self.forgotten_at,
        }


@dataclass(frozen=True, slots=True)
class RetirementRecord:
    retirement_id: str
    review_ref: str
    target_plane: str
    target_id: str
    retirement_ref: str
    retired_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "retirement_id": self.retirement_id,
            "review_ref": self.review_ref,
            "target_plane": self.target_plane,
            "target_id": self.target_id,
            "retirement_ref": self.retirement_ref,
            "retired_at": self.retired_at,
        }


class ForgettingRetirementManager:
    """Review-gated forgetting and retirement with retained anchors and rollback-safe forgetting."""

    def __init__(self, *, updater: RollbackSafeUpdater | None = None) -> None:
        self.updater = updater or RollbackSafeUpdater()
        self._forget_counter = 0
        self._retire_counter = 0
        self._forgetting_records: list[ForgettingRecord] = []
        self._retirement_records: list[RetirementRecord] = []

    def forget_episodic_events(
        self,
        *,
        review_ref: str,
        review_queue: Any,
        episodic_store: EpisodicMemoryStore,
        event_ids: list[str],
        summary_event_id: str,
        summary: str,
        conversation_id: str,
        turn_id: str,
        provenance_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        normalized_review_ref = _require_non_empty_str(review_ref, "review_ref")
        normalized_event_ids = _require_unique_str_list(event_ids, "event_ids")
        if not normalized_event_ids:
            raise ForgettingRetirementError("forgetting requires at least one event_id")
        review = self._approved_review(
            review_ref=normalized_review_ref,
            review_queue=review_queue,
            expected_target_plane="episodic",
            expected_candidate_kind="episodic_forgetting",
        )
        payload = _require_mapping(review.get("payload", {}), "review_payload")
        reviewed_event_ids = payload.get("event_ids")
        if reviewed_event_ids is not None:
            expected_ids = _require_unique_str_list(reviewed_event_ids, "review_payload.event_ids")
            if expected_ids != normalized_event_ids:
                raise ForgettingRetirementError("reviewed event_ids must match the forgetting event_ids")

        state_before = episodic_store.export_state()
        self._forget_counter += 1
        forgetting_id = f"phase4-forgetting-{self._forget_counter:08d}"
        normalized_summary_event_id = _require_non_empty_str(summary_event_id, "summary_event_id")
        normalized_summary = _require_non_empty_str(summary, "summary")
        supplied_provenance = _require_unique_str_list(provenance_refs or [], "provenance_refs")

        def mutator(state: dict[str, Any]) -> dict[str, Any]:
            episodic_state = state["episodic"]
            events = episodic_state.get("events", [])
            if not isinstance(events, list):
                raise ForgettingRetirementError("episodic export must contain an events list")
            retained_events: list[dict[str, Any]] = []
            forgotten_events: list[dict[str, Any]] = []
            for event in events:
                event_map = _require_mapping(event, "episodic_event")
                if event_map.get("event_id") in normalized_event_ids:
                    forgotten_events.append(event_map)
                else:
                    retained_events.append(event_map)
            if len(forgotten_events) != len(normalized_event_ids):
                missing = sorted(set(normalized_event_ids) - {item["event_id"] for item in forgotten_events})
                raise ForgettingRetirementError(f"episodic events not found for forgetting: {missing}")
            summary_provenance = _merge_unique(
                [item.get("provenance_refs", []) for item in forgotten_events] + [supplied_provenance]
            )
            retained_events.append(
                {
                    "event_id": normalized_summary_event_id,
                    "conversation_id": _require_non_empty_str(conversation_id, "conversation_id"),
                    "turn_id": _require_non_empty_str(turn_id, "turn_id"),
                    "event_type": "episodic_forgetting_summary",
                    "event_summary": normalized_summary,
                    "content_refs": [f"forgotten://{item['event_id']}" for item in forgotten_events],
                    "provenance_refs": summary_provenance,
                    "created_at": utc_timestamp(),
                    "correction_markers": [],
                    "correction_status": "original",
                }
            )
            episodic_state["events"] = retained_events
            return state

        applied = self.updater.apply_batch(
            label=forgetting_id,
            conversation_id=_require_non_empty_str(conversation_id, "conversation_id"),
            turn_id=_require_non_empty_str(turn_id, "turn_id"),
            event_ids=list(normalized_event_ids),
            plane_exports={"episodic": state_before},
            mutator=mutator,
        )
        if applied.status != "applied":
            raise ForgettingRetirementError(applied.reason or "forgetting batch was rejected")

        updated_state = deepcopy(applied.updated_state)
        try:
            episodic_store.load_state(updated_state["episodic"])
        except Exception as exc:  # noqa: BLE001 - restore is the governed fallback.
            restored = self.updater.restore_batch(rollback_ref=applied.rollback_ref)
            episodic_store.load_state(deepcopy(restored.updated_state)["episodic"])
            raise ForgettingRetirementError(
                f"forgetting load failed and rollback state was restored: {exc}"
            ) from exc

        record = ForgettingRecord(
            forgetting_id=forgetting_id,
            review_ref=normalized_review_ref,
            forgotten_event_ids=list(normalized_event_ids),
            summary_event_id=normalized_summary_event_id,
            rollback_ref=applied.rollback_ref,
            replay_id=applied.replay_id,
            state_bytes_before=canonical_size_bytes(state_before),
            state_bytes_after=canonical_size_bytes(episodic_store.export_state()),
            forgotten_at=utc_timestamp(),
        )
        self._forgetting_records.append(record)
        return {
            "forgetting": record.to_dict(),
            "review_candidate_id": review["candidate_id"],
            "applied_batch": applied.to_dict(),
            "episodic_state": episodic_store.export_state(),
        }

    def retire_procedure(
        self,
        *,
        review_ref: str,
        review_queue: Any,
        procedural_store: ProceduralMemoryStore,
        procedure_id: str,
    ) -> dict[str, Any]:
        normalized_review_ref = _require_non_empty_str(review_ref, "review_ref")
        normalized_procedure_id = _require_non_empty_str(procedure_id, "procedure_id")
        review = self._approved_review(
            review_ref=normalized_review_ref,
            review_queue=review_queue,
            expected_target_plane="procedural",
            expected_candidate_kind="procedural_retirement",
        )
        payload = _require_mapping(review.get("payload", {}), "review_payload")
        payload_procedure_id = payload.get("procedure_id")
        if payload_procedure_id is not None and _require_non_empty_str(
            payload_procedure_id, "review_payload.procedure_id"
        ) != normalized_procedure_id:
            raise ForgettingRetirementError("reviewed procedure_id must match the retirement procedure_id")

        self._retire_counter += 1
        retirement_id = f"phase4-retirement-{self._retire_counter:08d}"
        retirement_ref = f"retire://phase4/{retirement_id}"
        procedural_store.retire_procedure(
            procedure_id=normalized_procedure_id,
            retirement_ref=retirement_ref,
        )
        record = RetirementRecord(
            retirement_id=retirement_id,
            review_ref=normalized_review_ref,
            target_plane="procedural",
            target_id=normalized_procedure_id,
            retirement_ref=retirement_ref,
            retired_at=utc_timestamp(),
        )
        self._retirement_records.append(record)
        return {
            "retirement": record.to_dict(),
            "review_candidate_id": review["candidate_id"],
            "procedure_state": procedural_store.procedure_state(normalized_procedure_id),
        }

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_04.forgetting_retirement.v1",
            "forgetting_records": [record.to_dict() for record in self._forgetting_records],
            "retirement_records": [record.to_dict() for record in self._retirement_records],
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        if payload.get("schema") != "agifcore.phase_04.forgetting_retirement.v1":
            raise ForgettingRetirementError("forgetting retirement schema mismatch")
        forgetting_records = payload.get("forgetting_records", [])
        retirement_records = payload.get("retirement_records", [])
        if not isinstance(forgetting_records, list) or not isinstance(retirement_records, list):
            raise ForgettingRetirementError("forgetting_records and retirement_records must be lists")
        self._forgetting_records = []
        self._retirement_records = []
        self._forget_counter = 0
        self._retire_counter = 0
        for record_payload in forgetting_records:
            record_map = _require_mapping(record_payload, "forgetting_record")
            record = ForgettingRecord(
                forgetting_id=_require_non_empty_str(record_map.get("forgetting_id"), "forgetting_id"),
                review_ref=_require_non_empty_str(record_map.get("review_ref"), "review_ref"),
                forgotten_event_ids=_require_unique_str_list(
                    record_map.get("forgotten_event_ids", []), "forgotten_event_ids"
                ),
                summary_event_id=_require_non_empty_str(record_map.get("summary_event_id"), "summary_event_id"),
                rollback_ref=_require_non_empty_str(record_map.get("rollback_ref"), "rollback_ref"),
                replay_id=record_map.get("replay_id"),
                state_bytes_before=record_map.get("state_bytes_before"),
                state_bytes_after=record_map.get("state_bytes_after"),
                forgotten_at=_require_non_empty_str(record_map.get("forgotten_at"), "forgotten_at"),
            )
            if record.replay_id is not None:
                _require_non_empty_str(record.replay_id, "replay_id")
            if not isinstance(record.state_bytes_before, int) or record.state_bytes_before <= 0:
                raise ForgettingRetirementError("state_bytes_before must be a positive integer")
            if not isinstance(record.state_bytes_after, int) or record.state_bytes_after <= 0:
                raise ForgettingRetirementError("state_bytes_after must be a positive integer")
            self._forgetting_records.append(record)
            suffix = record.forgetting_id.split("-")[-1]
            if suffix.isdigit():
                self._forget_counter = max(self._forget_counter, int(suffix))
        for record_payload in retirement_records:
            record_map = _require_mapping(record_payload, "retirement_record")
            record = RetirementRecord(
                retirement_id=_require_non_empty_str(record_map.get("retirement_id"), "retirement_id"),
                review_ref=_require_non_empty_str(record_map.get("review_ref"), "review_ref"),
                target_plane=_require_non_empty_str(record_map.get("target_plane"), "target_plane"),
                target_id=_require_non_empty_str(record_map.get("target_id"), "target_id"),
                retirement_ref=_require_non_empty_str(record_map.get("retirement_ref"), "retirement_ref"),
                retired_at=_require_non_empty_str(record_map.get("retired_at"), "retired_at"),
            )
            self._retirement_records.append(record)
            suffix = record.retirement_id.split("-")[-1]
            if suffix.isdigit():
                self._retire_counter = max(self._retire_counter, int(suffix))

    def _approved_review(
        self,
        *,
        review_ref: str,
        review_queue: Any,
        expected_target_plane: str,
        expected_candidate_kind: str,
    ) -> dict[str, Any]:
        if not hasattr(review_queue, "export_state"):
            raise ForgettingRetirementError("review_queue must expose export_state()")
        queue_state = _require_mapping(review_queue.export_state(), "review_queue_state")
        queue_candidates = queue_state.get("candidates", [])
        if not isinstance(queue_candidates, list):
            raise ForgettingRetirementError("review_queue export must contain a candidates list")
        for item in queue_candidates:
            candidate = _require_mapping(item, "review_candidate")
            if candidate.get("review_ref") != review_ref:
                continue
            if _require_non_empty_str(candidate.get("status"), "status") != "approved":
                raise ForgettingRetirementError("lifecycle action requires an approved review candidate")
            if _require_non_empty_str(candidate.get("target_plane"), "target_plane") != expected_target_plane:
                raise ForgettingRetirementError("review candidate target_plane does not match lifecycle action")
            if _require_non_empty_str(candidate.get("candidate_kind"), "candidate_kind") != expected_candidate_kind:
                raise ForgettingRetirementError("review candidate kind does not match lifecycle action")
            return candidate
        raise ForgettingRetirementError(f"review_ref not found in review queue: {review_ref}")
