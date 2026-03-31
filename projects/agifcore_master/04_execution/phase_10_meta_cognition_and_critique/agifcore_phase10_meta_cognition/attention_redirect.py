from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    AttentionRedirect,
    AttentionRedirectSnapshot,
    MAX_ATTENTION_REDIRECTS,
    RedirectTargetKind,
    make_trace_ref,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)


def _redirect(*, target_kind: RedirectTargetKind, target_ref: str, reason: str, priority: int) -> AttentionRedirect:
    payload = {
        "target_kind": target_kind.value,
        "target_ref": target_ref,
        "reason": reason,
        "priority": priority,
    }
    return AttentionRedirect(
        redirect_id=make_trace_ref("attention_redirect", payload),
        target_kind=target_kind,
        target_ref=target_ref,
        reason=reason,
        priority=priority,
        redirect_hash=stable_hash_payload(payload),
    )


class AttentionRedirectEngine:
    """Choose the next bounded place to look without mutating lower-phase state."""

    SCHEMA = "agifcore.phase_10.attention_redirect.v1"

    def build_snapshot(
        self,
        *,
        meta_cognition_observer_state: Mapping[str, Any],
        weak_answer_diagnosis_state: Mapping[str, Any],
        support_state_resolution_state: Mapping[str, Any],
        rich_expression_turn_state: Mapping[str, Any],
    ) -> AttentionRedirectSnapshot:
        observer = require_schema(
            meta_cognition_observer_state,
            "agifcore.phase_10.meta_cognition_observer.v1",
            "meta_cognition_observer_state",
        )
        diagnosis = require_schema(
            weak_answer_diagnosis_state,
            "agifcore.phase_10.weak_answer_diagnosis.v1",
            "weak_answer_diagnosis_state",
        )
        support = require_schema(
            support_state_resolution_state,
            "agifcore.phase_07.support_state_logic.v1",
            "support_state_resolution_state",
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

        turn_id = require_non_empty_str(str(rich_expression_turn.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        redirects: list[AttentionRedirect] = []

        if support_state in {"search_needed", "unknown"}:
            redirects.append(
                _redirect(
                    target_kind=RedirectTargetKind.SUPPORT_STATE,
                    target_ref=str(support.get("resolution_hash", "")).strip() or "phase7.support_state_logic",
                    reason="support-state honesty requires a bounded evidence re-check before stronger claims",
                    priority=1,
                )
            )
        if any("contradiction" in str(item.get("kind", "")).lower() for item in list(diagnosis.get("items", ())) if isinstance(item, Mapping)):
            redirects.append(
                _redirect(
                    target_kind=RedirectTargetKind.CONTRADICTION_PROBE,
                    target_ref=str(overlay.get("contract_hash", "")).strip() or "phase9.overlay_contract",
                    reason="contradiction-oriented diagnosis needs a bounded contradiction probe",
                    priority=2,
                )
            )
        elif observer.get("observation_count", 0):
            redirects.append(
                _redirect(
                    target_kind=RedirectTargetKind.RICH_EXPRESSION,
                    target_ref=str(rich_expression_turn.get("snapshot_hash", "")).strip() or "phase9.rich_expression_turn",
                    reason="rich-expression output should be re-checked against the weak-answer diagnosis",
                    priority=2,
                )
            )

        redirects = redirects[:MAX_ATTENTION_REDIRECTS]
        stop_reason = "bounded_redirects_emitted" if redirects else "no_redirect"
        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "redirect_count": len(redirects),
            "redirects": [item.to_dict() for item in redirects],
            "stop_reason": stop_reason,
        }
        return AttentionRedirectSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            redirect_count=len(redirects),
            redirects=tuple(redirects),
            stop_reason=stop_reason,
            snapshot_hash=stable_hash_payload(payload),
        )
