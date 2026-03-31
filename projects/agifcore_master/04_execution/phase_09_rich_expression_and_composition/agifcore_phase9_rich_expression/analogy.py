from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    AnalogyMode,
    AnalogyMapping,
    AnalogySnapshot,
    MAX_ANALOGIES_PER_RESPONSE,
    MAX_LANE_NOTES,
    MAX_TRACE_REFS,
    Phase9RichExpressionError,
    clamp_score,
    make_trace_ref,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

_ANALOGY_LIBRARY: dict[str, tuple[str, str, str, str]] = {
    "thermodynamics": (
        "Heat moving through materials",
        "Water flowing downhill in a channel",
        "Both follow a gradient-driven transfer pattern.",
        "The analogy breaks when material-specific thermal properties dominate behavior.",
    ),
    "fluid_dynamics": (
        "Pressure-driven fluid flow",
        "Traffic moving through narrow streets",
        "Both show bottlenecks and path-dependent throughput limits.",
        "Vehicle intent and lane rules have no direct fluid equivalent.",
    ),
    "mechanics": (
        "Force and resistance in motion",
        "Pushing a loaded cart on rough ground",
        "Both require balancing applied force against opposing friction-like effects.",
        "Complex multi-body interactions need direct mechanics, not only metaphor.",
    ),
    "weather_climate": (
        "Weather pattern accumulation",
        "Repeated small deposits filling a reservoir",
        "Both rely on cumulative inputs over time windows.",
        "Sudden regime shifts in weather are not captured by simple reservoir framing.",
    ),
}


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


def _mapping(
    *,
    source_point: str,
    target_point: str,
    why_it_helps: str,
    break_limit: str,
    supporting_refs: tuple[str, ...],
    confidence: float,
) -> AnalogyMapping:
    payload = {
        "source_point": source_point,
        "target_point": target_point,
        "why_it_helps": why_it_helps,
        "break_limit": break_limit,
        "supporting_refs": list(supporting_refs),
        "confidence": clamp_score(confidence),
    }
    mapping_hash = stable_hash_payload(payload)
    return AnalogyMapping(
        mapping_id=make_trace_ref("analogy_mapping", payload),
        source_point=source_point,
        target_point=target_point,
        why_it_helps=why_it_helps,
        break_limit=break_limit,
        supporting_refs=supporting_refs,
        confidence=clamp_score(confidence),
        mapping_hash=mapping_hash,
    )


class AnalogyEngine:
    """Produce bounded analogies with explicit mapping and break conditions."""

    SCHEMA = "agifcore.phase_09.analogy.v1"

    def build_snapshot(
        self,
        *,
        entity_request_inference_state: Mapping[str, Any],
        visible_reasoning_summary_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
    ) -> AnalogySnapshot:
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
        support = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )

        turn_id = require_non_empty_str(str(inference.get("turn_id", "")).strip(), "turn_id")
        cues = [str(item).strip() for item in list(inference.get("science_topic_cues", ())) if str(item).strip()]
        uncertainty = [str(item).strip() for item in list(summary.get("uncertainty", ())) if str(item).strip()]
        evidence_refs = _clean_items(
            [str(item).strip() for item in list(summary.get("evidence_refs", ())) if str(item).strip()],
            ceiling=MAX_TRACE_REFS,
        )
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        source_domain_ref = "domain::unknown_source"
        target_domain_ref = "domain::everyday_analogy_target"

        mappings: list[AnalogyMapping] = []
        for cue in cues:
            if len(mappings) >= MAX_ANALOGIES_PER_RESPONSE:
                break
            if cue not in _ANALOGY_LIBRARY:
                continue
            source, target, help_note, break_limit = _ANALOGY_LIBRARY[cue]
            source_domain_ref = f"domain::{cue}"
            target_domain_ref = "domain::bounded_everyday_structure"
            mappings.append(
                _mapping(
                    source_point=source,
                    target_point=target,
                    why_it_helps=help_note,
                    break_limit=break_limit,
                    supporting_refs=evidence_refs[:3],
                    confidence=0.74 if support_state in {"grounded", "inferred"} else 0.58,
                )
            )

        if not mappings:
            fallback_break = uncertainty[0] if uncertainty else "Analogy is illustrative only and does not prove correctness."
            mappings.append(
                _mapping(
                    source_point="Known supported structure",
                    target_point="Simplified everyday structure",
                    why_it_helps="The mapping helps explain shape, not proof strength.",
                    break_limit=fallback_break,
                    supporting_refs=evidence_refs[:2],
                    confidence=0.52,
                )
            )

        support_refs = _clean_items(
            [
                *evidence_refs,
                str(summary.get("causal_chain_ref", "")).strip(),
                str(summary.get("summary_hash", "")).strip(),
            ],
            ceiling=MAX_TRACE_REFS,
        )
        payload_for_trace = {
            "turn_id": turn_id,
            "mapping_hashes": [item.mapping_hash for item in mappings],
            "support_state": support_state,
            "source_domain_ref": source_domain_ref,
            "target_domain_ref": target_domain_ref,
        }
        analogy_trace_ref = make_trace_ref("analogy_trace", payload_for_trace)
        analogy_mode = (
            AnalogyMode.STRUCTURAL
            if support_state in {"grounded", "inferred"}
            else AnalogyMode.BOUNDED_BRIDGE
        )
        lane_notes = _clean_items(
            [
                "Analogy lane includes explicit source-target mappings.",
                "Analogy lane always includes break limits.",
                "Analogy lane does not use metaphor as proof.",
            ],
            ceiling=MAX_LANE_NOTES,
        )

        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "analogy_mode": analogy_mode.value,
            "source_domain_ref": source_domain_ref,
            "target_domain_ref": target_domain_ref,
            "analogy_count": len(mappings),
            "mappings": [item.to_dict() for item in mappings],
            "analogy_trace_ref": analogy_trace_ref,
            "support_refs": list(support_refs),
            "lane_notes": list(lane_notes),
        }
        if len(mappings) > MAX_ANALOGIES_PER_RESPONSE:
            raise Phase9RichExpressionError("analogy count exceeds Phase 9 ceiling")

        return AnalogySnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            analogy_mode=analogy_mode,
            source_domain_ref=source_domain_ref,
            target_domain_ref=target_domain_ref,
            analogy_count=len(mappings),
            mappings=tuple(mappings),
            analogy_trace_ref=analogy_trace_ref,
            support_refs=support_refs,
            lane_notes=lane_notes,
            snapshot_hash=stable_hash_payload(payload),
        )
