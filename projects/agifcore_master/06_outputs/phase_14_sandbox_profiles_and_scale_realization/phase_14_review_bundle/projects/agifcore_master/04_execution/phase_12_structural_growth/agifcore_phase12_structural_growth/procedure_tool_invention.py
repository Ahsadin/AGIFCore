from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    CandidateState,
    MAX_PROCEDURE_TOOL_INVENTION_CANDIDATES,
    ProcedureToolInventionCandidate,
    ProcedureToolInventionSnapshot,
    ProcedureToolKind,
    bounded_unique,
    infer_phase12_scenario,
    make_trace_ref,
    require_non_empty_str,
    require_phase11_cycle,
    require_schema,
    stable_hash_payload,
)


class ProcedureToolInventionEngine:
    SCHEMA = "agifcore.phase_12.procedure_tool_invention.v1"

    def build_snapshot(
        self,
        *,
        phase11_cycle_state: Mapping[str, Any],
        reflection_control_state: Mapping[str, Any],
        curiosity_gap_selection_state: Mapping[str, Any],
    ) -> ProcedureToolInventionSnapshot:
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
        refs = bounded_unique(
            [
                *list(overlay.get("evidence_refs", ())),
                *list(overlay.get("read_only_phase10_refs", ())),
            ],
            ceiling=6,
            field_name="procedure_tool_invention.supporting_refs",
        )
        if scenario == "weak":
            invention_kind = ProcedureToolKind.TRIAGE_CHECKLIST
            skill_anchor_ref = "skill::phase12.local_evidence_recheck_protocol"
            procedure_statement = "Before reusing a weak explanation, require one bounded freshness check on the local evidence lane and defer all wider restructuring."
            preconditions = ("support_state=search_needed", "local evidence still missing or stale")
            limits = ("candidate only", "no automatic execution", "no external search")
        else:
            invention_kind = ProcedureToolKind.REVIEW_PROTOCOL
            skill_anchor_ref = "skill::phase12.contradiction_boundary_review_protocol"
            procedure_statement = "When contradiction pressure repeats after an adopted improvement, run one bounded boundary review before proposing domain growth."
            preconditions = ("adopted proposal exists", "monitoring refs present")
            limits = ("candidate only", "no automatic execution", "no phase13_or_phase14_scope")
        payload = {
            "invention_kind": invention_kind.value,
            "skill_anchor_ref": skill_anchor_ref,
            "procedure_statement": procedure_statement,
            "preconditions": list(preconditions),
            "limits": list(limits),
            "supporting_refs": list(refs[:4]),
        }
        candidate = ProcedureToolInventionCandidate(
            candidate_id=make_trace_ref("phase12_procedure_tool", payload),
            invention_kind=invention_kind,
            skill_anchor_ref=skill_anchor_ref,
            procedure_statement=procedure_statement,
            preconditions=preconditions,
            limits=limits,
            sandbox_compatibility_note="planning-only candidate; stays outside runtime execution and connector enablement.",
            non_auto_execute=True,
            candidate_state=CandidateState.CANDIDATE,
            supporting_refs=refs[:4],
            candidate_hash=stable_hash_payload(payload),
        )
        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "candidate_ids": [candidate.candidate_id],
        }
        return ProcedureToolInventionSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            candidate_count=min(1, MAX_PROCEDURE_TOOL_INVENTION_CANDIDATES),
            candidates=(candidate,),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
