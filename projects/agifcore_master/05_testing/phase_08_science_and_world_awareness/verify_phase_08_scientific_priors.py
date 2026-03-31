from __future__ import annotations

import json

import _phase_08_verifier_common as vc

VERIFIER = "verify_phase_08_scientific_priors"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_08_scientific_priors_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase8_science_world_awareness.contracts",
    "agifcore_phase8_science_world_awareness.scientific_priors",
)
RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/__init__.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py",
    "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/scientific_priors.py",
)


def _build_prior_cell(
    *,
    cell_id: str,
    family_name: str,
    principle_id: str,
    seed_topic: str,
    plain_language_law: str,
    variables: tuple[str, ...],
    causal_mechanism: str,
    scope_limits: str,
    failure_case: str,
    worked_example: str,
    transfer_hint: str,
    cue_terms: tuple[str, ...],
    hidden_variable_hints: tuple[str, ...],
    provenance_refs: tuple[str, ...],
):
    from agifcore_phase8_science_world_awareness.contracts import ScientificPriorCell, stable_hash_payload

    payload = {
        "cell_id": cell_id,
        "family_name": family_name,
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
        "provenance_refs": list(provenance_refs),
    }
    return ScientificPriorCell(
        cell_id=cell_id,
        family_name=family_name,
        principle_id=principle_id,
        seed_topic=seed_topic,
        plain_language_law=plain_language_law,
        variables=variables,
        causal_mechanism=causal_mechanism,
        scope_limits=scope_limits,
        failure_case=failure_case,
        worked_example=worked_example,
        transfer_hint=transfer_hint,
        cue_terms=cue_terms,
        hidden_variable_hints=hidden_variable_hints,
        provenance_refs=provenance_refs,
        cell_hash=stable_hash_payload(payload),
    )


def _build_catalog() -> tuple[object, ...]:
    provenance_refs = (
        "projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-TRL-04_PHASE_8_SLICE_01_VERIFIER_COMMON_AND_PRIORS.md",
        "projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md",
        "projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/scientific_priors.py",
    )
    return (
        _build_prior_cell(
            cell_id="phase8.prior.custom.001",
            family_name="scientific_prior",
            principle_id="coastal_weather_baseline",
            seed_topic="weather and climate",
            plain_language_law="Coastal conditions shift through local water, wind, and cooling cycles.",
            variables=("coastal_proximity", "humidity", "sunset", "wind_direction"),
            causal_mechanism="Sea-air exchange and evening cooling can change near-shore conditions.",
            scope_limits="Gives bounded directional guidance, not exact live readings.",
            failure_case="An inland front can overpower the coastal baseline.",
            worked_example="A shoreline block can stay muggy after sunset while inland air cools faster.",
            transfer_hint="Check coast, time of day, and moisture before drawing conclusions.",
            cue_terms=("coastal", "humidity", "sunset", "shore", "evening"),
            hidden_variable_hints=("sea breeze", "night cooling", "water proximity"),
            provenance_refs=provenance_refs,
        ),
        _build_prior_cell(
            cell_id="phase8.prior.custom.002",
            family_name="scientific_prior",
            principle_id="measurement_uncertainty",
            seed_topic="measurement and uncertainty",
            plain_language_law="Freshness and instrumentation limits control how much certainty is safe.",
            variables=("measurement_error", "sampling_bias", "missing_variables"),
            causal_mechanism="Observed values are filtered through sensor and sampling limits.",
            scope_limits="Required guardrail for weak or current-fact requests.",
            failure_case="A stale reading can look precise while being wrong.",
            worked_example="One outdated reading cannot prove the current state of a system.",
            transfer_hint="Fail closed when the evidence is weak or freshness is unclear.",
            cue_terms=("current", "today", "latest", "exact", "measure", "uncertain"),
            hidden_variable_hints=("live reading", "sampling limits", "instrument drift"),
            provenance_refs=provenance_refs,
        ),
        _build_prior_cell(
            cell_id="phase8.prior.custom.003",
            family_name="scientific_prior",
            principle_id="orbital_momentum",
            seed_topic="motion and force",
            plain_language_law="Motion changes follow force balance and momentum exchange.",
            variables=("momentum", "mass", "force", "trajectory"),
            causal_mechanism="Acceleration emerges from net force, not from local weather cues.",
            scope_limits="Useful for motion reasoning only.",
            failure_case="Weather and moisture questions do not need orbital mechanics.",
            worked_example="A satellite path bends because of orbital forces, not humidity.",
            transfer_hint="Ignore this prior unless the request is about motion or forces.",
            cue_terms=("orbit", "momentum", "satellite", "trajectory", "acceleration"),
            hidden_variable_hints=("mass distribution", "net force", "slope"),
            provenance_refs=provenance_refs,
        ),
    )


