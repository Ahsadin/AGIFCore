from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_CURRENT_WORLD_EVIDENCE_INPUTS,
    MAX_SUMMARY_ITEMS_PER_FIELD,
    MAX_VISIBLE_REASONING_CHARACTERS,
    CurrentWorldDecision,
    Phase8ScienceWorldAwarenessError,
    UncertaintyBand,
    VisibleReasoningSummary,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)


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


def _clip(text: str, *, max_chars: int = 160) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[: max_chars - 1].rstrip() + "…"


def _decision_code(current: Mapping[str, Any]) -> CurrentWorldDecision:
    raw = str(current.get("decision", "")).strip()
    try:
        return CurrentWorldDecision(raw)
    except ValueError as exc:
        raise Phase8ScienceWorldAwarenessError(
            f"bounded_current_world_reasoning_state decision is invalid: {raw!r}"
        ) from exc


def _uncertainty_band(*, chain_fail_closed: bool, decision: CurrentWorldDecision, missing_count: int) -> UncertaintyBand:
    if decision in {
        CurrentWorldDecision.NEEDS_FRESH_INFORMATION,
        CurrentWorldDecision.LIVE_MEASUREMENT_REQUIRED,
        CurrentWorldDecision.INSUFFICIENT_LOCAL_EVIDENCE,
    }:
        return UncertaintyBand.HIGH
    if chain_fail_closed or missing_count > 0:
        return UncertaintyBand.MODERATE
    return UncertaintyBand.LOW


def _character_count(
    *,
    what_is_known: tuple[str, ...],
    what_is_inferred: tuple[str, ...],
    uncertainty: tuple[str, ...],
    what_would_verify: tuple[str, ...],
) -> int:
    rendered = (
        f"what_is_known: {' | '.join(what_is_known)}\n"
        f"what_is_inferred: {' | '.join(what_is_inferred)}\n"
        f"uncertainty: {' | '.join(uncertainty)}\n"
        f"what_would_verify: {' | '.join(what_would_verify)}"
    )
    return len(rendered)


def _enforce_ceiling(
    *,
    what_is_known: tuple[str, ...],
    what_is_inferred: tuple[str, ...],
    uncertainty: tuple[str, ...],
    what_would_verify: tuple[str, ...],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...], tuple[str, ...], int]:
    known = list(what_is_known)
    inferred = list(what_is_inferred)
    uncertain = list(uncertainty)
    verify = list(what_would_verify)

    def count() -> int:
        return _character_count(
            what_is_known=tuple(known),
            what_is_inferred=tuple(inferred),
            uncertainty=tuple(uncertain),
            what_would_verify=tuple(verify),
        )

    while count() > MAX_VISIBLE_REASONING_CHARACTERS:
        if len(verify) > 1:
            verify.pop()
            continue
        if len(uncertain) > 1:
            uncertain.pop()
            continue
        if len(inferred) > 1:
            inferred.pop()
            continue
        if len(known) > 1:
            known.pop()
            continue

        known[0] = _clip(known[0], max_chars=max(40, len(known[0]) - 20))
        inferred[0] = _clip(inferred[0], max_chars=max(40, len(inferred[0]) - 20))
        uncertain[0] = _clip(uncertain[0], max_chars=max(40, len(uncertain[0]) - 20))
        verify[0] = _clip(verify[0], max_chars=max(40, len(verify[0]) - 20))
        if count() <= MAX_VISIBLE_REASONING_CHARACTERS:
            break
        if all(len(item) <= 40 for item in [known[0], inferred[0], uncertain[0], verify[0]]):
            raise Phase8ScienceWorldAwarenessError(
                "visible reasoning summary could not be reduced under the Phase 8 character ceiling"
            )

    final_count = count()
    if final_count > MAX_VISIBLE_REASONING_CHARACTERS:
        raise Phase8ScienceWorldAwarenessError(
            f"visible reasoning summary exceeds the Phase 8 ceiling of {MAX_VISIBLE_REASONING_CHARACTERS}"
        )
    return tuple(known), tuple(inferred), tuple(uncertain), tuple(verify), final_count


