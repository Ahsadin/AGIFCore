from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    CrossDomainCompositionSnapshot,
    CrossDomainPatternElement,
    MAX_CROSS_DOMAIN_COMPOSITION_ELEMENTS,
    MAX_LANE_NOTES,
    MAX_REASON_CODES,
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
    label: str,
    source_domain: str,
    target_domain: str,
    note: str,
    confidence: float,
) -> CrossDomainPatternElement:
    payload = {
        "label": label,
        "source_domain": source_domain,
        "target_domain": target_domain,
        "note": note,
        "confidence": clamp_score(confidence),
    }
    element_hash = stable_hash_payload(payload)
    return CrossDomainPatternElement(
        element_id=make_trace_ref("cross_domain_element", payload),
        label=label,
        source_domain=source_domain,
        target_domain=target_domain,
        note=note,
        confidence=clamp_score(confidence),
        element_hash=element_hash,
    )


class CrossDomainCompositionEngine:
    """Compose exactly two bounded domains with fail-closed behavior."""

    SCHEMA = "agifcore.phase_09.cross_domain_composition.v1"

    def build_snapshot(
        self,
        *,
        question_interpretation_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        entity_request_inference_state: Mapping[str, Any],
        world_region_selection_state: Mapping[str, Any],
        concept_composition_state: Mapping[str, Any],
    ) -> CrossDomainCompositionSnapshot:
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
        regions = require_schema(
            world_region_selection_state,
            "agifcore.phase_08.world_region_selection.v1",
            "world_region_selection_state",
        )
        concept = require_schema(
            concept_composition_state,
            "agifcore.phase_09.concept_composition.v1",
            "concept_composition_state",
        )

        turn_id = require_non_empty_str(str(interpretation.get("turn_id", "")).strip(), "turn_id")
        concept_composition_ref = require_non_empty_str(
            str(concept.get("concept_composition_ref", "")).strip(),
            "concept_composition_ref",
        )
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"

        domain_candidates: list[str] = []
        target_domain_hint = str(interpretation.get("target_domain_hint", "")).strip()
        if target_domain_hint:
            domain_candidates.append(target_domain_hint)
        for cue in list(inference.get("science_topic_cues", ())):
            cue_label = str(cue).strip()
            if cue_label:
                domain_candidates.append(cue_label)
        for item in list(regions.get("candidates", ())):
            if not isinstance(item, Mapping):
                continue
            domain = str(item.get("target_domain", "")).strip()
            if domain:
                domain_candidates.append(domain)
        domains = list(_clean_items(domain_candidates, ceiling=6))

        fail_closed = False
        reason_codes: list[str] = []
        if len(domains) < 2:
            fail_closed = True
            reason_codes.append("insufficient_domains_for_cross_domain_composition")
            domains = [domains[0] if domains else "unspecified_domain", "missing_second_domain"]
        elif len(domains) > 2:
            reason_codes.append("domain_count_bounded_to_two")
            domains = domains[:2]

        source_domain_ref, target_domain_ref = domains[0], domains[1]
        concept_elements = [item for item in list(concept.get("elements", ())) if isinstance(item, Mapping)]
        elements: list[CrossDomainPatternElement] = []
        for item in concept_elements:
            if len(elements) >= MAX_CROSS_DOMAIN_COMPOSITION_ELEMENTS:
                break
            label = str(item.get("concept_label", "")).strip()
            if not label:
                continue
            role = str(item.get("role_in_composition", "")).strip() or "pattern_component"
            elements.append(
                _element(
                    label=label,
                    source_domain=source_domain_ref,
                    target_domain=target_domain_ref,
                    note=f"Mapped via role={role}.",
                    confidence=0.7 if support_state in {"grounded", "inferred"} else 0.52,
                )
            )

        if not elements:
            fail_closed = True
            reason_codes.append("no_composable_elements")
            elements.append(
                _element(
                    label="cross_domain_mapping_unavailable",
                    source_domain=source_domain_ref,
                    target_domain=target_domain_ref,
                    note="No bounded composable element was available from concept composition.",
                    confidence=0.3,
                )
            )

        if support_state in {"search_needed", "unknown"}:
            fail_closed = True
            reason_codes.append("support_state_requires_conservative_cross_domain_output")

        shared_pattern = (
            f"Cross-domain pattern between {source_domain_ref} and {target_domain_ref} "
            f"using {len(elements)} bounded pattern element(s)."
        )
        boundary_notes = _clean_items(
            [
                "Cross-domain composition defaults to exactly two domains.",
                "Cross-domain composition remains fail-closed on insufficient support.",
                "Cross-domain composition reuses concept_composition_ref for lineage continuity.",
            ],
            ceiling=MAX_LANE_NOTES,
        )
        lane_notes = _clean_items(
            [
                f"support_state={support_state}",
                f"fail_closed={fail_closed}",
                "No multi-domain widening is allowed without re-planning.",
            ],
            ceiling=MAX_LANE_NOTES,
        )

        reason_codes = list(_clean_items(reason_codes or ["none"], ceiling=MAX_REASON_CODES))
        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "composition_kind": "cross_domain",
            "concept_composition_ref": concept_composition_ref,
            "domain_refs": [source_domain_ref, target_domain_ref],
            "element_count": len(elements),
            "elements": [item.to_dict() for item in elements],
            "shared_pattern": shared_pattern,
            "boundary_notes": list(boundary_notes),
            "fail_closed": fail_closed,
            "reason_codes": reason_codes,
            "lane_notes": list(lane_notes),
        }
        if len(elements) > MAX_CROSS_DOMAIN_COMPOSITION_ELEMENTS:
            raise Phase9RichExpressionError("cross-domain composition element count exceeds Phase 9 ceiling")

        return CrossDomainCompositionSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            composition_kind="cross_domain",
            concept_composition_ref=concept_composition_ref,
            domain_refs=(source_domain_ref, target_domain_ref),
            element_count=len(elements),
            elements=tuple(elements),
            shared_pattern=shared_pattern,
            boundary_notes=boundary_notes,
            fail_closed=fail_closed,
            reason_codes=tuple(reason_codes),
            lane_notes=lane_notes,
            snapshot_hash=stable_hash_payload(payload),
        )
