from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_KEY_POINTS_PER_SECTION,
    MAX_LANE_NOTES,
    MAX_TEACHING_SECTIONS,
    MAX_TRACE_REFS,
    Phase9RichExpressionError,
    TeachingSection,
    TeachingSnapshot,
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


def _section(
    *,
    title: str,
    objective: str,
    key_points: tuple[str, ...],
    misconception_hint: str | None,
    verify_prompt: str | None,
    supporting_refs: tuple[str, ...],
) -> TeachingSection:
    payload = {
        "title": title,
        "objective": objective,
        "key_points": list(key_points),
        "misconception_hint": misconception_hint,
        "verify_prompt": verify_prompt,
        "supporting_refs": list(supporting_refs),
    }
    section_hash = stable_hash_payload(payload)
    return TeachingSection(
        section_id=make_trace_ref("teach_section", payload),
        title=title,
        objective=objective,
        key_points=key_points,
        misconception_hint=misconception_hint,
        verify_prompt=verify_prompt,
        supporting_refs=supporting_refs,
        section_hash=section_hash,
    )


class TeachingEngine:
    """Build a bounded teaching structure over already-supported Phase 8 outputs."""

    SCHEMA = "agifcore.phase_09.teaching.v1"

    def build_snapshot(
        self,
        *,
        question_interpretation_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        visible_reasoning_summary_state: Mapping[str, Any],
    ) -> TeachingSnapshot:
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

        turn_id = require_non_empty_str(str(interpretation.get("turn_id", "")).strip(), "turn_id")
        known = [str(item).strip() for item in list(summary.get("what_is_known", ())) if str(item).strip()]
        inferred = [str(item).strip() for item in list(summary.get("what_is_inferred", ())) if str(item).strip()]
        uncertainty = [str(item).strip() for item in list(summary.get("uncertainty", ())) if str(item).strip()]
        verify = [str(item).strip() for item in list(summary.get("what_would_verify", ())) if str(item).strip()]
        evidence_refs = _clean_items(
            [str(item).strip() for item in list(summary.get("evidence_refs", ())) if str(item).strip()],
            ceiling=MAX_TRACE_REFS,
        )

        sections: list[TeachingSection] = []
        sections.append(
            _section(
                title="Known Scope",
                objective="Start from what is directly supported in bounded local state.",
                key_points=_clean_items(known or ["No explicit known items were provided."], ceiling=MAX_KEY_POINTS_PER_SECTION),
                misconception_hint="Known anchors are not the same as complete certainty.",
                verify_prompt="Which known anchors are you relying on first?",
                supporting_refs=evidence_refs[:4],
            )
        )
        sections.append(
            _section(
                title="Derived Understanding",
                objective="Separate inferred points from direct anchors.",
                key_points=_clean_items(inferred or ["No higher-confidence inference was available."], ceiling=MAX_KEY_POINTS_PER_SECTION),
                misconception_hint="Inference quality depends on explicit support and declared uncertainty.",
                verify_prompt="Which inference would fail first if a missing variable changed?",
                supporting_refs=evidence_refs[:4],
            )
        )
        sections.append(
            _section(
                title="Uncertainty and Limits",
                objective="Preserve uncertainty instead of smoothing it away.",
                key_points=_clean_items(uncertainty or ["No explicit uncertainty items were provided."], ceiling=MAX_KEY_POINTS_PER_SECTION),
                misconception_hint="Fluent wording cannot upgrade weak support.",
                verify_prompt="Which uncertainty item blocks a stronger claim?",
                supporting_refs=evidence_refs[:4],
            )
        )
        sections.append(
            _section(
                title="Verification Path",
                objective="Show concrete next checks needed for stronger confidence.",
                key_points=_clean_items(verify or ["No next verification step was provided."], ceiling=MAX_KEY_POINTS_PER_SECTION),
                misconception_hint="Verification steps are required before raising confidence bands.",
                verify_prompt="What single verification step should happen first?",
                supporting_refs=evidence_refs[:4],
            )
        )

        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        if support_state in {"search_needed", "unknown"} and len(sections) < MAX_TEACHING_SECTIONS:
            sections.append(
                _section(
                    title="Honesty Boundary",
                    objective="Keep the non-answer boundary explicit when support is insufficient.",
                    key_points=(
                        "Current support state does not allow a fully grounded answer.",
                        "Do not replace missing support with stylistic confidence.",
                    ),
                    misconception_hint="A polished explanation does not remove the need for fresh support.",
                    verify_prompt="What evidence is missing before this can be treated as grounded?",
                    supporting_refs=evidence_refs[:2],
                )
            )

        sections = sections[:MAX_TEACHING_SECTIONS]
        prerequisite_notes = _clean_items(
            [
                f"discourse_mode_hint={str(interpretation.get('discourse_mode_hint', 'unknown')).strip() or 'unknown'}",
                f"support_state={support_state}",
                f"uncertainty_band={str(summary.get('uncertainty_band', 'unknown')).strip() or 'unknown'}",
            ],
            ceiling=MAX_LANE_NOTES,
        )
        lane_notes = _clean_items(
            [
                "Teaching lane remains read-only over Phase 7 and Phase 8 snapshots.",
                "Teaching lane does not upgrade support-state honesty.",
                "Teaching lane keeps uncertainty and verification steps visible.",
            ],
            ceiling=MAX_LANE_NOTES,
        )

        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "section_count": len(sections),
            "sections": [section.to_dict() for section in sections],
            "prerequisite_notes": list(prerequisite_notes),
            "lane_notes": list(lane_notes),
        }
        if len(sections) > MAX_TEACHING_SECTIONS:
            raise Phase9RichExpressionError("teaching section count exceeds Phase 9 ceiling")

        return TeachingSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            section_count=len(sections),
            sections=tuple(sections),
            prerequisite_notes=prerequisite_notes,
            lane_notes=lane_notes,
            snapshot_hash=stable_hash_payload(payload),
        )
