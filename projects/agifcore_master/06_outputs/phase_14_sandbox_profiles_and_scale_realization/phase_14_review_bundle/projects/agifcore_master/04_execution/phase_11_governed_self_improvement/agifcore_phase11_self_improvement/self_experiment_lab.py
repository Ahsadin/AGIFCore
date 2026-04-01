from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    ExperimentVerdict,
    MAX_SELF_EXPERIMENTS,
    SelfExperimentLabSnapshot,
    SelfExperimentRecord,
    clamp_score,
    require_phase10_turn_state,
    require_schema,
    stable_hash_payload,
)


def _candidate_boost(*, proposal_kind: str, support_state: str) -> float:
    if proposal_kind == "contradiction_probe":
        return 0.18 if support_state == "inferred" else 0.06
    if proposal_kind == "clarify_missing_variable":
        return 0.14 if support_state == "inferred" else 0.05
    if proposal_kind == "support_recheck":
        return 0.07 if support_state == "inferred" else 0.03
    return 0.08 if support_state == "inferred" else 0.04


class SelfExperimentLabEngine:
    SCHEMA = "agifcore.phase_11.self_experiment_lab.v1"

    def build_snapshot(
        self,
        *,
        proposal_generation_state: Mapping[str, Any],
        phase10_turn_state: Mapping[str, Any],
    ) -> SelfExperimentLabSnapshot:
        proposals = require_schema(
            proposal_generation_state,
            "agifcore.phase_11.proposal_generation.v1",
            "proposal_generation_state",
        )
        phase10_turn = require_phase10_turn_state(phase10_turn_state, "phase10_turn_state")
        overlay = phase10_turn["overlay_contract"]
        conversation_id = str(proposals.get("conversation_id"))
        turn_id = str(proposals.get("turn_id"))
        support_state = str(overlay.get("support_state", "unknown")).strip() or "unknown"

        experiments: list[SelfExperimentRecord] = []
        baseline_score = 0.56 if support_state == "inferred" else 0.41
        for proposal in list(proposals.get("proposals", ()))[:MAX_SELF_EXPERIMENTS]:
            if not isinstance(proposal, Mapping):
                continue
            proposal_id = str(proposal.get("proposal_id", "")).strip()
            proposal_kind = str(proposal.get("proposal_kind", "")).strip()
            candidate_score = clamp_score(baseline_score + _candidate_boost(proposal_kind=proposal_kind, support_state=support_state))
            regressions = []
            if support_state == "search_needed":
                regressions.append("support state still blocks direct adoption")
            if proposal_kind == "support_recheck":
                regressions.append("candidate still depends on a future support refresh")
            delta = clamp_score(candidate_score - baseline_score)
            verdict = (
                ExperimentVerdict.BLOCKED
                if support_state == "search_needed" and proposal_kind == "support_recheck"
                else ExperimentVerdict.IMPROVES
                if delta >= 0.05
                else ExperimentVerdict.MIXED
            )
            payload = {
                "proposal_id": proposal_id,
                "baseline_score": baseline_score,
                "candidate_score": candidate_score,
                "delta": delta,
                "support_state": support_state,
                "proposal_kind": proposal_kind,
            }
            experiments.append(
                SelfExperimentRecord(
                    experiment_id=f"experiment::{proposal_id}",
                    proposal_id=proposal_id,
                    baseline_score=baseline_score,
                    candidate_score=candidate_score,
                    delta=delta,
                    held_out_pack_ref=f"held_out::{proposal_id}",
                    regressions=tuple(regressions),
                    verdict=verdict,
                    safe_to_continue=verdict is not ExperimentVerdict.BLOCKED,
                    experiment_hash=stable_hash_payload(payload),
                )
            )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "experiment_ids": [experiment.experiment_id for experiment in experiments],
        }
        return SelfExperimentLabSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            experiment_count=len(experiments),
            experiments=tuple(experiments),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
