from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    CandidateState,
    DomainGenesisCandidate,
    DomainGenesisSnapshot,
    MAX_DOMAIN_GENESIS_ITEMS,
    bounded_unique,
    infer_phase12_scenario,
    make_trace_ref,
    require_non_empty_str,
    require_phase11_cycle,
    require_schema,
    stable_hash_payload,
)


class DomainGenesisEngine:
    SCHEMA = "agifcore.phase_12.domain_genesis.v1"

    def build_snapshot(
        self,
        *,
        phase11_cycle_state: Mapping[str, Any],
        reflection_control_state: Mapping[str, Any],
        curiosity_gap_selection_state: Mapping[str, Any],
        theory_formation_state: Mapping[str, Any],
    ) -> DomainGenesisSnapshot:
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
        require_schema(
            theory_formation_state,
            "agifcore.phase_12.theory_formation.v1",
            "theory_formation_state",
        )
        overlay = cycle["overlay_contract"]
        conversation_id = require_non_empty_str(cycle.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(cycle.get("turn_id"), "turn_id")
        scenario = infer_phase12_scenario(cycle)
        refs = bounded_unique(
            [
                *list(overlay.get("evidence_refs", ())),
                *list(overlay.get("monitoring_refs", ())),
                *list(overlay.get("read_only_phase10_refs", ())),
            ],
            ceiling=6,
            field_name="domain_genesis.supporting_refs",
        )
        if scenario == "weak":
            domain_label = "local_evidence_refresh_boundary"
            candidate_state = CandidateState.HELD
            boundary_statement = "This candidate would isolate local evidence-refresh handling from broad explanation reuse, but it stays held until contradiction pressure justifies a new domain boundary."
            activation_signals = ("repeated weak-support turns", "no contradiction-specific pressure", "fresh-evidence path still missing")
        else:
            domain_label = "microclimate_infrastructure_boundary"
            candidate_state = CandidateState.CANDIDATE
            boundary_statement = "This candidate would separate local infrastructure-like condition handling from broad world reasoning when contradiction patterns repeat under the same proof-domain family."
            activation_signals = ("contradiction-sensitive theory candidate", "adopted improvement plus monitoring refs", "cross-domain boundary pressure")
        payload = {
            "domain_label": domain_label,
            "parent_domain_ref": "building_home_infrastructure_events",
            "peer_domain_refs": ["maintenance_diagnostics", "planning_coordination_workflows"],
            "boundary_statement": boundary_statement,
            "activation_signals": list(activation_signals),
            "rejection_path": "Reject the candidate and keep the current proof-domain map unchanged if one bounded route change explains the pressure just as well.",
            "candidate_state": candidate_state.value,
            "supporting_refs": list(refs[:4]),
        }
        candidate = DomainGenesisCandidate(
            candidate_id=make_trace_ref("phase12_domain_genesis", payload),
            domain_label=domain_label,
            parent_domain_ref="building_home_infrastructure_events",
            peer_domain_refs=("maintenance_diagnostics", "planning_coordination_workflows"),
            boundary_statement=boundary_statement,
            activation_signals=activation_signals,
            rejection_path="Reject the candidate and keep the current proof-domain map unchanged if one bounded route change explains the pressure just as well.",
            candidate_state=candidate_state,
            supporting_refs=refs[:4],
            candidate_hash=stable_hash_payload(payload),
        )
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "candidate_ids": [candidate.candidate_id],
        }
        return DomainGenesisSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            candidate_count=min(1, MAX_DOMAIN_GENESIS_ITEMS),
            candidates=(candidate,),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
