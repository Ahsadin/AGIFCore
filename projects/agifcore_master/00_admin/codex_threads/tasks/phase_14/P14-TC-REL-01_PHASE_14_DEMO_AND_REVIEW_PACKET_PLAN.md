# P14-TC-REL-01 Phase 14 Demo And Review Packet Plan

- Task Card ID: `P14-TC-REL-01`
- Phase: `14`
- Title: `Phase 14 demo bundle and review packet planning`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles:
  - `Test & Replay Lead`
  - `Program Governor`
  - `Validation Agent`
- Allowed Models: `gpt-5.4-mini`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-REL-01_PHASE_14_DEMO_AND_REVIEW_PACKET_PLAN.md`
- Forbidden Files:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 15 and later artifacts

## Objective

- Goal: define the later Phase 14 demo-bundle layout and review packet order
- Expected Outputs:
  - demo bundle shape
  - review packet order
  - demo inspection rules
- Non-Goals:
  - runtime implementation
  - release/publication packaging
  - approval

## Required Reads First

- `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
- approved Phase 13 demo bundle
- `P14-TC-TRL-01` output
- `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`

## Step-by-Step Work Method

1. Define the demo bundle layout.
2. Define the sandbox enforcement demo surface.
3. Define the laptop and mobile constrained demo surfaces.
4. Define the manifest audit demo surface.
5. Define the user-review packet order.

## Required Cross-Checks

- demos must stay inspectable from files alone
- no demo may imply acceptance or phase completion
- no Phase 15 or 16 packaging creep

## Exit Criteria

- later review packet is exact, ordered, and bounded

## Handoff Target

- `Program Governor`
- then `Validation Agent`

## Anti-Drift Rule

- Do not expand into release execution or public claims.

## Explicit Proof That No Approval Is Implied

- Demo-package planning is not demo acceptance and does not approve Phase 14.
