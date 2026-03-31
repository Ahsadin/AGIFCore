from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_THEORY_FRAGMENTS,
    TheoryFragmentRecord,
    TheoryFragmentsSnapshot,
    make_trace_ref,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)


def _fragment(
    *,
    source_answer_id: str,
    fragment_label: str,
    fragment_statement: str,
    falsifier: str,
    next_verification_step: str,
) -> TheoryFragmentRecord:
    payload = {
        "source_answer_id": source_answer_id,
        "fragment_label": fragment_label,
        "fragment_statement": fragment_statement,
        "falsifier": falsifier,
        "next_verification_step": next_verification_step,
    }
    return TheoryFragmentRecord(
        fragment_id=make_trace_ref("theory_fragment", payload),
        source_answer_id=source_answer_id,
        fragment_label=fragment_label,
        fragment_statement=fragment_statement,
        falsifier=falsifier,
        next_verification_step=next_verification_step,
        record_hash=stable_hash_payload(payload),
    )


class TheoryFragmentsEngine:
    """Store bounded provisional fragments only when surprise signals justify them."""

    SCHEMA = "agifcore.phase_10.theory_fragments.v1"

    def build_snapshot(
        self,
        *,
        surprise_engine_state: Mapping[str, Any],
        thinker_tissue_state: Mapping[str, Any],
        science_world_turn_state: Mapping[str, Any],
        rich_expression_turn_state: Mapping[str, Any],
    ) -> TheoryFragmentsSnapshot:
        surprise = require_schema(
            surprise_engine_state,
            "agifcore.phase_10.surprise_engine.v1",
            "surprise_engine_state",
        )
        thinker = require_schema(
            thinker_tissue_state,
            "agifcore.phase_10.thinker_tissue.v1",
            "thinker_tissue_state",
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
        visible_reasoning = require_schema(
            science_world_turn.get("visible_reasoning_summary", {}),
            "agifcore.phase_08.visible_reasoning_summaries.v1",
            "science_world_turn_state.visible_reasoning_summary",
        )

        turn_id = require_non_empty_str(str(rich_expression_turn.get("turn_id", "")).strip(), "turn_id")
        source_answer_id = str(rich_expression_turn.get("snapshot_hash", "")).strip() or turn_id
        uncertainty = [str(item).strip() for item in list(visible_reasoning.get("uncertainty", ())) if str(item).strip()]
        proposals = [
            str(item).strip()
            for record in list(thinker.get("records", ()))
            if isinstance(record, Mapping)
            for item in list(record.get("bounded_proposals", ()))
            if str(item).strip()
        ]
        fragments: list[TheoryFragmentRecord] = []
        for event in list(surprise.get("events", ())):
            if not isinstance(event, Mapping):
                continue
            action = str(event.get("triggered_action", "")).strip()
            if action not in {"theory_fragment_candidate", "concept_refinement_candidate"}:
                continue
            fragments.append(
                _fragment(
                    source_answer_id=source_answer_id,
                    fragment_label="bounded_candidate_fragment",
                    fragment_statement="A hidden variable or contradiction-sensitive condition may explain the current weak answer.",
                    falsifier=uncertainty[0] if uncertainty else "A grounded counterexample would falsify this fragment.",
                    next_verification_step=proposals[0] if proposals else "recheck the cited support before treating this as stable",
                )
            )
            if len(fragments) >= MAX_THEORY_FRAGMENTS:
                break

        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "fragment_count": len(fragments),
            "fragments": [fragment.to_dict() for fragment in fragments],
        }
        return TheoryFragmentsSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            fragment_count=len(fragments),
            fragments=tuple(fragments),
            snapshot_hash=stable_hash_payload(payload),
        )
