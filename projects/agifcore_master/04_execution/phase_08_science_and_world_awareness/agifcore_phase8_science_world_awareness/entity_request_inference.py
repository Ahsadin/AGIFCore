from __future__ import annotations

import re
from typing import Any, Mapping

from .contracts import (
    MAX_INFERENCE_CANDIDATES,
    MAX_MATCHED_TERMS,
    MAX_REASON_CODES,
    EntityClass,
    EntityRequestCandidate,
    EntityRequestInferenceSnapshot,
    Phase8ScienceWorldAwarenessError,
    RequestType,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_phase7_intake_state,
    require_schema,
    stable_hash_payload,
)

_TOKEN_RE = re.compile(r"[a-z0-9']+")
_IN_REGION_RE = re.compile(r"\bin\s+([a-z0-9' -]{2,48})")

_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}

_REQUEST_TYPE_CUES: dict[RequestType, tuple[str, ...]] = {
    RequestType.CAUSAL_EXPLANATION: ("why", "cause", "causes", "causal", "because", "drives"),
    RequestType.DERIVED_ESTIMATE: ("estimate", "roughly", "around", "predict", "projection"),
    RequestType.STATUS_CHECK: ("status", "state", "latest", "current", "today", "now"),
    RequestType.DEFINITION: ("define", "definition", "meaning", "what is", "what are"),
    RequestType.COMPARISON: ("compare", "versus", "vs", "better", "worse", "than"),
    RequestType.CLASSIFICATION: ("type", "class", "category", "kind", "belongs"),
    RequestType.SCIENCE_EXPLANATION: ("how", "explain", "principle", "mechanism", "science"),
}

_ENTITY_CLASS_CUES: dict[EntityClass, tuple[str, ...]] = {
    EntityClass.PLACE: ("city", "country", "region", "coast", "inland", "district", "state"),
    EntityClass.PHYSICAL_SYSTEM: ("system", "network", "climate", "weather", "atmosphere"),
    EntityClass.MATERIAL: ("material", "metal", "plastic", "concrete", "soil", "water", "air"),
    EntityClass.ORGANISM: ("plant", "animal", "human", "organism", "crop", "species"),
    EntityClass.PROCESS: ("process", "flow", "reaction", "transfer", "growth", "decay"),
    EntityClass.MEASUREMENT: ("temperature", "pressure", "speed", "mass", "density", "rate"),
    EntityClass.ARTIFACT: ("device", "engine", "tool", "machine", "sensor", "instrument"),
}

_SCIENCE_TOPIC_CUES: dict[str, tuple[str, ...]] = {
    "thermodynamics": ("heat", "thermal", "temperature", "cooling", "warming"),
    "fluid_dynamics": ("flow", "pressure", "wind", "drain", "leak"),
    "mechanics": ("force", "motion", "friction", "mass", "acceleration"),
    "weather_climate": ("weather", "climate", "humidity", "rain", "storm"),
    "measurement_uncertainty": ("current", "latest", "today", "exact", "uncertain"),
}

_HIDDEN_VARIABLE_CUES: dict[str, tuple[str, ...]] = {
    "time_of_day": ("morning", "afternoon", "evening", "night"),
    "seasonal_baseline": ("winter", "summer", "spring", "autumn", "season"),
    "surface_material": ("asphalt", "concrete", "soil", "water", "shade"),
    "sensor_freshness": ("latest", "now", "live", "updated", "current"),
    "context_missing": ("depends", "context", "assume", "unclear", "ambiguous"),
}


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _unique_bounded(values: list[str], *, ceiling: int) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        cleaned = str(item).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
        if len(result) >= ceiling:
            break
    return tuple(result)


