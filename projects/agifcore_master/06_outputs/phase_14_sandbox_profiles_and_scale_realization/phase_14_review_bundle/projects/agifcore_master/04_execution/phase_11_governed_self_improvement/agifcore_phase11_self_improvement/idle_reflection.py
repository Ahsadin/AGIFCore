from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_IDLE_REFLECTION_ITEMS,
    IdleReflectionSnapshot,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)


class IdleReflectionEngine:
    SCHEMA = "agifcore.phase_11.idle_reflection.v1"

    def build_snapshot(self, *, offline_reflection_and_consolidation_state: Mapping[str, Any]) -> IdleReflectionSnapshot:
        reflection = require_schema(
            offline_reflection_and_consolidation_state,
            "agifcore.phase_11.offline_reflection_and_consolidation.v1",
            "offline_reflection_and_consolidation_state",
        )
        conversation_id = require_non_empty_str(reflection.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(reflection.get("turn_id"), "turn_id")
        item_ids = [str(item.get("item_id", "")).strip() for item in list(reflection.get("items", ())) if isinstance(item, Mapping)]
        processed = tuple(item_id for item_id in item_ids[:MAX_IDLE_REFLECTION_ITEMS] if item_id)
        deferred = tuple(item_id for item_id in item_ids[MAX_IDLE_REFLECTION_ITEMS:] if item_id)
        ran = bool(processed)
        stop_reason = "bounded_idle_cycle_complete" if ran else "no_pending_reflection_items"
        if deferred:
            stop_reason = "idle_reflection_budget_reached"
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "processed": list(processed),
            "deferred": list(deferred),
            "ran": ran,
            "stop_reason": stop_reason,
        }
        return IdleReflectionSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            ran=ran,
            processed_item_ids=processed,
            deferred_item_ids=deferred,
            stop_reason=stop_reason,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
