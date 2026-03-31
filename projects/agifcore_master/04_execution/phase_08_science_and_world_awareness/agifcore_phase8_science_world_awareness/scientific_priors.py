from __future__ import annotations

import re
from typing import Any, Mapping

from .contracts import (
    MAX_MATCHED_TERMS,
    MAX_SELECTED_PRIORS,
    MAX_REASON_CODES,
    Phase8ScienceWorldAwarenessError,
    ScientificPriorCell,
    ScientificPriorsSnapshot,
    SelectedScientificPrior,
    clamp_score,
    require_mapping,
    require_non_empty_str,
    stable_hash_payload,
)

_TOKEN_RE = re.compile(r"[a-z0-9']+")
_TOPIC_TOKEN_LIMIT = 8


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _unique_bounded(values: list[str], *, ceiling: int) -> tuple[str, ...]:
    unique = sorted({item.strip() for item in values if item and item.strip()})
    return tuple(unique[:ceiling])


def _validate_catalog(catalog: tuple[ScientificPriorCell, ...]) -> tuple[ScientificPriorCell, ...]:
    if not catalog:
        raise Phase8ScienceWorldAwarenessError("scientific prior catalog cannot be empty")
    for index, cell in enumerate(catalog):
        if not isinstance(cell, ScientificPriorCell):
            raise Phase8ScienceWorldAwarenessError(
                f"scientific prior catalog entry {index} must be a ScientificPriorCell"
            )
        if not cell.provenance_refs:
            raise Phase8ScienceWorldAwarenessError(
                f"scientific prior {cell.cell_id} must include at least one provenance ref"
            )
        for ref in cell.provenance_refs:
            require_non_empty_str(ref, f"scientific prior {cell.cell_id} provenance_ref")
    return catalog


def _match_terms(cell_terms: tuple[str, ...], *, query_terms: set[str], normalized_text: str) -> tuple[str, ...]:
    matched: list[str] = []
    for term in cell_terms:
        normalized_term = term.strip().lower()
        if not normalized_term:
            continue
        if " " in normalized_term:
            if normalized_term in normalized_text:
                matched.append(term)
            continue
        if normalized_term in query_terms:
            matched.append(term)
    return _unique_bounded(matched, ceiling=MAX_MATCHED_TERMS)


def _catalog_row(
    *,
    index: int,
    seed_topic: str,
    principle_id: str,
    plain_language_law: str,
    variables: tuple[str, ...],
    causal_mechanism: str,
    scope_limits: str,
    failure_case: str,
    worked_example: str,
    transfer_hint: str,
    cue_terms: tuple[str, ...],
    hidden_variable_hints: tuple[str, ...],
) -> ScientificPriorCell:
    payload = {
        "cell_id": f"phase8.prior.{index:03d}",
        "family_name": "scientific_prior",
        "principle_id": principle_id,
        "seed_topic": seed_topic,
        "plain_language_law": plain_language_law,
        "variables": list(variables),
        "causal_mechanism": causal_mechanism,
        "scope_limits": scope_limits,
        "failure_case": failure_case,
        "worked_example": worked_example,
        "transfer_hint": transfer_hint,
        "cue_terms": list(cue_terms),
        "hidden_variable_hints": list(hidden_variable_hints),
        "provenance_refs": [
            "projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md",
            "projects/agifcore_master/01_plan/COMPONENT_CATALOG.md#CC-010",
            "projects/agifcore_master/01_plan/COMPONENT_CATALOG.md#CC-021",
            "agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8c_governed_structural_growth/agif_phase8c_governed_structural_growth/contracts.py",
            "agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8c_governed_structural_growth/agif_phase8c_governed_structural_growth/runtime.py",
        ],
    }
    cell_hash = stable_hash_payload(payload)
    return ScientificPriorCell(
        cell_id=payload["cell_id"],
        family_name=payload["family_name"],
        principle_id=payload["principle_id"],
        seed_topic=payload["seed_topic"],
        plain_language_law=payload["plain_language_law"],
        variables=variables,
        causal_mechanism=payload["causal_mechanism"],
        scope_limits=payload["scope_limits"],
        failure_case=payload["failure_case"],
        worked_example=payload["worked_example"],
        transfer_hint=payload["transfer_hint"],
        cue_terms=cue_terms,
        hidden_variable_hints=hidden_variable_hints,
        provenance_refs=tuple(payload["provenance_refs"]),
        cell_hash=cell_hash,
    )


