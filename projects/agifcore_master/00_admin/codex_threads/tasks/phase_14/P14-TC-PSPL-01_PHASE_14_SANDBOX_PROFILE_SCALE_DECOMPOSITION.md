# P14-TC-PSPL-01 Phase 14 Sandbox Profile Scale Decomposition

- Task Card ID: `P14-TC-PSPL-01`
- Phase: `14`
- Title: `Phase 14 future runtime-family decomposition`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Product & Sandbox Pod Lead`
- Supporting Roles:
  - `Architecture & Contract Lead`
  - `Source Cartographer`
  - `Constitution Keeper`
- Allowed Models: `gpt-5.3-codex`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-PSPL-01_PHASE_14_SANDBOX_PROFILE_SCALE_DECOMPOSITION.md`
- Forbidden Files:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 15 and later artifacts

## Objective

- Goal: decompose the future Phase 14 runtime family for sandbox, limits, manifests, profiles, budgets, and dormant proofs
- Expected Outputs:
  - future module family
  - execution order
  - stop/escalation points
- Non-Goals:
  - runtime code
  - verifier code
  - approval

## Required Reads First

- approved Phase 2 through Phase 13 plans and execution surfaces
- `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
- `P14-TC-SC-01` output
- `P14-TC-ACL-01` output
- `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
- `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
- `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`

## Step-by-Step Work Method

1. Define the future family under `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/`.
2. Keep the module set explicit:
   - `contracts.py`
   - `sandbox_policy.py`
   - `wasmtime_fuel_limits.py`
   - `wasmtime_memory_limits.py`
   - `wasmtime_wall_time_limits.py`
   - `cell_manifest.py`
   - `tissue_manifest.py`
   - `profile_manifests.py`
   - `active_cell_budget.py`
   - `dormant_cell_survival.py`
   - `sandbox_profile_shell.py`
3. Order implementation:
   - contracts
   - sandbox and limit families
   - manifests and profiles
   - budget enforcement
   - dormant proofs
   - thin shell
4. Identify exactly where Phase 13 runtime interfaces are consumed without mutation.

## Required Cross-Checks

- no runtime code written now
- no Phase 15 behavior
- no Phase 16 behavior
- no hidden correctness privilege
- no conflation of manifests with proof

## Exit Criteria

- future module family, execution order, and stop points are explicit

## Handoff Target

- `Program Governor`

## Anti-Drift Rule

- Do not author canonical plan truth alone and do not implement code in this run.

## Explicit Proof That No Approval Is Implied

- Decomposition planning does not earn or approve Phase 14.
