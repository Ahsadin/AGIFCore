from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_SUPPORTING_REFS,
    MAX_THOUGHT_EPISODES,
    ThoughtEpisodeRecord,
    ThoughtEpisodesSnapshot,
    optional_bounded_unique,
    require_phase10_turn_state,
    require_schema,
    stable_hash_payload,
)


class ThoughtEpisodesEngine:
    SCHEMA = "agifcore.phase_11.thought_episodes.v1"

    def build_snapshot(
        self,
        *,
        offline_reflection_and_consolidation_state: Mapping[str, Any],
        proposal_generation_state: Mapping[str, Any],
        phase10_turn_state: Mapping[str, Any],
    ) -> ThoughtEpisodesSnapshot:
        reflection = require_schema(
            offline_reflection_and_consolidation_state,
            "agifcore.phase_11.offline_reflection_and_consolidation.v1",
            "offline_reflection_and_consolidation_state",
        )
        proposals = require_schema(
            proposal_generation_state,
            "agifcore.phase_11.proposal_generation.v1",
            "proposal_generation_state",
        )
        phase10_turn = require_phase10_turn_state(phase10_turn_state, "phase10_turn_state")
        overlay = phase10_turn["overlay_contract"]
        episodes: list[ThoughtEpisodeRecord] = []
        reflection_items = list(reflection.get("items", ()))
        for proposal, reflection_item in zip(list(proposals.get("proposals", ())), reflection_items):
            if len(episodes) >= MAX_THOUGHT_EPISODES:
                break
            if not isinstance(proposal, Mapping) or not isinstance(reflection_item, Mapping):
                continue
            proposal_id = str(proposal.get("proposal_id", "")).strip()
            note = (
                f"Bounded proposal {proposal_id} stays tied to "
                f"{str(reflection_item.get('source_kind', 'reflection')).strip()} without promoting it to runtime truth."
            )
            falsifier = " ".join(str(proposal.get("falsifier", "")).split()).strip()
            trace_refs = optional_bounded_unique(
                [
                    str(reflection_item.get("item_id", "")).strip(),
                    str(reflection_item.get("source_ref", "")).strip(),
                    str(overlay.get("strategy_journal_ref", "")).strip(),
                    str(overlay.get("diagnosis_ref", "")).strip(),
                ],
                ceiling=MAX_SUPPORTING_REFS,
            )
            payload = {
                "proposal_id": proposal_id,
                "episode_note": note,
                "falsifier": falsifier,
                "trace_refs": list(trace_refs),
            }
            episodes.append(
                ThoughtEpisodeRecord(
                    episode_id=f"episode::{proposal_id}",
                    proposal_id=proposal_id,
                    episode_note=note,
                    falsifier=falsifier,
                    trace_refs=trace_refs,
                    episode_hash=stable_hash_payload(payload),
                )
            )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": str(reflection.get("conversation_id")),
            "turn_id": str(reflection.get("turn_id")),
            "episode_ids": [item.episode_id for item in episodes],
        }
        return ThoughtEpisodesSnapshot(
            schema=self.SCHEMA,
            conversation_id=str(reflection.get("conversation_id")),
            turn_id=str(reflection.get("turn_id")),
            episode_count=len(episodes),
            episodes=tuple(episodes),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
