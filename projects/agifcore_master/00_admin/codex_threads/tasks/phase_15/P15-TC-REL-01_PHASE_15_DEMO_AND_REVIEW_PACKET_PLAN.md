# P15-TC-REL-01 Phase 15 Demo And Review Packet Plan

- Task Card ID: `P15-TC-REL-01`
- Phase: `15`
- Title: `Phase 15 demo-bundle and review-packet planning`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles:
  - `Program Governor`
  - `Test & Replay Lead`
  - `Validation Agent`
- Allowed Models: `gpt-5.4-mini`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-REL-01_PHASE_15_DEMO_AND_REVIEW_PACKET_PLAN.md`
- Forbidden Files:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 16 and later artifacts

## Objective

- Goal: define the later Phase 15 demo-bundle shape and review-packet order without leaking Phase 16 behavior
- Expected Outputs:
  - demo-bundle layout
  - review-packet order
  - later summary/demo surface list
- Non-Goals:
  - runtime logic
  - public release packaging
  - approval

## Required Reads First

- `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
- approved Phase 14 review-bundle structure
- `Test & Replay Lead` verifier and evidence plan
- `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`

## Step-by-Step Work Method

1. Define the demo bundle layout.
2. Define the real desktop chat final-demo surface.
3. Define the soak-summary review surface.
4. Define the closure-audit-summary review surface.
5. Define the user-review packet order.

## Required Cross-Checks

- demos must stay inspectable from files alone
- no demo may imply approval or public release
- no terminal-only primary demo
- no Phase 16 packaging creep

## Exit Criteria

- later review packet is exact, ordered, and bounded

## Handoff Target

- `Program Governor`
- `Validation Agent`

## Anti-Drift Rule

- Do not expand into release execution or public claims.

## Explicit Proof That No Approval Is Implied

- Demo-package planning is not acceptance.
