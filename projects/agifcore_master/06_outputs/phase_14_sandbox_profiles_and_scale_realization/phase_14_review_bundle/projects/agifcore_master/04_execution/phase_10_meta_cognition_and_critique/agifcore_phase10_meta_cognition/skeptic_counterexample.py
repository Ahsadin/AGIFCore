from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_SKEPTIC_BRANCHES,
    SkepticCounterexampleRecord,
    SkepticCounterexampleSnapshot,
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


def _branch(
    *,
    what_could_make_this_wrong: str,
    what_variable_could_flip_the_answer: str,
    what_counterexample_weakens_the_theory: str,
    changed_answer_after_skeptic: bool,
    forced_fallback: bool,
    supporting_refs: tuple[str, ...],
) -> SkepticCounterexampleRecord:
    payload = {
        "what_could_make_this_wrong": what_could_make_this_wrong,
        "what_variable_could_flip_the_answer": what_variable_could_flip_the_answer,
        "what_counterexample_weakens_the_theory": what_counterexample_weakens_the_theory,
        "changed_answer_after_skeptic": changed_answer_after_skeptic,
        "forced_fallback": forced_fallback,
        "supporting_refs": list(supporting_refs),
    }
    return SkepticCounterexampleRecord(
        branch_id=make_trace_ref("skeptic_branch", payload),
        what_could_make_this_wrong=what_could_make_this_wrong,
        what_variable_could_flip_the_answer=what_variable_could_flip_the_answer,
        what_counterexample_weakens_the_theory=what_counterexample_weakens_the_theory,
        changed_answer_after_skeptic=changed_answer_after_skeptic,
        forced_fallback=forced_fallback,
        supporting_refs=supporting_refs,
        record_hash=stable_hash_payload(payload),
    )


class SkepticCounterexampleEngine:
    """Ask what could make the answer wrong, but keep the branch count bounded."""

    SCHEMA = "agifcore.phase_10.skeptic_counterexample.v1"

    def build_snapshot(
        self,
        *,
        support_state_resolution_state: Mapping[str, Any],
        science_world_turn_state: Mapping[str, Any],
        rich_expression_turn_state: Mapping[str, Any],
    ) -> SkepticCounterexampleSnapshot:
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
        visible_reasoning = require_schema(
            science_world_turn.get("visible_reasoning_summary", {}),
            "agifcore.phase_08.visible_reasoning_summaries.v1",
            "science_world_turn_state.visible_reasoning_summary",
        )

        turn_id = require_non_empty_str(str(rich_expression_turn.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        uncertainty = [str(item).strip() for item in list(visible_reasoning.get("uncertainty", ())) if str(item).strip()]
        principle_refs = [str(item).strip() for item in list(visible_reasoning.get("principle_refs", ())) if str(item).strip()]
        evidence_refs = _clean_items(
            [str(item).strip() for item in list(visible_reasoning.get("evidence_refs", ())) if str(item).strip()],
            ceiling=6,
        )

        branches: list[SkepticCounterexampleRecord] = []
        branches.append(
            _branch(
                what_could_make_this_wrong="A hidden variable or fresher local evidence could break the current answer.",
                what_variable_could_flip_the_answer=uncertainty[0] if uncertainty else "the unresolved local variable",
                what_counterexample_weakens_the_theory="A recent observation that contradicts the bounded explanation would weaken it immediately.",
                changed_answer_after_skeptic=support_state in {"search_needed", "unknown"},
                forced_fallback=support_state in {"search_needed", "unknown"},
                supporting_refs=evidence_refs[:3],
            )
        )
        if support_state in {"grounded", "inferred"} and len(branches) < MAX_SKEPTIC_BRANCHES:
            branches.append(
                _branch(
                    what_could_make_this_wrong="The current principle choice may fit only part of the situation.",
                    what_variable_could_flip_the_answer=principle_refs[0] if principle_refs else "the governing prior",
                    what_counterexample_weakens_the_theory="A case where the same input leads to the opposite outcome would weaken the chosen explanation.",
                    changed_answer_after_skeptic=False,
                    forced_fallback=False,
                    supporting_refs=evidence_refs[:2],
                )
            )

        branches = branches[:MAX_SKEPTIC_BRANCHES]
        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "branch_count": len(branches),
            "branches": [branch.to_dict() for branch in branches],
        }
        return SkepticCounterexampleSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            branch_count=len(branches),
            branches=tuple(branches),
            snapshot_hash=stable_hash_payload(payload),
        )
