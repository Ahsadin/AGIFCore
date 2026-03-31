from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    DiagnosisKind,
    MAX_TRACE_REFS,
    MAX_WEAK_ANSWER_DIAGNOSIS_ITEMS,
    Phase10MetaCognitionError,
    WeakAnswerDiagnosisItem,
    WeakAnswerDiagnosisSnapshot,
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


def _item(
    *,
    kind: DiagnosisKind,
    why_weak: str,
    missing_support_or_signal: str,
    next_step: str,
    support_honesty_preserved: bool,
    supporting_refs: tuple[str, ...],
) -> WeakAnswerDiagnosisItem:
    payload = {
        "kind": kind.value,
        "why_weak": why_weak,
        "missing_support_or_signal": missing_support_or_signal,
        "next_step": next_step,
        "support_honesty_preserved": support_honesty_preserved,
        "supporting_refs": list(supporting_refs),
    }
    return WeakAnswerDiagnosisItem(
        diagnosis_id=make_trace_ref("weak_answer_diagnosis", payload),
        kind=kind,
        why_weak=why_weak,
        missing_support_or_signal=missing_support_or_signal,
        next_step=next_step,
        support_honesty_preserved=support_honesty_preserved,
        supporting_refs=supporting_refs,
        diagnosis_hash=stable_hash_payload(payload),
    )


class WeakAnswerDiagnosisEngine:
    """Explain why an answer remains weak without claiming more certainty than support allows."""

    SCHEMA = "agifcore.phase_10.weak_answer_diagnosis.v1"

    def build_snapshot(
        self,
        *,
        support_state_resolution_state: Mapping[str, Any],
        answer_contract_state: Mapping[str, Any],
        science_world_turn_state: Mapping[str, Any],
        rich_expression_turn_state: Mapping[str, Any],
    ) -> WeakAnswerDiagnosisSnapshot:
        support = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
        )
        answer_contract = require_schema(
            answer_contract_state,
            "agifcore.phase_07.answer_contract.v1",
            "answer_contract_state",
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
        overlay = require_schema(
            rich_expression_turn.get("overlay_contract", {}),
            "agifcore.phase_09.overlay_contract.v1",
            "rich_expression_turn_state.overlay_contract",
        )
        visible_reasoning = require_schema(
            science_world_turn.get("visible_reasoning_summary", {}),
            "agifcore.phase_08.visible_reasoning_summaries.v1",
            "science_world_turn_state.visible_reasoning_summary",
        )
        science_reflection = require_schema(
            science_world_turn.get("science_reflection", {}),
            "agifcore.phase_08.science_reflection.v1",
            "science_world_turn_state.science_reflection",
        )

        turn_id = require_non_empty_str(str(rich_expression_turn.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        final_answer_mode = str(answer_contract.get("final_answer_mode", "unknown")).strip() or "unknown"
        public_response_text = str(overlay.get("public_response_text", "")).strip()
        uncertainty = [str(item).strip() for item in list(overlay.get("uncertainty_statements", ())) if str(item).strip()]
        evidence_refs = _clean_items(
            [str(item).strip() for item in list(overlay.get("evidence_refs", ())) if str(item).strip()],
            ceiling=MAX_TRACE_REFS,
        )
        reflection_records = list(science_reflection.get("records", ()))

        items: list[WeakAnswerDiagnosisItem] = []
        if support_state in {"search_needed", "unknown"}:
            items.append(
                _item(
                    kind=DiagnosisKind.WEAK_SUPPORT,
                    why_weak="The answer cannot be stronger because the lower-phase support state is not grounded.",
                    missing_support_or_signal="support_state remains search_needed or unknown",
                    next_step="obtain the missing local evidence before upgrading confidence",
                    support_honesty_preserved=True,
                    supporting_refs=evidence_refs[:3],
                )
            )
        if uncertainty:
            items.append(
                _item(
                    kind=DiagnosisKind.MISSING_VARIABLE,
                    why_weak="Visible uncertainty still points to at least one unresolved variable.",
                    missing_support_or_signal=uncertainty[0],
                    next_step="clarify or measure the uncertainty-driving variable",
                    support_honesty_preserved=True,
                    supporting_refs=evidence_refs[:3],
                )
            )
        if any("contradiction" in str(record.get("kind", "")).lower() or "contradiction" in str(record.get("note", "")).lower() for record in reflection_records if isinstance(record, Mapping)):
            items.append(
                _item(
                    kind=DiagnosisKind.CONTRADICTION_RISK,
                    why_weak="Science reflection already exposes a contradiction-oriented signal.",
                    missing_support_or_signal="contradiction signal in science_reflection",
                    next_step="re-check the cited support and fall back if the contradiction holds",
                    support_honesty_preserved=True,
                    supporting_refs=evidence_refs[:3],
                )
            )
        if len(public_response_text.split()) < 12 or final_answer_mode in {"search_needed", "unknown", "abstain"}:
            items.append(
                _item(
                    kind=DiagnosisKind.VAGUE_EXPLANATION,
                    why_weak="The current answer shape is too weak to name an exact fault honestly.",
                    missing_support_or_signal=f"final_answer_mode={final_answer_mode}",
                    next_step="reframe the explanation around expected state, actual state, and first visible failure",
                    support_honesty_preserved=True,
                    supporting_refs=evidence_refs[:2],
                )
            )
        if support_state == "inferred":
            items.append(
                _item(
                    kind=DiagnosisKind.SUPPORT_THIN,
                    why_weak="The answer is bounded and useful, but it still rides on inferred support instead of fully grounded support.",
                    missing_support_or_signal="support_state is inferred",
                    next_step="keep the uncertainty visible and avoid precision theater",
                    support_honesty_preserved=True,
                    supporting_refs=evidence_refs[:2],
                )
            )

        items = items[:MAX_WEAK_ANSWER_DIAGNOSIS_ITEMS]
        if len(items) > MAX_WEAK_ANSWER_DIAGNOSIS_ITEMS:
            raise Phase10MetaCognitionError("weak-answer diagnosis item count exceeds Phase 10 ceiling")

        summary = (
            "The answer is weak because support is incomplete or contradicted, so the next safe move is bounded re-checking."
            if items
            else "No bounded weakness was detected."
        )
        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "item_count": len(items),
            "items": [item.to_dict() for item in items],
            "summary": summary,
        }
        return WeakAnswerDiagnosisSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            item_count=len(items),
            items=tuple(items),
            summary=summary,
            snapshot_hash=stable_hash_payload(payload),
        )
