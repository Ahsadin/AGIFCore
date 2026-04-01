# P14-TC-ACL-01 Phase 14 Boundaries And Contracts

- Task Card ID: `P14-TC-ACL-01`
- Phase: `14`
- Title: `Phase 14 boundary and contract planning`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles:
  - `Program Governor`
  - `Product & Sandbox Pod Lead`
  - `Constitution Keeper`
- Allowed Models: `gpt-5.4`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-ACL-01_PHASE_14_BOUNDARIES_AND_CONTRACTS.md`
- Forbidden Files:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 15 and later artifacts

## Objective

- Goal: define what belongs in each Phase 14 subsystem, what may enter from Phase 13, and what is forbidden from Phase 15 and Phase 16
- Expected Outputs:
  - subsystem boundary rules
  - allowed-interface rules
  - forbidden-leak rules
- Non-Goals:
  - redesign of earlier phases
  - runtime implementation
  - approval

## Required Reads First

- `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
- `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
- `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- approved Phase 13 plan and runtime surfaces
- `P14-TC-SC-01` output

## Step-by-Step Work Method

1. Define what belongs in each Phase 14 subsystem only.
2. Define allowed Phase 13 interfaces.
3. Define manifest/profile/budget/proof contract strategy.
4. Define forbidden Phase 15 and 16 leaks.
5. Pass implementation-shape implications to Governor and Product & Sandbox Pod.

## Required Cross-Checks

- no giant deployment shell
- no profile-specific correctness divergence
- no sandbox-as-integrity-substitute
- no soak or release behavior inside Phase 14

## Exit Criteria

- boundary rules are explicit enough to verify later
- phase separation is machine-checkable rather than descriptive only

## Handoff Target

- `Program Governor`
- then `Product & Sandbox Pod Lead`

## Anti-Drift Rule

- Do not redesign earlier phases, runtime lanes, or the team.

## Explicit Proof That No Approval Is Implied

- Boundary framing is planning truth only and does not approve the phase.
