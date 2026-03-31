from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_THINKER_TISSUE_ITEMS,
    ThinkerTissueRecord,
    ThinkerTissueSnapshot,
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


def _record(
    *,
    watched_failures: tuple[str, ...],
    watched_weak_answers: tuple[str, ...],
    watched_repeated_uncertainty: tuple[str, ...],
    asked_what_is_missing: tuple[str, ...],
    bounded_proposals: tuple[str, ...],
    governance_mode: str,
) -> ThinkerTissueRecord:
    payload = {
        "watched_failures": list(watched_failures),
        "watched_weak_answers": list(watched_weak_answers),
        "watched_repeated_uncertainty": list(watched_repeated_uncertainty),
        "asked_what_is_missing": list(asked_what_is_missing),
        "bounded_proposals": list(bounded_proposals),
        "governance_mode": governance_mode,
    }
    return ThinkerTissueRecord(
        record_id=make_trace_ref("thinker_tissue", payload),
        watched_failures=watched_failures,
        watched_weak_answers=watched_weak_answers,
        watched_repeated_uncertainty=watched_repeated_uncertainty,
        asked_what_is_missing=asked_what_is_missing,
        bounded_proposals=bounded_proposals,
        governance_mode=governance_mode,
        record_hash=stable_hash_payload(payload),
    )


class ThinkerTissueEngine:
    """Aggregate bounded critique signals without becoming an unrestricted self-edit loop."""

    SCHEMA = "agifcore.phase_10.thinker_tissue.v1"

    def build_snapshot(
        self,
        *,
        meta_cognition_observer_state: Mapping[str, Any],
        weak_answer_diagnosis_state: Mapping[str, Any],
        skeptic_counterexample_state: Mapping[str, Any],
    ) -> ThinkerTissueSnapshot:
        observer = require_schema(
            meta_cognition_observer_state,
            "agifcore.phase_10.meta_cognition_observer.v1",
            "meta_cognition_observer_state",
        )
        diagnosis = require_schema(
            weak_answer_diagnosis_state,
            "agifcore.phase_10.weak_answer_diagnosis.v1",
            "weak_answer_diagnosis_state",
        )
        skeptic = require_schema(
            skeptic_counterexample_state,
            "agifcore.phase_10.skeptic_counterexample.v1",
            "skeptic_counterexample_state",
        )

        turn_id = require_non_empty_str(str(observer.get("turn_id", "")).strip(), "turn_id")
        failures = [str(item.get("detail", "")).strip() for item in list(observer.get("observations", ())) if isinstance(item, Mapping) and str(item.get("detail", "")).strip()]
        weak_answers = [str(item.get("kind", "")).strip() for item in list(diagnosis.get("items", ())) if isinstance(item, Mapping) and str(item.get("kind", "")).strip()]
        repeated_uncertainty = [str(item).strip() for item in list(observer.get("repeated_uncertainty_signals", ())) if str(item).strip()]
        missing = [str(item).strip() for item in list(observer.get("missing_needs", ())) if str(item).strip()]
        skeptic_prompts = [
            str(item.get("what_variable_could_flip_the_answer", "")).strip()
            for item in list(skeptic.get("branches", ()))
            if isinstance(item, Mapping) and str(item.get("what_variable_could_flip_the_answer", "")).strip()
        ]

        record = _record(
            watched_failures=_clean_items(failures or ["no watched failure"], ceiling=MAX_THINKER_TISSUE_ITEMS),
            watched_weak_answers=_clean_items(weak_answers or ["no weak-answer flag"], ceiling=MAX_THINKER_TISSUE_ITEMS),
            watched_repeated_uncertainty=_clean_items(repeated_uncertainty or ["no repeated uncertainty"], ceiling=MAX_THINKER_TISSUE_ITEMS),
            asked_what_is_missing=_clean_items(missing + skeptic_prompts, ceiling=MAX_THINKER_TISSUE_ITEMS),
            bounded_proposals=_clean_items(
                [
                    "recheck support before stronger claims",
                    "preserve uncertainty in the public explanation",
                    "stop if contradiction survives the re-check",
                ],
                ceiling=MAX_THINKER_TISSUE_ITEMS,
            ),
            governance_mode="bounded_meta_cognition",
        )
        item_count = min(
            MAX_THINKER_TISSUE_ITEMS,
            len(record.watched_failures)
            + len(record.watched_weak_answers)
            + len(record.watched_repeated_uncertainty),
        )
        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "item_count": item_count,
            "records": [record.to_dict()],
        }
        return ThinkerTissueSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            item_count=item_count,
            records=(record,),
            snapshot_hash=stable_hash_payload(payload),
        )
