from __future__ import annotations

import re
from typing import Any, Mapping

from .contracts import (
    MAX_MATCHED_TERMS,
    MAX_REASON_CODES,
    MAX_REGION_CANDIDATES,
    Phase8ScienceWorldAwarenessError,
    RegionKind,
    WorldRegionCandidate,
    WorldRegionSelectionSnapshot,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

_TOKEN_RE = re.compile(r"[a-z0-9']+")


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _unique_bounded(values: list[str], *, ceiling: int) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        value = str(item).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
        if len(result) >= ceiling:
            break
    return tuple(result)


def _to_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _overlap_terms(left: list[str], right: set[str], *, limit: int = MAX_MATCHED_TERMS) -> tuple[str, ...]:
    matched = [term for term in left if term in right]
    return _unique_bounded(matched, ceiling=limit)


def _pick_inference_candidate(inference: Mapping[str, Any]) -> dict[str, Any] | None:
    candidates = [require_mapping(item, "entity_request_candidate") for item in list(inference.get("candidates", ()))]
    if not candidates:
        return None
    selected_id = str(inference.get("selected_candidate_id", "")).strip()
    if selected_id:
        for candidate in candidates:
            if str(candidate.get("candidate_id", "")).strip() == selected_id:
                return candidate
    return max(candidates, key=lambda item: _to_float(item.get("confidence", 0.0)))


class WorldRegionSelectionEngine:
    """Select bounded world-region candidates from Phase 8 inference and Phase 6 read-only state."""

    SCHEMA = "agifcore.phase_08.world_region_selection.v1"

    def build_snapshot(
        self,
        *,
        entity_request_inference_state: Mapping[str, Any],
        target_domain_registry_state: Mapping[str, Any],
        world_model_state: Mapping[str, Any],
    ) -> WorldRegionSelectionSnapshot:
        inference = require_schema(
            entity_request_inference_state,
            "agifcore.phase_08.entity_request_inference.v1",
            "entity_request_inference_state",
        )
        target_domains = require_schema(
            target_domain_registry_state,
            "agifcore.phase_06.target_domains.v1",
            "target_domain_registry_state",
        )
        world_model = require_schema(
            world_model_state,
            "agifcore.phase_06.world_model.v1",
            "world_model_state",
        )

        conversation_id = require_non_empty_str(inference.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(inference.get("turn_id"), "turn_id")
        request_id = f"{conversation_id}::{turn_id}"

        normalized_text = str(inference.get("normalized_text", "")).strip().lower()
        extracted_terms = [
            str(item).strip().lower()
            for item in list(inference.get("extracted_terms", ()))
            if str(item).strip()
        ]
        cue_terms = [
            str(item).strip().lower()
            for item in list(inference.get("science_topic_cues", ()))
            if str(item).strip()
        ]
        query_terms = set(_tokens(normalized_text))
        query_terms.update(extracted_terms)
        query_terms.update(cue_terms)

        selected_inference = _pick_inference_candidate(inference)
        if selected_inference is None:
            raise Phase8ScienceWorldAwarenessError("entity_request_inference_state contains no candidates")

        selected_candidate_id = require_non_empty_str(
            selected_inference.get("candidate_id"), "selected_inference.candidate_id"
        )
        target_domain_hint = str(selected_inference.get("target_domain_hint", "")).strip() or None
        region_hint = str(selected_inference.get("region_hint", "")).strip().lower() or None
        entity_label = str(selected_inference.get("entity_label", "")).strip().lower() or None
        support_state_hint = str(inference.get("support_state_hint", "")).strip().lower()
        ambiguous_request = bool(selected_inference.get("ambiguous_request"))
        live_current_requested = bool(selected_inference.get("live_current_requested"))

        if region_hint:
            query_terms.update(_tokens(region_hint))
        if entity_label:
            query_terms.update(_tokens(entity_label))

        candidates_by_key: dict[tuple[str, str, str | None], WorldRegionCandidate] = {}
        domain_structures = [
            require_mapping(item, "target_domain_structure") for item in list(target_domains.get("structures", ()))
        ]
        world_entities = [require_mapping(item, "world_entity") for item in list(world_model.get("entities", ()))]

        for domain in domain_structures:
            domain_id = require_non_empty_str(domain.get("domain_id"), "target_domain_structure.domain_id")
            domain_name = require_non_empty_str(domain.get("domain_name"), "target_domain_structure.domain_name")
            descriptor_tokens = [
                str(item).strip().lower() for item in list(domain.get("descriptor_tokens", ())) if str(item).strip()
            ]
            name_tokens = _tokens(domain_name)

            reason_codes: list[str] = []
            score = 0.0
            matched_terms: list[str] = []
            supporting_refs = [f"phase6.target_domains::{domain_id}", selected_candidate_id]

            if target_domain_hint == domain_id:
                score += 0.56
                reason_codes.append("target_domain_hint_match")

            descriptor_matches = _overlap_terms(descriptor_tokens, query_terms)
            if descriptor_matches:
                matched_terms.extend(descriptor_matches)
                score += min(0.24, 0.12 * len(descriptor_matches))
                reason_codes.append("descriptor_token_overlap")

            name_matches = _overlap_terms(name_tokens, query_terms)
            if name_matches:
                matched_terms.extend(name_matches)
                score += min(0.18, 0.09 * len(name_matches))
                reason_codes.append("domain_name_overlap")

            if score <= 0.0:
                continue

            candidate_payload = {
                "request_id": request_id,
                "kind": RegionKind.TARGET_DOMAIN.value,
                "domain_id": domain_id,
                "domain_name": domain_name,
                "confidence": clamp_score(score),
                "matched_terms": list(_unique_bounded(matched_terms, ceiling=MAX_MATCHED_TERMS)),
                "reason_codes": list(_unique_bounded(reason_codes, ceiling=MAX_REASON_CODES)),
                "supporting_refs": supporting_refs,
            }
            candidate = WorldRegionCandidate(
                region_id=f"wrs::{request_id}::target::{len(candidates_by_key) + 1:02d}",
                region_label=domain_name,
                region_kind=RegionKind.TARGET_DOMAIN,
                target_domain=domain_id,
                supporting_refs=tuple(_unique_bounded(supporting_refs, ceiling=MAX_MATCHED_TERMS)),
                matched_terms=_unique_bounded(matched_terms, ceiling=MAX_MATCHED_TERMS),
                reason_codes=_unique_bounded(reason_codes, ceiling=MAX_REASON_CODES),
                confidence=candidate_payload["confidence"],
                candidate_hash=stable_hash_payload(candidate_payload),
            )
            key = (candidate.region_kind.value, candidate.region_label, candidate.target_domain)
            previous = candidates_by_key.get(key)
            if previous is None or candidate.confidence > previous.confidence:
                candidates_by_key[key] = candidate

        if region_hint:
            hint_tokens = _tokens(region_hint)
            matched = _overlap_terms(hint_tokens, query_terms)
            reason_codes = ["region_hint_from_inference", "active_context_hint"]
            score = clamp_score(0.52 + (0.04 * len(matched)))
            if target_domain_hint:
                score = clamp_score(score + 0.08)
                reason_codes.append("target_domain_context_present")
            candidate_payload = {
                "request_id": request_id,
                "kind": RegionKind.ACTIVE_CONTEXT.value,
                "region_hint": region_hint,
                "target_domain_hint": target_domain_hint,
                "confidence": score,
                "matched_terms": list(matched),
                "reason_codes": reason_codes,
                "supporting_refs": [selected_candidate_id],
            }
            candidate = WorldRegionCandidate(
                region_id=f"wrs::{request_id}::active::01",
                region_label=region_hint,
                region_kind=RegionKind.ACTIVE_CONTEXT,
                target_domain=target_domain_hint,
                supporting_refs=(selected_candidate_id,),
                matched_terms=matched,
                reason_codes=_unique_bounded(reason_codes, ceiling=MAX_REASON_CODES),
                confidence=score,
                candidate_hash=stable_hash_payload(candidate_payload),
            )
            key = (candidate.region_kind.value, candidate.region_label, candidate.target_domain)
            candidates_by_key[key] = candidate

        for entity in world_entities:
            target_domain = str(entity.get("target_domain", "")).strip() or None
            if target_domain is None:
                continue
            status = str(entity.get("status", "")).strip().lower()
            if status in {"blocked", "held"}:
                continue

            label = str(entity.get("label", "")).strip()
            if not label:
                continue
            label_tokens = _tokens(label)
            if not label_tokens:
                continue

            score = 0.14
            reason_codes: list[str] = []
            matched_terms = list(_overlap_terms(label_tokens, query_terms))
            if matched_terms:
                score += min(0.30, 0.10 * len(matched_terms))
                reason_codes.append("world_entity_label_overlap")

            if target_domain_hint and target_domain == target_domain_hint:
                score += 0.26
                reason_codes.append("world_entity_target_domain_match")
            if region_hint and any(token in label_tokens for token in _tokens(region_hint)):
                score += 0.18
                reason_codes.append("world_entity_region_hint_overlap")

            world_confidence = clamp_score(_to_float(entity.get("world_confidence"), 0.0))
            score += 0.20 * world_confidence
            if world_confidence >= 0.65:
                reason_codes.append("world_entity_confidence_support")
            if score < 0.32:
                continue

            entity_id = str(entity.get("entity_id", "")).strip()
            source_refs = [str(item).strip() for item in list(entity.get("source_refs", ())) if str(item).strip()]
            supporting_refs = [f"phase6.world_model::{entity_id}", selected_candidate_id, *source_refs[:2]]

            candidate_payload = {
                "request_id": request_id,
                "kind": RegionKind.WORLD_ENTITY.value,
                "entity_id": entity_id,
                "label": label,
                "target_domain": target_domain,
                "confidence": clamp_score(score),
                "matched_terms": matched_terms,
                "reason_codes": list(_unique_bounded(reason_codes, ceiling=MAX_REASON_CODES)),
                "supporting_refs": supporting_refs,
            }
            candidate = WorldRegionCandidate(
                region_id=f"wrs::{request_id}::entity::{len(candidates_by_key) + 1:02d}",
                region_label=label,
                region_kind=RegionKind.WORLD_ENTITY,
                target_domain=target_domain,
                supporting_refs=_unique_bounded(supporting_refs, ceiling=MAX_MATCHED_TERMS),
                matched_terms=_unique_bounded(matched_terms, ceiling=MAX_MATCHED_TERMS),
                reason_codes=_unique_bounded(reason_codes, ceiling=MAX_REASON_CODES),
                confidence=clamp_score(score),
                candidate_hash=stable_hash_payload(candidate_payload),
            )
            key = (candidate.region_kind.value, candidate.region_label, candidate.target_domain)
            previous = candidates_by_key.get(key)
            if previous is None or candidate.confidence > previous.confidence:
                candidates_by_key[key] = candidate

        ranked = sorted(
            candidates_by_key.values(),
            key=lambda item: (item.confidence, item.region_kind.value, item.region_label),
            reverse=True,
        )[:MAX_REGION_CANDIDATES]

        snapshot_reasons: list[str] = []
        if target_domain_hint:
            snapshot_reasons.append("target_domain_hint_available")
        if region_hint:
            snapshot_reasons.append("region_hint_available")
        if ambiguous_request:
            snapshot_reasons.append("ambiguous_request_from_inference")
        if live_current_requested:
            snapshot_reasons.append("live_current_requested_from_inference")
        if support_state_hint in {"search_needed", "unknown"}:
            snapshot_reasons.append(f"support_state_hint:{support_state_hint}")

        selected_region_id: str | None = None
        unresolved = True
        if ranked:
            safe_threshold = 0.6
            if ambiguous_request or support_state_hint in {"search_needed", "unknown"}:
                safe_threshold = 0.72
            top = ranked[0]
            if top.confidence >= safe_threshold:
                selected_region_id = top.region_id
                unresolved = False
                snapshot_reasons.append("safe_region_selected")
            else:
                snapshot_reasons.append("no_safe_region_above_threshold")
        else:
            snapshot_reasons.append("no_region_candidates_from_phase6_state")

        if unresolved:
            snapshot_reasons.append("unresolved_preserved")

        snapshot_payload = {
            "schema": self.SCHEMA,
            "request_id": request_id,
            "candidate_hashes": [candidate.candidate_hash for candidate in ranked],
            "selected_region_id": selected_region_id,
            "unresolved": unresolved,
            "reason_codes": list(_unique_bounded(snapshot_reasons, ceiling=MAX_REASON_CODES)),
        }
        return WorldRegionSelectionSnapshot(
            schema=self.SCHEMA,
            request_id=request_id,
            candidate_count=len(ranked),
            selected_region_id=selected_region_id,
            candidates=tuple(ranked),
            unresolved=unresolved,
            reason_codes=_unique_bounded(snapshot_reasons, ceiling=MAX_REASON_CODES),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
