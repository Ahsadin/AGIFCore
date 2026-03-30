from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from .continuity_memory import ContinuityMemoryStore
from .episodic_memory import EpisodicMemoryStore
from .rollback_safe_updates import RollbackSafeUpdater
from .semantic_memory import SemanticMemoryStore


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class CorrectionHandlingError(ValueError):
    """Raised when correction handling cannot remain explicit and rollback-safe."""


def _require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CorrectionHandlingError(f"{field_name} must be a non-empty string")
    return value


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise CorrectionHandlingError(f"{field_name} must be a mapping")
    return dict(value)


@dataclass(frozen=True, slots=True)
class CorrectionResult:
    correction_id: str
    target_plane: str
    target_id: str
    replacement_id: str
    rollback_ref: str
    replay_id: str | None
    applied_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "correction_id": self.correction_id,
            "target_plane": self.target_plane,
            "target_id": self.target_id,
            "replacement_id": self.replacement_id,
            "rollback_ref": self.rollback_ref,
            "replay_id": self.replay_id,
            "applied_at": self.applied_at,
        }


class CorrectionHandler:
    """Explicit before/after correction flow over episodic plus semantic or continuity memory."""

    def __init__(self, *, updater: RollbackSafeUpdater | None = None) -> None:
        self.updater = updater or RollbackSafeUpdater()
        self._counter = 0

    def apply_correction(
        self,
        *,
        correction_id: str,
        conversation_id: str,
        turn_id: str,
        event_id: str,
        reason: str,
        target_plane: str,
        target_id: str,
        corrected_payload: Mapping[str, Any],
        episodic_store: EpisodicMemoryStore,
        semantic_store: SemanticMemoryStore | None = None,
        continuity_store: ContinuityMemoryStore | None = None,
    ) -> dict[str, Any]:
        normalized_correction_id = _require_non_empty_str(correction_id, "correction_id")
        normalized_target_plane = _require_non_empty_str(target_plane, "target_plane")
        normalized_target_id = _require_non_empty_str(target_id, "target_id")
        payload = _require_mapping(corrected_payload, "corrected_payload")
        self._counter += 1
        replacement_id = f"{normalized_target_plane}-correction-{self._counter:08d}"

        plane_exports: dict[str, Any] = {"episodic": episodic_store.export_state()}
        if normalized_target_plane == "semantic":
            if semantic_store is None:
                raise CorrectionHandlingError("semantic_store is required for semantic correction")
            plane_exports["semantic"] = semantic_store.export_state()
        elif normalized_target_plane == "continuity":
            if continuity_store is None:
                raise CorrectionHandlingError("continuity_store is required for continuity correction")
            plane_exports["continuity"] = continuity_store.export_state()
        else:
            raise CorrectionHandlingError("target_plane must be semantic or continuity")

        def mutator(state: dict[str, Any]) -> dict[str, Any]:
            episodic_state = state["episodic"]
            events = episodic_state.get("events", [])
            matched = False
            for event in events:
                if event.get("event_id") == event_id:
                    markers = list(event.get("correction_markers", []))
                    markers.append(
                        {
                            "correction_id": normalized_correction_id,
                            "reason": _require_non_empty_str(reason, "reason"),
                            "corrected_at": utc_timestamp(),
                            "replacement_event_id": replacement_id,
                        }
                    )
                    event["correction_markers"] = markers
                    event["correction_status"] = "corrected"
                    matched = True
                    break
            if not matched:
                raise CorrectionHandlingError(f"episodic event not found: {event_id}")

            if normalized_target_plane == "semantic":
                semantic_entries = state["semantic"].get("entries", [])
                original_entry: dict[str, Any] | None = None
                for entry in semantic_entries:
                    if entry.get("entry_id") == normalized_target_id:
                        entry["status"] = "superseded"
                        entry["superseded_by"] = replacement_id
                        refs = list(entry.get("correction_refs", []))
                        if normalized_correction_id not in refs:
                            refs.append(normalized_correction_id)
                        entry["correction_refs"] = refs
                        original_entry = deepcopy(entry)
                        break
                if original_entry is None:
                    raise CorrectionHandlingError(f"semantic entry not found: {normalized_target_id}")
                semantic_entries.append(
                    {
                        **original_entry,
                        "entry_id": replacement_id,
                        "abstraction": _require_non_empty_str(
                            payload.get("abstraction") or payload.get("summary"),
                            "abstraction",
                        ),
                        "status": "active",
                        "superseded_by": None,
                        "correction_refs": [normalized_correction_id],
                        "created_at": utc_timestamp(),
                        "updated_at": utc_timestamp(),
                    }
                )
            else:
                continuity_anchors = state["continuity"].get("anchors", [])
                original_anchor: dict[str, Any] | None = None
                for anchor in continuity_anchors:
                    if anchor.get("anchor_id") == normalized_target_id:
                        anchor["status"] = "superseded"
                        anchor["superseded_by"] = replacement_id
                        refs = list(anchor.get("correction_refs", []))
                        if normalized_correction_id not in refs:
                            refs.append(normalized_correction_id)
                        anchor["correction_refs"] = refs
                        original_anchor = deepcopy(anchor)
                        break
                if original_anchor is None:
                    raise CorrectionHandlingError(f"continuity anchor not found: {normalized_target_id}")
                continuity_anchors.append(
                    {
                        **original_anchor,
                        "anchor_id": replacement_id,
                        "statement": _require_non_empty_str(
                            payload.get("statement") or payload.get("summary"),
                            "statement",
                        ),
                        "status": "active",
                        "superseded_by": None,
                        "correction_refs": [normalized_correction_id],
                        "created_at": utc_timestamp(),
                        "updated_at": utc_timestamp(),
                    }
                )
            return state

        applied = self.updater.apply_batch(
            label=f"phase4-correction-{normalized_correction_id}",
            conversation_id=_require_non_empty_str(conversation_id, "conversation_id"),
            turn_id=_require_non_empty_str(turn_id, "turn_id"),
            event_ids=[_require_non_empty_str(event_id, "event_id")],
            plane_exports=plane_exports,
            mutator=mutator,
        )
        if applied.status != "applied":
            raise CorrectionHandlingError(applied.reason or "correction batch was rejected")

        episodic_store.add_correction_marker(
            event_id=event_id,
            correction_id=normalized_correction_id,
            reason=_require_non_empty_str(reason, "reason"),
            replacement_event_id=replacement_id,
        )
        if normalized_target_plane == "semantic":
            assert semantic_store is not None
            original = semantic_store.entry_state(normalized_target_id)
            semantic_store.mark_superseded(
                entry_id=normalized_target_id,
                superseded_by=replacement_id,
                correction_ref=normalized_correction_id,
            )
            semantic_store.add_entry(
                entry_id=replacement_id,
                concept_type=original["concept_type"],
                abstraction=_require_non_empty_str(
                    payload.get("abstraction") or payload.get("summary"),
                    "abstraction",
                ),
                provenance_refs=list(original["provenance_refs"]),
                review_ref=original["review_ref"],
                source_candidate_id=original["source_candidate_id"],
                supporting_refs=list(original["supporting_refs"]),
                graph_refs=list(original["graph_refs"]),
                metadata={"correction_id": normalized_correction_id},
            )
        else:
            assert continuity_store is not None
            continuity_store.mark_superseded(
                anchor_id=normalized_target_id,
                superseded_by=replacement_id,
                correction_ref=normalized_correction_id,
            )
            continuity_store.record_anchor(
                anchor_id=replacement_id,
                subject=_require_non_empty_str(payload.get("subject") or "self", "subject"),
                continuity_kind=_require_non_empty_str(
                    payload.get("continuity_kind") or "self_history",
                    "continuity_kind",
                ),
                statement=_require_non_empty_str(
                    payload.get("statement") or payload.get("summary"),
                    "statement",
                ),
                provenance_refs=[normalized_target_id, event_id],
                metadata={"correction_id": normalized_correction_id},
            )

        result = CorrectionResult(
            correction_id=normalized_correction_id,
            target_plane=normalized_target_plane,
            target_id=normalized_target_id,
            replacement_id=replacement_id,
            rollback_ref=applied.rollback_ref,
            replay_id=applied.replay_id,
            applied_at=utc_timestamp(),
        )
        return {
            "correction": result.to_dict(),
            "applied_batch": applied.to_dict(),
            "episodic_state": episodic_store.export_state(),
            "target_state": (
                semantic_store.export_state()
                if normalized_target_plane == "semantic"
                else continuity_store.export_state()
            ),
        }
