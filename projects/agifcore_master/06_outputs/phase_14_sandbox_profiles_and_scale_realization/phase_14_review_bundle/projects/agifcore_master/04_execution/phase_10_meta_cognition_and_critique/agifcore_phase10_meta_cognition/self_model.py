from __future__ import annotations

from typing import Any, Mapping

from .contracts import (
    MAX_SELF_MODEL_RECORDS,
    MAX_TRACE_REFS,
    Phase10MetaCognitionError,
    SelfModelRecord,
    SelfModelSnapshot,
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


def _record(
    *,
    knows: tuple[str, ...],
    infers: tuple[str, ...],
    unknowns: tuple[str, ...],
    answer_mode: str,
    confidence_band: str,
    confidence_reason: str,
    what_would_verify: tuple[str, ...],
    anchor_refs: tuple[str, ...],
) -> SelfModelRecord:
    payload = {
        "knows": list(knows),
        "infers": list(infers),
        "unknowns": list(unknowns),
        "answer_mode": answer_mode,
        "confidence_band": confidence_band,
        "confidence_reason": confidence_reason,
        "what_would_verify": list(what_would_verify),
        "anchor_refs": list(anchor_refs),
    }
    return SelfModelRecord(
        record_id=make_trace_ref("self_model_record", payload),
        knows=knows,
        infers=infers,
        unknowns=unknowns,
        answer_mode=answer_mode,
        confidence_band=confidence_band,
        confidence_reason=confidence_reason,
        what_would_verify=what_would_verify,
        anchor_refs=anchor_refs,
        record_hash=stable_hash_payload(payload),
    )


class SelfModelEngine:
    """Build a bounded self-model over continuity-backed self-knowledge and live support state."""

    SCHEMA = "agifcore.phase_10.self_model.v1"

    def build_snapshot(
        self,
        *,
        support_state_resolution_state: Mapping[str, Any],
        answer_contract_state: Mapping[str, Any],
        self_knowledge_surface_state: Mapping[str, Any],
        rich_expression_turn_state: Mapping[str, Any],
        continuity_memory_state: Mapping[str, Any] | None = None,
    ) -> SelfModelSnapshot:
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
        self_knowledge = require_schema(
            self_knowledge_surface_state,
            "agifcore.phase_07.self_knowledge_surface.v1",
            "self_knowledge_surface_state",
        )
        rich_expression_turn = require_schema(
            rich_expression_turn_state,
            "agifcore.phase_09.rich_expression_turn.v1",
            "rich_expression_turn_state",
        )
        continuity = None
        if continuity_memory_state is not None:
            continuity = require_schema(
                continuity_memory_state,
                "agifcore.phase_04.continuity_memory.v1",
                "continuity_memory_state",
            )

        turn_id = require_non_empty_str(str(answer_contract.get("turn_id", "")).strip(), "turn_id")
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        answer_mode = str(answer_contract.get("final_answer_mode", "unknown")).strip() or "unknown"
        self_statements = [
            str(item.get("statement", "")).strip()
            for item in list(self_knowledge.get("statements", ()))
            if isinstance(item, Mapping) and str(item.get("statement", "")).strip()
        ]
        self_anchor_refs = [
            str(ref).strip()
            for item in list(self_knowledge.get("statements", ()))
            if isinstance(item, Mapping)
            for ref in list(item.get("anchor_refs", ()))
            if str(ref).strip()
        ]
        continuity_refs = [
            str(item.get("anchor_id", "")).strip()
            for item in list((continuity or {}).get("anchors", ()))
            if isinstance(item, Mapping) and str(item.get("anchor_id", "")).strip()
        ]
        uncertainty = [
            str(item).strip()
            for item in list(
                require_schema(
                    rich_expression_turn.get("overlay_contract", {}),
                    "agifcore.phase_09.overlay_contract.v1",
                    "rich_expression_turn_state.overlay_contract",
                ).get("uncertainty_statements", ())
            )
            if str(item).strip()
        ]
        selected_lane = str(rich_expression_turn.get("selected_lane", "unknown")).strip() or "unknown"

        confidence_band = "high" if support_state == "grounded" else "moderate" if support_state == "inferred" else "low"
        confidence_reason = (
            "current lower-phase support is grounded"
            if support_state == "grounded"
            else "current lower-phase support is inferred but bounded"
            if support_state == "inferred"
            else "current lower-phase support remains incomplete"
        )

        records: list[SelfModelRecord] = []
        records.append(
            _record(
                knows=_clean_items(self_statements[:2] or ["AGIFCore can only claim continuity-backed self-knowledge."], ceiling=3),
                infers=_clean_items(
                    [
                        f"current rich-expression lane={selected_lane}",
                        f"current answer mode={answer_mode}",
                    ],
                    ceiling=3,
                ),
                unknowns=_clean_items(
                    uncertainty[:2]
                    or (["fresh local evidence is still needed"] if support_state in {"search_needed", "unknown"} else ["no additional self-model unknown was surfaced"]),
                    ceiling=3,
                ),
                answer_mode=answer_mode,
                confidence_band=confidence_band,
                confidence_reason=confidence_reason,
                what_would_verify=_clean_items(
                    [
                        "recheck the cited evidence trail if contradiction appears",
                        "obtain the missing local evidence before upgrading support",
                    ]
                    if support_state in {"search_needed", "unknown"}
                    else ["re-run contradiction and support checks against current evidence refs"],
                    ceiling=3,
                ),
                anchor_refs=_clean_items(self_anchor_refs + continuity_refs, ceiling=MAX_TRACE_REFS),
            )
        )

        if support_state in {"search_needed", "unknown"} and len(records) < MAX_SELF_MODEL_RECORDS:
            records.append(
                _record(
                    knows=("current answer honesty boundary remains active",),
                    infers=("weak-answer diagnosis is expected to stay bounded",),
                    unknowns=_clean_items(uncertainty[:3] or ["the exact fault cannot be claimed from current state"], ceiling=3),
                    answer_mode=answer_mode,
                    confidence_band="low",
                    confidence_reason="support-state honesty prevents exact fault claims",
                    what_would_verify=("capture the missing local signal before treating this as grounded",),
                    anchor_refs=_clean_items(self_anchor_refs + continuity_refs, ceiling=MAX_TRACE_REFS),
                )
            )

        records = records[:MAX_SELF_MODEL_RECORDS]
        if len(records) > MAX_SELF_MODEL_RECORDS:
            raise Phase10MetaCognitionError("self-model record count exceeds Phase 10 ceiling")

        payload = {
            "schema": self.SCHEMA,
            "turn_id": turn_id,
            "record_count": len(records),
            "records": [record.to_dict() for record in records],
        }
        return SelfModelSnapshot(
            schema=self.SCHEMA,
            turn_id=turn_id,
            record_count=len(records),
            records=tuple(records),
            snapshot_hash=stable_hash_payload(payload),
        )