class ScientificPriorsEngine:
    """Build a bounded scientific-prior snapshot from a Phase 8 inference-like state."""

    SCHEMA = "agifcore.phase_08.scientific_priors.v1"

    def build_catalog(self) -> tuple[ScientificPriorCell, ...]:
        return (
            _catalog_row(
                index=1,
                seed_topic="place and region",
                principle_id="place_region_context",
                plain_language_law="Where something happens changes what inputs and constraints matter.",
                variables=("latitude", "elevation", "distance_from_water", "surface_type"),
                causal_mechanism="Terrain and land-water mix alter heat storage and airflow.",
                scope_limits="Useful for bounded regional differences, not exact live readings.",
                failure_case="A sheltered valley can diverge from nearby regional averages.",
                worked_example="A coastal district often swings less in temperature than inland blocks.",
                transfer_hint="Compare terrain, elevation, and water proximity before committing.",
                cue_terms=("coast", "coastal", "inland", "region", "city", "valley", "hill"),
                hidden_variable_hints=("distance from water", "elevation", "surface material"),
            ),
            _catalog_row(
                index=2,
                seed_topic="time and season",
                principle_id="time_season_cycle",
                plain_language_law="Time of day and season shift baseline energy and moisture inputs.",
                variables=("time_of_day", "season", "day_length", "sun_angle"),
                causal_mechanism="Solar input and cooling windows change state transitions.",
                scope_limits="Pattern-level guidance only; exact values still require measurements.",
                failure_case="A fast front can temporarily override expected seasonal behavior.",
                worked_example="Late-day pavement heat can keep urban evenings warmer.",
                transfer_hint="Check local time cycle before estimating directional changes.",
                cue_terms=("winter", "summer", "spring", "autumn", "night", "sunset", "morning"),
                hidden_variable_hints=("hours since sunset", "cloud cover", "seasonal baseline"),
            ),
            _catalog_row(
                index=3,
                seed_topic="weather and climate",
                principle_id="weather_driver_interaction",
                plain_language_law="Wind, moisture, and cloud cover jointly shape local conditions.",
                variables=("humidity", "wind_speed", "wind_direction", "cloud_cover"),
                causal_mechanism="Advection and moisture balance regulate heat and precipitation signals.",
                scope_limits="Does not replace local sensors when current values are requested.",
                failure_case="Microclimates can invert broader regional expectations.",
                worked_example="Onshore wind can cool one district while inland heat persists.",
                transfer_hint="Look for interacting drivers instead of a single-cause shortcut.",
                cue_terms=("weather", "climate", "humid", "humidity", "wind", "storm", "rain"),
                hidden_variable_hints=("wind direction", "cloud cover", "moisture source"),
            ),
            _catalog_row(
                index=4,
                seed_topic="motion and force",
                principle_id="force_balance",
                plain_language_law="Observed motion reflects net forces and constraints.",
                variables=("force", "mass", "friction", "slope"),
                causal_mechanism="Acceleration and resistance emerge from force balance.",
                scope_limits="Explains directionality; exact trajectories need calibrated measurements.",
                failure_case="Unmodeled friction or compliance can flip the expected outcome.",
                worked_example="A bike slows faster uphill when friction and slope combine.",
                transfer_hint="Identify driving and resisting forces before inferring behavior.",
                cue_terms=("motion", "force", "speed", "push", "pull", "friction"),
                hidden_variable_hints=("surface friction", "mass distribution", "slope"),
            ),
            _catalog_row(
                index=5,
                seed_topic="energy and heat",
                principle_id="heat_transfer_pathways",
                plain_language_law="Temperature outcomes depend on storage, transfer, and dissipation paths.",
                variables=("radiation", "conduction", "convection", "thermal_mass"),
                causal_mechanism="Heat accumulates and dissipates based on material and airflow.",
                scope_limits="Supports bounded explanation; exact temperatures need current data.",
                failure_case="Wind shifts can rapidly change apparent local heat behavior.",
                worked_example="Dark asphalt can remain warm after sunset due to stored heat.",
                transfer_hint="Check material and airflow before inferring heat persistence.",
                cue_terms=("heat", "hot", "warm", "cool", "temperature", "thermal"),
                hidden_variable_hints=("surface material", "wind speed", "shade"),
            ),
            _catalog_row(
                index=6,
                seed_topic="flow and pressure",
                principle_id="flow_resistance_balance",
                plain_language_law="Flow and pressure outcomes depend on pathway resistance and gradients.",
                variables=("pressure", "gradient", "resistance", "capacity"),
                causal_mechanism="Gradient-driven transport is constrained by pathway impedance.",
                scope_limits="Good for causal direction; exact rates require direct measurement.",
                failure_case="Hidden bottlenecks can dominate outcomes despite low nominal demand.",
                worked_example="Blocked drainage can cause flooding under moderate rainfall.",
                transfer_hint="Trace bottlenecks and gradients before claiming certainty.",
                cue_terms=("flow", "pressure", "drain", "flood", "air", "leak"),
                hidden_variable_hints=("drainage capacity", "path resistance", "starting pressure"),
            ),
            _catalog_row(
                index=7,
                seed_topic="growth and decay",
                principle_id="resource_constraint_growth",
                plain_language_law="Growth and decline depend on resource balance and stage constraints.",
                variables=("resource_input", "resource_loss", "stage", "stress"),
                causal_mechanism="Net accumulation follows competing gain and loss channels.",
                scope_limits="Useful for trend logic, not precise forecast magnitudes.",
                failure_case="Stress shocks can reverse expected growth trend quickly.",
                worked_example="Crop yield response can invert under water stress.",
                transfer_hint="Check stage and limiting resources before projecting trend.",
                cue_terms=("grow", "growth", "decay", "crop", "plant", "yield"),
                hidden_variable_hints=("water availability", "soil condition", "development stage"),
            ),
            _catalog_row(
                index=8,
                seed_topic="human systems and incentives",
                principle_id="incentive_supply_demand",
                plain_language_law="Behavior in human systems shifts with incentives and constraints.",
                variables=("supply", "demand", "friction", "latency"),
                causal_mechanism="Decision responses follow changing costs, benefits, and bottlenecks.",
                scope_limits="Supports directional reasoning; current market facts still need freshness checks.",
                failure_case="Policy or logistics shocks can dominate expected incentive response.",
                worked_example="Transport bottlenecks can raise prices despite stable production.",
                transfer_hint="Identify incentive gradients and friction points before estimating outcomes.",
                cue_terms=("market", "price", "demand", "supply", "rent", "cost"),
                hidden_variable_hints=("storage loss", "transport bottleneck", "policy shift"),
            ),
            _catalog_row(
                index=9,
                seed_topic="measurement and uncertainty",
                principle_id="measurement_uncertainty",
                plain_language_law="Any claim is bounded by measurement quality and missing variables.",
                variables=("measurement_error", "sampling_bias", "missing_variables"),
                causal_mechanism="Observed values are filtered through instrument and sampling limits.",
                scope_limits="Mandatory guardrail for live-current and exact-value requests.",
                failure_case="Sparse or stale observations can produce false confidence.",
                worked_example="A single stale reading cannot prove current local status.",
                transfer_hint="Raise uncertainty when freshness or instrumentation is weak.",
                cue_terms=("current", "latest", "today", "exact", "measure", "uncertain"),
                hidden_variable_hints=("missing live reading", "sampling limits", "instrument drift"),
            ),
        )

    def build_snapshot(
        self,
        *,
        entity_request_inference_state: Mapping[str, Any],
        prior_catalog: tuple[ScientificPriorCell, ...] | None = None,
    ) -> ScientificPriorsSnapshot:
        inference = require_mapping(entity_request_inference_state, "entity_request_inference_state")
        conversation_id = require_non_empty_str(inference.get("conversation_id"), "conversation_id")
        turn_id = require_non_empty_str(inference.get("turn_id"), "turn_id")
        request_id = f"{conversation_id}::{turn_id}"

        normalized_text = str(inference.get("normalized_text", "")).strip().lower()
        extracted_terms = [
            str(item).strip().lower()
            for item in list(inference.get("extracted_terms", ()))
            if str(item).strip()
        ]
        science_topic_cues = [
            str(item).strip().lower()
            for item in list(inference.get("science_topic_cues", ()))
            if str(item).strip()
        ]
        hidden_variable_cues = [
            str(item).strip().lower()
            for item in list(inference.get("hidden_variable_cues", ()))
            if str(item).strip()
        ]
        if not normalized_text and not extracted_terms:
            raise Phase8ScienceWorldAwarenessError(
                "entity_request_inference_state must include normalized_text or extracted_terms"
            )

        catalog = prior_catalog if prior_catalog is not None else self.build_catalog()
        available_catalog = _validate_catalog(tuple(catalog))

        query_terms = set(_tokens(normalized_text))
        query_terms.update(extracted_terms)
        query_terms.update(science_topic_cues)
        query_terms.update(hidden_variable_cues)

        scored: list[tuple[float, ScientificPriorCell, tuple[str, ...], tuple[str, ...], tuple[str, ...]]] = []
        for cell in available_catalog:
            cue_matches = _match_terms(
                cell.cue_terms,
                query_terms=query_terms,
                normalized_text=normalized_text,
            )
            hidden_matches = _match_terms(
                cell.hidden_variable_hints,
                query_terms=query_terms,
                normalized_text=normalized_text,
            )

            topic_bonus = 0.0
            seed_topic_tokens = set(_tokens(cell.seed_topic))
            if seed_topic_tokens.intersection(query_terms):
                topic_bonus = 0.15
            if set(science_topic_cues).intersection(seed_topic_tokens):
                topic_bonus = 0.3

            score = clamp_score((len(cue_matches) * 0.16) + (len(hidden_matches) * 0.24) + topic_bonus)
            reason_codes: list[str] = []
            if cue_matches:
                reason_codes.append("cue_term_match")
            if hidden_matches:
                reason_codes.append("hidden_variable_match")
            if topic_bonus > 0.0:
                reason_codes.append("seed_topic_alignment")
            if score > 0.0:
                scored.append(
                    (
                        score,
                        cell,
                        cue_matches,
                        hidden_matches,
                        tuple(reason_codes[:MAX_REASON_CODES]),
                    )
                )

        scored.sort(key=lambda row: (row[0], row[1].principle_id), reverse=True)
        selected_rows = scored[:MAX_SELECTED_PRIORS]

        selected_priors: list[SelectedScientificPrior] = []
        selected_cells: list[ScientificPriorCell] = []
        selected_ids: list[str] = []
        selection_notes: list[str] = []

        for index, (score, cell, cue_matches, hidden_matches, reason_codes) in enumerate(selected_rows, start=1):
            selection_payload = {
                "request_id": request_id,
                "selection_index": index,
                "cell_id": cell.cell_id,
                "principle_id": cell.principle_id,
                "matched_cue_terms": list(cue_matches),
                "matched_hidden_variables": list(hidden_matches),
                "relevance_score": score,
                "reason_codes": list(reason_codes),
                "cell_hash": cell.cell_hash,
            }
            selection = SelectedScientificPrior(
                selection_id=f"{request_id}::prior::{index:02d}",
                cell_id=cell.cell_id,
                principle_id=cell.principle_id,
                matched_cue_terms=cue_matches,
                matched_hidden_variables=hidden_matches,
                relevance_score=score,
                reason_codes=reason_codes,
                provenance_refs=cell.provenance_refs,
                selection_hash=stable_hash_payload(selection_payload),
            )
            selected_priors.append(selection)
            selected_cells.append(cell)
            selected_ids.append(cell.cell_id)

        if not selected_priors:
            selection_notes.append("no_prior_matched")
            # Always keep uncertainty guardrail available when nothing else matches.
            fallback = next((cell for cell in available_catalog if cell.principle_id == "measurement_uncertainty"), None)
            if fallback is not None:
                fallback_payload = {
                    "request_id": request_id,
                    "selection_index": 1,
                    "cell_id": fallback.cell_id,
                    "principle_id": fallback.principle_id,
                    "matched_cue_terms": [],
                    "matched_hidden_variables": [],
                    "relevance_score": 0.05,
                    "reason_codes": ["uncertainty_guardrail_fallback"],
                    "cell_hash": fallback.cell_hash,
                }
                fallback_selection = SelectedScientificPrior(
                    selection_id=f"{request_id}::prior::01",
                    cell_id=fallback.cell_id,
                    principle_id=fallback.principle_id,
                    matched_cue_terms=(),
                    matched_hidden_variables=(),
                    relevance_score=0.05,
                    reason_codes=("uncertainty_guardrail_fallback",),
                    provenance_refs=fallback.provenance_refs,
                    selection_hash=stable_hash_payload(fallback_payload),
                )
                selected_priors.append(fallback_selection)
                selected_cells.append(fallback)
                selected_ids.append(fallback.cell_id)
                selection_notes.append("measurement_uncertainty_fallback_applied")
        else:
            selection_notes.append("prior_selection_complete")

        if len(selected_priors) > MAX_SELECTED_PRIORS:
            raise Phase8ScienceWorldAwarenessError(
                f"selected prior count exceeds Phase 8 ceiling of {MAX_SELECTED_PRIORS}"
            )

        snapshot_payload = {
            "schema": self.SCHEMA,
            "request_id": request_id,
            "available_prior_count": len(available_catalog),
            "selected_prior_ids": list(selected_ids),
            "selection_hashes": [selection.selection_hash for selection in selected_priors],
            "selection_notes": selection_notes,
        }
        return ScientificPriorsSnapshot(
            schema=self.SCHEMA,
            request_id=request_id,
            available_prior_count=len(available_catalog),
            selected_prior_count=len(selected_priors),
            selected_prior_ids=tuple(selected_ids),
            selected_priors=tuple(selected_priors),
            selected_cells=tuple(selected_cells),
            selection_notes=_unique_bounded(selection_notes, ceiling=_TOPIC_TOKEN_LIMIT),
            snapshot_hash=stable_hash_payload(snapshot_payload),
        )
