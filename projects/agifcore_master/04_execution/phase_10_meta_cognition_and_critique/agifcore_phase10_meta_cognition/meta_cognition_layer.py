from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    CritiqueOutcome,
    MetaCognitionLayerSnapshot,
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


class MetaCognitionLayerEngine:
    """Coordinate Phase 10 critique outputs without taking over response realization."""

    SCHEMA = "agifcore.phase_10.meta_cognition_layer.v1"

    def build_snapshot(
        self,
        *,
        self_model_state: Mapping[str, Any],
        meta_cognition_observer_state: Mapping[str, Any],
        attention_redirect_state: Mapping[str, Any],
        skeptic_counterexample_state: Mapping[str, Any],
        strategy_journal_state: Mapping[str, Any],
        thinker_tissue_state: Mapping[str, Any],
        surprise_engine_state: Mapping[str, Any],
        theory_fragments_state: Mapping[str, Any],
        weak_answer_diagnosis_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
    ) -> MetaCognitionLayerSnapshot:
        self_model = require_schema(self_model_state, "agifcore.phase_10.self_model.v1", "self_model_state")
        observer = require_schema(meta_cognition_observer_state, "agifcore.phase_10.meta_cognition_observer.v1", "meta_cognition_observer_state")
        redirect = require_schema(attention_redirect_state, "agifcore.phase_10.attention_redirect.v1", "attention_redirect_state")
        skeptic = require_schema(skeptic_counterexample_state, "agifcore.phase_10.skeptic_counterexample.v1", "skeptic_counterexample_state")
        journal = require_schema(strategy_journal_state, "agifcore.phase_10.strategy_journal.v1", "strategy_journal_state")
        thinker = require_schema(thinker_tissue_state, "agifcore.phase_10.thinker_tissue.v1", "thinker_tissue_state")
        surprise = require_schema(surprise_engine_state, "agifcore.phase_10.surprise_engine.v1", "surprise_engine_state")
        fragments = require_schema(theory_fragments_state, "agifcore.phase_10.theory_fragments.v1", "theory_fragments_state")
        diagnosis = require_schema(weak_answer_diagnosis_state, "agifcore.phase_10.weak_answer_diagnosis.v1", "weak_answer_diagnosis_state")
        support = require_schema(support_state_resolution_state, "agifcore.phase_07.support_state_logic.v1", "support_state_resolution_state")

        turn_id = require_non_empty_str(str(self_model.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        diagnosis_kinds = {str(item.get("kind", "")).strip() for item in list(diagnosis.get("items", ())) if isinstance(item, Mapping)}
        surprise_events = list(surprise.get("events", ()))
        skeptic_changed = any(bool(item.get("changed_answer_after_skeptic")) for item in list(skeptic.get("branches", ())) if isinstance(item, Mapping))

        if any(bool(item.get("detected_contradiction")) for item in surprise_events if isinstance(item, Mapping)) and skeptic_changed:
            selected_outcome = CritiqueOutcome.ABSTAIN
        elif support_state in {"search_needed", "unknown"} and redirect.get("redirect_count", 0):
            selected_outcome = CritiqueOutcome.RECHECK_SUPPORT
        elif "vague_explanation" in diagnosis_kinds:
            selected_outcome = CritiqueOutcome.REFRAME_EXPLANATION
        elif "missing_variable" in diagnosis_kinds:
            selected_outcome = CritiqueOutcome.CLARIFY
        else:
            selected_outcome = CritiqueOutcome.NO_REDIRECT

        active_modules = _clean_items(
            [
                "self_model" if self_model.get("record_count", 0) else "",
                "meta_cognition_observer" if observer.get("observation_count", 0) else "",
                "attention_redirect" if redirect.get("redirect_count", 0) else "",
                "skeptic_counterexample" if skeptic.get("branch_count", 0) else "",
                "strategy_journal" if journal.get("entry_count", 0) else "",
                "thinker_tissue" if thinker.get("item_count", 0) else "",
                "surprise_engine" if surprise.get("event_count", 0) else "",
                "theory_fragments" if fragments.get("fragment_count", 0) else "",
                "weak_answer_diagnosis" if diagnosis.get("item_count", 0) else "",
            ],
            ceiling=9,
        )
        outcome_notes = _clean_items(
            [
                f"selected_outcome={selected_outcome.value}",
                f"support_state={support_state}",
                "Phase 10 stays read-only over Phase 7, 8, and 9 snapshots.",
            ],
            ceiling=6,
        )
        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "selected_outcome": selected_outcome.value,
            "redirect_required": selected_outcome is not CritiqueOutcome.NO_REDIRECT,
            "active_modules": list(active_modules),
            "outcome_notes": list(outcome_notes),
        }
        return MetaCognitionLayerSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            selected_outcome=selected_outcome,
            redirect_required=selected_outcome is not CritiqueOutcome.NO_REDIRECT,
            active_modules=active_modules,
            outcome_notes=outcome_notes,
            snapshot_hash=stable_hash_payload(payload),
        )
