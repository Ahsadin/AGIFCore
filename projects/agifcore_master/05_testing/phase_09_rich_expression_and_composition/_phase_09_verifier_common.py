from __future__ import annotations

import importlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

PHASE = "9"
PHASE_NAME = "phase_09_rich_expression_and_composition"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"
TEST_ROOT_NAME = "05_testing"
RUNTIME_PACKAGE = "agifcore_phase9_rich_expression"
PHASE_09_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition"
PHASE_07_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_07_conversation_core"
PHASE_08_RUNTIME_PARENT = "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness"

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/01_plan/DEMO_PROTOCOL.md",
)

CONTRACT_REFS = (
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py",
    "projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/answer_contract.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/science_world_turn.py",
)

RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/contracts.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/teaching.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/comparison.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/planning.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/synthesis.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/analogy.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/concept_composition.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/cross_domain_composition.py",
    "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/audience_aware_explanation_quality.py",
)

OPTIONAL_COORDINATOR_FILE = "projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/rich_expression_turn.py"

COMMON_TEST_FILE = "projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/_phase_09_verifier_common.py"

REQUIRED_REPORT_FILES = (
    "phase_09_teaching_report.json",
    "phase_09_comparison_report.json",
    "phase_09_planning_report.json",
    "phase_09_synthesis_report.json",
    "phase_09_analogy_report.json",
    "phase_09_concept_composition_report.json",
    "phase_09_cross_domain_composition_report.json",
    "phase_09_audience_aware_explanation_quality_report.json",
)

EXPECTED_REPORT_VERIFIERS = {
    "phase_09_teaching_report.json": "verify_phase_09_teaching",
    "phase_09_comparison_report.json": "verify_phase_09_comparison",
    "phase_09_planning_report.json": "verify_phase_09_planning",
    "phase_09_synthesis_report.json": "verify_phase_09_synthesis",
    "phase_09_analogy_report.json": "verify_phase_09_analogy",
    "phase_09_concept_composition_report.json": "verify_phase_09_concept_composition",
    "phase_09_cross_domain_composition_report.json": "verify_phase_09_cross_domain_composition",
    "phase_09_audience_aware_explanation_quality_report.json": "verify_phase_09_audience_aware_explanation_quality",
}


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
TEST_ROOT = PROJECT_ROOT / TEST_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_09_evidence"
DEMO_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME / "phase_09_demo_bundle"
MANIFEST_PATH = EVIDENCE_DIR / "phase_09_evidence_manifest.json"


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_path() -> None:
    runtime_path = str(REPO_ROOT / PHASE_09_RUNTIME_PARENT)
    if runtime_path not in sys.path:
        sys.path.insert(0, runtime_path)


ensure_runtime_import_path()


from agifcore_phase9_rich_expression.contracts import make_trace_ref, stable_hash_payload


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
        normalized = str(path)
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def checked_files_for(verifier_file: str) -> list[str]:
    return dedupe_paths([*PLAN_REFS, *CONTRACT_REFS, *RUNTIME_FILES, COMMON_TEST_FILE, verifier_file])


def coordinator_status_note() -> str:
    if (REPO_ROOT / OPTIONAL_COORDINATOR_FILE).exists():
        return "rich_expression_turn.py is present; lane tests still call engines directly"
    return "rich_expression_turn.py is pending; lane tests cover direct engine calls only"


def report_dependency_failures(required_reports: tuple[str, ...]) -> list[str]:
    failures: list[str] = []
    for filename in required_reports:
        report_path = EVIDENCE_DIR / filename
        if not report_path.exists():
            failures.append(filename)
            continue
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        if payload.get("status") != "pass":
            failures.append(filename)
    return failures


