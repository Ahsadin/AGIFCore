from __future__ import annotations

from typing import Any, Mapping

from .attention_redirect import AttentionRedirectEngine
from .contracts import (
    MAX_PUBLIC_EXPLANATION_CHARACTERS,
    CritiqueOutcome,
    MetaCognitionTurnSnapshot,
    Phase10OverlayContract,
    Phase10MetaCognitionError,
    make_trace_ref,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)
from .meta_cognition_layer import MetaCognitionLayerEngine
from .meta_cognition_observer import MetaCognitionObserverEngine
from .self_model import SelfModelEngine
from .skeptic_counterexample import SkepticCounterexampleEngine
from .strategy_journal import StrategyJournalEngine
from .surprise_engine import SurpriseEngine
from .theory_fragments import TheoryFragmentsEngine
from .thinker_tissue import ThinkerTissueEngine
from .weak_answer_diagnosis import WeakAnswerDiagnosisEngine


class MetaCognitionTurnError(Phase10MetaCognitionError):
    """Raised when the composed Phase 10 turn is inconsistent."""


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


def _clip_text(text: str, *, ceiling: int = MAX_PUBLIC_EXPLANATION_CHARACTERS) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= ceiling:
        return cleaned
    return cleaned[: ceiling - 1].rstrip() + "…"


def _optional_ref(value: Any) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(str(value).split()).strip()
    return cleaned or None


