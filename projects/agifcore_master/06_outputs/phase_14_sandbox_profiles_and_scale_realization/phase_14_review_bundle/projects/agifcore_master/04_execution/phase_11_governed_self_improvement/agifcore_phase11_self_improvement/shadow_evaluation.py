from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_SHADOW_EVALUATIONS,
    MAX_SUPPORTING_REFS,
    ShadowEvaluationRecord,
    ShadowEvaluationSnapshot,
    optional_bounded_unique,
    require_phase10_turn_state,
    require_schema,
    stable_hash_payload,
)


class ShadowEvaluationEngine:
    SCHEMA = "agifcore.phase_11.shadow_evaluation.v1"

    def build_snapshot(
        self,
        *,
        self_experiment_lab_state: Mapping[str, Any],
        phase10_turn_state: Mapping[str, Any],
    ) -> ShadowEvaluationSnapshot:
        experiments = require_schema(
            self_experiment_lab_state,
            "agifcore.phase_11.self_experiment_lab.v1",
            "self_experiment_lab_state",
        )
        phase10_turn = require_phase10_turn_state(phase10_turn_state, "phase10_turn_state")
        overlay = phase10_turn["overlay_contract"]
        observer = phase10_turn.get("meta_cognition_observer", {})
        conversation_id = str(experiments.get("conversation_id"))
        turn_id = str(experiments.get("turn_id"))
        support_state = str(overlay.get("support_state", "unknown")).strip() or "unknown"
        repeated_uncertainty = [str(item).strip() for item in list(observer.get("repeated_uncertainty_signals", ()))]

        evaluations: list[ShadowEvaluationRecord] = []
        for experiment in list(experiments.get("experiments", ()))[:MAX_SHADOW_EVALUATIONS]:
            if not isinstance(experiment, Mapping):
                continue
            proposal_id = str(experiment.get("proposal_id", "")).strip()
            delta = float(experiment.get("delta", 0.0))
            regressions = [str(item).strip() for item in list(experiment.get("regressions", ())) if str(item).strip()]
            uncertainty_notes = []
            if support_state == "search_needed":
                uncertainty_notes.append("support remains unresolved, so measurement stays advisory")
            uncertainty_notes.extend(repeated_uncertainty[:2])
            ready_for_measurement = delta > 0 and support_state == "inferred" and bool(experiment.get("safe_to_continue", False))
            payload = {
                "proposal_id": proposal_id,
                "baseline_score": float(experiment.get("baseline_score", 0.0)),
                "candidate_score": float(experiment.get("candidate_score", 0.0)),
                "delta": delta,
                "regressions": regressions,
                "uncertainty_notes": uncertainty_notes,
                "ready_for_measurement": ready_for_measurement,
            }
            evaluations.append(
                ShadowEvaluationRecord(
                    evaluation_id=f"shadow_eval::{proposal_id}",
                    proposal_id=proposal_id,
                    baseline_score=float(experiment.get("baseline_score", 0.0)),
                    candidate_score=float(experiment.get("candidate_score", 0.0)),
                    delta=delta,
                    regressions=tuple(regressions),
                    uncertainty_notes=tuple(uncertainty_notes),
                    ready_for_measurement=ready_for_measurement,
                    supporting_refs=optional_bounded_unique(
                        [
                            str(experiment.get("experiment_id", "")).strip(),
                            str(experiment.get("held_out_pack_ref", "")).strip(),
                            str(overlay.get("observer_ref", "")).strip(),
                        ],
                        ceiling=MAX_SUPPORTING_REFS,
                    ),
                    evaluation_hash=stable_hash_payload(payload),
                )
            )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "evaluation_ids": [evaluation.evaluation_id for evaluation in evaluations],
        }
        return ShadowEvaluationSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            evaluation_count=len(evaluations),
            evaluations=tuple(evaluations),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
