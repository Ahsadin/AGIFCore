from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_SURPRISE_EVENTS,
    SurpriseEngineRecord,
    SurpriseEngineSnapshot,
    SurpriseTrigger,
    make_trace_ref,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)


def _record(
    *,
    detected_contradiction: bool,
    detected_missing_variable: bool,
    detected_boundary_failure: bool,
    detected_wrong_prior_choice: bool,
    detected_weak_causal_chain: bool,
    triggered_action: SurpriseTrigger,
    trigger_reason: str,
    supporting_refs: tuple[str, ...],
) -> SurpriseEngineRecord:
    payload = {
        "detected_contradiction": detected_contradiction,
        "detected_missing_variable": detected_missing_variable,
        "detected_boundary_failure": detected_boundary_failure,
        "detected_wrong_prior_choice": detected_wrong_prior_choice,
        "detected_weak_causal_chain": detected_weak_causal_chain,
        "triggered_action": triggered_action.value,
        "trigger_reason": trigger_reason,
        "supporting_refs": list(supporting_refs),
    }
    return SurpriseEngineRecord(
        event_id=make_trace_ref("surprise_event", payload),
        detected_contradiction=detected_contradiction,
        detected_missing_variable=detected_missing_variable,
        detected_boundary_failure=detected_boundary_failure,
        detected_wrong_prior_choice=detected_wrong_prior_choice,
        detected_weak_causal_chain=detected_weak_causal_chain,
        triggered_action=triggered_action,
        trigger_reason=trigger_reason,
        supporting_refs=supporting_refs,
        record_hash=stable_hash_payload(payload),
    )


class SurpriseEngine:
    """Detect contradiction and anomaly signals and emit only bounded follow-up actions."""

    SCHEMA = "agifcore.phase_10.surprise_engine.v1"

    def build_snapshot(
        self,
        *,
        meta_cognition_observer_state: Mapping[str, Any],
        skeptic_counterexample_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        science_world_turn_state: Mapping[str, Any],
    ) -> SurpriseEngineSnapshot:
        observer = require_schema(
            meta_cognition_observer_state,
            "agifcore.phase_10.meta_cognition_observer.v1",
            "meta_cognition_observer_state",
        )
        skeptic = require_schema(
            skeptic_counterexample_state,
            "agifcore.phase_10.skeptic_counterexample.v1",
            "skeptic_counterexample_state",
        )
        support = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )
        science_world_turn = require_schema(
            science_world_turn_state,
            "agifcore.phase_08.science_world_turn.v1",
            "science_world_turn_state",
        )
        visible_reasoning = require_schema(
            science_world_turn.get("visible_reasoning_summary", {}),
            "agifcore.phase_08.visible_reasoning_summaries.v1",
            "science_world_turn_state.visible_reasoning_summary",
        )
        science_reflection = require_schema(
            science_world_turn.get("science_reflection", {}),
            "agifcore.phase_08.science_reflection.v1",
            "science_world_turn_state.science_reflection",
        )
        entity_request = require_schema(
            science_world_turn.get("entity_request_inference", {}),
            "agifcore.phase_08.entity_request_inference.v1",
            "science_world_turn_state.entity_request_inference",
        )

        turn_id = require_non_empty_str(str(observer.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        contradiction = any("contradiction" in str(record.get("kind", "")).lower() or "contradiction" in str(record.get("note", "")).lower() for record in list(science_reflection.get("records", ())) if isinstance(record, Mapping))
        missing_variable = bool(list(entity_request.get("hidden_variable_cues", ()))) or bool(list(visible_reasoning.get("uncertainty", ())))
        boundary_failure = support_state in {"search_needed", "unknown"}
        wrong_prior_choice = any("wrong_prior" in str(record.get("kind", "")).lower() for record in list(science_reflection.get("records", ())) if isinstance(record, Mapping))
        weak_causal_chain = "causal_chain_ref" in visible_reasoning and not str(visible_reasoning.get("causal_chain_ref", "")).strip()
        changed_after_skeptic = any(bool(item.get("changed_answer_after_skeptic")) for item in list(skeptic.get("branches", ())) if isinstance(item, Mapping))
        evidence_refs = tuple(str(item).strip() for item in list(visible_reasoning.get("evidence_refs", ())) if str(item).strip())[:4]

        events: list[SurpriseEngineRecord] = []
        if contradiction:
            if changed_after_skeptic or boundary_failure:
                triggered_action = SurpriseTrigger.HONEST_FALLBACK
            elif missing_variable or wrong_prior_choice or weak_causal_chain:
                triggered_action = SurpriseTrigger.THEORY_FRAGMENT_CANDIDATE
            else:
                triggered_action = SurpriseTrigger.RECHECK_SUPPORT
            events.append(
                _record(
                    detected_contradiction=True,
                    detected_missing_variable=missing_variable,
                    detected_boundary_failure=boundary_failure,
                    detected_wrong_prior_choice=wrong_prior_choice,
                    detected_weak_causal_chain=weak_causal_chain,
                    triggered_action=triggered_action,
                    trigger_reason="contradiction signal reached the surprise engine",
                    supporting_refs=evidence_refs,
                )
            )
        elif missing_variable or boundary_failure or wrong_prior_choice or weak_causal_chain:
            events.append(
                _record(
                    detected_contradiction=False,
                    detected_missing_variable=missing_variable,
                    detected_boundary_failure=boundary_failure,
                    detected_wrong_prior_choice=wrong_prior_choice,
                    detected_weak_causal_chain=weak_causal_chain,
                    triggered_action=SurpriseTrigger.THEORY_FRAGMENT_CANDIDATE if missing_variable and not boundary_failure else SurpriseTrigger.RECHECK_SUPPORT,
                    trigger_reason="bounded anomaly signal reached the surprise engine",
                    supporting_refs=evidence_refs,
                )
            )

        events = events[:MAX_SURPRISE_EVENTS]
        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "event_count": len(events),
            "events": [event.to_dict() for event in events],
        }
        return SurpriseEngineSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            event_count=len(events),
            events=tuple(events),
            snapshot_hash=stable_hash_payload(payload),
        )
