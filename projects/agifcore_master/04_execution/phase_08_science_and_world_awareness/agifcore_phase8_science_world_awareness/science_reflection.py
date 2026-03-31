from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_REFLECTION_RECORDS,
    CurrentWorldDecision,
    Phase8ScienceWorldAwarenessError,
    ReflectionKind,
    ScienceReflectionRecord,
    ScienceReflectionSnapshot,
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


def _clip(text: str, *, max_chars: int = 220) -> str:
    cleaned = " ".join(str(text).split())
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


class ScienceReflectionEngine:
    """Build bounded post-run science reflection records under Phase 8 limits."""

    SCHEMA = "agifcore.phase_08.science_reflection.v1"

    def build_snapshot(
        self,
        *,
        scientific_priors_state: Mapping[str, Any],
        causal_chain_state: Mapping[str, Any],
        bounded_current_world_reasoning_state: Mapping[str, Any],
    ) -> ScienceReflectionSnapshot:
        priors = require_schema(
            scientific_priors_state,
            "agifcore.phase_08.scientific_priors.v1",
            "scientific_priors_state",
        )
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

        request_id = require_non_empty_str(chain.get("request_id"), "causal_chain_state.request_id")
        if str(priors.get("request_id", "")).strip() != request_id:
            raise Phase8ScienceWorldAwarenessError(
                "scientific_priors_state request_id must match causal_chain_state request_id"
            )
        if str(current.get("request_id", "")).strip() != request_id:
            raise Phase8ScienceWorldAwarenessError(
                "bounded_current_world_reasoning_state request_id must match causal_chain_state request_id"
            )

        chain_id = require_non_empty_str(chain.get("chain_id"), "causal_chain_state.chain_id")
        prior_snapshot_ref = (
            str(priors.get("snapshot_hash", "")).strip()
            or str(priors.get("selected_prior_ids", [request_id])[0]).strip()
            or request_id
        )
        current_snapshot_ref = (
            str(current.get("snapshot_hash", "")).strip()
            or str(current.get("decision", "")).strip()
            or request_id
        )

        decision = _decision_code(current)
        chain_fail_closed = _to_bool(chain.get("fail_closed"))
        missing_variables = [str(item).strip() for item in list(chain.get("missing_variables", ())) if str(item).strip()]

        selected_priors = [item for item in list(priors.get("selected_priors", ())) if isinstance(item, Mapping)]
        top_prior_score = 0.0
        top_prior_id = "none"
        if selected_priors:
            best = max(selected_priors, key=lambda item: float(item.get("relevance_score", 0.0)))
            top_prior_score = float(best.get("relevance_score", 0.0))
            top_prior_id = str(best.get("selection_id", "")).strip() or str(best.get("cell_id", "")).strip() or "unknown_prior"

        records: list[ScienceReflectionRecord] = []
        seen_keys: set[tuple[str, str, str]] = set()

        def add_record(
            *,
            kind: ReflectionKind,
            note: str,
            source_ref: str,
            next_step: str | None = None,
            increases_uncertainty: bool,
        ) -> None:
            if len(records) >= MAX_REFLECTION_RECORDS:
                return
            clean_note = _clip(require_non_empty_str(note, "science_reflection.note"))
            clean_source = require_non_empty_str(source_ref, "science_reflection.source_ref")
            clean_next = _clip(next_step) if next_step else None
            key = (kind.value, clean_note, clean_source)
            if key in seen_keys:
                return
            seen_keys.add(key)
            index = len(records) + 1
            payload = {
                "request_id": request_id,
                "record_index": index,
                "kind": kind.value,
                "note": clean_note,
                "source_ref": clean_source,
                "next_verification_step": clean_next,
                "increases_uncertainty": bool(increases_uncertainty),
            }
            records.append(
                ScienceReflectionRecord(
                    record_id=f"sr::{request_id}::{index:02d}",
                    kind=kind,
                    note=clean_note,
                    source_ref=clean_source,
                    next_verification_step=clean_next,
                    increases_uncertainty=bool(increases_uncertainty),
                    record_hash=stable_hash_payload(payload),
                )
            )

        if not selected_priors:
            add_record(
                kind=ReflectionKind.WEAK_PRIOR_CHOICE,
                note="No scientific prior was selected for this run, so mechanism grounding is weak.",
                source_ref=prior_snapshot_ref,
                next_step="Select at least one relevant prior cell before finalizing mechanism claims.",
                increases_uncertainty=True,
            )
        elif top_prior_score < 0.55:
            add_record(
                kind=ReflectionKind.WEAK_PRIOR_CHOICE,
                note=(
                    f"Top prior ({top_prior_id}) has low relevance score {top_prior_score:.3f}, "
                    "which weakens confidence in the causal path."
                ),
                source_ref=prior_snapshot_ref,
                next_step="Re-rank priors or add stronger domain-matched priors for this entity and request.",
                increases_uncertainty=True,
            )

        for variable in missing_variables:
            add_record(
                kind=ReflectionKind.MISSING_VARIABLE,
                note=f"Missing variable blocks bounded causal confidence: {variable}.",
                source_ref=chain_id,
                next_step=f"Measure or constrain variable '{variable}' and re-run causal reasoning.",
                increases_uncertainty=True,
            )

        if chain_fail_closed:
            add_record(
                kind=ReflectionKind.FALSIFIER,
                note="A fail-closed causal step is an active falsifier condition for this run.",
                source_ref=chain_id,
                next_step="Repair or replace fail-closed support before accepting the causal conclusion.",
                increases_uncertainty=True,
            )
        elif decision in {
            CurrentWorldDecision.NEEDS_FRESH_INFORMATION,
            CurrentWorldDecision.LIVE_MEASUREMENT_REQUIRED,
            CurrentWorldDecision.INSUFFICIENT_LOCAL_EVIDENCE,
        }:
            add_record(
                kind=ReflectionKind.FALSIFIER,
                note="A fresh measurement that contradicts local support would falsify this run.",
                source_ref=current_snapshot_ref,
                next_step="Acquire fresh evidence for the same entity/region and compare against current chain claims.",
                increases_uncertainty=True,
            )

        if decision is CurrentWorldDecision.LIVE_MEASUREMENT_REQUIRED:
            next_step = "Collect a live measurement now; do not claim exact current-world status without it."
        elif decision is CurrentWorldDecision.NEEDS_FRESH_INFORMATION:
            next_step = "Fetch updated external evidence, then replay bounded current-world reasoning."
        elif missing_variables:
            next_step = f"Resolve missing variable '{missing_variables[0]}' and rerun the chain."
        else:
            next_step = "Re-run bounded science reasoning after any new evidence update."
        add_record(
            kind=ReflectionKind.NEXT_VERIFICATION_STEP,
            note=f"Most immediate verification action: {next_step}",
            source_ref=current_snapshot_ref,
            next_step=next_step,
            increases_uncertainty=False,
        )

        uncertainty_triggers: list[str] = []
        if any(record.kind is ReflectionKind.WEAK_PRIOR_CHOICE for record in records):
            uncertainty_triggers.append("weak_prior_choice")
        if missing_variables:
            uncertainty_triggers.append("missing_variable")
        if chain_fail_closed:
            uncertainty_triggers.append("chain_fail_closed")
        if decision in {
            CurrentWorldDecision.NEEDS_FRESH_INFORMATION,
            CurrentWorldDecision.LIVE_MEASUREMENT_REQUIRED,
            CurrentWorldDecision.INSUFFICIENT_LOCAL_EVIDENCE,
        }:
            uncertainty_triggers.append(f"current_world_decision:{decision.value}")

        uncertainty_should_increase = bool(uncertainty_triggers)
        if uncertainty_should_increase:
            add_record(
                kind=ReflectionKind.UNCERTAINTY_INCREASE,
                note=f"Uncertainty should increase due to: {', '.join(uncertainty_triggers)}.",
                source_ref=current_snapshot_ref,
                next_step="Apply stricter answer limits until verification steps are completed.",
                increases_uncertainty=True,
            )

        payload = {
            "schema": self.SCHEMA,
            "request_id": request_id,
            "record_count": len(records),
            "records": [record.to_dict() for record in records],
            "uncertainty_should_increase": uncertainty_should_increase,
        }
        return ScienceReflectionSnapshot(
            schema=self.SCHEMA,
            request_id=request_id,
            record_count=len(records),
            records=tuple(records),
            uncertainty_should_increase=uncertainty_should_increase,
            reflection_hash=stable_hash_payload(payload),
        )