def _cue_hits(
    *,
    normalized_text: str,
    token_set: set[str],
    cue_map: dict[str, tuple[str, ...]],
) -> tuple[str, ...]:
    hits: list[str] = []
    for label, cues in cue_map.items():
        for cue in cues:
            cue_norm = cue.strip().lower()
            if not cue_norm:
                continue
            if " " in cue_norm:
                if cue_norm in normalized_text:
                    hits.append(label)
                    break
            elif cue_norm in token_set:
                hits.append(label)
                break
    return _unique_bounded(hits, ceiling=MAX_MATCHED_TERMS)


def _request_type_rankings(
    *,
    normalized_text: str,
    token_set: set[str],
    interpretation: dict[str, Any],
) -> tuple[RequestType, ...]:
    scores: dict[RequestType, int] = {kind: 0 for kind in _REQUEST_TYPE_CUES}
    for kind, cues in _REQUEST_TYPE_CUES.items():
        for cue in cues:
            cue_norm = cue.lower()
            if " " in cue_norm:
                if cue_norm in normalized_text:
                    scores[kind] += 2
            elif cue_norm in token_set:
                scores[kind] += 1

    if bool(interpretation.get("comparison_requested")):
        scores[RequestType.COMPARISON] += 3
    if bool(interpretation.get("live_current_requested")):
        scores[RequestType.STATUS_CHECK] += 3
    if bool(interpretation.get("ambiguous_request")):
        scores[RequestType.CAUSAL_EXPLANATION] -= 1
    if "how" in token_set or "why" in token_set:
        scores[RequestType.SCIENCE_EXPLANATION] += 2

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    picked = [kind for kind, score in ranked if score > 0]
    if not picked:
        return (RequestType.UNKNOWN,)
    return tuple(picked[:3])


def _entity_class_for_label(*, label: str, token_set: set[str]) -> EntityClass:
    label_tokens = set(_tokens(label))
    combined = token_set.union(label_tokens)
    best_class = EntityClass.UNKNOWN
    best_score = 0
    for entity_class, cues in _ENTITY_CLASS_CUES.items():
        score = sum(1 for cue in cues if cue in combined)
        if score > best_score:
            best_class = entity_class
            best_score = score
    return best_class


def _entity_labels(
    *,
    normalized_text: str,
    extracted_terms: tuple[str, ...],
    target_domain_hint: str | None,
) -> tuple[str, ...]:
    labels: list[str] = []
    region_match = _IN_REGION_RE.search(normalized_text)
    if region_match:
        labels.append(region_match.group(1).strip())

    raw_tokens = _tokens(normalized_text)
    meaningful = [token for token in raw_tokens if token not in _STOPWORDS and len(token) > 2]
    for index in range(0, max(0, len(meaningful) - 1)):
        phrase = f"{meaningful[index]} {meaningful[index + 1]}"
        if phrase not in labels:
            labels.append(phrase)
        if len(labels) >= 6:
            break

    for term in extracted_terms:
        if term not in _STOPWORDS and len(term) > 2:
            labels.append(term)
        if len(labels) >= 8:
            break

    if target_domain_hint:
        labels.append(target_domain_hint.replace("_", " "))
    if not labels:
        labels.append("unspecified_entity")
    return _unique_bounded(labels, ceiling=8)


def _support_hints(
    *,
    interpretation: dict[str, Any],
    support_state_resolution_state: Mapping[str, Any] | None,
) -> tuple[str, str]:
    if support_state_resolution_state is not None:
        support = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )
        support_state_hint = str(support.get("support_state", "unknown")).strip() or "unknown"
        knowledge_gap_reason_hint = str(support.get("knowledge_gap_reason", "none")).strip() or "none"
        return support_state_hint, knowledge_gap_reason_hint

    if bool(interpretation.get("live_current_requested")):
        return "search_needed", "needs_fresh_information"
    if bool(interpretation.get("ambiguous_request")):
        return "unknown", "ambiguous_request"
    return "unknown", "none"


