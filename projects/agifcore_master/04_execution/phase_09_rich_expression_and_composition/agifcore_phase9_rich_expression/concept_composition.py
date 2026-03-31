from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    ConceptCompositionElement,
    ConceptCompositionSnapshot,
    MAX_CONCEPT_COMPOSITION_ELEMENTS,
    MAX_LANE_NOTES,
    MAX_TRACE_REFS,
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


def _element(
    *,
    concept_label: str,
    role_in_composition: str,
    supporting_refs: tuple[str, ...],
    confidence: float,
) -> ConceptCompositionElement:
    payload = {
        "concept_label": concept_label,
        "role_in_composition": role_in_composition,
        "supporting_refs": list(supporting_refs),
        "confidence": clamp_score(confidence),
    }
    element_hash = stable_hash_payload(payload)
    return ConceptCompositionElement(
        element_id=make_trace_ref("concept_element", payload),
        concept_label=concept_label,
        role_in_composition=role_in_composition,
        supporting_refs=supporting_refs,
        confidence=clamp_score(confidence),
        element_hash=element_hash,
    )


class ConceptCompositionEngine:
    """Compose a bounded concept set into an inspectable composite view."""

    SCHEMA = "agifcore.phase_09.concept_composition.v1"

    def build_snapshot(
        self,
        *,
        entity_request_inference_state: Mapping[str, Any],
        scientific_priors_state: Mapping[str, Any],
        visible_reasoning_summary_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
    ) -> ConceptCompositionSnapshot:
        inference = require_schema(
            entity_request_inference_state,
            "agifcore.phase_08.entity_request_inference.v1",
            "entity_request_inference_state",
        )
        priors = require_schema(
            scientific_priors_state,
            "agifcore.phase_08.scientific_priors.v1",
            "scientific_priors_state",
        )
        summary = require_schema(
            visible_reasoning_summary_state,
            "agifcore.phase_08.visible_reasoning_summaries.v1",
            "visible_reasoning_summary_state",
        )
        support = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )

        turn_id = require_non_empty_str(str(inference.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        selected_prior_ids = [str(item).strip() for item in list(priors.get("selected_prior_ids", ())) if str(item).strip()]
        cue_terms = [str(item).strip() for item in list(inference.get("science_topic_cues", ())) if str(item).strip()]
        evidence_refs = _clean_items(
            [str(item).strip() for item in list(summary.get("evidence_refs", ())) if str(item).strip()],
            ceiling=MAX_TRACE_REFS,
        )

        elements: list[ConceptCompositionElement] = []
        for prior_id in selected_prior_ids:
            if len(elements) >= MAX_CONCEPT_COMPOSITION_ELEMENTS:
                break
            elements.append(
                _element(
                    concept_label=prior_id,
                    role_in_composition="governing_principle",
                    supporting_refs=evidence_refs[:3],
                    confidence=0.82 if support_state in {"grounded", "inferred"} else 0.61,
                )
            )
        for cue in cue_terms:
            if len(elements) >= MAX_CONCEPT_COMPOSITION_ELEMENTS:
                break
            elements.append(
                _element(
                    concept_label=cue,
                    role_in_composition="context_modifier",
                    supporting_refs=evidence_refs[:2],
                    confidence=0.66,
                )
            )

        fail_closed = False
        lane_notes: list[str] = [
            "Concept composition lane preserves explicit composition inputs.",
            "Concept composition lane is bounded and read-only over upstream support.",
        ]
        if not elements:
            fail_closed = True
            elements.append(
                _element(
                    concept_label="insufficient_supported_concepts",
                    role_in_composition="fail_closed_placeholder",
                    supporting_refs=(turn_id,),
                    confidence=0.3,
                )
            )
            lane_notes.append("Composition failed closed due to missing composable inputs.")

        composed_view = (
            f"Composite view built from {len(elements)} bounded concept element(s) under support_state={support_state}."
        )
        if support_state in {"search_needed", "unknown"}:
            fail_closed = True
            composed_view += " Output remains constrained because support is not fully grounded."
            lane_notes.append("Support-state boundary forces conservative composition.")

        trace_payload = {
            "turn_id": turn_id,
            "element_hashes": [item.element_hash for item in elements],
            "support_state": support_state,
            "fail_closed": fail_closed,
        }
        concept_composition_ref = make_trace_ref("concept_composition", trace_payload)

        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "element_count": len(elements),
            "elements": [item.to_dict() for item in elements],
            "composed_view": composed_view,
            "concept_composition_ref": concept_composition_ref,
            "fail_closed": fail_closed,
            "lane_notes": list(_clean_items(lane_notes, ceiling=MAX_LANE_NOTES)),
        }
        if len(elements) > MAX_CONCEPT_COMPOSITION_ELEMENTS:
            raise Phase9RichExpressionError("concept composition element count exceeds Phase 9 ceiling")

        return ConceptCompositionSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            element_count=len(elements),
            elements=tuple(elements),
            composed_view=composed_view,
            concept_composition_ref=concept_composition_ref,
            fail_closed=fail_closed,
            lane_notes=_clean_items(lane_notes, ceiling=MAX_LANE_NOTES),
            snapshot_hash=stable_hash_payload(payload),
        )
