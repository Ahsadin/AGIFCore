# Phase 6 Demo Index

## Purpose

This bundle is the user-review demo package for Phase 6. It is evidence-backed only and does not approve, complete, or close Phase 6.

## Inspectable Files

- `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_evidence_manifest.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_entity_classes_report.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_target_domain_structures_report.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_world_model_representation_report.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_candidate_futures_report.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_what_if_simulation_report.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_fault_pressure_overload_conflict_report.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_instrumentation_report.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_usefulness_scoring_report.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_causal_simulation_demo.json`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_stress_conflict_demo.json`

## Demo Contents

1. `phase_06_causal_simulation_demo.md`
2. `phase_06_stress_conflict_demo.md`
3. `phase_06_causal_simulation_demo.json`
4. `phase_06_stress_conflict_demo.json`

## Runnable Demo Surfaces

- `python3 projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/run_phase_06_causal_simulation_demo.py`
- `python3 projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/run_phase_06_stress_conflict_demo.py`

These commands regenerate the machine-readable demo exports in the demo bundle from the real Phase 6 fixture chain.

## Evidence Summary

- The evidence manifest reports `available_report_count: 8`, `missing_reports: []`, `invalid_reports: []`, and `status: phase_6_verifier_family_pass`.
- Phase 6 remains `open` in the evidence manifest.
- Every required report listed in the manifest has `status: pass`.

## What The User Can Verify

- The world model is read-only, provenance-linked, and separated from the Phase 4 and Phase 5 stores.
- Candidate futures are real branch records with state codes and replay-safe provenance.
- What-if simulation is deterministic, trace-linked, and fail-closed when the inputs demand it.
- Fault, pressure, conflict, and overload lanes are machine-checkable and chained from the earlier outputs.
- Instrumentation and usefulness scoring are evidence-linked and bounded.
- The demo bundle includes runnable machine-readable demo exports, not markdown-only summaries.

## Demo Rules

- Use only the exact file paths above.
- Do not treat this bundle as approval.
- Do not treat this bundle as phase completion.
- Do not use any Phase 7 or Phase 8 claims.
