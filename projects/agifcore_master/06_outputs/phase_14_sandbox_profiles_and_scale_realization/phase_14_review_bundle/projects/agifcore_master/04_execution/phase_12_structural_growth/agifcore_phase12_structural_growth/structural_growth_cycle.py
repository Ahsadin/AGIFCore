from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_EVIDENCE_REFS,
    MAX_SUPPORTING_REFS,
    Phase12OverlayContract,
    StructuralGrowthCycleSnapshot,
    bounded_unique,
    require_non_empty_str,
    require_phase11_cycle,
    stable_hash_payload,
)
from .curiosity_gap_selection import CuriosityGapSelectionEngine
from .domain_genesis import DomainGenesisEngine
from .procedure_tool_invention import ProcedureToolInventionEngine
from .reflection_control import ReflectionControlEngine
from .self_model_feedback import SelfModelFeedbackEngine
from .self_reorganization import SelfReorganizationEngine
from .theory_formation import TheoryFormationEngine


class StructuralGrowthCycleEngine:
    SCHEMA = "agifcore.phase_12.structural_growth_cycle.v1"

    def __init__(self) -> None:
        self.self_model_feedback = SelfModelFeedbackEngine()
        self.reflection_control = ReflectionControlEngine()
        self.curiosity_gap_selection = CuriosityGapSelectionEngine()
        self.theory_formation = TheoryFormationEngine()
        self.procedure_tool_invention = ProcedureToolInventionEngine()
        self.self_reorganization = SelfReorganizationEngine()
        self.domain_genesis = DomainGenesisEngine()

    def run_cycle(self, *, phase11_cycle_state: Mapping[str, Any]) -> StructuralGrowthCycleSnapshot:
        phase11_cycle = require_phase11_cycle(phase11_cycle_state, "phase11_cycle_state")
        phase11_overlay = phase11_cycle["overlay_contract"]
        conversation_id = require_non_empty_str(phase11_cycle.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(phase11_cycle.get("turn_id"), "turn_id")

        feedback = self.self_model_feedback.build_snapshot(phase11_cycle_state=phase11_cycle)
        reflection = self.reflection_control.build_snapshot(
            self_model_feedback_state=feedback.to_dict(),
            phase11_cycle_state=phase11_cycle,
        )
        gaps = self.curiosity_gap_selection.build_snapshot(
            self_model_feedback_state=feedback.to_dict(),
            reflection_control_state=reflection.to_dict(),
            phase11_cycle_state=phase11_cycle,
        )
        theories = self.theory_formation.build_snapshot(
            phase11_cycle_state=phase11_cycle,
            reflection_control_state=reflection.to_dict(),
            curiosity_gap_selection_state=gaps.to_dict(),
        )
        procedures = self.procedure_tool_invention.build_snapshot(
            phase11_cycle_state=phase11_cycle,
            reflection_control_state=reflection.to_dict(),
            curiosity_gap_selection_state=gaps.to_dict(),
        )
        reorganization = self.self_reorganization.build_snapshot(
            phase11_cycle_state=phase11_cycle,
            reflection_control_state=reflection.to_dict(),
            curiosity_gap_selection_state=gaps.to_dict(),
        )
        domains = self.domain_genesis.build_snapshot(
            phase11_cycle_state=phase11_cycle,
            reflection_control_state=reflection.to_dict(),
            curiosity_gap_selection_state=gaps.to_dict(),
            theory_formation_state=theories.to_dict(),
        )

        selected_gap_ids = tuple(item.gap_id for item in gaps.gaps)
        candidate_theory_ids = tuple(item.candidate_id for item in theories.candidates)
        candidate_domain_ids = tuple(item.candidate_id for item in domains.candidates)
        candidate_procedure_ids = tuple(item.candidate_id for item in procedures.candidates)
        reorganization_refs = tuple(item.candidate_id for item in reorganization.candidates)
        read_only_phase11_refs = bounded_unique(
            [
                *list(phase11_overlay.get("evidence_refs", ())),
                *list(phase11_overlay.get("monitoring_refs", ())),
                *list(phase11_overlay.get("rollback_refs", ())),
                *list(phase11_overlay.get("inquiry_refs", ())),
                str(phase11_cycle.get("snapshot_hash", "")).strip(),
            ],
            ceiling=MAX_SUPPORTING_REFS,
            field_name="read_only_phase11_refs",
        )
        evidence_refs = bounded_unique(
            [
                *list(read_only_phase11_refs),
                *list(selected_gap_ids),
                *list(candidate_theory_ids),
                *list(candidate_domain_ids),
                *list(candidate_procedure_ids),
                *list(reorganization_refs),
            ],
            ceiling=MAX_EVIDENCE_REFS,
            field_name="evidence_refs",
        )
        overlay_payload = {
            "schema": "agifcore.phase_12.overlay_contract.v1",
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "phase11_interfaces": [
                str(phase11_cycle.get("schema")),
                str(phase11_overlay.get("schema")),
            ],
            "support_state": str(phase11_overlay.get("support_state", "unknown")).strip() or "unknown",
            "selected_gap_ids": list(selected_gap_ids),
            "candidate_theory_ids": list(candidate_theory_ids),
            "candidate_domain_ids": list(candidate_domain_ids),
            "candidate_procedure_ids": list(candidate_procedure_ids),
            "reorganization_refs": list(reorganization_refs),
            "read_only_phase11_refs": list(read_only_phase11_refs),
            "evidence_refs": list(evidence_refs),
        }
        overlay_contract = Phase12OverlayContract(
            schema="agifcore.phase_12.overlay_contract.v1",
            conversation_id=conversation_id,
            turn_id=turn_id,
            phase11_interfaces=tuple(overlay_payload["phase11_interfaces"]),
            support_state=str(overlay_payload["support_state"]),
            selected_gap_ids=selected_gap_ids,
            candidate_theory_ids=candidate_theory_ids,
            candidate_domain_ids=candidate_domain_ids,
            candidate_procedure_ids=candidate_procedure_ids,
            reorganization_refs=reorganization_refs,
            read_only_phase11_refs=read_only_phase11_refs,
            evidence_refs=evidence_refs,
            contract_hash=stable_hash_payload(overlay_payload),
        )
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "phase11_cycle_hash": str(phase11_cycle.get("snapshot_hash", "")).strip(),
            "self_model_feedback_hash": feedback.snapshot_hash,
            "reflection_control_hash": reflection.snapshot_hash,
            "curiosity_gap_selection_hash": gaps.snapshot_hash,
            "theory_formation_hash": theories.snapshot_hash,
            "procedure_tool_invention_hash": procedures.snapshot_hash,
            "self_reorganization_hash": reorganization.snapshot_hash,
            "domain_genesis_hash": domains.snapshot_hash,
            "overlay_contract_hash": overlay_contract.contract_hash,
        }
        return StructuralGrowthCycleSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            phase11_cycle_hash=str(phase11_cycle.get("snapshot_hash", "")).strip(),
            self_model_feedback=feedback,
            reflection_control=reflection,
            curiosity_gap_selection=gaps,
            theory_formation=theories,
            procedure_tool_invention=procedures,
            self_reorganization=reorganization,
            domain_genesis=domains,
            overlay_contract=overlay_contract,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
