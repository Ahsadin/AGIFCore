from __future__ import annotations

from typing import Any, Mapping

from .adoption_or_rejection_pipeline import AdoptionOrRejectionPipelineEngine
from .before_after_measurement import BeforeAfterMeasurementEngine
from .contracts import (
    MAX_EVIDENCE_REFS,
    MAX_SUPPORTING_REFS,
    Phase11OverlayContract,
    SelfImprovementCycleSnapshot,
    bounded_unique,
    optional_bounded_unique,
    require_non_empty_str,
    require_phase10_turn_state,
    stable_hash_payload,
)
from .idle_reflection import IdleReflectionEngine
from .offline_reflection_and_consolidation import OfflineReflectionAndConsolidationEngine
from .post_adoption_monitoring import PostAdoptionMonitoringEngine
from .proposal_generation import ProposalGenerationEngine
from .rollback_proof import RollbackProofEngine
from .self_experiment_lab import SelfExperimentLabEngine
from .self_initiated_inquiry_engine import SelfInitiatedInquiryEngine
from .shadow_evaluation import ShadowEvaluationEngine
from .thought_episodes import ThoughtEpisodesEngine


class SelfImprovementCycleEngine:
    SCHEMA = "agifcore.phase_11.self_improvement_cycle.v1"

    def __init__(self) -> None:
        self.offline_reflection_and_consolidation = OfflineReflectionAndConsolidationEngine()
        self.idle_reflection = IdleReflectionEngine()
        self.proposal_generation = ProposalGenerationEngine()
        self.self_experiment_lab = SelfExperimentLabEngine()
        self.shadow_evaluation = ShadowEvaluationEngine()
        self.before_after_measurement = BeforeAfterMeasurementEngine()
        self.adoption_or_rejection_pipeline = AdoptionOrRejectionPipelineEngine()
        self.post_adoption_monitoring = PostAdoptionMonitoringEngine()
        self.rollback_proof = RollbackProofEngine()
        self.thought_episodes = ThoughtEpisodesEngine()
        self.self_initiated_inquiry_engine = SelfInitiatedInquiryEngine()

    def run_cycle(self, *, phase10_turn_state: Mapping[str, Any]) -> SelfImprovementCycleSnapshot:
        phase10_turn = require_phase10_turn_state(phase10_turn_state, "phase10_turn_state")
        overlay = phase10_turn["overlay_contract"]
        conversation_id = require_non_empty_str(phase10_turn.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(phase10_turn.get("turn_id"), "turn_id")
        offline_reflection = self.offline_reflection_and_consolidation.build_snapshot(phase10_turn_state=phase10_turn)
        idle_reflection = self.idle_reflection.build_snapshot(
            offline_reflection_and_consolidation_state=offline_reflection.to_dict()
        )
        proposals = self.proposal_generation.build_snapshot(
            offline_reflection_and_consolidation_state=offline_reflection.to_dict(),
            idle_reflection_state=idle_reflection.to_dict(),
            phase10_turn_state=phase10_turn,
        )
        experiments = self.self_experiment_lab.build_snapshot(
            proposal_generation_state=proposals.to_dict(),
            phase10_turn_state=phase10_turn,
        )
        shadow_evaluation = self.shadow_evaluation.build_snapshot(
            self_experiment_lab_state=experiments.to_dict(),
            phase10_turn_state=phase10_turn,
        )
        measurements = self.before_after_measurement.build_snapshot(
            shadow_evaluation_state=shadow_evaluation.to_dict()
        )
        adoption = self.adoption_or_rejection_pipeline.build_snapshot(
            proposal_generation_state=proposals.to_dict(),
            before_after_measurement_state=measurements.to_dict(),
            phase10_turn_state=phase10_turn,
        )
        monitoring = self.post_adoption_monitoring.build_snapshot(
            adoption_or_rejection_pipeline_state=adoption.to_dict(),
            before_after_measurement_state=measurements.to_dict(),
        )
        rollback = self.rollback_proof.build_snapshot(
            adoption_or_rejection_pipeline_state=adoption.to_dict(),
            before_after_measurement_state=measurements.to_dict(),
        )
        thought_episodes = self.thought_episodes.build_snapshot(
            offline_reflection_and_consolidation_state=offline_reflection.to_dict(),
            proposal_generation_state=proposals.to_dict(),
            phase10_turn_state=phase10_turn,
        )
        inquiry = self.self_initiated_inquiry_engine.build_snapshot(
            idle_reflection_state=idle_reflection.to_dict(),
            phase10_turn_state=phase10_turn,
            post_adoption_monitoring_state=monitoring.to_dict(),
        )

        decisions = list(adoption.decisions)
        adopted_ids = tuple(item.proposal_id for item in decisions if item.decision.value == "adopted")
        held_ids = tuple(item.proposal_id for item in decisions if item.decision.value == "held")
        rejected_ids = tuple(item.proposal_id for item in decisions if item.decision.value == "rejected")
        read_only_phase10_refs = bounded_unique(
            [
                str(overlay.get("self_model_ref", "")).strip(),
                str(overlay.get("observer_ref", "")).strip(),
                str(overlay.get("strategy_journal_ref", "")).strip(),
                str(overlay.get("skeptic_ref", "")).strip(),
                str(overlay.get("surprise_ref", "")).strip(),
                str(overlay.get("diagnosis_ref", "")).strip(),
                *list(overlay.get("theory_fragment_refs", ())),
                *list(overlay.get("redirect_refs", ())),
            ],
            ceiling=MAX_SUPPORTING_REFS,
            field_name="read_only_phase10_refs",
        )
        evidence_refs = bounded_unique(
            [
                *list(overlay.get("evidence_refs", ())),
                *[item.measurement_id for item in measurements.measurements],
                *[item.decision_id for item in adoption.decisions],
                *[item.monitoring_id for item in monitoring.items],
                *[item.rollback_id for item in rollback.rollbacks],
                *[item.inquiry_id for item in inquiry.inquiries],
            ],
            ceiling=MAX_EVIDENCE_REFS,
            field_name="evidence_refs",
        )
        overlay_payload = {
            "schema": "agifcore.phase_11.overlay_contract.v1",
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "phase10_interfaces": [
                str(phase10_turn.get("schema")),
                str(overlay.get("schema")),
            ],
            "support_state": str(overlay.get("support_state", "unknown")).strip() or "unknown",
            "adopted_proposal_ids": list(adopted_ids),
            "held_proposal_ids": list(held_ids),
            "rejected_proposal_ids": list(rejected_ids),
            "monitoring_refs": [item.monitoring_id for item in monitoring.items],
            "rollback_refs": [item.rollback_id for item in rollback.rollbacks],
            "inquiry_refs": [item.inquiry_id for item in inquiry.inquiries],
            "read_only_phase10_refs": list(read_only_phase10_refs),
            "evidence_refs": list(evidence_refs),
        }
        phase11_overlay = Phase11OverlayContract(
            schema="agifcore.phase_11.overlay_contract.v1",
            conversation_id=conversation_id,
            turn_id=turn_id,
            phase10_interfaces=tuple(overlay_payload["phase10_interfaces"]),
            support_state=str(overlay_payload["support_state"]),
            adopted_proposal_ids=adopted_ids,
            held_proposal_ids=held_ids,
            rejected_proposal_ids=rejected_ids,
            monitoring_refs=tuple(overlay_payload["monitoring_refs"]),
            rollback_refs=tuple(overlay_payload["rollback_refs"]),
            inquiry_refs=tuple(overlay_payload["inquiry_refs"]),
            read_only_phase10_refs=read_only_phase10_refs,
            evidence_refs=evidence_refs,
            contract_hash=stable_hash_payload(overlay_payload),
        )
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "phase10_turn_hash": str(phase10_turn.get("snapshot_hash", "")).strip(),
            "offline_reflection_and_consolidation_hash": offline_reflection.snapshot_hash,
            "idle_reflection_hash": idle_reflection.snapshot_hash,
            "proposal_generation_hash": proposals.snapshot_hash,
            "self_experiment_lab_hash": experiments.snapshot_hash,
            "shadow_evaluation_hash": shadow_evaluation.snapshot_hash,
            "before_after_measurement_hash": measurements.snapshot_hash,
            "adoption_or_rejection_pipeline_hash": adoption.snapshot_hash,
            "post_adoption_monitoring_hash": monitoring.snapshot_hash,
            "rollback_proof_hash": rollback.snapshot_hash,
            "thought_episodes_hash": thought_episodes.snapshot_hash,
            "self_initiated_inquiry_engine_hash": inquiry.snapshot_hash,
            "overlay_contract_hash": phase11_overlay.contract_hash,
        }
        return SelfImprovementCycleSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            phase10_turn_hash=str(phase10_turn.get("snapshot_hash", "")).strip(),
            offline_reflection_and_consolidation=offline_reflection,
            idle_reflection=idle_reflection,
            proposal_generation=proposals,
            self_experiment_lab=experiments,
            shadow_evaluation=shadow_evaluation,
            before_after_measurement=measurements,
            adoption_or_rejection_pipeline=adoption,
            post_adoption_monitoring=monitoring,
            rollback_proof=rollback,
            thought_episodes=thought_episodes,
            self_initiated_inquiry_engine=inquiry,
            overlay_contract=phase11_overlay,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
