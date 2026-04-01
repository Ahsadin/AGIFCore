from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_REFLECTION_CONTROL_ACTIONS,
    ReflectionControlAction,
    ReflectionControlSnapshot,
    ReflectionDecision,
    infer_phase12_scenario,
    make_trace_ref,
    require_non_empty_str,
    require_phase11_cycle,
    require_schema,
    stable_hash_payload,
)


class ReflectionControlEngine:
    SCHEMA = "agifcore.phase_12.reflection_control.v1"

    def build_snapshot(
        self,
        *,
        self_model_feedback_state: Mapping[str, Any],
        phase11_cycle_state: Mapping[str, Any],
    ) -> ReflectionControlSnapshot:
        feedback = require_schema(
            self_model_feedback_state,
            "agifcore.phase_12.self_model_feedback.v1",
            "self_model_feedback_state",
        )
        cycle = require_phase11_cycle(phase11_cycle_state, "phase11_cycle_state")
        conversation_id = require_non_empty_str(feedback.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(feedback.get("turn_id"), "turn_id")
        scenario = infer_phase12_scenario(cycle)
        feedback_items = [item for item in list(feedback.get("items", ())) if isinstance(item, Mapping)]
        actions: list[ReflectionControlAction] = []

        def add_action(*, target_lane: str, decision: ReflectionDecision, reason: str, supporting_feedback_ids: tuple[str, ...], stop_reason: str) -> None:
            payload = {
                "target_lane": target_lane,
                "decision": decision.value,
                "reason": reason,
                "supporting_feedback_ids": list(supporting_feedback_ids),
                "stop_reason": stop_reason,
            }
            actions.append(
                ReflectionControlAction(
                    action_id=make_trace_ref("phase12_reflection_control", payload),
                    target_lane=target_lane,
                    decision=decision,
                    reason=reason,
                    supporting_feedback_ids=supporting_feedback_ids,
                    stop_reason=stop_reason,
                    action_hash=stable_hash_payload(payload),
                )
            )

        if scenario == "weak":
            add_action(
                target_lane="theory_formation",
                decision=ReflectionDecision.ADVANCE,
                reason="Weak-support repetition is strong enough to justify one bounded theory candidate.",
                supporting_feedback_ids=tuple(item.get("feedback_id", "") for item in feedback_items[:1]),
                stop_reason="stop after at most one weak-support theory candidate",
            )
            add_action(
                target_lane="procedure_tool_invention",
                decision=ReflectionDecision.ADVANCE,
                reason="A reusable review protocol is safer than widening structural mutation when support is still thin.",
                supporting_feedback_ids=tuple(item.get("feedback_id", "") for item in feedback_items[1:2] or feedback_items[:1]),
                stop_reason="stop after one candidate procedure or tool policy",
            )
            add_action(
                target_lane="self_reorganization",
                decision=ReflectionDecision.HOLD,
                reason="Structural mutation stays held until contradiction pressure is stronger than weak-support pressure.",
                supporting_feedback_ids=tuple(item.get("feedback_id", "") for item in feedback_items[:1]),
                stop_reason="hold route changes this cycle",
            )
        else:
            add_action(
                target_lane="theory_formation",
                decision=ReflectionDecision.ADVANCE,
                reason="Contradiction-linked evidence is strong enough to refine theory candidates now.",
                supporting_feedback_ids=tuple(item.get("feedback_id", "") for item in feedback_items[:1]),
                stop_reason="stop after at most two theory candidates",
            )
            add_action(
                target_lane="self_reorganization",
                decision=ReflectionDecision.ADVANCE,
                reason="The adopted-improvement chain provides enough support to model one bounded structural candidate.",
                supporting_feedback_ids=tuple(item.get("feedback_id", "") for item in feedback_items[1:2] or feedback_items[:1]),
                stop_reason="stop after one reorganization candidate",
            )
            add_action(
                target_lane="domain_genesis",
                decision=ReflectionDecision.HOLD,
                reason="Domain genesis stays candidate-bound and may not widen the domain surface until the theory path is visible.",
                supporting_feedback_ids=tuple(item.get("feedback_id", "") for item in feedback_items[2:3] or feedback_items[:1]),
                stop_reason="hold domain adoption and keep one candidate only",
            )

        bounded_actions = tuple(actions[:MAX_REFLECTION_CONTROL_ACTIONS])
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "action_ids": [item.action_id for item in bounded_actions],
        }
        return ReflectionControlSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            action_count=len(bounded_actions),
            actions=bounded_actions,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
