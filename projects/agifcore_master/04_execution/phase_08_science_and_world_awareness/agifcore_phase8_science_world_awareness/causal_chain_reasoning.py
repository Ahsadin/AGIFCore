from __future__ import annotations

import re
from typing import Any, Mapping

from .contracts import (
    MAX_CAUSAL_CHAIN_STEPS,
    MAX_MATCHED_TERMS,
    MAX_REASON_CODES,
    CausalChainSnapshot,
    CausalChainStep,
    ChainStepKind,
    Phase8ScienceWorldAwarenessError,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    require_schema,
    stable_hash_payload,
)

_TOKEN_RE = re.compile(r"[a-z0-9']+")


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _to_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _unique_bounded(values: list[str], *, ceiling: int) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        normalized = str(item).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
        if len(result) >= ceiling:
            break
    return tuple(result)


def _pick_inference_candidate(inference: Mapping[str, Any]) -> dict[str, Any] | None:
    candidates = [require_mapping(item, "entity_request_candidate") for item in list(inference.get("candidates", ()))]
    if not candidates:
        return None
    selected_id = str(inference.get("selected_candidate_id", "")).strip()
    if selected_id:
        for candidate in candidates:
            if str(candidate.get("candidate_id", "")).strip() == selected_id:
                return candidate
    return max(candidates, key=lambda item: _to_float(item.get("confidence"), 0.0))


def _pick_region(region_state: Mapping[str, Any]) -> dict[str, Any] | None:
    candidates = [require_mapping(item, "world_region_candidate") for item in list(region_state.get("candidates", ()))]
    if not candidates:
        return None
    selected_region_id = str(region_state.get("selected_region_id", "")).strip()
    if selected_region_id:
        for candidate in candidates:
            if str(candidate.get("region_id", "")).strip() == selected_region_id:
                return candidate
    return max(candidates, key=lambda item: _to_float(item.get("confidence"), 0.0))


