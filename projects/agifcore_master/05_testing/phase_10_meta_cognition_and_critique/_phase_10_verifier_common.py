from __future__ import annotations

import importlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

PHASE = "10"
PHASE_NAME = "phase_10_meta_cognition_and_critique"
OUTPUT_ROOT_NAME = "06_outputs"
RUNTIME_PACKAGE = "agifcore_phase10_meta_cognition"
PHASE_10_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique"
PHASE_09_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition"
PHASE_07_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_07_conversation_core"

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/01_plan/DEMO_PROTOCOL.md",
)

CONTRACT_REFS = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/self_knowledge_surface.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/science_world_turn.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/contracts.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/rich_expression_turn.py",
)

RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/contracts.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/self_model.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/meta_cognition_layer.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/attention_redirect.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/meta_cognition_observer.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/skeptic_counterexample.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/strategy_journal.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/thinker_tissue.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/surprise_engine.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/theory_fragments.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/weak_answer_diagnosis.py",
    "projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/meta_cognition_turn.py",
)

COMMON_TEST_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/_phase_10_verifier_common.py"

REQUIRED_REPORT_FILES = (
    "phase_10_self_model_report.json",
    "phase_10_meta_cognition_layer_report.json",
    "phase_10_attention_redirect_report.json",
    "phase_10_meta_cognition_observer_report.json",
    "phase_10_skeptic_counterexample_report.json",
    "phase_10_strategy_journal_report.json",
    "phase_10_thinker_tissue_report.json",
    "phase_10_surprise_engine_report.json",
    "phase_10_theory_fragments_report.json",
    "phase_10_weak_answer_diagnosis_report.json",
)

EXPECTED_REPORT_VERIFIERS = {
    "phase_10_self_model_report.json": "verify_phase_10_self_model",
    "phase_10_meta_cognition_layer_report.json": "verify_phase_10_meta_cognition_layer",
    "phase_10_attention_redirect_report.json": "verify_phase_10_attention_redirect",
    "phase_10_meta_cognition_observer_report.json": "verify_phase_10_meta_cognition_observer",
    "phase_10_skeptic_counterexample_report.json": "verify_phase_10_skeptic_counterexample",
    "phase_10_strategy_journal_report.json": "verify_phase_10_strategy_journal",
    "phase_10_thinker_tissue_report.json": "verify_phase_10_thinker_tissue",
    "phase_10_surprise_engine_report.json": "verify_phase_10_surprise_engine",
    "phase_10_theory_fragments_report.json": "verify_phase_10_theory_fragments",
    "phase_10_weak_answer_diagnosis_report.json": "verify_phase_10_weak_answer_diagnosis",
}


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
TEST_ROOT = PROJECT_ROOT / "05_testing" / PHASE_NAME
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_10_evidence"
DEMO_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_10_demo_bundle"
MANIFEST_PATH = EVIDENCE_DIR / "phase_10_evidence_manifest.json"


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_paths() -> None:
    for runtime_parent in (
        REPO_ROOT / PHASE_10_RUNTIME_PARENT,
        REPO_ROOT / PHASE_09_RUNTIME_PARENT,
        REPO_ROOT / PHASE_07_RUNTIME_PARENT,
    ):
        runtime_str = str(runtime_parent)
        if runtime_str not in sys.path:
            sys.path.insert(0, runtime_str)


ensure_runtime_import_paths()

from agifcore_phase10_meta_cognition.contracts import make_trace_ref, stable_hash_payload
from agifcore_phase10_meta_cognition.meta_cognition_turn import MetaCognitionTurnEngine
from agifcore_phase7_conversation.self_knowledge_surface import SelfKnowledgeSurfaceEngine
from agifcore_phase9_rich_expression.rich_expression_turn import RichExpressionTurnEngine


def dump_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[str]) -> list[str]:
    return [path for path in paths if not (REPO_ROOT / path).exists()]


def runtime_modules_available(module_names: tuple[str, ...]) -> bool:
    try:
        for module_name in module_names:
            importlib.import_module(module_name)
    except Exception:
        return False
    return True


def dedupe_paths(paths: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        result.append(path)
    return result


def checked_files_for(verifier_file: str) -> list[str]:
    return dedupe_paths([*PLAN_REFS, *CONTRACT_REFS, *RUNTIME_FILES, COMMON_TEST_FILE, verifier_file])


def build_blocked_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertion_ids: list[str],
    blocker_kind: str,
    blocker_message: str,
    missing: list[str] | None = None,
) -> dict[str, Any]:
    blocker: dict[str, Any] = {"kind": blocker_kind, "message": blocker_message}
    if missing:
        blocker["missing_files"] = missing
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "blocked",
        "blocker": blocker,
        "checked_files": checked_files,
        "assertions": [{"id": item, "result": "blocked"} for item in assertion_ids],
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "notes": ["Phase 10 remains open", "no approval implied"],
    }


