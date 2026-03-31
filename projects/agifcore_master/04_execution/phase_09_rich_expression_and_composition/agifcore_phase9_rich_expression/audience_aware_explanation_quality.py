from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    AudienceAwareExplanationQualitySnapshot,
    AudienceProfile,
    BrevityLevel,
    ExpressionLane,
    MAX_AUDIENCE_PROFILE_BRANCHES,
    MAX_LANE_NOTES,
    Phase9RichExpressionError,
    TerminologyDensity,
    make_trace_ref,
    require_non_empty_str,
    require_phase7_intake_state,
    require_schema,
    stable_hash_payload,
)

_NOVICE_CUES = {"simple", "beginner", "new to", "eli5", "plain language"}
_TECHNICAL_CUES = {"technical", "detailed", "equation", "formal", "exact"}
_EXECUTIVE_CUES = {"executive", "brief", "summary", "short", "high-level"}


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


def _audience_profile(normalized_text: str) -> AudienceProfile:
    lowered = normalized_text.lower()
    if any(cue in lowered for cue in _NOVICE_CUES):
        return AudienceProfile.NOVICE
    if any(cue in lowered for cue in _TECHNICAL_CUES):
        return AudienceProfile.TECHNICAL
    if any(cue in lowered for cue in _EXECUTIVE_CUES):
        return AudienceProfile.EXECUTIVE
    return AudienceProfile.PRACTITIONER


def _style_for_profile(profile: AudienceProfile) -> tuple[TerminologyDensity, BrevityLevel]:
    if profile is AudienceProfile.NOVICE:
        return TerminologyDensity.LOW, BrevityLevel.BALANCED
    if profile is AudienceProfile.TECHNICAL:
        return TerminologyDensity.HIGH, BrevityLevel.DETAILED
    if profile is AudienceProfile.EXECUTIVE:
        return TerminologyDensity.MEDIUM, BrevityLevel.BRIEF
    return TerminologyDensity.MEDIUM, BrevityLevel.BALANCED


def _section_order_for_lane(lane: ExpressionLane) -> tuple[str, ...]:
    if lane is ExpressionLane.TEACHING:
        return ("scope", "steps", "misconceptions", "verification")
    if lane is ExpressionLane.COMPARISON:
        return ("axes", "asymmetry", "limits", "verification")
    if lane is ExpressionLane.PLANNING:
        return ("steps", "dependencies", "stop_points", "verification")
    if lane is ExpressionLane.ANALOGY:
        return ("mapping", "helpfulness", "break_limits", "verification")
    if lane is ExpressionLane.CONCEPT_COMPOSITION:
        return ("inputs", "composed_view", "boundaries", "verification")
    if lane is ExpressionLane.CROSS_DOMAIN_COMPOSITION:
        return ("domains", "shared_pattern", "boundaries", "verification")
    return ("known", "inferred", "uncertainty", "verification")


class AudienceAwareExplanationQualityEngine:
    """Choose bounded wording controls without mutating support or trace state."""

    SCHEMA = "agifcore.phase_09.audience_aware_explanation_quality.v1"

    def build_snapshot(
        self,
        *,
        intake_state: Mapping[str, Any],
        question_interpretation_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        utterance_plan_state: Mapping[str, Any],
        selected_lane: ExpressionLane,
        anti_generic_filler_state: Mapping[str, Any] | None = None,
    ) -> AudienceAwareExplanationQualitySnapshot:
        intake = require_phase7_intake_state(intake_state, "intake_state")
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
        require_schema(
            utterance_plan_state,
            "agifcore.phase_07.utterance_plan.v1",
            "utterance_plan_state",
        )
        anti_filler_status = "not_provided"
        if anti_generic_filler_state is not None:
            anti_filler = require_schema(
                anti_generic_filler_state,
                "agifcore.phase_07.anti_generic_filler.v1",
                "anti_generic_filler_state",
            )
            anti_filler_status = str(anti_filler.get("status", "unknown")).strip() or "unknown"

        turn_id = require_non_empty_str(str(interpretation.get("turn_id", "")).strip(), "turn_id")
        intake_turn_id = require_non_empty_str(str(intake.get("turn_id", "")).strip(), "intake_state.turn_id")
        if intake_turn_id != turn_id:
            raise Phase9RichExpressionError("intake_state.turn_id must match question_interpretation_state.turn_id")

        normalized_text = require_non_empty_str(str(intake.get("normalized_text", "")).strip(), "intake_state.normalized_text")
        profile = _audience_profile(normalized_text)
        terminology_density, brevity_level = _style_for_profile(profile)
        section_order = _section_order_for_lane(selected_lane)
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        uncertainty_preserved = support_state in {"grounded", "inferred", "search_needed", "unknown"}
        caution_preserved = support_state in {"search_needed", "unknown"}
        rewrite_applied = profile is not AudienceProfile.PRACTITIONER

        anti_filler_checks = _clean_items(
            [
                f"anti_filler_status={anti_filler_status}",
                "no_generic_openers",
                "preserve_uncertainty_statements",
                "do_not_upgrade_support_state_by_wording",
                make_trace_ref("audience_lane", {"turn_id": turn_id, "lane": selected_lane.value}),
            ],
            ceiling=MAX_LANE_NOTES,
        )

        branch_count = 4
        if branch_count > MAX_AUDIENCE_PROFILE_BRANCHES:
            raise Phase9RichExpressionError("audience profile branch count exceeds Phase 9 ceiling")

        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "audience_profile": profile.value,
            "terminology_density": terminology_density.value,
            "brevity_level": brevity_level.value,
            "section_order": list(section_order),
            "anti_filler_checks": list(anti_filler_checks),
            "uncertainty_preserved": uncertainty_preserved,
            "caution_preserved": caution_preserved,
            "rewrite_applied": rewrite_applied,
        }
        return AudienceAwareExplanationQualitySnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            audience_profile=profile,
            terminology_density=terminology_density,
            brevity_level=brevity_level,
            section_order=section_order,
            anti_filler_checks=anti_filler_checks,
            uncertainty_preserved=uncertainty_preserved,
            caution_preserved=caution_preserved,
            rewrite_applied=rewrite_applied,
            quality_hash=stable_hash_payload(payload),
        )