class EntityRequestInferenceEngine:
    """Infer bounded entity/request candidates from Phase 7 intake and interpretation."""

    SCHEMA = "agifcore.phase_08.entity_request_inference.v1"

    def build_snapshot(
        self,
        *,
        intake_state: Mapping[str, Any],
        question_interpretation_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any] | None = None,
    ) -> EntityRequestInferenceSnapshot:
        intake = require_phase7_intake_state(intake_state, "intake_state")
        interpretation = require_schema(
            question_interpretation_state,
            "agifcore.phase_07.question_interpretation.v1",
            "question_interpretation_state",
        )

        conversation_id = require_non_empty_str(intake.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(intake.get("turn_id"), "turn_id")
        normalized_text = require_non_empty_str(intake.get("normalized_text"), "normalized_text")
        raw_text_hash = require_non_empty_str(intake.get("intake_hash"), "intake_hash")
        extracted_terms = _unique_bounded(
            [str(item).strip().lower() for item in list(interpretation.get("extracted_terms", ())) if str(item).strip()],
            ceiling=24,
        )
        token_set = set(_tokens(normalized_text))

        target_domain_hint = interpretation.get("target_domain_hint")
        if target_domain_hint is not None:
            target_domain_hint = require_non_empty_str(target_domain_hint, "target_domain_hint")

        support_state_hint, knowledge_gap_reason_hint = _support_hints(
            interpretation=interpretation,
            support_state_resolution_state=support_state_resolution_state,
        )

        request_type_ranked = _request_type_rankings(
            normalized_text=normalized_text.lower(),
            token_set=token_set,
            interpretation=interpretation,
        )
        labels = _entity_labels(
            normalized_text=normalized_text.lower(),
            extracted_terms=extracted_terms,
            target_domain_hint=target_domain_hint,
        )
        science_cues = _cue_hits(
            normalized_text=normalized_text.lower(),
            token_set=token_set,
            cue_map=_SCIENCE_TOPIC_CUES,
        )
        hidden_cues = _cue_hits(
            normalized_text=normalized_text.lower(),
            token_set=token_set,
            cue_map=_HIDDEN_VARIABLE_CUES,
        )

        live_current_requested = bool(interpretation.get("live_current_requested"))
        ambiguous_request = bool(interpretation.get("ambiguous_request"))

        candidates: list[EntityRequestCandidate] = []
        for label_index, label in enumerate(labels):
            request_types = request_type_ranked[:2] if label_index < 2 else request_type_ranked[:1]
            for request_type in request_types:
                if len(candidates) >= MAX_INFERENCE_CANDIDATES:
                    break

                entity_class = _entity_class_for_label(label=label, token_set=token_set)
                region_hint = label if entity_class is EntityClass.PLACE else None
                if region_hint is None and target_domain_hint and "region" in target_domain_hint:
                    region_hint = target_domain_hint

                matched_terms = _unique_bounded(
                    _tokens(label) + list(extracted_terms) + list(science_cues),
                    ceiling=MAX_MATCHED_TERMS,
                )
                reason_codes: list[str] = []
                if request_type is not RequestType.UNKNOWN:
                    reason_codes.append(f"request_type:{request_type.value}")
                if entity_class is not EntityClass.UNKNOWN:
                    reason_codes.append(f"entity_class:{entity_class.value}")
                if science_cues:
                    reason_codes.append("science_topic_cues_detected")
                if hidden_cues:
                    reason_codes.append("hidden_variable_cues_detected")
                if live_current_requested:
                    reason_codes.append("live_current_requested")
                if ambiguous_request:
                    reason_codes.append("ambiguous_request")
                if support_state_hint in {"search_needed", "unknown"}:
                    reason_codes.append(f"support_state_hint:{support_state_hint}")
                reason_codes = list(_unique_bounded(reason_codes, ceiling=MAX_REASON_CODES))

                confidence = 0.2
                if label != "unspecified_entity":
                    confidence += 0.2
                if request_type is not RequestType.UNKNOWN:
                    confidence += 0.15
                if entity_class is not EntityClass.UNKNOWN:
                    confidence += 0.15
                if science_cues:
                    confidence += 0.1
                if hidden_cues:
                    confidence += 0.1
                if live_current_requested:
                    confidence -= 0.05
                if ambiguous_request:
                    confidence -= 0.15
                if support_state_hint in {"search_needed", "unknown"}:
                    confidence -= 0.1

                candidate_payload = {
                    "candidate_id": f"eri::{turn_id}::{len(candidates) + 1:02d}",
                    "entity_label": label,
                    "entity_class": entity_class.value,
                    "request_type": request_type.value,
                    "science_topic_cues": list(science_cues),
                    "matched_terms": list(matched_terms),
                    "hidden_variable_cues": list(hidden_cues),
                    "target_domain_hint": target_domain_hint,
                    "region_hint": region_hint,
                    "live_current_requested": live_current_requested,
                    "ambiguous_request": ambiguous_request,
                    "confidence": clamp_score(confidence),
                    "reason_codes": list(reason_codes),
                }
                candidates.append(
                    EntityRequestCandidate(
                        candidate_id=candidate_payload["candidate_id"],
                        entity_label=candidate_payload["entity_label"],
                        entity_class=entity_class,
                        request_type=request_type,
                        science_topic_cues=tuple(science_cues),
                        matched_terms=tuple(matched_terms),
                        hidden_variable_cues=tuple(hidden_cues),
                        target_domain_hint=target_domain_hint,
                        region_hint=region_hint,
                        live_current_requested=live_current_requested,
                        ambiguous_request=ambiguous_request,
                        confidence=candidate_payload["confidence"],
                        reason_codes=tuple(reason_codes),
                        candidate_hash=stable_hash_payload(candidate_payload),
                    )
                )

        if not candidates:
            raise Phase8ScienceWorldAwarenessError("entity/request inference produced no candidates")

        candidates = candidates[:MAX_INFERENCE_CANDIDATES]
        top_candidate = sorted(candidates, key=lambda item: item.confidence, reverse=True)[0]
        can_select = top_candidate.confidence >= 0.45
        if ambiguous_request and top_candidate.confidence < 0.7:
            can_select = False
        selected_candidate_id = top_candidate.candidate_id if can_select else None

        inference_notes: list[str] = []
        if live_current_requested:
            inference_notes.append("live_current_requested_from_phase7")
        if ambiguous_request:
            inference_notes.append("ambiguity_detected_from_phase7")
        if bool(interpretation.get("self_knowledge_requested")):
            inference_notes.append("self_knowledge_requested_from_phase7")
        if knowledge_gap_reason_hint == "needs_fresh_information":
            inference_notes.append("fresh_information_honesty_preserved")
        inference_notes.append(f"support_state_hint:{support_state_hint}")
        inference_notes.append(f"knowledge_gap_reason_hint:{knowledge_gap_reason_hint}")
        inference_notes = list(_unique_bounded(inference_notes, ceiling=MAX_REASON_CODES))

        payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "raw_text_hash": raw_text_hash,
            "normalized_text": normalized_text,
            "extracted_terms": list(extracted_terms),
            "candidate_count": len(candidates),
            "selected_candidate_id": selected_candidate_id,
            "candidates": [candidate.to_dict() for candidate in candidates],
            "science_topic_cues": list(science_cues),
            "hidden_variable_cues": list(hidden_cues),
            "support_state_hint": support_state_hint,
            "knowledge_gap_reason_hint": knowledge_gap_reason_hint,
            "inference_notes": list(inference_notes),
        }
        return EntityRequestInferenceSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            raw_text_hash=raw_text_hash,
            normalized_text=normalized_text,
            extracted_terms=extracted_terms,
            candidate_count=len(candidates),
            selected_candidate_id=selected_candidate_id,
            candidates=tuple(candidates),
            science_topic_cues=science_cues,
            hidden_variable_cues=hidden_cues,
            support_state_hint=support_state_hint,
            knowledge_gap_reason_hint=knowledge_gap_reason_hint,
            inference_notes=tuple(inference_notes),
            inference_hash=stable_hash_payload(payload),
        )