def build_pass_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertions: list[dict[str, Any]],
    anchors: Mapping[str, Any],
    notes: list[str],
) -> dict[str, Any]:
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "pass",
        "checked_files": checked_files,
        "assertions": assertions,
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "anchors": dict(anchors),
        "notes": [*notes, "Phase 10 remains open", "no approval implied"],
    }


def refresh_evidence_manifest() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    missing_reports: list[str] = []
    invalid_reports: list[str] = []
    for filename in REQUIRED_REPORT_FILES:
        report_path = EVIDENCE_DIR / filename
        if not report_path.exists():
            missing_reports.append(filename)
            continue
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        status = str(payload.get("status", "unknown"))
        if status not in {"pass", "blocked"}:
            invalid_reports.append(filename)
        if payload.get("phase") != PHASE:
            invalid_reports.append(filename)
        if payload.get("verifier") != EXPECTED_REPORT_VERIFIERS[filename]:
            invalid_reports.append(filename)
        reports.append(
            {
                "report_id": filename.removeprefix("phase_10_").removesuffix("_report.json"),
                "path": rel(report_path),
                "status": status,
            }
        )
    invalid_reports = sorted(set(invalid_reports))
    overall_pass = (
        not missing_reports
        and not invalid_reports
        and len(reports) == len(REQUIRED_REPORT_FILES)
        and all(report["status"] == "pass" for report in reports)
    )
    manifest = {
        "phase": PHASE,
        "phase_remains_open": True,
        "required_report_count": len(REQUIRED_REPORT_FILES),
        "available_report_count": len(reports),
        "missing_reports": missing_reports,
        "invalid_reports": invalid_reports,
        "reports": reports,
        "status": "phase_10_verifier_family_pass" if overall_pass else "phase_10_verifier_family_incomplete",
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 10 remains open",
            "manifest is rebuilt from actual report files on disk",
            "no approval implied",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def write_report(report_path: Path, payload: Mapping[str, Any]) -> None:
    dump_json(report_path, payload)
    refresh_evidence_manifest()


def assert_inputs_unchanged(before: Any, after: Any, field_name: str) -> None:
    if before != after:
        raise AssertionError(f"{field_name} mutated during verification")


def deep_copy(value: Any) -> Any:
    return deepcopy(value)


def build_phase7_intake_state(
    *,
    conversation_id: str,
    turn_id: str,
    raw_text: str,
    active_context_refs: tuple[str, ...] = (),
) -> dict[str, Any]:
    normalized_text = " ".join(raw_text.split()).strip().lower()
    base = {
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "raw_text": raw_text,
        "normalized_text": normalized_text,
        "active_context_refs": list(active_context_refs),
        "token_count": len(raw_text.split()),
        "character_count": len(raw_text),
        "contains_code_block": "```" in raw_text,
        "ends_with_question": raw_text.rstrip().endswith("?"),
    }
    base["intake_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_07.raw_text_intake.v1", **base}


def build_phase7_question_interpretation_state(
    *,
    conversation_id: str,
    turn_id: str,
    raw_text_hash: str,
    user_intent: str,
    discourse_mode_hint: str,
    question_category: str,
    target_domain_hint: str | None,
    live_current_requested: bool,
    ambiguous_request: bool,
    self_knowledge_requested: bool,
    local_artifact_requested: bool,
    correction_hint: bool,
    repeated_fact_hint: bool,
    comparison_requested: bool,
    extracted_terms: tuple[str, ...],
    signal_notes: tuple[str, ...],
) -> dict[str, Any]:
    base = {
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "raw_text_hash": raw_text_hash,
        "user_intent": user_intent,
        "discourse_mode_hint": discourse_mode_hint,
        "question_category": question_category,
        "target_domain_hint": target_domain_hint,
        "live_current_requested": live_current_requested,
        "ambiguous_request": ambiguous_request,
        "self_knowledge_requested": self_knowledge_requested,
        "local_artifact_requested": local_artifact_requested,
        "correction_hint": correction_hint,
        "repeated_fact_hint": repeated_fact_hint,
        "comparison_requested": comparison_requested,
        "token_count": len(user_intent.split()),
        "extracted_terms": list(extracted_terms),
        "signal_notes": list(signal_notes),
    }
    base["interpretation_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_07.question_interpretation.v1", **base}


def build_phase7_support_resolution_state(
    *,
    conversation_id: str,
    turn_id: str,
    support_state: str,
    knowledge_gap_reason: str,
    next_action: str,
    evidence_refs: tuple[str, ...] = (),
    blocked_refs: tuple[str, ...] = (),
    selected_domain_ids: tuple[str, ...] = (),
    reason_codes: tuple[str, ...] = (),
) -> dict[str, Any]:
    base = {
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "support_state": support_state,
        "knowledge_gap_reason": knowledge_gap_reason,
        "next_action": next_action,
        "evidence_refs": list(evidence_refs),
        "blocked_refs": list(blocked_refs),
        "selected_domain_ids": list(selected_domain_ids),
        "reason_codes": list(reason_codes),
        "memory_review_ref": make_trace_ref("memory_review", {"conversation_id": conversation_id, "turn_id": turn_id, "support_state": support_state}),
        "simulation_trace_ref": make_trace_ref("simulation_trace", {"conversation_id": conversation_id, "turn_id": turn_id}),
        "critic_trace_ref": make_trace_ref("critic_trace", {"conversation_id": conversation_id, "turn_id": turn_id}),
        "governance_trace_ref": make_trace_ref("governance_trace", {"conversation_id": conversation_id, "turn_id": turn_id}),
    }
    base["resolution_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_07.support_state_logic.v1", **base}


def build_phase7_utterance_plan_state(
    *,
    conversation_id: str,
    turn_id: str,
    discourse_mode: str,
    response_sections: tuple[str, ...],
    sentence_obligations: tuple[str, ...],
    constraint_slots: tuple[str, ...],
    branch_count: int = 4,
) -> dict[str, Any]:
    base = {
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "discourse_mode": discourse_mode,
        "response_sections": list(response_sections),
        "sentence_obligations": list(sentence_obligations),
        "constraint_slots": list(constraint_slots),
        "branch_count": branch_count,
        "planner_trace_ref": make_trace_ref("planner_trace", {"conversation_id": conversation_id, "turn_id": turn_id, "discourse_mode": discourse_mode}),
    }
    base["plan_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_07.utterance_plan.v1", **base}


def build_phase7_answer_contract_state(
    *,
    conversation_id: str,
    turn_id: str,
    user_intent: str,
    discourse_mode: str,
    support_state: str,
    knowledge_gap_reason: str,
    next_action: str,
    final_answer_mode: str,
    response_text: str,
    evidence_refs: tuple[str, ...],
    planner_trace_ref: str,
    simulation_trace_ref: str,
    critic_trace_ref: str,
    governance_trace_ref: str,
    memory_review_ref: str,
    active_context_refs: tuple[str, ...] = (),
) -> dict[str, Any]:
    base = {
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "user_intent": user_intent,
        "active_context_refs": list(active_context_refs),
        "planner_trace_ref": planner_trace_ref,
        "simulation_trace_ref": simulation_trace_ref,
        "critic_trace_ref": critic_trace_ref,
        "governance_trace_ref": governance_trace_ref,
        "response_text": response_text,
        "abstain_or_answer": "abstain" if final_answer_mode in {"abstain", "unknown"} else "answer",
        "memory_review_ref": memory_review_ref,
        "discourse_mode": discourse_mode,
        "support_state": support_state,
        "knowledge_gap_reason": knowledge_gap_reason,
        "next_action": next_action,
        "final_answer_mode": final_answer_mode,
        "evidence_refs": list(evidence_refs),
    }
    base["contract_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_07.answer_contract.v1", **base}


def build_phase7_anti_generic_filler_state(*, output_text: str, fallback_action: str = "answer") -> dict[str, Any]:
    base = {
        "status": "pass",
        "fallback_action": fallback_action,
        "output_text": output_text,
        "violations": [],
    }
    base["guardrail_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_07.anti_generic_filler.v1", **base}


def build_continuity_memory_state(*, turn_id: str) -> dict[str, Any]:
    anchors = [
        {
            "anchor_id": f"continuity::{turn_id}::limits",
            "subject": "agifcore_runtime",
            "continuity_kind": "self_limit",
            "statement": "AGIFCore can report only what is supported by local traces and current governed state.",
            "provenance_refs": ["continuity.provenance.self_limit"],
            "created_at": "2026-03-31T00:00:00Z",
            "updated_at": "2026-03-31T00:00:00Z",
            "status": "active",
            "superseded_by": None,
            "correction_refs": [],
            "metadata": {"kind": "bounded_self_knowledge"},
        },
        {
            "anchor_id": f"continuity::{turn_id}::phase_status",
            "subject": "agifcore_runtime",
            "continuity_kind": "self_status",
            "statement": "Phase 10 critique can diagnose weakness, but it may not self-improve or self-reorganize.",
            "provenance_refs": ["continuity.provenance.phase10_boundary"],
            "created_at": "2026-03-31T00:00:00Z",
            "updated_at": "2026-03-31T00:00:00Z",
            "status": "active",
            "superseded_by": None,
            "correction_refs": [],
            "metadata": {"kind": "phase_boundary"},
        },
    ]
    return {
        "schema": "agifcore.phase_04.continuity_memory.v1",
        "store_id": "continuity-store.phase10",
        "max_entries": 16,
        "anchors": anchors,
    }


def build_phase8_entity_request_inference_state(
    *,
    conversation_id: str,
    turn_id: str,
    normalized_text: str,
    extracted_terms: tuple[str, ...],
    science_topic_cues: tuple[str, ...],
    hidden_variable_cues: tuple[str, ...],
    candidates: tuple[dict[str, Any], ...],
    support_state_hint: str,
    knowledge_gap_reason_hint: str,
    inference_notes: tuple[str, ...],
) -> dict[str, Any]:
    base = {
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "raw_text_hash": make_trace_ref("raw_text", {"conversation_id": conversation_id, "turn_id": turn_id, "normalized_text": normalized_text}),
        "normalized_text": normalized_text,
        "extracted_terms": list(extracted_terms),
        "candidate_count": len(candidates),
        "selected_candidate_id": candidates[0]["candidate_id"] if candidates else None,
        "candidates": [dict(candidate) for candidate in candidates],
        "science_topic_cues": list(science_topic_cues),
        "hidden_variable_cues": list(hidden_variable_cues),
        "support_state_hint": support_state_hint,
        "knowledge_gap_reason_hint": knowledge_gap_reason_hint,
        "inference_notes": list(inference_notes),
    }
    base["inference_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_08.entity_request_inference.v1", **base}


def build_entity_request_candidate(
    *,
    candidate_id: str,
    entity_label: str,
    entity_class: str,
    request_type: str,
    science_topic_cues: tuple[str, ...],
    matched_terms: tuple[str, ...],
    hidden_variable_cues: tuple[str, ...],
    target_domain_hint: str | None,
    region_hint: str | None,
    live_current_requested: bool,
    ambiguous_request: bool,
    confidence: float,
    reason_codes: tuple[str, ...],
) -> dict[str, Any]:
    base = {
        "candidate_id": candidate_id,
        "entity_label": entity_label,
        "entity_class": entity_class,
        "request_type": request_type,
        "science_topic_cues": list(science_topic_cues),
        "matched_terms": list(matched_terms),
        "hidden_variable_cues": list(hidden_variable_cues),
        "target_domain_hint": target_domain_hint,
        "region_hint": region_hint,
        "live_current_requested": live_current_requested,
        "ambiguous_request": ambiguous_request,
        "confidence": confidence,
        "reason_codes": list(reason_codes),
    }
    base["candidate_hash"] = stable_hash_payload(base)
    return base


def build_phase8_scientific_priors_state(*, request_id: str, selected_prior_ids: tuple[str, ...]) -> dict[str, Any]:
    selected_priors = [
        {
            "selection_id": f"prior::{request_id}::{index}",
            "cell_id": prior_id,
            "principle_id": f"principle::{prior_id}",
            "matched_cue_terms": ["weather", "measurement"],
            "matched_hidden_variables": ["microclimate"],
            "relevance_score": 0.8 - (index * 0.05),
            "reason_codes": ["bounded_match"],
            "provenance_refs": [f"prior.provenance::{prior_id}"],
            "selection_hash": stable_hash_payload({"request_id": request_id, "cell_id": prior_id, "index": index}),
        }
        for index, prior_id in enumerate(selected_prior_ids)
    ]
    selected_cells = [
        {
            "cell_id": prior_id,
            "family_name": "critic",
            "principle_id": f"principle::{prior_id}",
            "seed_topic": "weather_climate",
            "plain_language_law": "Local measurements can fail when hidden variables dominate.",
            "variables": ["temperature", "humidity", "measurement freshness"],
            "causal_mechanism": "Observed answer quality depends on both signal quality and hidden variables.",
            "scope_limits": "bounded local reasoning only",
            "failure_case": "stale measurement",
            "worked_example": "fresh local weather station reading",
            "transfer_hint": "re-check the local signal before stronger claims",
            "cue_terms": ["weather", "measurement"],
            "hidden_variable_hints": ["microclimate"],
            "provenance_refs": [f"prior.provenance::{prior_id}"],
            "cell_hash": stable_hash_payload({"prior_id": prior_id}),
        }
        for prior_id in selected_prior_ids
    ]
    base = {
        "request_id": request_id,
        "available_prior_count": len(selected_cells),
        "selected_prior_count": len(selected_priors),
        "selected_prior_ids": list(selected_prior_ids),
        "selected_priors": selected_priors,
        "selected_cells": selected_cells,
        "selection_notes": ["bounded prior selection only"],
    }
    base["snapshot_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_08.scientific_priors.v1", **base}


def build_phase8_world_region_selection_state(*, request_id: str, selected_region_id: str) -> dict[str, Any]:
    candidate = {
        "region_id": selected_region_id,
        "region_label": "bounded local region",
        "region_kind": "local",
        "target_domain": "weather_climate",
        "supporting_refs": ["region.provenance.local"],
        "matched_terms": ["local", "weather"],
        "reason_codes": ["bounded_local_region"],
        "confidence": 0.79,
        "candidate_hash": stable_hash_payload({"request_id": request_id, "region_id": selected_region_id}),
    }
    base = {
        "request_id": request_id,
        "candidate_count": 1,
        "selected_region_id": selected_region_id,
        "candidates": [candidate],
        "unresolved": False,
        "reason_codes": ["bounded_region_selected"],
    }
    base["snapshot_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_08.world_region_selection.v1", **base}


def build_phase8_bounded_current_world_reasoning_state(
    *,
    request_id: str,
    decision: str,
    live_current_requested: bool,
    needs_fresh_information: bool,
    live_measurement_required: bool,
    exact_current_fact_allowed: bool,
    bounded_local_support_refs: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    reason_codes: tuple[str, ...],
) -> dict[str, Any]:
    base = {
        "request_id": request_id,
        "decision": decision,
        "live_current_requested": live_current_requested,
        "needs_fresh_information": needs_fresh_information,
        "live_measurement_required": live_measurement_required,
        "exact_current_fact_allowed": exact_current_fact_allowed,
        "bounded_local_support_refs": list(bounded_local_support_refs),
        "evidence_refs": list(evidence_refs),
        "evidence_input_count": len(evidence_refs),
        "reason_codes": list(reason_codes),
    }
    base["snapshot_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_08.bounded_current_world_reasoning.v1", **base}


def build_phase8_visible_reasoning_summary_state(
    *,
    request_id: str,
    what_is_known: tuple[str, ...],
    what_is_inferred: tuple[str, ...],
    uncertainty: tuple[str, ...],
    what_would_verify: tuple[str, ...],
    principle_refs: tuple[str, ...],
    causal_chain_ref: str,
    uncertainty_band: str,
    live_measurement_required: bool,
    evidence_refs: tuple[str, ...],
) -> dict[str, Any]:
    base = {
        "request_id": request_id,
        "what_is_known": list(what_is_known),
        "what_is_inferred": list(what_is_inferred),
        "uncertainty": list(uncertainty),
        "what_would_verify": list(what_would_verify),
        "principle_refs": list(principle_refs),
        "causal_chain_ref": causal_chain_ref,
        "uncertainty_band": uncertainty_band,
        "live_measurement_required": live_measurement_required,
        "character_count": sum(len(item) for item in [*what_is_known, *what_is_inferred, *uncertainty, *what_would_verify]) + 4,
        "evidence_refs": list(evidence_refs),
    }
    base["summary_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_08.visible_reasoning_summaries.v1", **base}


def build_phase8_science_reflection_state(*, request_id: str, records: tuple[dict[str, Any], ...], uncertainty_should_increase: bool) -> dict[str, Any]:
    base = {
        "request_id": request_id,
        "record_count": len(records),
        "records": [dict(record) for record in records],
        "uncertainty_should_increase": uncertainty_should_increase,
    }
    base["reflection_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_08.science_reflection.v1", **base}


def build_science_reflection_record(
    *,
    record_id: str,
    kind: str,
    note: str,
    source_ref: str,
    next_verification_step: str | None,
    increases_uncertainty: bool,
) -> dict[str, Any]:
    base = {
        "record_id": record_id,
        "kind": kind,
        "note": note,
        "source_ref": source_ref,
        "next_verification_step": next_verification_step,
        "increases_uncertainty": increases_uncertainty,
    }
    base["record_hash"] = stable_hash_payload(base)
    return base


def build_phase8_science_world_turn_state(
    *,
    conversation_id: str,
    turn_id: str,
    entity_request_inference: Mapping[str, Any],
    scientific_priors: Mapping[str, Any],
    world_region_selection: Mapping[str, Any],
    bounded_current_world_reasoning: Mapping[str, Any],
    visible_reasoning_summary: Mapping[str, Any],
    science_reflection: Mapping[str, Any],
) -> dict[str, Any]:
    causal_chain = {
        "schema": "agifcore.phase_08.causal_chain_reasoning.v1",
        "request_id": turn_id,
        "snapshot_hash": stable_hash_payload({"conversation_id": conversation_id, "turn_id": turn_id, "kind": "causal_chain"}),
        "chain_steps": ["observe local state", "keep uncertainty visible", "stop before unsupported upgrade"],
    }
    payload = {
        "schema": "agifcore.phase_08.science_world_turn.v1",
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "phase4_interfaces": ["agifcore.phase_04.continuity_memory.v1"],
        "phase5_interfaces": ["phase5.support_selection_result"],
        "phase6_interfaces": [
            "agifcore.phase_06.target_domains.v1",
            "agifcore.phase_06.world_model.v1",
            "agifcore.phase_06.what_if_simulation.v1",
            "agifcore.phase_06.usefulness_scoring.v1",
        ],
        "phase7_interfaces": [
            "agifcore.phase_07.raw_text_intake.v1",
            "agifcore.phase_07.question_interpretation.v1",
            "agifcore.phase_07.support_state_logic.v1",
            "agifcore.phase_07.answer_contract.v1",
        ],
        "entity_request_inference": dict(entity_request_inference),
        "scientific_priors": dict(scientific_priors),
        "world_region_selection": dict(world_region_selection),
        "causal_chain": causal_chain,
        "bounded_current_world_reasoning": dict(bounded_current_world_reasoning),
        "visible_reasoning_summary": dict(visible_reasoning_summary),
        "science_reflection": dict(science_reflection),
    }
    payload["snapshot_hash"] = stable_hash_payload(
        {
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "entity_request_inference_hash": entity_request_inference.get("inference_hash"),
            "scientific_priors_hash": scientific_priors.get("snapshot_hash"),
            "world_region_selection_hash": world_region_selection.get("snapshot_hash"),
            "bounded_current_world_reasoning_hash": bounded_current_world_reasoning.get("snapshot_hash"),
            "visible_reasoning_summary_hash": visible_reasoning_summary.get("summary_hash"),
            "science_reflection_hash": science_reflection.get("reflection_hash"),
        }
    )
    return payload


def build_phase10_fixture(*, scenario: str) -> dict[str, Any]:
    if scenario not in {"weak", "contradiction"}:
        raise ValueError(f"unknown scenario: {scenario}")

    conversation_id = f"conv-p10-{scenario}"
    turn_id = f"turn-p10-{scenario}"
    raw_text = (
        "Why was this weak and what should be checked first?"
        if scenario == "weak"
        else "These signals contradict each other. Compare them and show where the answer could break."
    )
    discourse_mode = "synthesize" if scenario == "weak" else "compare"
    intake = build_phase7_intake_state(conversation_id=conversation_id, turn_id=turn_id, raw_text=raw_text)
    interpretation = build_phase7_question_interpretation_state(
        conversation_id=conversation_id,
        turn_id=turn_id,
        raw_text_hash=intake["intake_hash"],
        user_intent=raw_text.lower(),
        discourse_mode_hint=discourse_mode,
        question_category="ordinary",
        target_domain_hint="weather_climate",
        live_current_requested=False,
        ambiguous_request=False,
        self_knowledge_requested=True,
        local_artifact_requested=False,
        correction_hint=False,
        repeated_fact_hint=False,
        comparison_requested=scenario == "contradiction",
        extracted_terms=("weak", "diagnosis", "support", "self", "contradiction") if scenario == "weak" else ("contradiction", "compare", "break", "self"),
        signal_notes=("phase10_fixture", scenario),
    )
    support = build_phase7_support_resolution_state(
        conversation_id=conversation_id,
        turn_id=turn_id,
        support_state="search_needed" if scenario == "weak" else "inferred",
        knowledge_gap_reason="missing_local_evidence" if scenario == "weak" else "none",
        next_action="clarify" if scenario == "weak" else "answer",
        evidence_refs=(f"phase10.support.ref.{scenario}.001",),
        selected_domain_ids=("weather_climate",),
        reason_codes=("bounded_local_support", "phase10_fixture"),
    )
    utterance_plan = build_phase7_utterance_plan_state(
        conversation_id=conversation_id,
        turn_id=turn_id,
        discourse_mode=discourse_mode,
        response_sections=("scope", "bounded_answer", "limits"),
        sentence_obligations=("preserve honesty", "keep support visible"),
        constraint_slots=("support_state", "uncertainty"),
    )
    answer_contract = build_phase7_answer_contract_state(
        conversation_id=conversation_id,
        turn_id=turn_id,
        user_intent=raw_text.lower(),
        discourse_mode=discourse_mode,
        support_state=support["support_state"],
        knowledge_gap_reason=support["knowledge_gap_reason"],
        next_action=support["next_action"],
        final_answer_mode="search_needed" if scenario == "weak" else "derived_explanation",
        response_text="Bounded explanation placeholder for Phase 10 fixture.",
        evidence_refs=tuple(support["evidence_refs"]),
        planner_trace_ref=utterance_plan["planner_trace_ref"],
        simulation_trace_ref=support["simulation_trace_ref"],
        critic_trace_ref=support["critic_trace_ref"],
        governance_trace_ref=support["governance_trace_ref"],
        memory_review_ref=support["memory_review_ref"],
    )
    anti_generic_filler = build_phase7_anti_generic_filler_state(output_text="Bounded fallback surface remains available.")
    continuity_memory = build_continuity_memory_state(turn_id=turn_id)
    self_knowledge = SelfKnowledgeSurfaceEngine().build_snapshot(
        question_interpretation_state=interpretation,
        support_state_resolution_state=support,
        continuity_memory_state=continuity_memory,
    ).to_dict()

    candidate = build_entity_request_candidate(
        candidate_id=f"candidate::{turn_id}",
        entity_label="local weather reasoning",
        entity_class="environment",
        request_type="diagnostic_explanation" if scenario == "weak" else "contradiction_check",
        science_topic_cues=("weather_climate",),
        matched_terms=("weather", "local"),
        hidden_variable_cues=("microclimate",) if scenario == "contradiction" else ("stale_measurement",),
        target_domain_hint="weather_climate",
        region_hint="local_region",
        live_current_requested=False,
        ambiguous_request=False,
        confidence=0.81,
        reason_codes=("bounded_phase10_fixture",),
    )
    entity_request_inference = build_phase8_entity_request_inference_state(
        conversation_id=conversation_id,
        turn_id=turn_id,
        normalized_text=intake["normalized_text"],
        extracted_terms=tuple(interpretation["extracted_terms"]),
        science_topic_cues=("weather_climate",),
        hidden_variable_cues=("microclimate",) if scenario == "contradiction" else ("stale_measurement",),
        candidates=(candidate,),
        support_state_hint=support["support_state"],
        knowledge_gap_reason_hint=support["knowledge_gap_reason"],
        inference_notes=("phase10_fixture",),
    )
    scientific_priors = build_phase8_scientific_priors_state(request_id=turn_id, selected_prior_ids=("critic.prior.weather",))
    world_region_selection = build_phase8_world_region_selection_state(request_id=turn_id, selected_region_id="region.local")
    bounded_current_world_reasoning = build_phase8_bounded_current_world_reasoning_state(
        request_id=turn_id,
        decision="bounded_answer_with_limits" if scenario == "contradiction" else "needs_fresh_information",
        live_current_requested=False,
        needs_fresh_information=scenario == "weak",
        live_measurement_required=scenario == "weak",
        exact_current_fact_allowed=False,
        bounded_local_support_refs=("phase8.local.ref.001",),
        evidence_refs=("phase8.evidence.ref.001", "phase8.evidence.ref.002"),
        reason_codes=("bounded_current_world", "phase10_fixture"),
    )
    visible_reasoning_summary = build_phase8_visible_reasoning_summary_state(
        request_id=turn_id,
        what_is_known=("A local explanation can stay bounded to the current evidence trail.", "The request is diagnostic rather than open-world research."),
        what_is_inferred=("The answer should stay honest about uncertainty.",),
        uncertainty=(
            ("No fresh local measurement is present yet.", "A stale sensor could be hiding the real variable.")
            if scenario == "weak"
            else ("A conflicting local reading could reverse the current explanation.", "A hidden microclimate factor could break the comparison.")
        ),
        what_would_verify=("Check the freshest local measurement.", "Compare the contradictory signal against the cited evidence trail."),
        principle_refs=("measurement_uncertainty", "bounded_local_reasoning"),
        causal_chain_ref=f"causal_chain::{turn_id}",
        uncertainty_band="high" if scenario == "weak" else "moderate",
        live_measurement_required=scenario == "weak",
        evidence_refs=("phase8.summary.ref.001", "phase8.summary.ref.002"),
    )
    science_reflection = build_phase8_science_reflection_state(
        request_id=turn_id,
        records=(
            (
                build_science_reflection_record(
                    record_id=f"reflection::{turn_id}::support_gap",
                    kind="support_gap",
                    note="Fresh local evidence is still missing.",
                    source_ref="phase8.summary.ref.001",
                    next_verification_step="Check the freshest local measurement.",
                    increases_uncertainty=True,
                ),
            )
            if scenario == "weak"
            else (
                build_science_reflection_record(
                    record_id=f"reflection::{turn_id}::contradiction",
                    kind="contradiction_signal",
                    note="Two visible cues point in different directions.",
                    source_ref="phase8.summary.ref.002",
                    next_verification_step="Re-check the cited support before claiming a stable comparison.",
                    increases_uncertainty=True,
                ),
            )
        ),
        uncertainty_should_increase=True,
    )
    science_world_turn = build_phase8_science_world_turn_state(
        conversation_id=conversation_id,
        turn_id=turn_id,
        entity_request_inference=entity_request_inference,
        scientific_priors=scientific_priors,
        world_region_selection=world_region_selection,
        bounded_current_world_reasoning=bounded_current_world_reasoning,
        visible_reasoning_summary=visible_reasoning_summary,
        science_reflection=science_reflection,
    )
    rich_expression_turn = RichExpressionTurnEngine().run_turn(
        intake_state=intake,
        question_interpretation_state=interpretation,
        support_state_resolution_state=support,
        utterance_plan_state=utterance_plan,
        answer_contract_state=answer_contract,
        science_world_turn_state=science_world_turn,
        anti_generic_filler_state=anti_generic_filler,
    ).to_dict()
    return {
        "scenario": scenario,
        "intake": intake,
        "interpretation": interpretation,
        "support": support,
        "utterance_plan": utterance_plan,
        "answer_contract": answer_contract,
        "anti_generic_filler": anti_generic_filler,
        "continuity_memory": continuity_memory,
        "self_knowledge": self_knowledge,
        "science_world_turn": science_world_turn,
        "rich_expression_turn": rich_expression_turn,
    }


def run_phase10_turn(*, scenario: str) -> dict[str, Any]:
    fixture = build_phase10_fixture(scenario=scenario)
    before = deep_copy(fixture)
    turn = MetaCognitionTurnEngine().run_turn(
        support_state_resolution_state=fixture["support"],
        answer_contract_state=fixture["answer_contract"],
        self_knowledge_surface_state=fixture["self_knowledge"],
        science_world_turn_state=fixture["science_world_turn"],
        rich_expression_turn_state=fixture["rich_expression_turn"],
        continuity_memory_state=fixture["continuity_memory"],
    )
    assert_inputs_unchanged(before, fixture, f"phase10 {scenario} fixture inputs")
    return {"fixture": fixture, "turn": turn}


def write_demo_payload(*, filename: str, payload: Mapping[str, Any]) -> Path:
    path = DEMO_DIR / filename
    dump_json(path, payload)
    return path


def write_demo_markdown(*, filename: str, lines: list[str]) -> Path:
    path = DEMO_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def build_demo_index() -> None:
    index_json = {
        "phase": PHASE,
        "status": "open",
        "scenario_files": [
            "phase_10_why_was_this_weak_demo.json",
            "phase_10_contradiction_demo.json",
        ],
        "supporting_evidence_manifest": "phase_10_evidence_manifest.json",
        "notes": [
            "summary only",
            "Phase 10 remains open",
            "no approval implied",
        ],
    }
    write_demo_payload(filename="phase_10_demo_index.json", payload=index_json)
    write_demo_markdown(
        filename="phase_10_demo_index.md",
        lines=[
            "# Phase 10 Demo Index",
            "",
            "Phase 10 remains `open`. This bundle is for inspection only and does not imply approval or finality.",
            "",
            "Demo scenarios:",
            "",
            "- `phase_10_why_was_this_weak_demo.md` for a bounded weak-answer diagnosis path.",
            "- `phase_10_contradiction_demo.md` for a bounded contradiction and counterexample path.",
            "",
            "Supporting demo payloads:",
            "",
            "- `phase_10_why_was_this_weak_demo.json`",
            "- `phase_10_contradiction_demo.json`",
            "",
            "Evidence source:",
            "",
            f"- [{MANIFEST_PATH.name}]({MANIFEST_PATH})",
            "",
            "Truth note:",
            "",
            "- the bundle is local-file inspectable only",
            "- no approval language is used",
        ],
    )