def build_blocked_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertion_ids: list[str],
    blocker_kind: str,
    blocker_message: str,
    missing: list[str] | None = None,
    dependency_reports: list[str] | None = None,
) -> dict[str, Any]:
    blocker: dict[str, Any] = {"kind": blocker_kind, "message": blocker_message}
    if missing:
        blocker["missing_files"] = missing
    if dependency_reports:
        blocker["dependency_reports"] = dependency_reports
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "blocked",
        "blocker": blocker,
        "checked_files": checked_files,
        "assertions": [{"id": assertion_id, "result": "blocked"} for assertion_id in assertion_ids],
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "notes": ["Phase 9 remains open", "no approval implied"],
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
        "notes": [*notes, coordinator_status_note(), "Phase 9 remains open", "no approval implied"],
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
        if payload.get("outputs", {}).get("report") != rel(report_path):
            invalid_reports.append(filename)
        assertions = payload.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            invalid_reports.append(filename)
        reports.append(
            {
                "report_id": filename.removeprefix("phase_09_").removesuffix("_report.json"),
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
        "status": "phase_9_verifier_family_pass" if overall_pass else "phase_9_verifier_family_incomplete",
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 9 remains open",
            "manifest is rebuilt from actual report files on disk",
            "no approval implied",
            coordinator_status_note(),
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


def build_phase8_scientific_priors_state(
    *,
    request_id: str,
    selected_prior_specs: tuple[dict[str, Any], ...],
    selection_notes: tuple[str, ...],
) -> dict[str, Any]:
    selected_priors: list[dict[str, Any]] = []
    selected_cells: list[dict[str, Any]] = []
    selected_ids: list[str] = []
    for spec in selected_prior_specs:
        selected_ids.append(str(spec["cell_id"]))
        cell_base = {
            "cell_id": spec["cell_id"],
            "family_name": spec["family_name"],
            "principle_id": spec["principle_id"],
            "seed_topic": spec["seed_topic"],
            "plain_language_law": spec["plain_language_law"],
            "variables": list(spec["variables"]),
            "causal_mechanism": spec["causal_mechanism"],
            "scope_limits": spec["scope_limits"],
            "failure_case": spec["failure_case"],
            "worked_example": spec["worked_example"],
            "transfer_hint": spec["transfer_hint"],
            "cue_terms": list(spec["cue_terms"]),
            "hidden_variable_hints": list(spec["hidden_variable_hints"]),
            "provenance_refs": list(spec["provenance_refs"]),
        }
        cell_base["cell_hash"] = stable_hash_payload(cell_base)
        selected_cells.append(cell_base)
        prior_base = {
            "selection_id": spec["selection_id"],
            "cell_id": spec["cell_id"],
            "principle_id": spec["principle_id"],
            "matched_cue_terms": list(spec["matched_cue_terms"]),
            "matched_hidden_variables": list(spec["matched_hidden_variables"]),
            "relevance_score": spec["relevance_score"],
            "reason_codes": list(spec["reason_codes"]),
            "provenance_refs": list(spec["provenance_refs"]),
        }
        prior_base["selection_hash"] = stable_hash_payload(prior_base)
        selected_priors.append(prior_base)
    base = {
        "request_id": request_id,
        "available_prior_count": len(selected_cells),
        "selected_prior_count": len(selected_priors),
        "selected_prior_ids": selected_ids,
        "selected_priors": selected_priors,
        "selected_cells": selected_cells,
        "selection_notes": list(selection_notes),
    }
    base["snapshot_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_08.scientific_priors.v1", **base}


def build_phase8_world_region_selection_state(
    *,
    request_id: str,
    candidates: tuple[dict[str, Any], ...],
    selected_region_id: str | None,
    reason_codes: tuple[str, ...],
    unresolved: bool = False,
) -> dict[str, Any]:
    base = {
        "request_id": request_id,
        "candidate_count": len(candidates),
        "selected_region_id": selected_region_id,
        "candidates": [dict(candidate) for candidate in candidates],
        "unresolved": unresolved,
        "reason_codes": list(reason_codes),
    }
    base["snapshot_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_08.world_region_selection.v1", **base}


def build_world_region_candidate(
    *,
    region_id: str,
    region_label: str,
    region_kind: str,
    target_domain: str | None,
    supporting_refs: tuple[str, ...],
    matched_terms: tuple[str, ...],
    reason_codes: tuple[str, ...],
    confidence: float,
) -> dict[str, Any]:
    base = {
        "region_id": region_id,
        "region_label": region_label,
        "region_kind": region_kind,
        "target_domain": target_domain,
        "supporting_refs": list(supporting_refs),
        "matched_terms": list(matched_terms),
        "reason_codes": list(reason_codes),
        "confidence": confidence,
    }
    base["candidate_hash"] = stable_hash_payload(base)
    return base


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


def build_phase8_science_reflection_state(
    *,
    request_id: str,
    records: tuple[dict[str, Any], ...],
    uncertainty_should_increase: bool,
) -> dict[str, Any]:
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


def build_phase09_concept_fixture_for_cross_domain(*, request_id: str, support_state: str) -> dict[str, Any]:
    elements = [
        {
            "element_id": make_trace_ref(
                "concept_element",
                {"request_id": request_id, "label": "weather_climate", "role": "governing_principle"},
            ),
            "concept_label": "weather_climate",
            "role_in_composition": "governing_principle",
            "supporting_refs": ["phase8.summary.ref.060"],
            "confidence": 0.86,
        },
        {
            "element_id": make_trace_ref(
                "concept_element",
                {"request_id": request_id, "label": "place_region_context", "role": "context_modifier"},
            ),
            "concept_label": "place_region_context",
            "role_in_composition": "context_modifier",
            "supporting_refs": ["phase8.summary.ref.061"],
            "confidence": 0.72,
        },
    ]
    for element in elements:
        element["element_hash"] = stable_hash_payload(
            {
                "concept_label": element["concept_label"],
                "role_in_composition": element["role_in_composition"],
                "supporting_refs": element["supporting_refs"],
                "confidence": element["confidence"],
            }
        )
    fail_closed = support_state in {"search_needed", "unknown"}
    base = {
        "turn_id": request_id,
        "element_count": len(elements),
        "elements": elements,
        "composed_view": f"Composite view for {request_id} with {len(elements)} elements.",
        "concept_composition_ref": make_trace_ref(
            "concept_composition",
            {"request_id": request_id, "support_state": support_state, "elements": [item["element_hash"] for item in elements]},
        ),
        "fail_closed": fail_closed,
        "lane_notes": [
            "Concept composition fixture stays bounded for cross-domain composition tests.",
            "The fixture preserves an explicit concept_composition_ref.",
        ],
    }
    base["snapshot_hash"] = stable_hash_payload(base)
    return {"schema": "agifcore.phase_09.concept_composition.v1", **base}


def deep_copy(value: Any) -> Any:
    return deepcopy(value)
