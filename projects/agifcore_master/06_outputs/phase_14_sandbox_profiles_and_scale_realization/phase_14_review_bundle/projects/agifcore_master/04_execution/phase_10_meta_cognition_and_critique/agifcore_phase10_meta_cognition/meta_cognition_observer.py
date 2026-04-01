from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_META_COGNITION_OBSERVATIONS,
    MetaCognitionObservation,
    MetaCognitionObserverSnapshot,
    ObservationKind,
    Phase10MetaCognitionError,
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


def _observation(*, kind: ObservationKind, detail: str, source_ref: str, severity: float) -> MetaCognitionObservation:
    payload = {
        "kind": kind.value,
        "detail": detail,
        "source_ref": source_ref,
        "severity": clamp_score(severity),
    }
    return MetaCognitionObservation(
        observation_id=make_trace_ref("meta_observation", payload),
        kind=kind,
        detail=detail,
        source_ref=source_ref,
        severity=clamp_score(severity),
        observation_hash=stable_hash_payload(payload),
    )


class MetaCognitionObserverEngine:
    """Observe weak-support, contradiction, and repeated uncertainty signals without rewriting the answer."""

    SCHEMA = "agifcore.phase_10.meta_cognition_observer.v1"

    def build_snapshot(
        self,
        *,
        support_state_resolution_state: Mapping[str, Any],
        science_world_turn_state: Mapping[str, Any],
        rich_expression_turn_state: Mapping[str, Any],
    ) -> MetaCognitionObserverSnapshot:
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
        rich_expression_turn = require_schema(
            rich_expression_turn_state,
            "agifcore.phase_09.rich_expression_turn.v1",
            "rich_expression_turn_state",
        )
        overlay = require_schema(
            rich_expression_turn.get("overlay_contract", {}),
            "agifcore.phase_09.overlay_contract.v1",
            "rich_expression_turn_state.overlay_contract",
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

        turn_id = require_non_empty_str(str(rich_expression_turn.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        uncertainty = [str(item).strip() for item in list(visible_reasoning.get("uncertainty", ())) if str(item).strip()]
        weak_flags: list[str] = []
        missing_needs: list[str] = []
        observations: list[MetaCognitionObservation] = []

        if support_state in {"search_needed", "unknown"}:
            weak_flags.append("support_state_not_grounded")
            missing_needs.append("missing local evidence before stronger claims")
            observations.append(
                _observation(
                    kind=ObservationKind.SUPPORT_GAP,
                    detail="Current support-state blocks a stronger claim.",
                    source_ref=str(support.get("resolution_hash", "")).strip() or "phase7.support_state_logic",
                    severity=0.92,
                )
            )
        if len(uncertainty) >= 2:
            observations.append(
                _observation(
                    kind=ObservationKind.REPEATED_UNCERTAINTY,
                    detail="Multiple uncertainty statements remain active in the lower-phase summary.",
                    source_ref=str(visible_reasoning.get("summary_hash", "")).strip() or "phase8.visible_reasoning_summary",
                    severity=0.78,
                )
            )
        reflection_records = list(science_reflection.get("records", ()))
        if any("contradiction" in str(record.get("kind", "")).lower() or "contradiction" in str(record.get("note", "")).lower() for record in reflection_records if isinstance(record, Mapping)):
            weak_flags.append("contradiction_signal_detected")
            observations.append(
                _observation(
                    kind=ObservationKind.CONTRADICTION_SIGNAL,
                    detail="Science reflection already contains a contradiction-oriented signal.",
                    source_ref=str(science_reflection.get("reflection_hash", "")).strip() or "phase8.science_reflection",
                    severity=0.88,
                )
            )
        if support_state in {"inferred", "search_needed", "unknown"}:
            observations.append(
                _observation(
                    kind=ObservationKind.WEAK_ANSWER_SIGNAL,
                    detail="The current answer stays bounded but still needs critique before it can be trusted further.",
                    source_ref=str(overlay.get("contract_hash", "")).strip() or "phase9.overlay_contract",
                    severity=0.73,
                )
            )
        if uncertainty:
            missing_needs.append("clarify or measure the uncertainty-driving variable")
            observations.append(
                _observation(
                    kind=ObservationKind.MISSING_NEED,
                    detail="At least one missing or unverified variable remains visible.",
                    source_ref=str(visible_reasoning.get("summary_hash", "")).strip() or "phase8.visible_reasoning_summary",
                    severity=0.7,
                )
            )

        observations = observations[:MAX_META_COGNITION_OBSERVATIONS]
        if len(observations) > MAX_META_COGNITION_OBSERVATIONS:
            raise Phase10MetaCognitionError("meta-cognition observation count exceeds Phase 10 ceiling")

        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "observation_count": len(observations),
            "observations": [item.to_dict() for item in observations],
            "weak_answer_flags": list(_clean_items(weak_flags or ["no_weak_answer_flag"], ceiling=MAX_META_COGNITION_OBSERVATIONS)),
            "repeated_uncertainty_signals": list(_clean_items(uncertainty or ["no_repeated_uncertainty_signal"], ceiling=MAX_META_COGNITION_OBSERVATIONS)),
            "missing_needs": list(_clean_items(missing_needs or ["no_missing_need"], ceiling=MAX_META_COGNITION_OBSERVATIONS)),
        }
        return MetaCognitionObserverSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            observation_count=len(observations),
            observations=tuple(observations),
            weak_answer_flags=_clean_items(weak_flags or ["no_weak_answer_flag"], ceiling=MAX_META_COGNITION_OBSERVATIONS),
            repeated_uncertainty_signals=_clean_items(uncertainty or ["no_repeated_uncertainty_signal"], ceiling=MAX_META_COGNITION_OBSERVATIONS),
            missing_needs=_clean_items(missing_needs or ["no_missing_need"], ceiling=MAX_META_COGNITION_OBSERVATIONS),
            snapshot_hash=stable_hash_payload(payload),
        )
