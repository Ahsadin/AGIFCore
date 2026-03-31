from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_LANE_NOTES,
    MAX_SYNTHESIS_INPUTS,
    MAX_TRACE_REFS,
    MAX_UNCERTAINTY_ITEMS,
    Phase9RichExpressionError,
    SynthesisInput,
    SynthesisSnapshot,
    UncertaintyLevel,
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


def _input(
    *,
    input_kind: str,
    summary: str,
    support_ref: str,
    uncertainty_note: str | None,
) -> SynthesisInput:
    payload = {
        "input_kind": input_kind,
        "summary": summary,
        "support_ref": support_ref,
        "uncertainty_note": uncertainty_note,
    }
    input_hash = stable_hash_payload(payload)
    return SynthesisInput(
        input_id=make_trace_ref("synthesis_input", payload),
        input_kind=input_kind,
        summary=summary,
        support_ref=support_ref,
        uncertainty_note=uncertainty_note,
        input_hash=input_hash,
    )


class SynthesisEngine:
    """Build bounded synthesis while preserving support-state honesty."""

    SCHEMA = "agifcore.phase_09.synthesis.v1"

    def build_snapshot(
        self,
        *,
        question_interpretation_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        visible_reasoning_summary_state: Mapping[str, Any],
        science_reflection_state: Mapping[str, Any],
        bounded_current_world_reasoning_state: Mapping[str, Any],
    ) -> SynthesisSnapshot:
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
        bounded_current_world = require_schema(
            bounded_current_world_reasoning_state,
            "agifcore.phase_08.bounded_current_world_reasoning.v1",
            "bounded_current_world_reasoning_state",
        )

        turn_id = require_non_empty_str(str(interpretation.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        support_honest = support_state in {"grounded", "inferred", "search_needed", "unknown"}

        known = [str(item).strip() for item in list(summary.get("what_is_known", ())) if str(item).strip()]
        inferred = [str(item).strip() for item in list(summary.get("what_is_inferred", ())) if str(item).strip()]
        uncertainty = [str(item).strip() for item in list(summary.get("uncertainty", ())) if str(item).strip()]
        verify = [str(item).strip() for item in list(summary.get("what_would_verify", ())) if str(item).strip()]
        evidence_refs = _clean_items(
            [str(item).strip() for item in list(summary.get("evidence_refs", ())) if str(item).strip()],
            ceiling=MAX_TRACE_REFS,
        )
        reflection_records = [item for item in list(reflection.get("records", ())) if isinstance(item, Mapping)]

        synthesis_inputs: list[SynthesisInput] = []
        for item in known:
            if len(synthesis_inputs) >= MAX_SYNTHESIS_INPUTS:
                break
            synthesis_inputs.append(
                _input(
                    input_kind="known_anchor",
                    summary=item,
                    support_ref=evidence_refs[0] if evidence_refs else turn_id,
                    uncertainty_note=None,
                )
            )
        for item in inferred:
            if len(synthesis_inputs) >= MAX_SYNTHESIS_INPUTS:
                break
            synthesis_inputs.append(
                _input(
                    input_kind="inference",
                    summary=item,
                    support_ref=evidence_refs[1] if len(evidence_refs) > 1 else (evidence_refs[0] if evidence_refs else turn_id),
                    uncertainty_note="Inference depends on bounded support and may weaken if missing variables change.",
                )
            )
        for item in reflection_records:
            if len(synthesis_inputs) >= MAX_SYNTHESIS_INPUTS:
                break
            note = str(item.get("note", "")).strip()
            if not note:
                continue
            source_ref = str(item.get("source_ref", "")).strip() or turn_id
            synthesis_inputs.append(
                _input(
                    input_kind="reflection",
                    summary=note,
                    support_ref=source_ref,
                    uncertainty_note=(
                        "Reflection suggests uncertainty increase."
                        if coerce_bool(item.get("increases_uncertainty"))
                        else None
                    ),
                )
            )

        if not synthesis_inputs:
            synthesis_inputs.append(
                _input(
                    input_kind="fallback",
                    summary="No composable supported inputs were available in this turn.",
                    support_ref=turn_id,
                    uncertainty_note="Synthesis output remains bounded and non-upgraded.",
                )
            )

        unresolved_conflicts = _clean_items(
            uncertainty + [str(item.get("note", "")).strip() for item in reflection_records if str(item.get("note", "")).strip()],
            ceiling=MAX_UNCERTAINTY_ITEMS,
        )
        missing_support = _clean_items(
            (
                verify
                if support_state in {"search_needed", "unknown"}
                else ["No additional missing-support blocker declared for this support state."]
            ),
            ceiling=MAX_UNCERTAINTY_ITEMS,
        )

        uncertainty_level = UncertaintyLevel.LOW
        if support_state in {"search_needed", "unknown"}:
            uncertainty_level = UncertaintyLevel.HIGH
        elif unresolved_conflicts:
            uncertainty_level = UncertaintyLevel.MODERATE
        if coerce_bool(bounded_current_world.get("needs_fresh_information")):
            uncertainty_level = UncertaintyLevel.HIGH

        merged_summary = (
            f"Bounded synthesis combines {len(synthesis_inputs)} inputs while preserving support_state={support_state}. "
            f"Uncertainty level remains {uncertainty_level.value} with {len(unresolved_conflicts)} surfaced conflict(s)."
        )

        lane_notes = _clean_items(
            [
                "Synthesis lane is read-only over Phase 8 outputs.",
                "Synthesis lane preserves declared uncertainty instead of smoothing it away.",
                "Synthesis lane never upgrades support state.",
            ],
            ceiling=MAX_LANE_NOTES,
        )

        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "input_count": len(synthesis_inputs),
            "inputs": [item.to_dict() for item in synthesis_inputs],
            "merged_summary": merged_summary,
            "unresolved_conflicts": list(unresolved_conflicts),
            "missing_support": list(missing_support),
            "uncertainty_level": uncertainty_level.value,
            "preserves_support_honesty": support_honest,
            "lane_notes": list(lane_notes),
        }
        if len(synthesis_inputs) > MAX_SYNTHESIS_INPUTS:
            raise Phase9RichExpressionError("synthesis input count exceeds Phase 9 ceiling")

        return SynthesisSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            input_count=len(synthesis_inputs),
            inputs=tuple(synthesis_inputs),
            merged_summary=merged_summary,
            unresolved_conflicts=unresolved_conflicts,
            missing_support=missing_support,
            uncertainty_level=uncertainty_level,
            preserves_support_honesty=support_honest,
            lane_notes=lane_notes,
            snapshot_hash=stable_hash_payload(payload),
        )