class MetaCognitionTurnEngine:
    """Thin coordinator over read-only Phase 7, Phase 8, and Phase 9 snapshots."""

    SCHEMA = "agifcore.phase_10.meta_cognition_turn.v1"

    def __init__(self) -> None:
        self.self_model = SelfModelEngine()
        self.meta_cognition_observer = MetaCognitionObserverEngine()
        self.weak_answer_diagnosis = WeakAnswerDiagnosisEngine()
        self.attention_redirect = AttentionRedirectEngine()
        self.skeptic_counterexample = SkepticCounterexampleEngine()
        self.thinker_tissue = ThinkerTissueEngine()
        self.surprise_engine = SurpriseEngine()
        self.theory_fragments = TheoryFragmentsEngine()
        self.strategy_journal = StrategyJournalEngine()
        self.meta_cognition_layer = MetaCognitionLayerEngine()

    def run_turn(
        self,
        *,
        support_state_resolution_state: Mapping[str, Any],
        answer_contract_state: Mapping[str, Any],
        self_knowledge_surface_state: Mapping[str, Any],
        science_world_turn_state: Mapping[str, Any],
        rich_expression_turn_state: Mapping[str, Any],
        continuity_memory_state: Mapping[str, Any] | None = None,
    ) -> MetaCognitionTurnSnapshot:
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
        if continuity_memory_state is not None:
            require_schema(
                continuity_memory_state,
                "agifcore.phase_04.continuity_memory.v1",
                "continuity_memory_state",
            )

        conversation_id = require_non_empty_str(str(answer_contract.get("conversation_id", "")).strip(), "conversation_id")
        turn_id = require_non_empty_str(str(answer_contract.get("turn_id", "")).strip(), "turn_id")
        if str(rich_expression_turn.get("conversation_id", "")).strip() != conversation_id:
            raise MetaCognitionTurnError("rich_expression_turn_state conversation_id must match answer_contract_state")
        if str(rich_expression_turn.get("turn_id", "")).strip() != turn_id:
            raise MetaCognitionTurnError("rich_expression_turn_state turn_id must match answer_contract_state")
        if str(science_world_turn.get("conversation_id", "")).strip() != conversation_id:
            raise MetaCognitionTurnError("science_world_turn_state conversation_id must match answer_contract_state")
        if str(science_world_turn.get("turn_id", "")).strip() != turn_id:
            raise MetaCognitionTurnError("science_world_turn_state turn_id must match answer_contract_state")

        self_model = self.self_model.build_snapshot(
            support_state_resolution_state=support,
            answer_contract_state=answer_contract,
            self_knowledge_surface_state=self_knowledge,
            rich_expression_turn_state=rich_expression_turn,
            continuity_memory_state=continuity_memory_state,
        )
        observer = self.meta_cognition_observer.build_snapshot(
            support_state_resolution_state=support,
            science_world_turn_state=science_world_turn,
            rich_expression_turn_state=rich_expression_turn,
        )
        diagnosis = self.weak_answer_diagnosis.build_snapshot(
            support_state_resolution_state=support,
            answer_contract_state=answer_contract,
            science_world_turn_state=science_world_turn,
            rich_expression_turn_state=rich_expression_turn,
        )
        redirect = self.attention_redirect.build_snapshot(
            meta_cognition_observer_state=observer.to_dict(),
            weak_answer_diagnosis_state=diagnosis.to_dict(),
            support_state_resolution_state=support,
            rich_expression_turn_state=rich_expression_turn,
        )
        skeptic = self.skeptic_counterexample.build_snapshot(
            support_state_resolution_state=support,
            science_world_turn_state=science_world_turn,
            rich_expression_turn_state=rich_expression_turn,
        )
        thinker = self.thinker_tissue.build_snapshot(
            meta_cognition_observer_state=observer.to_dict(),
            weak_answer_diagnosis_state=diagnosis.to_dict(),
            skeptic_counterexample_state=skeptic.to_dict(),
        )
        surprise = self.surprise_engine.build_snapshot(
            meta_cognition_observer_state=observer.to_dict(),
            skeptic_counterexample_state=skeptic.to_dict(),
            support_state_resolution_state=support,
            science_world_turn_state=science_world_turn,
        )
        theory_fragments = self.theory_fragments.build_snapshot(
            surprise_engine_state=surprise.to_dict(),
            thinker_tissue_state=thinker.to_dict(),
            science_world_turn_state=science_world_turn,
            rich_expression_turn_state=rich_expression_turn,
        )
        strategy_journal = self.strategy_journal.build_snapshot(
            self_model_state=self_model.to_dict(),
            weak_answer_diagnosis_state=diagnosis.to_dict(),
            attention_redirect_state=redirect.to_dict(),
            support_state_resolution_state=support,
            science_world_turn_state=science_world_turn,
        )
        meta_layer = self.meta_cognition_layer.build_snapshot(
            self_model_state=self_model.to_dict(),
            meta_cognition_observer_state=observer.to_dict(),
            attention_redirect_state=redirect.to_dict(),
            skeptic_counterexample_state=skeptic.to_dict(),
            strategy_journal_state=strategy_journal.to_dict(),
            thinker_tissue_state=thinker.to_dict(),
            surprise_engine_state=surprise.to_dict(),
            theory_fragments_state=theory_fragments.to_dict(),
            weak_answer_diagnosis_state=diagnosis.to_dict(),
            support_state_resolution_state=support,
        )

        rich_overlay = require_schema(
            rich_expression_turn.get("overlay_contract", {}),
            "agifcore.phase_09.overlay_contract.v1",
            "rich_expression_turn_state.overlay_contract",
        )
        support_state = str(support.get("support_state", "unknown")).strip() or "unknown"
        public_explanation = diagnosis.summary
        if meta_layer.selected_outcome is CritiqueOutcome.ABSTAIN:
            public_explanation = "The contradiction check stayed unresolved, so the safe outcome is to abstain rather than pretend certainty."
        elif meta_layer.selected_outcome is CritiqueOutcome.RECHECK_SUPPORT:
            public_explanation = "The answer is bounded but weak because support is incomplete, so the next safe move is to re-check support."
        elif meta_layer.selected_outcome is CritiqueOutcome.REFRAME_EXPLANATION:
            public_explanation = "The answer needs a tighter explanation shape that keeps the same support honesty boundary."
        elif meta_layer.selected_outcome is CritiqueOutcome.CLARIFY:
            public_explanation = "A missing variable or ambiguity remains, so the next safe move is a bounded clarification."
        public_explanation = _clip_text(public_explanation)

        self_model_ref = make_trace_ref("self_model", {"turn_id": turn_id, "snapshot_hash": self_model.snapshot_hash})
        observer_ref = make_trace_ref("meta_observer", {"turn_id": turn_id, "snapshot_hash": observer.snapshot_hash})
        strategy_journal_ref = make_trace_ref("strategy_journal", {"turn_id": turn_id, "snapshot_hash": strategy_journal.snapshot_hash})
        skeptic_ref = make_trace_ref("skeptic", {"turn_id": turn_id, "snapshot_hash": skeptic.snapshot_hash})
        surprise_ref = make_trace_ref("surprise", {"turn_id": turn_id, "snapshot_hash": surprise.snapshot_hash})
        diagnosis_ref = make_trace_ref("weak_answer_diagnosis", {"turn_id": turn_id, "snapshot_hash": diagnosis.snapshot_hash})
        redirect_refs = _clean_items(
            [str(item.get("redirect_id", "")).strip() for item in list(redirect.to_dict().get("redirects", ())) if isinstance(item, Mapping) and str(item.get("redirect_id", "")).strip()],
            ceiling=8,
        ) if redirect.redirect_count else ()
        theory_fragment_refs = tuple(fragment.fragment_id for fragment in theory_fragments.fragments)
        upstream_revision_trace_ref = _optional_ref(rich_overlay.get("revision_trace_ref"))
        upstream_consolidation_trace_ref = _optional_ref(rich_overlay.get("consolidation_trace_ref"))
        upstream_reorganization_trace_ref = _optional_ref(rich_overlay.get("reorganization_trace_ref"))
        evidence_refs = _clean_items(
            [
                *[str(item).strip() for item in list(rich_overlay.get("evidence_refs", ())) if str(item).strip()],
                str(support.get("resolution_hash", "")).strip(),
                str(science_world_turn.get("snapshot_hash", "")).strip(),
                str(rich_expression_turn.get("snapshot_hash", "")).strip(),
            ],
            ceiling=24,
        )
        overlay_payload = {
            "schema": "agifcore.phase_10.overlay_contract.v1",
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "selected_outcome": meta_layer.selected_outcome.value,
            "phase7_interfaces": [
                str(answer_contract.get("schema")),
                str(self_knowledge.get("schema")),
                "agifcore.phase_07.support_state_logic.v1",
            ],
            "phase8_interfaces": [
                str(science_world_turn.get("schema")),
                str(science_world_turn.get("visible_reasoning_summary", {}).get("schema", "")),
                str(science_world_turn.get("science_reflection", {}).get("schema", "")),
            ],
            "phase9_interfaces": [
                str(rich_expression_turn.get("schema")),
                str(rich_overlay.get("schema")),
            ],
            "support_state": support_state,
            "support_honesty_preserved": all(bool(item.support_honesty_preserved) for item in diagnosis.items),
            "public_explanation": public_explanation,
            "self_model_ref": self_model_ref,
            "observer_ref": observer_ref,
            "strategy_journal_ref": strategy_journal_ref,
            "skeptic_ref": skeptic_ref,
            "surprise_ref": surprise_ref,
            "theory_fragment_refs": list(theory_fragment_refs),
            "diagnosis_ref": diagnosis_ref,
            "redirect_refs": list(redirect_refs),
            "upstream_revision_trace_ref": upstream_revision_trace_ref,
            "upstream_consolidation_trace_ref": upstream_consolidation_trace_ref,
            "upstream_reorganization_trace_ref": upstream_reorganization_trace_ref,
            "evidence_refs": list(evidence_refs),
        }
        overlay_contract = Phase10OverlayContract(
            schema="agifcore.phase_10.overlay_contract.v1",
            conversation_id=conversation_id,
            turn_id=turn_id,
            selected_outcome=meta_layer.selected_outcome,
            phase7_interfaces=tuple(overlay_payload["phase7_interfaces"]),
            phase8_interfaces=tuple(overlay_payload["phase8_interfaces"]),
            phase9_interfaces=tuple(overlay_payload["phase9_interfaces"]),
            support_state=support_state,
            support_honesty_preserved=bool(overlay_payload["support_honesty_preserved"]),
            public_explanation=public_explanation,
            self_model_ref=self_model_ref,
            observer_ref=observer_ref,
            strategy_journal_ref=strategy_journal_ref,
            skeptic_ref=skeptic_ref,
            surprise_ref=surprise_ref,
            theory_fragment_refs=theory_fragment_refs,
            diagnosis_ref=diagnosis_ref,
            redirect_refs=redirect_refs,
            upstream_revision_trace_ref=upstream_revision_trace_ref,
            upstream_consolidation_trace_ref=upstream_consolidation_trace_ref,
            upstream_reorganization_trace_ref=upstream_reorganization_trace_ref,
            evidence_refs=evidence_refs,
            contract_hash=stable_hash_payload(overlay_payload),
        )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "support_resolution_hash": str(support.get("resolution_hash", "")).strip(),
            "self_knowledge_hash": str(self_knowledge.get("snapshot_hash", "")).strip(),
            "answer_contract_hash": str(answer_contract.get("contract_hash", "")).strip(),
            "science_world_turn_hash": str(science_world_turn.get("snapshot_hash", "")).strip(),
            "rich_expression_turn_hash": str(rich_expression_turn.get("snapshot_hash", "")).strip(),
            "self_model_hash": self_model.snapshot_hash,
            "meta_cognition_layer_hash": meta_layer.snapshot_hash,
            "attention_redirect_hash": redirect.snapshot_hash,
            "meta_cognition_observer_hash": observer.snapshot_hash,
            "skeptic_counterexample_hash": skeptic.snapshot_hash,
            "strategy_journal_hash": strategy_journal.snapshot_hash,
            "thinker_tissue_hash": thinker.snapshot_hash,
            "surprise_engine_hash": surprise.snapshot_hash,
            "theory_fragments_hash": theory_fragments.snapshot_hash,
            "weak_answer_diagnosis_hash": diagnosis.snapshot_hash,
            "overlay_contract_hash": overlay_contract.contract_hash,
        }
        return MetaCognitionTurnSnapshot(
            schema=self.SCHEMA,
            conversation_id=conversation_id,
            turn_id=turn_id,
            support_resolution_hash=str(support.get("resolution_hash", "")).strip(),
            self_knowledge_hash=str(self_knowledge.get("snapshot_hash", "")).strip(),
            answer_contract_hash=str(answer_contract.get("contract_hash", "")).strip(),
            science_world_turn_hash=str(science_world_turn.get("snapshot_hash", "")).strip(),
            rich_expression_turn_hash=str(rich_expression_turn.get("snapshot_hash", "")).strip(),
            self_model=self_model,
            meta_cognition_layer=meta_layer,
            attention_redirect=redirect,
            meta_cognition_observer=observer,
            skeptic_counterexample=skeptic,
            strategy_journal=strategy_journal,
            thinker_tissue=thinker,
            surprise_engine=surprise,
            theory_fragments=theory_fragments,
            weak_answer_diagnosis=diagnosis,
            overlay_contract=overlay_contract,
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
