from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    CuriosityGapRecord,
    CuriosityGapSelectionSnapshot,
    GapKind,
    MAX_CURIOSITY_GAP_SELECTION_ITEMS,
    bounded_unique,
    infer_phase12_scenario,
    make_trace_ref,
    require_non_empty_str,
    require_phase11_cycle,
    require_schema,
    stable_hash_payload,
)


class CuriosityGapSelectionEngine:
    SCHEMA = "agifcore.phase_12.curiosity_gap_selection.v1"

    def build_snapshot(
        self,
        *,
        self_model_feedback_state: Mapping[str, Any],
        reflection_control_state: Mapping[str, Any],
        phase11_cycle_state: Mapping[str, Any],
    ) -> CuriosityGapSelectionSnapshot:
        feedback = require_schema(
            self_model_feedback_state,
            "agifcore.phase_12.self_model_feedback.v1",
            "self_model_feedback_state",
        )
        require_schema(
            reflection_control_state,
            "agifcore.phase_12.reflection_control.v1",
            "reflection_control_state",
        )
        cycle = require_phase11_cycle(phase11_cycle_state, "phase11_cycle_state")
        overlay = cycle["overlay_contract"]
        conversation_id = require_non_empty_str(feedback.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(feedback.get("turn_id"), "turn_id")
        scenario = infer_phase12_scenario(cycle)
        phase11_refs = bounded_unique(
            [
                *list(overlay.get("read_only_phase10_refs", ())),
                *list(overlay.get("evidence_refs", ())),
                *list(overlay.get("monitoring_refs", ())),
                *list(overlay.get("inquiry_refs", ())),
            ],
            ceiling=8,
            field_name="curiosity_gap_selection.supporting_refs",
        )
        gaps: list[CuriosityGapRecord] = []

        def add_gap(
            *,
            gap_kind: GapKind,
            ranked_priority: int,
            chosen_target_lane: str,
            why_selected: str,
            deferred_alternatives: tuple[str, ...],
            stop_condition: str,
            supporting_refs: tuple[str, ...],
        ) -> None:
            payload = {
                "gap_kind": gap_kind.value,
                "ranked_priority": ranked_priority,
                "chosen_target_lane": chosen_target_lane,
                "why_selected": why_selected,
                "deferred_alternatives": list(deferred_alternatives),
                "stop_condition": stop_condition,
                "supporting_refs": list(supporting_refs),
            }
            gaps.append(
                CuriosityGapRecord(
                    gap_id=make_trace_ref("phase12_gap", payload),
                    gap_kind=gap_kind,
                    ranked_priority=ranked_priority,
                    chosen_target_lane=chosen_target_lane,
                    why_selected=why_selected,
                    deferred_alternatives=deferred_alternatives,
                    stop_condition=stop_condition,
                    supporting_refs=supporting_refs,
                    gap_hash=stable_hash_payload(payload),
                )
            )

        if scenario == "weak":
            add_gap(
                gap_kind=GapKind.PROCEDURE_GAP,
                ranked_priority=1,
                chosen_target_lane="procedure_tool_invention",
                why_selected="The highest-yield local improvement is a bounded review protocol for local evidence freshness.",
                deferred_alternatives=("domain_genesis", "self_reorganization"),
                stop_condition="stop after one candidate review protocol",
                supporting_refs=phase11_refs[:4],
            )
            add_gap(
                gap_kind=GapKind.THEORY_GAP,
                ranked_priority=2,
                chosen_target_lane="theory_formation",
                why_selected="The second gap is structural explanation quality, not new domain creation.",
                deferred_alternatives=("self_reorganization",),
                stop_condition="stop after one weak-support theory candidate",
                supporting_refs=phase11_refs[:5],
            )
        else:
            add_gap(
                gap_kind=GapKind.STRUCTURAL_GAP,
                ranked_priority=1,
                chosen_target_lane="self_reorganization",
                why_selected="The adopted-improvement and monitoring chain point to one congested structural review lane.",
                deferred_alternatives=("procedure_tool_invention",),
                stop_condition="stop after one bounded structural candidate",
                supporting_refs=phase11_refs[:5],
            )
            add_gap(
                gap_kind=GapKind.DOMAIN_GAP,
                ranked_priority=2,
                chosen_target_lane="domain_genesis",
                why_selected="The contradiction pattern suggests one missing boundary candidate between broad reasoning and local condition handling.",
                deferred_alternatives=("self_reorganization", "procedure_tool_invention"),
                stop_condition="stop after one bounded domain candidate",
                supporting_refs=phase11_refs[:6],
            )

        bounded_gaps = tuple(gaps[:MAX_CURIOSITY_GAP_SELECTION_ITEMS])
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "gap_ids": [item.gap_id for item in bounded_gaps],
        }
        return CuriosityGapSelectionSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            gap_count=len(bounded_gaps),
            gaps=bounded_gaps,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
