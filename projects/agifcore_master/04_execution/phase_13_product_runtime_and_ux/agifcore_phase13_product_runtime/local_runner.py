from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .contracts import (
    BLOCKED_SURFACES,
    CONVERSATION_TURN_SCHEMA,
    DESKTOP_UI_VIEWS,
    MAX_EVIDENCE_REFS,
    PHASE10_SCHEMA,
    PHASE11_SCHEMA,
    PHASE12_SCHEMA,
    PUBLIC_SURFACES,
    ROUTE_TO_SURFACE,
    SESSION_OPEN_SCHEMA,
    bounded_unique,
    build_blocked_surface_record,
    infer_final_answer_mode,
    infer_knowledge_gap_reason,
    infer_next_action,
    make_ref,
    normalize_support_state,
    require_mapping,
    require_schema,
    stable_hash_payload,
)


class LocalRunner:
    def __init__(
        self,
        *,
        fixture: Mapping[str, Any],
        phase10_turn_state: Mapping[str, Any],
        phase11_cycle_state: Mapping[str, Any],
        phase12_cycle_state: Mapping[str, Any],
    ) -> None:
        self._fixture = require_mapping(fixture, "fixture")
        self._phase10_turn = require_schema(phase10_turn_state, PHASE10_SCHEMA, "phase10_turn_state")
        self._phase11_cycle = require_schema(
            phase11_cycle_state,
            PHASE11_SCHEMA,
            "phase11_cycle_state",
        )
        self._phase12_cycle = require_schema(
            phase12_cycle_state,
            PHASE12_SCHEMA,
            "phase12_cycle_state",
        )
        self._phase10_overlay = require_mapping(self._phase10_turn.get("overlay_contract"), "phase10_overlay")
        self._phase11_overlay = require_mapping(self._phase11_cycle.get("overlay_contract"), "phase11_overlay")
        self._phase12_overlay = require_mapping(self._phase12_cycle.get("overlay_contract"), "phase12_overlay")
        self._conversation_id = str(self._phase12_cycle.get("conversation_id"))
        self._turn_id = str(self._phase12_cycle.get("turn_id"))
        self._support_state = normalize_support_state(str(self._phase12_overlay.get("support_state", "unknown")))
        self._selected_outcome = str(self._phase10_overlay.get("selected_outcome", "recheck_support"))
        self._session_id = make_ref(
            "phase13_session",
            {
                "conversation_id": self._conversation_id,
                "turn_id": self._turn_id,
                "phase12_cycle_hash": self._phase12_cycle.get("snapshot_hash"),
            },
        )
        self._source_prompt = str(self._fixture.get("intake", {}).get("raw_text", "")).strip()
        self._public_explanation = str(self._phase10_overlay.get("public_explanation", "")).strip()
        rich_expression_turn = self._fixture.get("rich_expression_turn") or {}
        synthesis_lane = rich_expression_turn.get("synthesis") or {}
        self._synthesis_summary = str(synthesis_lane.get("merged_summary", "")).strip()
        self._response_text = self._public_explanation or self._synthesis_summary or (
            "The product shell preserved the lower-phase trace but could not derive a safe user-facing summary."
        )
        self._evidence_refs = bounded_unique(
            [
                *list(self._phase10_overlay.get("evidence_refs", [])),
                *list(self._phase11_overlay.get("evidence_refs", [])),
                *list(self._phase12_overlay.get("evidence_refs", [])),
                str(self._phase10_turn.get("snapshot_hash", "")),
                str(self._phase11_cycle.get("snapshot_hash", "")),
                str(self._phase12_cycle.get("snapshot_hash", "")),
            ],
            ceiling=MAX_EVIDENCE_REFS,
            field_name="runner_evidence_refs",
        )
        self._trace_anchor_refs = bounded_unique(
            [
                str(self._phase10_overlay.get("observer_ref", "")),
                str(self._phase10_overlay.get("diagnosis_ref", "")),
                str(self._phase10_overlay.get("strategy_journal_ref", "")),
                str(self._phase10_overlay.get("self_model_ref", "")),
                str(self._phase10_overlay.get("skeptic_ref", "")),
                *list(self._phase11_overlay.get("monitoring_refs", [])),
                *list(self._phase11_overlay.get("rollback_refs", [])),
                *list(self._phase11_overlay.get("inquiry_refs", [])),
                *list(self._phase12_overlay.get("selected_gap_ids", [])),
                *list(self._phase12_overlay.get("candidate_theory_ids", [])),
                *list(self._phase12_overlay.get("candidate_domain_ids", [])),
                *list(self._phase12_overlay.get("candidate_procedure_ids", [])),
                *list(self._phase12_overlay.get("reorganization_refs", [])),
            ],
            ceiling=MAX_EVIDENCE_REFS,
            field_name="runner_trace_anchor_refs",
        )
        self._memory_review_ref = make_ref(
            "memory_review",
            {
                "session_id": self._session_id,
                "conversation_id": self._conversation_id,
                "turn_id": self._turn_id,
                "phase12_cycle_hash": self._phase12_cycle.get("snapshot_hash"),
            },
        )

    def session_open(self) -> dict[str, Any]:
        blocked_surfaces = [
            build_blocked_surface_record(
                surface_name=surface_name,
                reason_code="reserved_surface_fail_closed",
                user_guidance=(
                    "This control surface stays blocked in the first Phase 13 slice so the product shell "
                    "cannot widen runtime authority."
                ),
                evidence_refs=self._evidence_refs,
                next_steps=("use conversation_turn", "inspect fail_closed_help"),
            )
            for surface_name in BLOCKED_SURFACES
        ]
        payload = {
            "schema": SESSION_OPEN_SCHEMA,
            "session_id": self._session_id,
            "conversation_id": self._conversation_id,
            "turn_id": self._turn_id,
            "support_state": self._support_state,
            "available_surfaces": list(PUBLIC_SURFACES),
            "blocked_surfaces": blocked_surfaces,
            "route_count": len(ROUTE_TO_SURFACE),
            "ui_view_count": len(DESKTOP_UI_VIEWS),
            "phase10_turn_hash": str(self._phase10_turn.get("snapshot_hash", "")),
            "phase11_cycle_hash": str(self._phase11_cycle.get("snapshot_hash", "")),
            "phase12_cycle_hash": str(self._phase12_cycle.get("snapshot_hash", "")),
            "public_explanation": self._public_explanation,
            "support_honesty_preserved": bool(self._phase10_overlay.get("support_honesty_preserved", True)),
            "evidence_refs": list(self._evidence_refs),
        }
        return {
            **payload,
            "session_hash": stable_hash_payload(payload),
        }

    def conversation_turn(self, *, user_text: str | None = None) -> dict[str, Any]:
        request_text = str(user_text or self._source_prompt or self._public_explanation).strip()
        knowledge_gap_reason = infer_knowledge_gap_reason(
            support_state=self._support_state,
            selected_outcome=self._selected_outcome,
        )
        next_action = infer_next_action(
            support_state=self._support_state,
            selected_outcome=self._selected_outcome,
        )
        final_answer_mode = infer_final_answer_mode(
            support_state=self._support_state,
            selected_outcome=self._selected_outcome,
        )
        response_kind = "bounded_answer"
        if final_answer_mode == "clarify":
            response_kind = "guided_clarification"
        elif final_answer_mode == "search_needed":
            response_kind = "guided_search"
        elif final_answer_mode == "unknown":
            response_kind = "fail_closed_unknown"
        payload = {
            "schema": CONVERSATION_TURN_SCHEMA,
            "session_id": self._session_id,
            "conversation_id": self._conversation_id,
            "turn_id": self._turn_id,
            "request_text": request_text,
            "response_text": self._response_text,
            "response_kind": response_kind,
            "abstain_or_answer": "abstain" if final_answer_mode in {"clarify", "search_needed", "unknown"} else "answer",
            "final_answer_mode": final_answer_mode,
            "support_state": self._support_state,
            "knowledge_gap_reason": knowledge_gap_reason,
            "next_action": next_action,
            "selected_outcome": self._selected_outcome,
            "support_honesty_preserved": bool(self._phase10_overlay.get("support_honesty_preserved", True)),
            "memory_review_ref": self._memory_review_ref,
            "trace_anchor_refs": list(self._trace_anchor_refs),
            "evidence_refs": list(self._evidence_refs),
            "phase12_cycle_hash": str(self._phase12_cycle.get("snapshot_hash", "")),
            "phase11_cycle_hash": str(self._phase11_cycle.get("snapshot_hash", "")),
            "phase10_turn_hash": str(self._phase10_turn.get("snapshot_hash", "")),
            "structural_growth_refs": list(self._phase12_overlay.get("selected_gap_ids", [])),
        }
        return {
            **payload,
            "turn_hash": stable_hash_payload(payload),
        }

    @property
    def phase10_turn(self) -> dict[str, Any]:
        return deepcopy(self._phase10_turn)

    @property
    def phase11_cycle(self) -> dict[str, Any]:
        return deepcopy(self._phase11_cycle)

    @property
    def phase12_cycle(self) -> dict[str, Any]:
        return deepcopy(self._phase12_cycle)
