from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_SELF_MODEL_FEEDBACK_ITEMS,
    MAX_SUPPORTING_REFS,
    SelfModelFeedbackItem,
    SelfModelFeedbackSnapshot,
    bounded_unique,
    infer_phase12_scenario,
    make_trace_ref,
    optional_bounded_unique,
    require_non_empty_str,
    require_phase11_cycle,
    stable_hash_payload,
)


class SelfModelFeedbackEngine:
    SCHEMA = "agifcore.phase_12.self_model_feedback.v1"

    def build_snapshot(self, *, phase11_cycle_state: Mapping[str, Any]) -> SelfModelFeedbackSnapshot:
        cycle = require_phase11_cycle(phase11_cycle_state, "phase11_cycle_state")
        overlay = cycle["overlay_contract"]
        conversation_id = require_non_empty_str(cycle.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(cycle.get("turn_id"), "turn_id")
        scenario = infer_phase12_scenario(cycle)
        supporting_refs = bounded_unique(
            [
                *list(overlay.get("read_only_phase10_refs", ())),
                *list(overlay.get("evidence_refs", ())),
                *list(overlay.get("monitoring_refs", ())),
                *list(overlay.get("rollback_refs", ())),
                *list(overlay.get("inquiry_refs", ())),
            ],
            ceiling=MAX_SUPPORTING_REFS,
            field_name="self_model_feedback.supporting_refs",
        )
        items: list[SelfModelFeedbackItem] = []

        def add_item(*, pressure_kind: str, problem_statement: str, recommended_lane: str, bounded_next_step: str, refs: tuple[str, ...]) -> None:
            payload = {
                "pressure_kind": pressure_kind,
                "problem_statement": problem_statement,
                "recommended_lane": recommended_lane,
                "bounded_next_step": bounded_next_step,
                "supporting_refs": list(refs),
            }
            item = SelfModelFeedbackItem(
                feedback_id=make_trace_ref("phase12_self_model_feedback", payload),
                pressure_kind=pressure_kind,
                problem_statement=problem_statement,
                recommended_lane=recommended_lane,
                bounded_next_step=bounded_next_step,
                supporting_refs=refs,
                feedback_hash=stable_hash_payload(payload),
            )
            items.append(item)

        if scenario == "weak":
            add_item(
                pressure_kind="support_gap_repeats",
                problem_statement="Repeated weak-support turns show that the current structure does not isolate local-evidence refresh from explanation drafting cleanly enough.",
                recommended_lane="procedure_tool_invention",
                bounded_next_step="Propose one reusable review protocol that checks local evidence freshness before explanation reuse.",
                refs=supporting_refs[:4],
            )
            add_item(
                pressure_kind="theory_boundary_thin",
                problem_statement="The current theory-fragment surface captures weak explanations, but the structural reason why those weak explanations recur is still under-specified.",
                recommended_lane="theory_formation",
                bounded_next_step="Form one bounded theory candidate that explains when missing local evidence should block stronger reuse.",
                refs=supporting_refs[:5],
            )
            add_item(
                pressure_kind="bounded_inquiry_queue_pressure",
                problem_statement="Bounded inquiry is active, but the selector still needs a clearer rule for when evidence gaps should trigger structural review instead of another answer attempt.",
                recommended_lane="curiosity_gap_selection",
                bounded_next_step="Select at most two structural blind spots and defer all others explicitly.",
                refs=supporting_refs[:6],
            )
        else:
            add_item(
                pressure_kind="contradiction_sensitive_theory_gap",
                problem_statement="Contradiction handling now produces improvement records, but the structural theory behind those improvements remains fragmented.",
                recommended_lane="theory_formation",
                bounded_next_step="Refine one contradiction-sensitive theory candidate directly from the approved Phase 11 evidence chain.",
                refs=supporting_refs[:5],
            )
            add_item(
                pressure_kind="review_lane_congestion",
                problem_statement="Adopted improvements and monitoring refs show that the current review lane is doing too much structural coordination in one place.",
                recommended_lane="self_reorganization",
                bounded_next_step="Propose one bounded route-shape change with explicit before, after, rejected alternative, and rollback target refs.",
                refs=supporting_refs[:6],
            )
            add_item(
                pressure_kind="domain_boundary_pressure",
                problem_statement="The contradiction pattern suggests a missing boundary between broad domain reasoning and local infrastructure-like conditions.",
                recommended_lane="domain_genesis",
                bounded_next_step="Propose one bounded domain candidate without widening the proof-domain set or mutating the existing domain map.",
                refs=supporting_refs[:6],
            )
            add_item(
                pressure_kind="procedure_reuse_gap",
                problem_statement="The improvement chain solved the immediate contradiction, but the reusable procedure for repeating that repair is still implicit.",
                recommended_lane="procedure_tool_invention",
                bounded_next_step="Propose one candidate review protocol anchored to the skill graph and explicitly non-auto-executing.",
                refs=supporting_refs[:4],
            )

        trimmed_items = tuple(items[:MAX_SELF_MODEL_FEEDBACK_ITEMS])
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "item_ids": [item.feedback_id for item in trimmed_items],
        }
        return SelfModelFeedbackSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            item_count=len(trimmed_items),
            items=trimmed_items,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
