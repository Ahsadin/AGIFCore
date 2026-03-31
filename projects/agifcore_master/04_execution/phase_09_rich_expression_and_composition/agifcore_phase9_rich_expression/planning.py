from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_LANE_NOTES,
    MAX_PLANNING_STEPS,
    MAX_TRACE_REFS,
    Phase9RichExpressionError,
    PlanningSnapshot,
    PlanningStep,
    coerce_bool,
    make_trace_ref,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)


def _clean_items(values: list[str], *, ceiling: int) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in values:
        cleaned = " ".join(str(raw).split()).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
        if len(result) >= ceiling:
            break
    return tuple(result)


def _step(
    *,
    step_index: int,
    action: str,
    dependency_refs: tuple[str, ...],
    verification_hint: str,
    caution_note: str | None,
    supporting_refs: tuple[str, ...],
    stop_if_unsure: bool,
) -> PlanningStep:
    payload = {
        "step_index": step_index,
        "action": action,
        "dependency_refs": list(dependency_refs),
        "verification_hint": verification_hint,
        "caution_note": caution_note,
        "supporting_refs": list(supporting_refs),
        "stop_if_unsure": stop_if_unsure,
    }
    step_hash = stable_hash_payload(payload)
    return PlanningStep(
        step_id=make_trace_ref("planning_step", payload),
        step_index=step_index,
        action=action,
        dependency_refs=dependency_refs,
        verification_hint=verification_hint,
        caution_note=caution_note,
        supporting_refs=supporting_refs,
        stop_if_unsure=stop_if_unsure,
        step_hash=step_hash,
    )


class PlanningEngine:
    """Build a bounded user-facing step plan without execution orchestration."""

    SCHEMA = "agifcore.phase_09.planning.v1"

    def build_snapshot(
        self,
        *,
        support_state_resolution_state: Mapping[str, Any],
        bounded_current_world_reasoning_state: Mapping[str, Any],
        visible_reasoning_summary_state: Mapping[str, Any],
        science_reflection_state: Mapping[str, Any],
    ) -> PlanningSnapshot:
        support = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )
        bounded = require_schema(
            bounded_current_world_reasoning_state,
            "agifcore.phase_08.bounded_current_world_reasoning.v1",
            "bounded_current_world_reasoning_state",
        )
        summary = require_schema(
            visible_reasoning_summary_state,
            "agifcore.phase_08.visible_reasoning_summaries.v1",
            "visible_reasoning_summary_state",
        )
        reflection = require_schema(
            science_reflection_state,
            "agifcore.phase_08.science_reflection.v1",
            "science_reflection_state",
        )

        request_id = require_non_empty_str(str(summary.get("request_id", "")).strip(), "request_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        decision = str(bounded.get("decision", "not_current_world_request")).strip() or "not_current_world_request"
        live_measurement_required = coerce_bool(bounded.get("live_measurement_required"))

        verify_items = [str(item).strip() for item in list(summary.get("what_would_verify", ())) if str(item).strip()]
        uncertainty = [str(item).strip() for item in list(summary.get("uncertainty", ())) if str(item).strip()]
        records = [item for item in list(reflection.get("records", ())) if isinstance(item, Mapping)]
        evidence_refs = _clean_items(
            [str(item).strip() for item in list(summary.get("evidence_refs", ())) if str(item).strip()],
            ceiling=MAX_TRACE_REFS,
        )

        steps: list[PlanningStep] = []
        step_index = 1
        for verify_text in verify_items:
            if len(steps) >= MAX_PLANNING_STEPS:
                break
            steps.append(
                _step(
                    step_index=step_index,
                    action=verify_text,
                    dependency_refs=evidence_refs[:2],
                    verification_hint="Confirm this step preserves the declared support-state boundary.",
                    caution_note="Do not treat this as executed automatically.",
                    supporting_refs=evidence_refs[:3],
                    stop_if_unsure=True,
                )
            )
            step_index += 1

        for item in records:
            if len(steps) >= MAX_PLANNING_STEPS:
                break
            next_step = str(item.get("next_verification_step", "")).strip()
            if not next_step:
                continue
            note = str(item.get("note", "")).strip() or "reflection-driven verification adjustment"
            source_ref = str(item.get("source_ref", "")).strip() or request_id
            steps.append(
                _step(
                    step_index=step_index,
                    action=next_step,
                    dependency_refs=(source_ref,),
                    verification_hint=f"Reflection note: {note}",
                    caution_note=None,
                    supporting_refs=(source_ref,),
                    stop_if_unsure=True,
                )
            )
            step_index += 1

        if not steps:
            fallback_action = "Preserve current bounded output and request additional evidence before stronger claims."
            steps.append(
                _step(
                    step_index=1,
                    action=fallback_action,
                    dependency_refs=evidence_refs[:1] or (request_id,),
                    verification_hint="Confirm that support-state honesty remains unchanged.",
                    caution_note="No executable task is produced by this lane.",
                    supporting_refs=evidence_refs[:2],
                    stop_if_unsure=True,
                )
            )

        if live_measurement_required and len(steps) < MAX_PLANNING_STEPS:
            steps.append(
                _step(
                    step_index=len(steps) + 1,
                    action="Obtain a fresh live measurement before asserting current status.",
                    dependency_refs=evidence_refs[:1] or (request_id,),
                    verification_hint=f"bounded_current_world_decision={decision}",
                    caution_note="Fail closed if fresh measurement cannot be obtained.",
                    supporting_refs=evidence_refs[:2],
                    stop_if_unsure=True,
                )
            )

        steps = steps[:MAX_PLANNING_STEPS]
        lane_notes = _clean_items(
            [
                f"support_state={support_state}",
                f"current_world_decision={decision}",
                f"uncertainty_items={len(uncertainty)}",
                "Planning lane outputs bounded steps only; it does not execute actions.",
            ],
            ceiling=MAX_LANE_NOTES,
        )

        payload = {
            "schema": self.SCHEMA,
            "turn_id": request_id,
            "step_count": len(steps),
            "steps": [step.to_dict() for step in steps],
            "lane_notes": list(lane_notes),
        }
        if len(steps) > MAX_PLANNING_STEPS:
            raise Phase9RichExpressionError("planning step count exceeds Phase 9 ceiling")

        return PlanningSnapshot(
            schema=self.SCHEMA,
            turn_id=request_id,
            step_count=len(steps),
            steps=tuple(steps),
            lane_notes=lane_notes,
            snapshot_hash=stable_hash_payload(payload),
        )
