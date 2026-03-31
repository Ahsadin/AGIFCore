from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_COMPARISON_AXES,
    MAX_LANE_NOTES,
    MAX_TRACE_REFS,
    ComparisonAxis,
    ComparisonSnapshot,
    Phase9RichExpressionError,
    clamp_score,
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


def _axis(
    *,
    axis_label: str,
    left_value: str,
    right_value: str,
    asymmetry_note: str,
    supporting_refs: tuple[str, ...],
    confidence: float,
) -> ComparisonAxis:
    payload = {
        "axis_label": axis_label,
        "left_value": left_value,
        "right_value": right_value,
        "asymmetry_note": asymmetry_note,
        "supporting_refs": list(supporting_refs),
        "confidence": clamp_score(confidence),
    }
    axis_hash = stable_hash_payload(payload)
    return ComparisonAxis(
        axis_id=make_trace_ref("comparison_axis", payload),
        axis_label=axis_label,
        left_value=left_value,
        right_value=right_value,
        asymmetry_note=asymmetry_note,
        supporting_refs=supporting_refs,
        confidence=clamp_score(confidence),
        axis_hash=axis_hash,
    )


class ComparisonEngine:
    """Build bounded, axis-based comparisons from read-only Phase 7/8 state."""

    SCHEMA = "agifcore.phase_09.comparison.v1"

    def build_snapshot(
        self,
        *,
        question_interpretation_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        entity_request_inference_state: Mapping[str, Any],
        visible_reasoning_summary_state: Mapping[str, Any],
    ) -> ComparisonSnapshot:
        interpretation = require_schema(
            question_interpretation_state,
            "agifcore.phase_07.question_interpretation.v1",
            "question_interpretation_state",
        )
        support = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )
        inference = require_schema(
            entity_request_inference_state,
            "agifcore.phase_08.entity_request_inference.v1",
            "entity_request_inference_state",
        )
        summary = require_schema(
            visible_reasoning_summary_state,
            "agifcore.phase_08.visible_reasoning_summaries.v1",
            "visible_reasoning_summary_state",
        )

        turn_id = require_non_empty_str(str(interpretation.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        knowledge_gap = str(support.get("knowledge_gap_reason", "none")).strip() or "none"
        uncertainty_band = str(summary.get("uncertainty_band", "unknown")).strip() or "unknown"

        candidate_labels = []
        for candidate in list(inference.get("candidates", ())):
            if isinstance(candidate, Mapping):
                label = str(candidate.get("entity_label", "")).strip()
                if label:
                    candidate_labels.append(label)
        left_label = candidate_labels[0] if candidate_labels else "primary_entity"
        right_label = candidate_labels[1] if len(candidate_labels) > 1 else "context_entity"

        known = [str(item).strip() for item in list(summary.get("what_is_known", ())) if str(item).strip()]
        inferred = [str(item).strip() for item in list(summary.get("what_is_inferred", ())) if str(item).strip()]
        uncertainty = [str(item).strip() for item in list(summary.get("uncertainty", ())) if str(item).strip()]
        evidence_refs = _clean_items(
            [str(item).strip() for item in list(summary.get("evidence_refs", ())) if str(item).strip()],
            ceiling=MAX_TRACE_REFS,
        )

        axes: list[ComparisonAxis] = []
        axes.append(
            _axis(
                axis_label="Support State",
                left_value=f"{left_label}: {support_state}",
                right_value=f"{right_label}: {support_state}",
                asymmetry_note=f"Both sides inherit the same support-state honesty boundary ({support_state}).",
                supporting_refs=evidence_refs[:3],
                confidence=0.82 if support_state in {"grounded", "inferred"} else 0.5,
            )
        )
        axes.append(
            _axis(
                axis_label="Known vs Inferred Coverage",
                left_value=f"known={len(known)}",
                right_value=f"inferred={len(inferred)}",
                asymmetry_note="Known anchors and inferred claims should never be merged into one certainty bucket.",
                supporting_refs=evidence_refs[:4],
                confidence=0.84,
            )
        )
        axes.append(
            _axis(
                axis_label="Uncertainty Exposure",
                left_value=f"uncertainty_band={uncertainty_band}",
                right_value=f"uncertainty_items={len(uncertainty)}",
                asymmetry_note="If uncertainty exists, comparison should preserve it instead of smoothing language.",
                supporting_refs=evidence_refs[:3],
                confidence=0.78,
            )
        )
        if bool(interpretation.get("comparison_requested")) and len(axes) < MAX_COMPARISON_AXES:
            axes.append(
                _axis(
                    axis_label="Intent Alignment",
                    left_value=f"comparison_requested={bool(interpretation.get('comparison_requested'))}",
                    right_value=f"knowledge_gap={knowledge_gap}",
                    asymmetry_note="Comparison intent is valid only when the knowledge gap is made explicit.",
                    supporting_refs=evidence_refs[:2],
                    confidence=0.73,
                )
            )

        axes = axes[:MAX_COMPARISON_AXES]
        if not axes:
            raise Phase9RichExpressionError("comparison lane could not construct any axis")

        lane_notes = _clean_items(
            [
                "Comparison lane uses explicit axes with declared asymmetry.",
                "Comparison lane remains read-only over support and reasoning snapshots.",
                "Comparison lane does not upgrade support confidence.",
            ],
            ceiling=MAX_LANE_NOTES,
        )

        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "axis_count": len(axes),
            "axes": [axis.to_dict() for axis in axes],
            "lane_notes": list(lane_notes),
        }
        if len(axes) > MAX_COMPARISON_AXES:
            raise Phase9RichExpressionError("comparison axis count exceeds Phase 9 ceiling")

        return ComparisonSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            axis_count=len(axes),
            axes=tuple(axes),
            lane_notes=lane_notes,
            snapshot_hash=stable_hash_payload(payload),
        )