def build_pass_report() -> dict[str, object]:
    from agifcore_phase8_science_world_awareness.contracts import MAX_SELECTED_PRIORS, ScientificPriorsSnapshot
    from agifcore_phase8_science_world_awareness.scientific_priors import ScientificPriorsEngine

    engine = ScientificPriorsEngine()
    catalog = _build_catalog()

    strong_snapshot = engine.build_snapshot(
        entity_request_inference_state={
            "conversation_id": "conv-priors",
            "turn_id": "turn-priors-1",
            "normalized_text": "What current coastal humidity changes after sunset?",
            "extracted_terms": ("current", "coastal", "humidity", "sunset"),
            "science_topic_cues": ("weather", "measurement"),
            "hidden_variable_cues": ("sea breeze", "sampling limits"),
        },
        prior_catalog=catalog,  # type: ignore[arg-type]
    )
    if not isinstance(strong_snapshot, ScientificPriorsSnapshot):
        raise RuntimeError("scientific priors engine did not return a ScientificPriorsSnapshot")
    if strong_snapshot.available_prior_count != 3:
        raise RuntimeError("catalog size was not preserved in the snapshot")
    if strong_snapshot.selected_prior_count != 2:
        raise RuntimeError("strong request should have selected exactly two priors")
    if strong_snapshot.selected_prior_count > MAX_SELECTED_PRIORS:
        raise RuntimeError("selected prior count exceeded the Phase 8 ceiling")

    selected_ids = set(strong_snapshot.selected_prior_ids)
    if "phase8.prior.custom.001" not in selected_ids or "phase8.prior.custom.002" not in selected_ids:
        raise RuntimeError("strong request did not select the relevant and ambiguous priors")
    if "phase8.prior.custom.003" in selected_ids:
        raise RuntimeError("irrelevant prior was selected for the strong request")
    if not all(prior.provenance_refs for prior in strong_snapshot.selected_priors):
        raise RuntimeError("selected priors lost their provenance refs")

    weak_snapshot = engine.build_snapshot(
        entity_request_inference_state={
            "conversation_id": "conv-priors",
            "turn_id": "turn-priors-2",
            "normalized_text": "Explain this briefly.",
            "extracted_terms": ("explain", "briefly"),
            "science_topic_cues": (),
            "hidden_variable_cues": (),
        },
        prior_catalog=catalog,  # type: ignore[arg-type]
    )
    if weak_snapshot.selected_prior_count != 1:
        raise RuntimeError("weak request should have failed closed to a single fallback prior")
    fallback = weak_snapshot.selected_priors[0]
    if fallback.principle_id != "measurement_uncertainty":
        raise RuntimeError("weak request did not fail closed to the measurement_uncertainty guardrail")
    if "measurement_uncertainty_fallback_applied" not in weak_snapshot.selection_notes:
        raise RuntimeError("weak request did not record the fallback note")

    report = vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES) + [
            "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/_phase_08_verifier_common.py",
            "projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_scientific_priors.py",
        ],
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "catalog-and-snapshot-contracts-validated", "result": "pass"},
            {"id": "relevant-and-ambiguous-priors-selected", "result": "pass"},
            {"id": "irrelevant-prior-not-selected", "result": "pass"},
            {"id": "weak-request-fails-closed", "result": "pass"},
            {"id": "provenance-refs-preserved", "result": "pass"},
        ],
        anchors={
            "catalog": [cell.to_dict() for cell in catalog],
            "strong_request": strong_snapshot.to_dict(),
            "weak_request": weak_snapshot.to_dict(),
            "selected_strong_priors": [prior.to_dict() for prior in strong_snapshot.selected_priors],
        },
        notes=["priors selection stays bounded and fail-closed when the catalog evidence is weak"],
    )
    vc.refresh_evidence_manifest()
    return report


def main() -> int:
    missing = vc.missing_files(list(vc.PLAN_REFS) + list(RUNTIME_FILES))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=list(vc.PLAN_REFS) + list(RUNTIME_FILES),
            assertion_ids=[
                "runtime-imports-available",
                "catalog-and-snapshot-contracts-validated",
                "relevant-and-ambiguous-priors-selected",
                "irrelevant-prior-not-selected",
                "weak-request-fails-closed",
                "provenance-refs-preserved",
            ],
            blocker_kind="missing_runtime_dependencies",
            blocker_message="Phase 8 scientific priors runtime files are not ready yet.",
            missing=missing,
        )
        vc.dump_json(REPORT_PATH, report)
        vc.refresh_evidence_manifest()
        print("phase_08 scientific_priors verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    report = build_pass_report()
    vc.dump_json(REPORT_PATH, report)
    vc.refresh_evidence_manifest()
    print("phase_08 scientific_priors verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