def _pick_selected_prior(priors_state: Mapping[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    selected_priors = [require_mapping(item, "selected_scientific_prior") for item in list(priors_state.get("selected_priors", ()))]
    selected_cells = [require_mapping(item, "scientific_prior_cell") for item in list(priors_state.get("selected_cells", ()))]
    if not selected_priors:
        return None, None
    best_prior = max(selected_priors, key=lambda item: _to_float(item.get("relevance_score"), 0.0))
    best_cell: dict[str, Any] | None = None
    best_cell_id = str(best_prior.get("cell_id", "")).strip()
    if best_cell_id:
        for cell in selected_cells:
            if str(cell.get("cell_id", "")).strip() == best_cell_id:
                best_cell = cell
                break
    return best_prior, best_cell


def _pick_world_entity(
    *,
    world_model: Mapping[str, Any],
    selected_region: Mapping[str, Any] | None,
    selected_candidate: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    entities = [require_mapping(item, "world_entity") for item in list(world_model.get("entities", ()))]
    if not entities:
        return None

    query_terms: set[str] = set()
    region_target_domain = None
    if selected_region is not None:
        query_terms.update(_tokens(str(selected_region.get("region_label", ""))))
        region_target_domain = str(selected_region.get("target_domain", "")).strip() or None
    if selected_candidate is not None:
        query_terms.update(_tokens(str(selected_candidate.get("entity_label", ""))))
        query_terms.update(str(item).strip().lower() for item in list(selected_candidate.get("matched_terms", ())) if str(item).strip())
        candidate_domain = str(selected_candidate.get("target_domain_hint", "")).strip()
        if not region_target_domain and candidate_domain:
            region_target_domain = candidate_domain

    best_entity: dict[str, Any] | None = None
    best_score = -1.0
    for entity in entities:
        entity_id = str(entity.get("entity_id", "")).strip()
        label = str(entity.get("label", "")).strip()
        if not entity_id or not label:
            continue
        status = str(entity.get("status", "")).strip().lower()
        if status in {"blocked", "held"}:
            continue

        score = 0.15
        entity_domain = str(entity.get("target_domain", "")).strip() or None
        if region_target_domain and entity_domain == region_target_domain:
            score += 0.45
        label_tokens = set(_tokens(label))
        overlap = len(label_tokens.intersection(query_terms))
        if overlap > 0:
            score += min(0.3, overlap * 0.1)
        score += 0.25 * clamp_score(_to_float(entity.get("world_confidence"), 0.0))
        if score > best_score:
            best_score = score
            best_entity = entity
    return best_entity


def _pick_simulation_entry(
    *,
    simulation_state: Mapping[str, Any],
    world_entity: Mapping[str, Any] | None,
    target_domain: str | None,
) -> dict[str, Any] | None:
    entries = [require_mapping(item, "what_if_simulation_entry") for item in list(simulation_state.get("entries", ()))]
    if not entries:
        return None

    entity_id = str(world_entity.get("entity_id", "")).strip() if world_entity is not None else ""
    filtered: list[dict[str, Any]] = []
    for entry in entries:
        entry_domain = str(entry.get("target_domain", "")).strip()
        source_entity_id = str(entry.get("source_entity_id", "")).strip()
        if entity_id and source_entity_id == entity_id:
            filtered.append(entry)
            continue
        if target_domain and entry_domain and entry_domain == target_domain:
            filtered.append(entry)

    pool = filtered if filtered else entries
    return max(
        pool,
        key=lambda item: (
            0 if _to_bool(item.get("fail_closed")) else 1,
            _to_float(item.get("confidence"), 0.0),
        ),
    )


def _pick_usefulness_domain(
    *,
    usefulness_state: Mapping[str, Any],
    target_domain: str | None,
) -> dict[str, Any] | None:
    domain_scores = [require_mapping(item, "usefulness_domain_score") for item in list(usefulness_state.get("domain_scores", ()))]
    if not domain_scores:
        return None
    if target_domain:
        for score in domain_scores:
            if str(score.get("domain_id", "")).strip() == target_domain:
                return score
    return max(domain_scores, key=lambda item: _to_float(item.get("weighted_score"), 0.0))


class CausalChainReasoningEngine:
    """Build a bounded causal chain from Phase 8 inputs and Phase 6 evidence."""

    SCHEMA = "agifcore.phase_08.causal_chain_reasoning.v1"

    def build_snapshot(
        self,
        *,
        entity_request_inference_state: Mapping[str, Any],
        scientific_priors_state: Mapping[str, Any],
        world_region_selection_state: Mapping[str, Any],
        world_model_state: Mapping[str, Any],
        what_if_simulation_state: Mapping[str, Any],
        usefulness_scoring_state: Mapping[str, Any],
    ) -> CausalChainSnapshot:
        inference = require_schema(
            entity_request_inference_state,
            "agifcore.phase_08.entity_request_inference.v1",
            "entity_request_inference_state",
        )
        priors = require_schema(
            scientific_priors_state,
            "agifcore.phase_08.scientific_priors.v1",
            "scientific_priors_state",
        )
        region_state = require_schema(
            world_region_selection_state,
            "agifcore.phase_08.world_region_selection.v1",
            "world_region_selection_state",
        )
        world_model = require_schema(
            world_model_state,
            "agifcore.phase_06.world_model.v1",
            "world_model_state",
        )
        simulation = require_schema(
            what_if_simulation_state,
            "agifcore.phase_06.what_if_simulation.v1",
            "what_if_simulation_state",
        )
        usefulness = require_schema(
            usefulness_scoring_state,
            "agifcore.phase_06.usefulness_scoring.v1",
            "usefulness_scoring_state",
        )

        conversation_id = require_non_empty_str(inference.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(inference.get("turn_id"), "turn_id")
        request_id = f"{conversation_id}::{turn_id}"
        if str(priors.get("request_id", "")).strip() != request_id:
            raise Phase8ScienceWorldAwarenessError("scientific_priors_state request_id must match inference request_id")
        if str(region_state.get("request_id", "")).strip() != request_id:
            raise Phase8ScienceWorldAwarenessError("world_region_selection_state request_id must match inference request_id")

        steps: list[CausalChainStep] = []
        missing_variables: list[str] = []
        weakest_link_reason = "chain_not_started"

        def add_step(
            *,
            step_kind: ChainStepKind,
            statement: str,
            principle_ref: str | None = None,
            region_ref: str | None = None,
            world_entity_ref: str | None = None,
            simulation_ref: str | None = None,
            usefulness_ref: str | None = None,
            evidence_refs: tuple[str, ...] = (),
            missing_variables_for_step: tuple[str, ...] = (),
            fail_closed: bool = False,
            reason_codes: tuple[str, ...] = (),
        ) -> None:
            if len(steps) >= MAX_CAUSAL_CHAIN_STEPS:
                return
            index = len(steps) + 1
            payload = {
                "request_id": request_id,
                "step_index": index,
                "step_kind": step_kind.value,
                "statement": statement,
                "principle_ref": principle_ref,
                "region_ref": region_ref,
                "world_entity_ref": world_entity_ref,
                "simulation_ref": simulation_ref,
                "usefulness_ref": usefulness_ref,
                "evidence_refs": list(evidence_refs),
                "missing_variables": list(missing_variables_for_step),
                "fail_closed": fail_closed,
                "reason_codes": list(reason_codes),
            }
            steps.append(
                CausalChainStep(
                    step_id=f"ccr::{request_id}::{index:02d}",
                    step_index=index,
                    step_kind=step_kind,
                    statement=require_non_empty_str(statement, "statement"),
                    principle_ref=principle_ref,
                    region_ref=region_ref,
                    world_entity_ref=world_entity_ref,
                    simulation_ref=simulation_ref,
                    usefulness_ref=usefulness_ref,
                    evidence_refs=evidence_refs,
                    missing_variables=missing_variables_for_step,
                    fail_closed=fail_closed,
                    reason_codes=reason_codes,
                    step_hash=stable_hash_payload(payload),
                )
            )

        selected_candidate = _pick_inference_candidate(inference)
        candidate_id = None
        entity_label = "unspecified_entity"
        request_type = "unknown"
        target_domain_hint = None
        support_state_hint = str(inference.get("support_state_hint", "unknown")).strip() or "unknown"
        knowledge_gap_reason_hint = str(inference.get("knowledge_gap_reason_hint", "none")).strip() or "none"
        ambiguous_request = False
        live_current_requested = False
        if selected_candidate is not None:
            candidate_id = str(selected_candidate.get("candidate_id", "")).strip() or None
            entity_label = str(selected_candidate.get("entity_label", "")).strip() or entity_label
            request_type = str(selected_candidate.get("request_type", "")).strip() or request_type
            target_domain_hint = str(selected_candidate.get("target_domain_hint", "")).strip() or None
            ambiguous_request = _to_bool(selected_candidate.get("ambiguous_request"))
            live_current_requested = _to_bool(selected_candidate.get("live_current_requested"))
        else:
            missing_variables.append("entity request candidate")
            weakest_link_reason = "missing_entity_request_candidate"

        request_reasons: list[str] = [f"request_type:{request_type}", f"support_state_hint:{support_state_hint}"]
        if ambiguous_request:
            request_reasons.append("ambiguous_request")
            missing_variables.append("clarified question framing")
            if weakest_link_reason == "chain_not_started":
                weakest_link_reason = "ambiguous_request"
        if live_current_requested:
            request_reasons.append("live_current_requested")
        if knowledge_gap_reason_hint == "needs_fresh_information":
            request_reasons.append("needs_fresh_information")
            missing_variables.append("fresh local measurement")
            if weakest_link_reason == "chain_not_started":
                weakest_link_reason = "needs_fresh_information"
        add_step(
            step_kind=ChainStepKind.REQUEST_FRAME,
            statement=f"Request frame targets '{entity_label}' as a {request_type} question.",
            evidence_refs=_unique_bounded(
                [candidate_id or "", str(inference.get("inference_hash", "")).strip()],
                ceiling=MAX_MATCHED_TERMS,
            ),
            missing_variables_for_step=_unique_bounded(missing_variables, ceiling=MAX_MATCHED_TERMS),
            fail_closed=knowledge_gap_reason_hint == "needs_fresh_information",
            reason_codes=_unique_bounded(request_reasons, ceiling=MAX_REASON_CODES),
        )

        selected_region = _pick_region(region_state)
        region_ref = None
        region_target_domain = target_domain_hint
        region_reasons: list[str] = []
        region_fail_closed = _to_bool(region_state.get("unresolved"))
        if selected_region is not None:
            region_ref = str(selected_region.get("region_id", "")).strip() or None
            region_label = str(selected_region.get("region_label", "")).strip() or "unspecified_region"
            region_kind = str(selected_region.get("region_kind", "")).strip() or "unknown"
            region_conf = clamp_score(_to_float(selected_region.get("confidence"), 0.0))
            region_target_domain = str(selected_region.get("target_domain", "")).strip() or region_target_domain
            if region_conf < 0.6:
                region_fail_closed = True
                region_reasons.append("region_confidence_below_safe_threshold")
                missing_variables.append("region-specific context")
                if weakest_link_reason == "chain_not_started":
                    weakest_link_reason = "weak_region_selection"
            add_step(
                step_kind=ChainStepKind.REGION_CONTEXT,
                statement=(
                    f"Region context uses '{region_label}' ({region_kind}) with confidence {region_conf:.2f}."
                ),
                region_ref=region_ref,
                evidence_refs=_unique_bounded(
                    [
                        region_ref or "",
                        str(region_state.get("snapshot_hash", "")).strip(),
                        candidate_id or "",
                    ],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=_unique_bounded(
                    ["region-specific context"] if region_fail_closed else [],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                fail_closed=region_fail_closed,
                reason_codes=_unique_bounded(
                    region_reasons + [str(item).strip() for item in list(selected_region.get("reason_codes", ())) if str(item).strip()],
                    ceiling=MAX_REASON_CODES,
                ),
            )
        else:
            region_fail_closed = True
            missing_variables.append("bounded region candidate")
            if weakest_link_reason == "chain_not_started":
                weakest_link_reason = "missing_region_context"
            add_step(
                step_kind=ChainStepKind.REGION_CONTEXT,
                statement="No bounded region candidate reached selection confidence.",
                evidence_refs=_unique_bounded(
                    [str(region_state.get("snapshot_hash", "")).strip(), candidate_id or ""],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=("bounded region candidate",),
                fail_closed=True,
                reason_codes=_unique_bounded(
                    [
                        "region_unresolved",
                        *[str(item).strip() for item in list(region_state.get("reason_codes", ())) if str(item).strip()],
                    ],
                    ceiling=MAX_REASON_CODES,
                ),
            )

        selected_prior, selected_cell = _pick_selected_prior(priors)
        principle_ref = None
        prior_fail_closed = False
        if selected_prior is not None:
            principle_ref = str(selected_prior.get("principle_id", "")).strip() or None
            relevance = clamp_score(_to_float(selected_prior.get("relevance_score"), 0.0))
            hidden_hints = [str(item).strip() for item in list(selected_cell.get("hidden_variable_hints", ())) if str(item).strip()] if selected_cell else []
            matched_hidden = [str(item).strip() for item in list(selected_prior.get("matched_hidden_variables", ())) if str(item).strip()]
            unresolved_hidden = [item for item in hidden_hints if item not in matched_hidden]
            if relevance < 0.25:
                prior_fail_closed = True
                missing_variables.extend(unresolved_hidden[:2] or ["high-confidence governing prior"])
                if weakest_link_reason == "chain_not_started":
                    weakest_link_reason = "weak_prior_relevance"
            add_step(
                step_kind=ChainStepKind.PRIOR_APPLICATION,
                statement=(
                    f"Applied principle '{principle_ref or 'unknown_principle'}' with relevance {relevance:.2f}."
                ),
                principle_ref=principle_ref,
                evidence_refs=_unique_bounded(
                    [
                        str(selected_prior.get("selection_id", "")).strip(),
                        str(selected_prior.get("selection_hash", "")).strip(),
                        str(priors.get("snapshot_hash", "")).strip(),
                    ],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=_unique_bounded(unresolved_hidden, ceiling=MAX_MATCHED_TERMS),
                fail_closed=prior_fail_closed,
                reason_codes=_unique_bounded(
                    [str(item).strip() for item in list(selected_prior.get("reason_codes", ())) if str(item).strip()]
                    + (["prior_relevance_below_safe_threshold"] if prior_fail_closed else []),
                    ceiling=MAX_REASON_CODES,
                ),
            )
        else:
            missing_variables.append("governing scientific prior")
            if weakest_link_reason == "chain_not_started":
                weakest_link_reason = "missing_scientific_prior"
            add_step(
                step_kind=ChainStepKind.PRIOR_APPLICATION,
                statement="No scientific prior selection was available for this request frame.",
                evidence_refs=_unique_bounded(
                    [str(priors.get("snapshot_hash", "")).strip()],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=("governing scientific prior",),
                fail_closed=True,
                reason_codes=("no_selected_prior",),
            )

        world_entity = _pick_world_entity(
            world_model=world_model,
            selected_region=selected_region,
            selected_candidate=selected_candidate,
        )
        world_entity_ref = None
        world_support_fail_closed = False
        if world_entity is not None:
            world_entity_ref = str(world_entity.get("entity_id", "")).strip() or None
            world_label = str(world_entity.get("label", "")).strip() or "unknown_entity"
            world_conf = clamp_score(_to_float(world_entity.get("world_confidence"), 0.0))
            if world_conf < 0.5:
                world_support_fail_closed = True
                missing_variables.append("high-confidence world entity support")
                if weakest_link_reason == "chain_not_started":
                    weakest_link_reason = "weak_world_entity_support"
            add_step(
                step_kind=ChainStepKind.WORLD_SUPPORT,
                statement=f"World support anchors on entity '{world_label}' with confidence {world_conf:.2f}.",
                region_ref=region_ref,
                world_entity_ref=world_entity_ref,
                evidence_refs=_unique_bounded(
                    [
                        f"phase6.world_model::{world_entity_ref}" if world_entity_ref else "",
                        str(world_model.get("snapshot_hash", "")).strip(),
                        *[str(item).strip() for item in list(world_entity.get("source_refs", ())) if str(item).strip()],
                    ],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=_unique_bounded(
                    ["high-confidence world entity support"] if world_support_fail_closed else [],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                fail_closed=world_support_fail_closed,
                reason_codes=_unique_bounded(
                    [
                        "world_entity_selected",
                        f"world_confidence:{world_conf:.2f}",
                        f"target_domain:{str(world_entity.get('target_domain', '')).strip() or 'unknown'}",
                    ],
                    ceiling=MAX_REASON_CODES,
                ),
            )
        else:
            missing_variables.append("grounded world entity support")
            if weakest_link_reason == "chain_not_started":
                weakest_link_reason = "missing_world_entity_support"
            add_step(
                step_kind=ChainStepKind.WORLD_SUPPORT,
                statement="No grounded world entity support matched the bounded request context.",
                region_ref=region_ref,
                evidence_refs=_unique_bounded(
                    [str(world_model.get("snapshot_hash", "")).strip()],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=("grounded world entity support",),
                fail_closed=True,
                reason_codes=("no_world_entity_match",),
            )

        target_domain = region_target_domain
        if target_domain is None and world_entity is not None:
            target_domain = str(world_entity.get("target_domain", "")).strip() or None

        simulation_entry = _pick_simulation_entry(
            simulation_state=simulation,
            world_entity=world_entity,
            target_domain=target_domain,
        )
        simulation_ref = None
        simulation_fail_closed = False
        if simulation_entry is not None:
            simulation_ref = str(simulation_entry.get("simulation_entry_id", "")).strip() or None
            outcome = str(simulation_entry.get("outcome", "")).strip() or "unknown"
            sim_conf = clamp_score(_to_float(simulation_entry.get("confidence"), 0.0))
            if _to_bool(simulation_entry.get("fail_closed")) or sim_conf < 0.5:
                simulation_fail_closed = True
                missing_variables.append("stable simulation support")
                if weakest_link_reason == "chain_not_started":
                    weakest_link_reason = "simulation_support_weak"
            add_step(
                step_kind=ChainStepKind.SIMULATION_CHECK,
                statement=f"Simulation check returned '{outcome}' with confidence {sim_conf:.2f}.",
                region_ref=region_ref,
                world_entity_ref=world_entity_ref,
                simulation_ref=simulation_ref,
                evidence_refs=_unique_bounded(
                    [
                        simulation_ref or "",
                        str(simulation.get("snapshot_hash", "")).strip(),
                        str(simulation_entry.get("future_id", "")).strip(),
                    ],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=_unique_bounded(
                    ["stable simulation support"] if simulation_fail_closed else [],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                fail_closed=simulation_fail_closed,
                reason_codes=_unique_bounded(
                    [
                        f"simulation_outcome:{outcome}",
                        *[str(item).strip() for item in list(simulation_entry.get("reason_codes", ())) if str(item).strip()],
                    ],
                    ceiling=MAX_REASON_CODES,
                ),
            )
        else:
            missing_variables.append("simulation evidence for selected context")
            if weakest_link_reason == "chain_not_started":
                weakest_link_reason = "missing_simulation_evidence"
            add_step(
                step_kind=ChainStepKind.SIMULATION_CHECK,
                statement="No simulation entry supported the selected context.",
                region_ref=region_ref,
                world_entity_ref=world_entity_ref,
                evidence_refs=_unique_bounded(
                    [str(simulation.get("snapshot_hash", "")).strip()],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=("simulation evidence for selected context",),
                fail_closed=True,
                reason_codes=("no_simulation_match",),
            )

        usefulness_domain = _pick_usefulness_domain(usefulness_state=usefulness, target_domain=target_domain)
        usefulness_ref = None
        usefulness_fail_closed = False
        if usefulness_domain is not None:
            domain_id = str(usefulness_domain.get("domain_id", "")).strip() or "unknown_domain"
            weighted_score = clamp_score(_to_float(usefulness_domain.get("weighted_score"), 0.0))
            domain_outcome = str(usefulness_domain.get("outcome", "")).strip() or "insufficient"
            overall_outcome = str(usefulness.get("overall_outcome", "")).strip() or "insufficient"
            usefulness_ref = f"phase6.usefulness::{domain_id}"
            if domain_outcome != "qualified" or overall_outcome != "qualified" or weighted_score < 0.6:
                usefulness_fail_closed = True
                missing_variables.append("multi-signal usefulness evidence")
                if weakest_link_reason == "chain_not_started":
                    weakest_link_reason = "usefulness_insufficient"
            add_step(
                step_kind=ChainStepKind.USEFULNESS_CHECK,
                statement=(
                    f"Usefulness domain '{domain_id}' is '{domain_outcome}' with weighted score {weighted_score:.2f}."
                ),
                region_ref=region_ref,
                world_entity_ref=world_entity_ref,
                simulation_ref=simulation_ref,
                usefulness_ref=usefulness_ref,
                evidence_refs=_unique_bounded(
                    [
                        usefulness_ref,
                        str(usefulness.get("snapshot_hash", "")).strip(),
                    ],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=_unique_bounded(
                    ["multi-signal usefulness evidence"] if usefulness_fail_closed else [],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                fail_closed=usefulness_fail_closed,
                reason_codes=_unique_bounded(
                    [
                        f"domain_outcome:{domain_outcome}",
                        f"overall_outcome:{overall_outcome}",
                        f"weighted_score:{weighted_score:.2f}",
                    ],
                    ceiling=MAX_REASON_CODES,
                ),
            )
        else:
            missing_variables.append("usefulness domain score")
            if weakest_link_reason == "chain_not_started":
                weakest_link_reason = "missing_usefulness_score"
            add_step(
                step_kind=ChainStepKind.USEFULNESS_CHECK,
                statement="No usefulness domain score was available for this chain.",
                region_ref=region_ref,
                world_entity_ref=world_entity_ref,
                simulation_ref=simulation_ref,
                evidence_refs=_unique_bounded(
                    [str(usefulness.get("snapshot_hash", "")).strip()],
                    ceiling=MAX_MATCHED_TERMS,
                ),
                missing_variables_for_step=("usefulness domain score",),
                fail_closed=True,
                reason_codes=("no_usefulness_domain_score",),
            )

        dedup_missing = _unique_bounded(missing_variables, ceiling=MAX_MATCHED_TERMS)
        add_step(
            step_kind=ChainStepKind.MISSING_VARIABLE,
            statement=(
                "Missing-variable check identified unresolved inputs."
                if dedup_missing
                else "Missing-variable check found no critical unresolved inputs in bounded evidence."
            ),
            principle_ref=principle_ref,
            region_ref=region_ref,
            world_entity_ref=world_entity_ref,
            simulation_ref=simulation_ref,
            usefulness_ref=usefulness_ref,
            evidence_refs=_unique_bounded(
                [
                    str(priors.get("snapshot_hash", "")).strip(),
                    str(region_state.get("snapshot_hash", "")).strip(),
                    str(world_model.get("snapshot_hash", "")).strip(),
                    str(simulation.get("snapshot_hash", "")).strip(),
                    str(usefulness.get("snapshot_hash", "")).strip(),
                ],
                ceiling=MAX_MATCHED_TERMS,
            ),
            missing_variables_for_step=dedup_missing,
            fail_closed=bool(dedup_missing),
            reason_codes=_unique_bounded(
                ["missing_variables_present"] if dedup_missing else ["no_critical_missing_variables"],
                ceiling=MAX_REASON_CODES,
            ),
        )

        if not steps:
            raise Phase8ScienceWorldAwarenessError("causal chain reasoning produced no steps")
        if len(steps) > MAX_CAUSAL_CHAIN_STEPS:
            raise Phase8ScienceWorldAwarenessError(
                f"causal step count exceeds Phase 8 ceiling of {MAX_CAUSAL_CHAIN_STEPS}"
            )

        fail_closed = any(step.fail_closed for step in steps)
        if weakest_link_reason == "chain_not_started":
            weakest_link_reason = "none_detected" if not fail_closed else "fail_closed_flag_present"

        principle_refs = _unique_bounded(
            [step.principle_ref or "" for step in steps if step.principle_ref],
            ceiling=MAX_MATCHED_TERMS,
        )
        world_entity_refs = _unique_bounded(
            [step.world_entity_ref or "" for step in steps if step.world_entity_ref],
            ceiling=MAX_MATCHED_TERMS,
        )
        simulation_refs = _unique_bounded(
            [step.simulation_ref or "" for step in steps if step.simulation_ref],
            ceiling=MAX_MATCHED_TERMS,
        )
        final_region_ref = next((step.region_ref for step in steps if step.region_ref), None)
        final_usefulness_ref = next((step.usefulness_ref for step in reversed(steps) if step.usefulness_ref), None)

        chain_payload = {
            "schema": self.SCHEMA,
            "request_id": request_id,
            "step_hashes": [step.step_hash for step in steps],
            "principle_refs": list(principle_refs),
            "region_ref": final_region_ref,
            "world_entity_refs": list(world_entity_refs),
            "simulation_refs": list(simulation_refs),
            "usefulness_ref": final_usefulness_ref,
            "missing_variables": list(dedup_missing),
            "fail_closed": fail_closed,
            "weakest_link_reason": weakest_link_reason,
        }
        chain_id = f"ccr::{stable_hash_payload({'request_id': request_id, 'steps': [step.step_hash for step in steps]})[:12]}"
        return CausalChainSnapshot(
            schema=self.SCHEMA,
            request_id=request_id,
            chain_id=chain_id,
            step_count=len(steps),
            steps=tuple(steps),
            principle_refs=principle_refs,
            region_ref=final_region_ref,
            world_entity_refs=world_entity_refs,
            simulation_refs=simulation_refs,
            usefulness_ref=final_usefulness_ref,
            missing_variables=dedup_missing,
            fail_closed=fail_closed,
            weakest_link_reason=weakest_link_reason,
            snapshot_hash=stable_hash_payload(chain_payload),
        )
