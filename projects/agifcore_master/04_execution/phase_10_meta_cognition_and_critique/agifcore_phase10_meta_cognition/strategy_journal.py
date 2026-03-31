from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_STRATEGY_JOURNAL_ENTRIES,
    StrategyJournalEntry,
    StrategyJournalSnapshot,
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


def _entry(
    *,
    reasoning_path: str,
    worked: tuple[str, ...],
    failed: tuple[str, ...],
    priors_used: tuple[str, ...],
    hidden_variables_seen: tuple[str, ...],
    question_types_that_still_break: tuple[str, ...],
    monitoring_note: str,
) -> StrategyJournalEntry:
    payload = {
        "reasoning_path": reasoning_path,
        "worked": list(worked),
        "failed": list(failed),
        "priors_used": list(priors_used),
        "hidden_variables_seen": list(hidden_variables_seen),
        "question_types_that_still_break": list(question_types_that_still_break),
        "monitoring_note": monitoring_note,
    }
    return StrategyJournalEntry(
        entry_id=make_trace_ref("strategy_journal", payload),
        reasoning_path=reasoning_path,
        worked=worked,
        failed=failed,
        priors_used=priors_used,
        hidden_variables_seen=hidden_variables_seen,
        question_types_that_still_break=question_types_that_still_break,
        monitoring_note=monitoring_note,
        entry_hash=stable_hash_payload(payload),
    )


class StrategyJournalEngine:
    """Record replayable notes about what worked, what failed, and what to monitor next."""

    SCHEMA = "agifcore.phase_10.strategy_journal.v1"

    def build_snapshot(
        self,
        *,
        self_model_state: Mapping[str, Any],
        weak_answer_diagnosis_state: Mapping[str, Any],
        attention_redirect_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        science_world_turn_state: Mapping[str, Any],
    ) -> StrategyJournalSnapshot:
        self_model = require_schema(
            self_model_state,
            "agifcore.phase_10.self_model.v1",
            "self_model_state",
        )
        diagnosis = require_schema(
            weak_answer_diagnosis_state,
            "agifcore.phase_10.weak_answer_diagnosis.v1",
            "weak_answer_diagnosis_state",
        )
        redirect = require_schema(
            attention_redirect_state,
            "agifcore.phase_10.attention_redirect.v1",
            "attention_redirect_state",
        )
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
        priors = require_schema(
            science_world_turn.get("scientific_priors", {}),
            "agifcore.phase_08.scientific_priors.v1",
            "science_world_turn_state.scientific_priors",
        )

        turn_id = require_non_empty_str(str(self_model.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        diagnosis_kinds = [
            str(item.get("kind", "")).strip()
            for item in list(diagnosis.get("items", ()))
            if isinstance(item, Mapping) and str(item.get("kind", "")).strip()
        ]
        redirect_targets = [
            str(item.get("target_kind", "")).strip()
            for item in list(redirect.get("redirects", ()))
            if isinstance(item, Mapping) and str(item.get("target_kind", "")).strip()
        ]
        selected_priors = [str(item).strip() for item in list(priors.get("selected_prior_ids", ())) if str(item).strip()]
        hidden_variables = [
            str(item).strip()
            for candidate in list(require_schema(science_world_turn.get("entity_request_inference", {}), "agifcore.phase_08.entity_request_inference.v1", "science_world_turn_state.entity_request_inference").get("candidates", ()))
            if isinstance(candidate, Mapping)
            for item in list(candidate.get("hidden_variable_cues", ()))
            if str(item).strip()
        ]

        entries: list[StrategyJournalEntry] = []
        entries.append(
            _entry(
                reasoning_path="phase_10_meta_cognition_turn",
                worked=_clean_items(
                    [
                        "support-state honesty stayed visible",
                        "diagnosis remained bounded",
                    ],
                    ceiling=3,
                ),
                failed=_clean_items(
                    diagnosis_kinds[:3] or ["no failure was surfaced"],
                    ceiling=3,
                ),
                priors_used=_clean_items(selected_priors or ["no_explicit_prior_selected"], ceiling=3),
                hidden_variables_seen=_clean_items(hidden_variables or ["no_hidden_variable_cue"], ceiling=3),
                question_types_that_still_break=_clean_items(
                    ["weak_diagnosis_request"] if support_state in {"search_needed", "unknown"} else ["contradiction_sensitive_case"],
                    ceiling=2,
                ),
                monitoring_note="Monitor whether the next redirect reduces uncertainty without upgrading support by language alone.",
            )
        )
        if redirect_targets and len(entries) < MAX_STRATEGY_JOURNAL_ENTRIES:
            entries.append(
                _entry(
                    reasoning_path="bounded_redirect_followup",
                    worked=_clean_items(["bounded redirect target chosen"], ceiling=2),
                    failed=_clean_items(["no fresh support yet"], ceiling=2) if support_state in {"search_needed", "unknown"} else _clean_items(["no failure escalation"], ceiling=2),
                    priors_used=_clean_items(selected_priors or ["no_explicit_prior_selected"], ceiling=2),
                    hidden_variables_seen=_clean_items(hidden_variables or ["no_hidden_variable_cue"], ceiling=2),
                    question_types_that_still_break=_clean_items(["under-specified contradiction"], ceiling=2),
                    monitoring_note=f"Redirect targets selected: {', '.join(redirect_targets[:2])}.",
                )
            )

        entries = entries[:MAX_STRATEGY_JOURNAL_ENTRIES]
        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "entry_count": len(entries),
            "entries": [entry.to_dict() for entry in entries],
        }
        return StrategyJournalSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            entry_count=len(entries),
            entries=tuple(entries),
            snapshot_hash=stable_hash_payload(payload),
        )
