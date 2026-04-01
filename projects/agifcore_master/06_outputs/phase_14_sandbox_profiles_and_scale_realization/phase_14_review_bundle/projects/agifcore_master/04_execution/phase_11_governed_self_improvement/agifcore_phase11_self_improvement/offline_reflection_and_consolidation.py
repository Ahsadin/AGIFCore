from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_IDLE_REFLECTION_ITEMS,
    MAX_OFFLINE_REFLECTION_ITEMS,
    MAX_SUPPORTING_REFS,
    OfflineReflectionAndConsolidationSnapshot,
    OfflineReflectionItem,
    make_trace_ref,
    optional_bounded_unique,
    require_mapping,
    require_non_empty_str,
    require_phase10_turn_state,
    stable_hash_payload,
)


class OfflineReflectionAndConsolidationEngine:
    SCHEMA = "agifcore.phase_11.offline_reflection_and_consolidation.v1"

    def build_snapshot(self, *, phase10_turn_state: Mapping[str, Any]) -> OfflineReflectionAndConsolidationSnapshot:
        turn = require_phase10_turn_state(phase10_turn_state, "phase10_turn_state")
        conversation_id = require_non_empty_str(turn.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(turn.get("turn_id"), "turn_id")
        diagnosis = require_mapping(turn.get("weak_answer_diagnosis"), "phase10_turn_state.weak_answer_diagnosis")
        observer = require_mapping(turn.get("meta_cognition_observer"), "phase10_turn_state.meta_cognition_observer")
        strategy = require_mapping(turn.get("strategy_journal"), "phase10_turn_state.strategy_journal")
        theory_fragments = require_mapping(turn.get("theory_fragments"), "phase10_turn_state.theory_fragments")

        items: list[OfflineReflectionItem] = []
        deferred_items: list[str] = []

        for raw_item in list(diagnosis.get("items", ())):
            if not isinstance(raw_item, Mapping):
                continue
            if len(items) >= MAX_OFFLINE_REFLECTION_ITEMS:
                deferred_items.append(str(raw_item.get("diagnosis_id", "")).strip())
                continue
            problem_statement = " ".join(str(raw_item.get("why_weak", "")).split()).strip()
            bounded_next_step = " ".join(str(raw_item.get("next_step", "")).split()).strip() or "keep the next step bounded and evidence-linked"
            source_kind = " ".join(str(raw_item.get("kind", "weak_signal")).split()).strip() or "weak_signal"
            source_ref = (
                optional_bounded_unique(list(raw_item.get("supporting_refs", ())), ceiling=1)[0]
                if optional_bounded_unique(list(raw_item.get("supporting_refs", ())), ceiling=1)
                else str(raw_item.get("diagnosis_id", "")).strip()
            )
            supporting_refs = optional_bounded_unique(
                [
                    *list(raw_item.get("supporting_refs", ())),
                    str(raw_item.get("diagnosis_id", "")).strip(),
                ],
                ceiling=MAX_SUPPORTING_REFS,
            )
            payload = {
                "conversation_id": conversation_id,
                "turn_id": turn_id,
                "source_kind": source_kind,
                "problem_statement": problem_statement,
                "bounded_next_step": bounded_next_step,
                "supporting_refs": list(supporting_refs),
            }
            items.append(
                OfflineReflectionItem(
                    item_id=make_trace_ref("offline_reflection_item", payload),
                    source_kind=source_kind,
                    source_ref=source_ref,
                    problem_statement=problem_statement,
                    proposed_focus=bounded_next_step,
                    bounded_next_step=bounded_next_step,
                    supporting_refs=supporting_refs,
                    item_hash=stable_hash_payload(payload),
                )
            )

        for missing_need in list(observer.get("missing_needs", ())):
            cleaned = " ".join(str(missing_need).split()).strip()
            if not cleaned:
                continue
            if len(items) >= MAX_OFFLINE_REFLECTION_ITEMS:
                deferred_items.append(cleaned)
                continue
            payload = {
                "conversation_id": conversation_id,
                "turn_id": turn_id,
                "source_kind": "missing_need",
                "problem_statement": cleaned,
                "bounded_next_step": cleaned,
            }
            items.append(
                OfflineReflectionItem(
                    item_id=make_trace_ref("offline_reflection_item", payload),
                    source_kind="missing_need",
                    source_ref=make_trace_ref("phase10_missing_need", payload),
                    problem_statement=cleaned,
                    proposed_focus=cleaned,
                    bounded_next_step=cleaned,
                    supporting_refs=optional_bounded_unique([cleaned], ceiling=1),
                    item_hash=stable_hash_payload(payload),
                )
            )

        for fragment in list(theory_fragments.get("fragments", ())):
            if not isinstance(fragment, Mapping):
                continue
            if len(items) >= MAX_OFFLINE_REFLECTION_ITEMS:
                deferred_items.append(str(fragment.get("fragment_id", "")).strip())
                continue
            problem_statement = " ".join(str(fragment.get("fragment_statement", "")).split()).strip()
            next_step = " ".join(str(fragment.get("next_verification_step", "")).split()).strip() or "re-check support before using the fragment"
            payload = {
                "conversation_id": conversation_id,
                "turn_id": turn_id,
                "source_kind": "theory_fragment",
                "problem_statement": problem_statement,
                "bounded_next_step": next_step,
            }
            items.append(
                OfflineReflectionItem(
                    item_id=make_trace_ref("offline_reflection_item", payload),
                    source_kind="theory_fragment",
                    source_ref=str(fragment.get("fragment_id", "")).strip() or make_trace_ref("phase10_fragment", payload),
                    problem_statement=problem_statement,
                    proposed_focus=next_step,
                    bounded_next_step=next_step,
                    supporting_refs=optional_bounded_unique(
                        [
                            str(fragment.get("fragment_id", "")).strip(),
                            str(fragment.get("falsifier", "")).strip(),
                        ],
                        ceiling=MAX_SUPPORTING_REFS,
                    ),
                    item_hash=stable_hash_payload(payload),
                )
            )

        consolidated_focuses = optional_bounded_unique(
            [
                *(item.proposed_focus for item in items),
                *[str(entry.get("monitoring_note", "")).strip() for entry in list(strategy.get("entries", ())) if isinstance(entry, Mapping)],
            ],
            ceiling=MAX_IDLE_REFLECTION_ITEMS,
        )
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "item_ids": [item.item_id for item in items],
            "consolidated_focuses": list(consolidated_focuses),
            "deferred_items": deferred_items,
        }
        return OfflineReflectionAndConsolidationSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            item_count=len(items),
            items=tuple(items),
            consolidated_focuses=consolidated_focuses,
            deferred_items=tuple(deferred_items),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
