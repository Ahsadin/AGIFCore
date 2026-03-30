# P6-TC-REL-02 Phase 6 Demo Bundle

## Header

- Task Card ID: `P6-TC-REL-02`
- Phase: `6`
- Title: `Phase 6 Demo Bundle`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_evidence_manifest.json`
  - all Phase 6 evidence reports

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-REL-02_PHASE_6_DEMO_BUNDLE.md`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_demo_index.md`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_causal_simulation_demo.md`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_causal_simulation_demo.json`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_stress_conflict_demo.md`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_stress_conflict_demo.json`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any audit or validation handoff
  - all Phase 7+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `codex/tc-p6-tc-rel-02-phase-6-demo-bundle`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P6-TC-REL-02`
- Rollback Tag Name: `rollback/P6-TC-REL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: package the Phase 6 causal simulation demo and stress/conflict demo from real Phase 6 evidence only.
- Expected Outputs:
  - this task card
  - the complete Phase 6 demo bundle
- Non-Goals:
  - runtime changes
  - verifier changes
  - phase approval

## Work Method

1. Read the evidence manifest and all eight machine-readable reports.
2. Write a demo index that points to the exact evidence artifacts.
3. Write one causal simulation demo and one stress/conflict demo using only evidence-backed claims.
4. Package machine-readable demo exports produced from the real Phase 6 test runners.
5. Keep the demo inspectable, review-only, and phase-local.

## Cross-Checks

- No unsupported summary text.
- No approval language.
- No Phase 7 or Phase 8 claims.

## Exit Criteria

- All required demo markdown and machine-readable demo files exist.
- Each demo points to exact evidence paths.
- The demo bundle is ready for audit.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Demo assembly is packaging only and does not approve or complete Phase 6.
