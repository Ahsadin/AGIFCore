from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_THEORY_FORMATION_CANDIDATES,
    TheoryFormationCandidate,
    TheoryFormationSnapshot,
    TheoryGrowthStatus,
    bounded_unique,
    infer_phase12_scenario,
    make_trace_ref,
    require_non_empty_str,
    require_phase11_cycle,
    require_schema,
    stable_hash_payload,
)


class TheoryFormationEngine:
    SCHEMA = "agifcore.phase_12.theory_formation.v1"

    def build_snapshot(
        self,
        *,
        phase11_cycle_state: Mapping[str, Any],
        reflection_control_state: Mapping[str, Any],
        curiosity_gap_selection_state: Mapping[str, Any],
    ) -> TheoryFormationSnapshot:
        cycle = require_phase11_cycle(phase11_cycle_state, "phase11_cycle_state")
        require_schema(
            reflection_control_state,
            "agifcore.phase_12.reflection_control.v1",
            "reflection_control_state",
        )
        require_schema(
            curiosity_gap_selection_state,
            "agifcore.phase_12.curiosity_gap_selection.v1",
            "curiosity_gap_selection_state",
        )
        overlay = cycle["overlay_contract"]
        conversation_id = require_non_empty_str(cycle.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(cycle.get("turn_id"), "turn_id")
        scenario = infer_phase12_scenario(cycle)
        source_refs = bounded_unique(
            [
                *list(overlay.get("read_only_phase10_refs", ())),
                *list(overlay.get("evidence_refs", ())),
                *list(overlay.get("monitoring_refs", ())),
            ],
            ceiling=8,
            field_name="theory_formation.source_refs",
        )
        candidates: list[TheoryFormationCandidate] = []

        def add_candidate(
            *,
            growth_status: TheoryGrowthStatus,
            source_fragment_ref: str,
            theory_label: str,
            theory_statement: str,
            assumption_refs: tuple[str, ...],
            mechanism_step_refs: tuple[str, ...],
            predicted_observable_refs: tuple[str, ...],
            falsifier_refs: tuple[str, ...],
            theory_confidence_band: str,
            verification_next_step: str,
        ) -> None:
            payload = {
                "growth_status": growth_status.value,
                "source_fragment_ref": source_fragment_ref,
                "theory_label": theory_label,
                "theory_statement": theory_statement,
                "assumption_refs": list(assumption_refs),
                "mechanism_step_refs": list(mechanism_step_refs),
                "predicted_observable_refs": list(predicted_observable_refs),
                "falsifier_refs": list(falsifier_refs),
                "theory_confidence_band": theory_confidence_band,
                "verification_next_step": verification_next_step,
            }
            candidates.append(
                TheoryFormationCandidate(
                    candidate_id=make_trace_ref("phase12_theory", payload),
                    growth_status=growth_status,
                    source_fragment_ref=source_fragment_ref,
                    theory_label=theory_label,
                    theory_statement=theory_statement,
                    assumption_refs=assumption_refs,
                    mechanism_step_refs=mechanism_step_refs,
                    predicted_observable_refs=predicted_observable_refs,
                    falsifier_refs=falsifier_refs,
                    theory_confidence_band=theory_confidence_band,
                    verification_next_step=verification_next_step,
                    candidate_hash=stable_hash_payload(payload),
                )
            )

        if scenario == "weak":
            add_candidate(
                growth_status=TheoryGrowthStatus.NEW_CANDIDATE,
                source_fragment_ref=source_refs[0],
                theory_label="local_measurement_dependency_boundary",
                theory_statement="Weak answers recur when local evidence freshness is missing and the explanation lane reuses general reasoning too early.",
                assumption_refs=(source_refs[0], source_refs[1]),
                mechanism_step_refs=("phase12.mechanism.local_evidence_gate", "phase12.mechanism.defer_explanation_reuse"),
                predicted_observable_refs=("phase12.observable.weaker_support_flag", "phase12.observable.review_protocol_needed"),
                falsifier_refs=("phase12.falsifier.fresh_local_measurement_still_weak",),
                theory_confidence_band="medium",
                verification_next_step="Replay the weak-support pack with a fresh local evidence ref and compare whether the structural pressure remains.",
            )
        else:
            add_candidate(
                growth_status=TheoryGrowthStatus.REFINE_EXISTING,
                source_fragment_ref=source_refs[0],
                theory_label="contradiction_sensitive_boundary_refinement",
                theory_statement="Contradiction repair improves when the review lane isolates conflict checking from explanation shaping before adoption decisions land.",
                assumption_refs=(source_refs[0], source_refs[1]),
                mechanism_step_refs=("phase12.mechanism.isolate_conflict_check", "phase12.mechanism.route_before_adoption"),
                predicted_observable_refs=("phase12.observable.lower_monitoring_regression", "phase12.observable.cleaner_reorganization_candidate"),
                falsifier_refs=("phase12.falsifier.same_contradiction_without_route_isolation",),
                theory_confidence_band="medium",
                verification_next_step="Replay the contradiction pack and compare whether the route-isolated candidate lowers regression pressure.",
            )
            add_candidate(
                growth_status=TheoryGrowthStatus.NEW_CANDIDATE,
                source_fragment_ref=source_refs[2],
                theory_label="micro_domain_boundary_candidate",
                theory_statement="A missing micro-domain boundary between broad world reasoning and local infrastructure-like conditions can hide stable contradiction patterns.",
                assumption_refs=(source_refs[1], source_refs[2]),
                mechanism_step_refs=("phase12.mechanism.boundary_candidate", "phase12.mechanism.local_condition_split"),
                predicted_observable_refs=("phase12.observable.domain_candidate_needed", "phase12.observable.fewer_cross_domain_conflicts"),
                falsifier_refs=("phase12.falsifier.domain_candidate_adds_no_explanatory_gain",),
                theory_confidence_band="low",
                verification_next_step="Hold one bounded domain candidate and check whether it explains the contradiction pattern better than a pure route change alone.",
            )

        bounded_candidates = tuple(candidates[:MAX_THEORY_FORMATION_CANDIDATES])
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "candidate_ids": [item.candidate_id for item in bounded_candidates],
        }
        return TheoryFormationSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            candidate_count=len(bounded_candidates),
            candidates=bounded_candidates,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
