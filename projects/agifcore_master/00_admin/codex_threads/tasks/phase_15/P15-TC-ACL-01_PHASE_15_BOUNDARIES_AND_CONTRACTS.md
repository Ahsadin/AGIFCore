# P15-TC-ACL-01 Phase 15 Boundaries And Contracts

- Task Card ID: `P15-TC-ACL-01`
- Phase: `15`
- Title: `Phase 15 boundary and contract framing`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles:
  - `Program Governor`
  - `Source Cartographer`
  - `Test & Replay Lead`
- Allowed Models: `gpt-5.4`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-ACL-01_PHASE_15_BOUNDARIES_AND_CONTRACTS.md`
- Forbidden Files:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 16 and later artifacts

## Objective

- Goal: define the Phase 15 subsystem boundaries, allowed Phase 13 and 14 interfaces, live-turn repair rules, forbidden leaks, and contract strategy
- Expected Outputs:
  - explicit boundary rules
  - allowed interface list
  - forbidden Phase 16 leak list
- Non-Goals:
  - runtime code
  - verifier code
  - approval

## Required Reads First

- `projects/agifcore_master/03_design/PUBLIC_RELEASE_MODEL.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
- `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- approved Phase 13 and Phase 14 plans and outputs
- `Source Cartographer` output

## Step-by-Step Work Method

1. Define what belongs in each Phase 15 subsystem only.
2. Define the live-turn repair lane separately from the proof-pack lanes.
3. Define allowed Phase 13 interfaces and desktop host rules.
4. Define allowed Phase 14 interfaces.
5. Define forbidden Phase 16 leaks.
6. Pass proof-family implications to `Program Governor` and `Test & Replay Lead`.

## Required Cross-Checks

- no giant mixed proof harness
- no release/publication leakage
- no runtime redesign
- no second runtime
- no UI-owned correctness
- no Phase 16 semantics

## Exit Criteria

- boundary rules are explicit enough to verify later

## Handoff Target

- `Program Governor`
- `Test & Replay Lead`

## Anti-Drift Rule

- Do not redesign earlier phases or the team.

## Explicit Proof That No Approval Is Implied

- Boundary framing is planning truth only.
- It does not approve or close Phase 15.
