from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    InquiryTriggerKind,
    MAX_ALLOWED_LOCAL_INPUTS,
    MAX_SELF_INITIATED_INQUIRIES,
    MonitoringStatus,
    SelfInitiatedInquiryRecord,
    SelfInitiatedInquirySnapshot,
    optional_bounded_unique,
    require_phase10_turn_state,
    require_schema,
    stable_hash_payload,
)


class SelfInitiatedInquiryEngine:
    SCHEMA = "agifcore.phase_11.self_initiated_inquiry_engine.v1"

    def build_snapshot(
        self,
        *,
        idle_reflection_state: Mapping[str, Any],
        phase10_turn_state: Mapping[str, Any],
        post_adoption_monitoring_state: Mapping[str, Any] | None = None,
    ) -> SelfInitiatedInquirySnapshot:
        idle_reflection = require_schema(idle_reflection_state, "agifcore.phase_11.idle_reflection.v1", "idle_reflection_state")
        phase10_turn = require_phase10_turn_state(phase10_turn_state, "phase10_turn_state")
        overlay = phase10_turn["overlay_contract"]
        observer = phase10_turn.get("meta_cognition_observer", {})
        monitoring_items = []
        if post_adoption_monitoring_state is not None:
            monitoring = require_schema(
                post_adoption_monitoring_state,
                "agifcore.phase_11.post_adoption_monitoring.v1",
                "post_adoption_monitoring_state",
            )
            monitoring_items = list(monitoring.get("items", ()))

        inquiries: list[SelfInitiatedInquiryRecord] = []
        support_state = str(overlay.get("support_state", "unknown")).strip() or "unknown"
        missing_needs = [str(item).strip() for item in list(observer.get("missing_needs", ())) if str(item).strip()]
        contradiction_present = any(
            str(item.get("kind", "")).strip() == InquiryTriggerKind.CONTRADICTION_SIGNAL.value
            for item in list(observer.get("observations", ()))
            if isinstance(item, Mapping)
        )

        trigger_kind: InquiryTriggerKind | None = None
        goal = ""
        if support_state == "search_needed" and missing_needs:
            trigger_kind = InquiryTriggerKind.MISSING_NEED
            goal = missing_needs[0]
        elif contradiction_present and not monitoring_items:
            trigger_kind = InquiryTriggerKind.CONTRADICTION_SIGNAL
            goal = "resolve the contradiction before any candidate can be promoted"
        elif any(str(item.get("current_status", "")).strip() == MonitoringStatus.ESCALATE.value for item in monitoring_items if isinstance(item, Mapping)):
            trigger_kind = InquiryTriggerKind.MONITORING_REGRESSION
            goal = "check whether monitoring drift requires rollback"

        if trigger_kind is not None and len(inquiries) < MAX_SELF_INITIATED_INQUIRIES:
            allowed_local_inputs = optional_bounded_unique(
                [
                    str(overlay.get("observer_ref", "")).strip(),
                    str(overlay.get("diagnosis_ref", "")).strip(),
                    str(overlay.get("strategy_journal_ref", "")).strip(),
                    *list(overlay.get("theory_fragment_refs", ())),
                ],
                ceiling=MAX_ALLOWED_LOCAL_INPUTS,
            )
            payload = {
                "trigger_kind": trigger_kind.value,
                "goal": goal,
                "allowed_local_inputs": list(allowed_local_inputs),
            }
            inquiries.append(
                SelfInitiatedInquiryRecord(
                    inquiry_id=f"inquiry::{stable_hash_payload(payload)[:12]}",
                    trigger_kind=trigger_kind,
                    goal=goal,
                    budget_limit="1 inquiry per cycle, local inputs only",
                    allowed_local_inputs=allowed_local_inputs,
                    stop_condition="stop when the missing need is clarified or the cycle ends",
                    inquiry_hash=stable_hash_payload(payload),
                )
            )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": str(idle_reflection.get("conversation_id")),
            "turn_id": str(idle_reflection.get("turn_id")),
            "inquiry_ids": [item.inquiry_id for item in inquiries],
        }
        return SelfInitiatedInquirySnapshot(
            schema=self.SCHEMA,
            conversation_id=str(idle_reflection.get("conversation_id")),
            turn_id=str(idle_reflection.get("turn_id")),
            inquiry_count=len(inquiries),
            inquiries=tuple(inquiries),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
