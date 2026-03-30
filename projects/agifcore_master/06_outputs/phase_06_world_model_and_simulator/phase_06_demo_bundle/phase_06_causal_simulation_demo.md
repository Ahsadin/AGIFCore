# Phase 6 Causal Simulation Demo

## Purpose

This demo shows the Phase 6 causal path from world model to candidate futures to what-if simulation using real evidence files only.

## Review Path

1. Start with the plan and evidence manifest:
   - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_evidence_manifest.json`
2. Confirm the world model contract surface:
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_world_model_representation_report.json`
3. Confirm the candidate future branch surface:
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_candidate_futures_report.json`
4. Confirm the what-if simulation surface:
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_what_if_simulation_report.json`
5. Confirm the runnable demo export:
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_causal_simulation_demo.json`

## Testable Rerun

Run this command from repo root:

```bash
python3 projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/run_phase_06_causal_simulation_demo.py
```

What it regenerates:

- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_causal_simulation_demo.json`

## What The Evidence Shows

- The world model report shows explicit Phase 4 and Phase 5 interfaces, separate world cells and relations, execution-disabled operators, and bounded provenance.
- The candidate futures report shows real branch records, projected outcomes, state codes, and provenance linked back to the world model.
- The what-if simulation report shows trace-linked simulation entries, read-only evaluation, a forced fail-closed path when the candidate future is abstaining, and branch-depth ceiling enforcement.

## Exact File Anchors To Inspect

- World model anchor:
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_world_model_representation_report.json`
- Candidate future anchor:
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_candidate_futures_report.json`
- What-if anchor:
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_what_if_simulation_report.json`
- Runnable demo export:
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_causal_simulation_demo.json`

## What The User Should Check

- The sample world entity and relation in the world model report are read-only and provenance-linked.
- The sample future in the candidate futures report has `projected_outcome: review_only_projected` and the `state_codes` list includes `read_only_projection` and `live_transfer_execution_disabled`.
- The sample simulation entry in the what-if report links to the input world entity and candidate future and records a trace of the causal path.
- The machine-readable demo export contains the same path as structured data with sample world entity, sample future, and sample simulation entry.
- The manifest still says Phase 6 remains open.

## What Failure Would Look Like

- The world model collapses into one mixed state object.
- Candidate futures appear without real branch records or provenance.
- What-if simulation lacks trace steps or fails to prove the branch-depth ceiling.
- Any file says Phase 6 is approved, complete, or closed.

## Status

Phase 6 remains open.
