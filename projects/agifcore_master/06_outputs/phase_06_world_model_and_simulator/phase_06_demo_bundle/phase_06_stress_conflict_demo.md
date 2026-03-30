# Phase 6 Stress and Conflict Demo

## Purpose

This demo shows the Phase 6 stress path from fault lanes to pressure lanes to conflict lanes to overload lanes, then into instrumentation and usefulness scoring using real evidence files only.

## Review Path

1. Start with the plan and evidence manifest:
   - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_evidence_manifest.json`
2. Confirm the lane chain surface:
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_fault_pressure_overload_conflict_report.json`
3. Confirm the instrumentation surface:
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_instrumentation_report.json`
4. Confirm the usefulness surface:
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_usefulness_scoring_report.json`
5. Confirm the runnable demo export:
   - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_stress_conflict_demo.json`

## Testable Rerun

Run this command from repo root:

```bash
python3 projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/run_phase_06_stress_conflict_demo.py
```

What it regenerates:

- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_stress_conflict_demo.json`

## What The Evidence Shows

- The fault/pressure/conflict/overload report shows real lane entries for each step in the chain and includes forced degraded-path checks for fault overlays, pressure fail-closed behavior, conflict hold or abstain behavior, and overload non-clear behavior.
- The instrumentation report shows machine-readable records, summaries, and metrics derived from the world model, futures, simulation, and lane outputs.
- The usefulness report shows evidence-linked inputs, threshold reasoning, the low-evidence collapse check, and the rebuilt manifest status from disk.

## Exact File Anchors To Inspect

- Lane-chain anchor:
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_fault_pressure_overload_conflict_report.json`
- Instrumentation anchor:
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_instrumentation_report.json`
- Usefulness anchor:
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_usefulness_scoring_report.json`
- Runnable demo export:
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_stress_conflict_demo.json`

## What The User Should Check

- The forced degraded-path anchors show that the lane logic is exercised, not just described.
- The lane report contains reason codes and provenance links for the fault, pressure, conflict, and overload outputs.
- The instrumentation report contains coverage summary records and metric IDs tied to actual runtime outputs.
- The usefulness report is evidence-linked and still reports Phase 6 as open through the manifest.
- The machine-readable demo export contains the normal lane chain plus forced degraded-path counts as structured data.

## What Failure Would Look Like

- Any lane appears only as prose without machine-checkable output.
- The forced degraded-path checks do not exist or do not trip.
- Instrumentation is missing event coverage or provenance links.
- Usefulness scoring ignores the evidence chain or bypasses the manifest rebuild.

## Status

Phase 6 remains open.