class VisibleReasoningSummaryEngine:
    """Build a bounded public reasoning summary from Phase 8 chain and current-world snapshots."""

    SCHEMA = "agifcore.phase_08.visible_reasoning_summaries.v1"

    def build_summary(
        self,
        *,
        causal_chain_state: Mapping[str, Any],
        bounded_current_world_reasoning_state: Mapping[str, Any],
    ) -> VisibleReasoningSummary:
        chain = require_schema(
            causal_chain_state,
            "agifcore.phase_08.causal_chain_reasoning.v1",
            "causal_chain_state",
        )
        current = require_schema(
            bounded_current_world_reasoning_state,
            "agifcore.phase_08.bounded_current_world_reasoning.v1",
            "bounded_current_world_reasoning_state",
        )

        request_id = require_non_empty_str(chain.get("request_id"), "request_id")
        if str(current.get("request_id", "")).strip() != request_id:
            raise Phase8ScienceWorldAwarenessError(
                "bounded_current_world_reasoning_state request_id must match causal_chain_state request_id"
            )

        chain_id = require_non_empty_str(chain.get("chain_id"), "causal_chain_state.chain_id")
        decision = _decision_code(current)
        chain_fail_closed = _to_bool(chain.get("fail_closed"))
        live_measurement_required = _to_bool(current.get("live_measurement_required"))

        principle_refs = _unique_bounded(
            [str(item).strip() for item in list(chain.get("principle_refs", ())) if str(item).strip()],
            ceiling=MAX_SUMMARY_ITEMS_PER_FIELD,
        )
        world_entity_refs = _unique_bounded(
            [str(item).strip() for item in list(chain.get("world_entity_refs", ())) if str(item).strip()],
            ceiling=MAX_SUMMARY_ITEMS_PER_FIELD,
        )
        simulation_refs = _unique_bounded(
            [str(item).strip() for item in list(chain.get("simulation_refs", ())) if str(item).strip()],
            ceiling=MAX_SUMMARY_ITEMS_PER_FIELD,
        )
        missing_variables = _unique_bounded(
            [str(item).strip() for item in list(chain.get("missing_variables", ())) if str(item).strip()],
            ceiling=MAX_SUMMARY_ITEMS_PER_FIELD,
        )

        known_items: list[str] = [
            f"Current-world decision: {decision.value}.",
            f"Causal chain anchor: {chain_id}.",
        ]
        if world_entity_refs:
            known_items.append(f"World evidence anchor: {world_entity_refs[0]}.")
        if str(chain.get("region_ref", "")).strip():
            known_items.append(f"Region anchor: {str(chain.get('region_ref')).strip()}.")

        inferred_items: list[str] = []
        if principle_refs:
            inferred_items.append(f"Applied principle references: {', '.join(principle_refs)}.")
        if simulation_refs:
            inferred_items.append(f"Simulation support references: {', '.join(simulation_refs)}.")
        if not inferred_items:
            inferred_items.append("No high-confidence derived inference beyond bounded evidence anchors.")

        uncertainty_items: list[str] = []
        weakest_link_reason = str(chain.get("weakest_link_reason", "")).strip() or "none_detected"
        uncertainty_items.append(f"Weakest-link reason: {weakest_link_reason}.")
        if missing_variables:
            uncertainty_items.append(f"Missing variables: {', '.join(missing_variables)}.")
        if chain_fail_closed:
            uncertainty_items.append("At least one causal step is fail-closed.")
        if decision in {
            CurrentWorldDecision.NEEDS_FRESH_INFORMATION,
            CurrentWorldDecision.LIVE_MEASUREMENT_REQUIRED,
            CurrentWorldDecision.INSUFFICIENT_LOCAL_EVIDENCE,
        }:
            uncertainty_items.append("Local evidence is insufficient for high-confidence current-world claims.")
        if not uncertainty_items:
            uncertainty_items.append("No additional uncertainty flags were raised in bounded checks.")

        verify_items: list[str] = []
        if live_measurement_required:
            verify_items.append("Collect a fresh live measurement for the target entity and region.")
        if decision is CurrentWorldDecision.NEEDS_FRESH_INFORMATION:
            verify_items.append("Fetch updated external evidence before asserting current status.")
        for variable in missing_variables:
            verify_items.append(f"Resolve missing variable: {variable}.")
            if len(verify_items) >= MAX_SUMMARY_ITEMS_PER_FIELD:
                break
        if not verify_items:
            verify_items.append("Re-run bounded reasoning after state changes and confirm stable evidence refs.")

        what_is_known = _unique_bounded(
            [_clip(item) for item in known_items],
            ceiling=MAX_SUMMARY_ITEMS_PER_FIELD,
        )
        what_is_inferred = _unique_bounded(
            [_clip(item) for item in inferred_items],
            ceiling=MAX_SUMMARY_ITEMS_PER_FIELD,
        )
        uncertainty = _unique_bounded(
            [_clip(item) for item in uncertainty_items],
            ceiling=MAX_SUMMARY_ITEMS_PER_FIELD,
        )
        what_would_verify = _unique_bounded(
            [_clip(item) for item in verify_items],
            ceiling=MAX_SUMMARY_ITEMS_PER_FIELD,
        )

        if not what_is_known:
            what_is_known = ("Bounded reasoning completed with minimal known anchors.",)
        if not what_is_inferred:
            what_is_inferred = ("No derived inference available.",)
        if not uncertainty:
            uncertainty = ("Uncertainty was not explicitly reported.",)
        if not what_would_verify:
            what_would_verify = ("No additional verification step was identified.",)

        what_is_known, what_is_inferred, uncertainty, what_would_verify, character_count = _enforce_ceiling(
            what_is_known=what_is_known,
            what_is_inferred=what_is_inferred,
            uncertainty=uncertainty,
            what_would_verify=what_would_verify,
        )

        uncertainty_band = _uncertainty_band(
            chain_fail_closed=chain_fail_closed,
            decision=decision,
            missing_count=len(missing_variables),
        )
        evidence_refs = _unique_bounded(
            [
                chain_id,
                str(chain.get("snapshot_hash", "")).strip(),
                str(current.get("snapshot_hash", "")).strip(),
                str(chain.get("region_ref", "")).strip(),
                str(chain.get("usefulness_ref", "")).strip(),
                *[str(item).strip() for item in list(current.get("bounded_local_support_refs", ())) if str(item).strip()],
                *[str(item).strip() for item in list(current.get("evidence_refs", ())) if str(item).strip()],
                *[str(item).strip() for item in list(chain.get("world_entity_refs", ())) if str(item).strip()],
                *[str(item).strip() for item in list(chain.get("simulation_refs", ())) if str(item).strip()],
                *[str(item).strip() for item in list(chain.get("principle_refs", ())) if str(item).strip()],
            ],
            ceiling=MAX_CURRENT_WORLD_EVIDENCE_INPUTS,
        )

        payload = {
            "schema": self.SCHEMA,
            "request_id": request_id,
            "what_is_known": list(what_is_known),
            "what_is_inferred": list(what_is_inferred),
            "uncertainty": list(uncertainty),
            "what_would_verify": list(what_would_verify),
            "principle_refs": list(principle_refs),
            "causal_chain_ref": chain_id,
            "uncertainty_band": uncertainty_band.value,
            "live_measurement_required": live_measurement_required,
            "character_count": character_count,
            "evidence_refs": list(evidence_refs),
        }

        return VisibleReasoningSummary(
            schema=self.SCHEMA,
            request_id=request_id,
            what_is_known=what_is_known,
            what_is_inferred=what_is_inferred,
            uncertainty=uncertainty,
            what_would_verify=what_would_verify,
            principle_refs=principle_refs,
            causal_chain_ref=chain_id,
            uncertainty_band=uncertainty_band,
            live_measurement_required=live_measurement_required,
            character_count=character_count,
            evidence_refs=evidence_refs,
            summary_hash=stable_hash_payload(payload),
        )

