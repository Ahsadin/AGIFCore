from __future__ import annotations

import re
from typing import Any, Mapping

from .contracts import (
    MAX_CURRENT_WORLD_EVIDENCE_INPUTS,
    MAX_REASON_CODES,
    BoundedCurrentWorldSnapshot,
    CurrentWorldDecision,
    Phase8ScienceWorldAwarenessError,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

_TOKEN_RE = re.compile(r"[a-z0-9']+")
_EXACT_CURRENT_CUES = {
    "exact",
    "exactly",
    "current",
    "latest",
    "live",
    "now",
    "realtime",
    "right",
    "today",
}
_STATUS_CHECK_HINTS = {"status_check", "derived_estimate", "comparison", "unknown"}
_FRESH_GAP_REASONS = {"needs_fresh_information"}
_UNKNOWN_OR_WEAK_REASONS = {
    "ambiguous_request",
    "missing_local_evidence",
    "conflicting_state",
    "blocked_by_policy",
}


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _unique_bounded(values: list[str], *, ceiling: int) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        normalized = str(item).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
        if len(result) >= ceiling:
            break
    return tuple(result)


def _pick_inference_candidate(inference: Mapping[str, Any]) -> dict[str, Any] | None:
    candidates = [require_mapping(item, "entity_request_candidate") for item in list(inference.get("candidates", ()))]
    if not candidates:
        return None
    selected_id = str(inference.get("selected_candidate_id", "")).strip()
    if selected_id:
        for candidate in candidates:
            if str(candidate.get("candidate_id", "")).strip() == selected_id:
                return candidate
    return candidates[0]


def _collect_evidence_refs(
    *,
    inference: Mapping[str, Any],
    chain: Mapping[str, Any],
    support: Mapping[str, Any] | None,
) -> tuple[str, ...]:
    refs: list[str] = []
    refs.extend(
        [
            str(inference.get("inference_hash", "")).strip(),
            str(chain.get("chain_id", "")).strip(),
            str(chain.get("snapshot_hash", "")).strip(),
            str(chain.get("region_ref", "")).strip(),
            str(chain.get("usefulness_ref", "")).strip(),
            *[str(item).strip() for item in list(chain.get("principle_refs", ())) if str(item).strip()],
            *[str(item).strip() for item in list(chain.get("world_entity_refs", ())) if str(item).strip()],
            *[str(item).strip() for item in list(chain.get("simulation_refs", ())) if str(item).strip()],
        ]
    )
    for step in list(chain.get("steps", ())):
        step_map = require_mapping(step, "causal_chain_step")
        refs.extend(str(item).strip() for item in list(step_map.get("evidence_refs", ())) if str(item).strip())
    if support is not None:
        refs.extend(str(item).strip() for item in list(support.get("evidence_refs", ())) if str(item).strip())
        refs.extend(str(item).strip() for item in list(support.get("blocked_refs", ())) if str(item).strip())
        refs.extend(
            [
                str(support.get("memory_review_ref", "")).strip(),
                str(support.get("simulation_trace_ref", "")).strip(),
                str(support.get("critic_trace_ref", "")).strip(),
                str(support.get("governance_trace_ref", "")).strip(),
            ]
        )
    return _unique_bounded(refs, ceiling=MAX_CURRENT_WORLD_EVIDENCE_INPUTS)


def _strong_local_support(chain: Mapping[str, Any]) -> bool:
    has_world_anchor = bool(list(chain.get("world_entity_refs", ())))
    has_sim_anchor = bool(list(chain.get("simulation_refs", ())))
    has_usefulness = bool(str(chain.get("usefulness_ref", "")).strip())
    has_missing_variables = bool(list(chain.get("missing_variables", ())))
    chain_fail_closed = _to_bool(chain.get("fail_closed"))
    step_fail_closed_count = sum(
        1 for step in list(chain.get("steps", ())) if _to_bool(require_mapping(step, "causal_chain_step").get("fail_closed"))
    )
    return has_world_anchor and has_usefulness and (has_sim_anchor or not has_missing_variables) and not chain_fail_closed and step_fail_closed_count == 0


class BoundedCurrentWorldReasoningEngine:
    """Determine bounded-local support vs fail-closed freshness decisions for current-world requests."""

    SCHEMA = "agifcore.phase_08.bounded_current_world_reasoning.v1"

    def build_snapshot(
        self,
        *,
        entity_request_inference_state: Mapping[str, Any],
        causal_chain_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any] | None = None,
    ) -> BoundedCurrentWorldSnapshot:
        inference = require_schema(
            entity_request_inference_state,
            "agifcore.phase_08.entity_request_inference.v1",
            "entity_request_inference_state",
        )
        chain = require_schema(
            causal_chain_state,
            "agifcore.phase_08.causal_chain_reasoning.v1",
            "causal_chain_state",
        )
        support: dict[str, Any] | None = None
        if support_state_resolution_state is not None:
            support = require_schema(
                support_state_resolution_state,
                "agifcore.phase_07.support_state_logic.v1",
                "support_state_resolution_state",
            )

        conversation_id = require_non_empty_str(inference.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(inference.get("turn_id"), "turn_id")
        request_id = f"{conversation_id}::{turn_id}"
        if str(chain.get("request_id", "")).strip() != request_id:
            raise Phase8ScienceWorldAwarenessError("causal_chain_state request_id must match inference request_id")

        selected_candidate = _pick_inference_candidate(inference)
        candidate_request_type = str(selected_candidate.get("request_type", "")).strip() if selected_candidate is not None else ""
        live_current_requested = _to_bool(selected_candidate.get("live_current_requested")) if selected_candidate is not None else False
        normalized_text = str(inference.get("normalized_text", "")).strip().lower()
        token_set = set(_tokens(normalized_text))

        support_state_hint = str(inference.get("support_state_hint", "")).strip().lower()
        knowledge_gap_reason_hint = str(inference.get("knowledge_gap_reason_hint", "")).strip().lower()
        next_action = ""
        if support is not None:
            support_state_hint = str(support.get("support_state", support_state_hint)).strip().lower() or support_state_hint
            knowledge_gap_reason_hint = (
                str(support.get("knowledge_gap_reason", knowledge_gap_reason_hint)).strip().lower() or knowledge_gap_reason_hint
            )
            next_action = str(support.get("next_action", "")).strip().lower()

        if "current" in token_set or "latest" in token_set or "today" in token_set or "now" in token_set:
            live_current_requested = True
        if support_state_hint == "search_needed" or knowledge_gap_reason_hint in _FRESH_GAP_REASONS:
            live_current_requested = True

        exact_current_fact_requested = bool(token_set.intersection(_EXACT_CURRENT_CUES)) and (
            live_current_requested or candidate_request_type in _STATUS_CHECK_HINTS
        )
        chain_fail_closed = _to_bool(chain.get("fail_closed"))
        strong_local_support = _strong_local_support(chain)

        reason_codes: list[str] = [
            f"support_state_hint:{support_state_hint or 'unknown'}",
            f"knowledge_gap_reason_hint:{knowledge_gap_reason_hint or 'none'}",
            f"request_type:{candidate_request_type or 'unknown'}",
            "no_external_search_execution",
        ]
        bounded_local_support_refs: tuple[str, ...] = ()
        needs_fresh_information = False
        live_measurement_required = False
        exact_current_fact_allowed = False

        if not live_current_requested:
            decision = CurrentWorldDecision.NOT_CURRENT_WORLD_REQUEST
            reason_codes.append("not_current_world_request")
        elif knowledge_gap_reason_hint in _FRESH_GAP_REASONS or support_state_hint == "search_needed" or next_action == "search_external":
            needs_fresh_information = True
            if exact_current_fact_requested:
                decision = CurrentWorldDecision.LIVE_MEASUREMENT_REQUIRED
                live_measurement_required = True
                reason_codes.append("exact_current_fact_requires_live_measurement")
            else:
                decision = CurrentWorldDecision.NEEDS_FRESH_INFORMATION
                reason_codes.append("fresh_information_required_by_phase7_honesty")
        elif exact_current_fact_requested and not strong_local_support:
            decision = CurrentWorldDecision.LIVE_MEASUREMENT_REQUIRED
            live_measurement_required = True
            needs_fresh_information = True
            reason_codes.append("unsupported_exact_current_fact_fail_closed")
        elif support_state_hint == "unknown" or knowledge_gap_reason_hint in _UNKNOWN_OR_WEAK_REASONS or chain_fail_closed:
            decision = CurrentWorldDecision.INSUFFICIENT_LOCAL_EVIDENCE
            reason_codes.append("insufficient_local_evidence")
        elif strong_local_support:
            decision = CurrentWorldDecision.BOUNDED_LOCAL_SUPPORT
            bounded_local_support_refs = _unique_bounded(
                [
                    str(chain.get("chain_id", "")).strip(),
                    str(chain.get("region_ref", "")).strip(),
                    str(chain.get("usefulness_ref", "")).strip(),
                    *[str(item).strip() for item in list(chain.get("world_entity_refs", ())) if str(item).strip()],
                    *[str(item).strip() for item in list(chain.get("simulation_refs", ())) if str(item).strip()],
                ],
                ceiling=MAX_CURRENT_WORLD_EVIDENCE_INPUTS,
            )
            exact_current_fact_allowed = not exact_current_fact_requested
            reason_codes.append("bounded_local_support_available")
            if exact_current_fact_requested:
                reason_codes.append("exact_current_fact_not_allowed_without_fresh_measurement")
        else:
            decision = CurrentWorldDecision.INSUFFICIENT_LOCAL_EVIDENCE
            reason_codes.append("bounded_support_below_threshold")

        evidence_refs = _collect_evidence_refs(inference=inference, chain=chain, support=support)
        payload = {
            "schema": self.SCHEMA,
            "request_id": request_id,
            "decision": decision.value,
            "live_current_requested": live_current_requested,
            "needs_fresh_information": needs_fresh_information,
            "live_measurement_required": live_measurement_required,
            "exact_current_fact_allowed": exact_current_fact_allowed,
            "bounded_local_support_refs": list(bounded_local_support_refs),
            "evidence_refs": list(evidence_refs),
            "evidence_input_count": len(evidence_refs),
            "reason_codes": list(_unique_bounded(reason_codes, ceiling=MAX_REASON_CODES)),
        }
        return BoundedCurrentWorldSnapshot(
            schema=self.SCHEMA,
            request_id=request_id,
            decision=decision,
            live_current_requested=live_current_requested,
            needs_fresh_information=needs_fresh_information,
            live_measurement_required=live_measurement_required,
            exact_current_fact_allowed=exact_current_fact_allowed,
            bounded_local_support_refs=bounded_local_support_refs,
            evidence_refs=evidence_refs,
            evidence_input_count=len(evidence_refs),
            reason_codes=_unique_bounded(reason_codes, ceiling=MAX_REASON_CODES),
            snapshot_hash=stable_hash_payload(payload),
        )
