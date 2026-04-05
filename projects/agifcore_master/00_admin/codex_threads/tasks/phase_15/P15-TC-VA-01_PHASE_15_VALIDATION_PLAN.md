# P15-TC-VA-01 Phase 15 Validation Plan

- Task Card ID: `P15-TC-VA-01`
- Phase: `15`
- Title: `Phase 15 planning-package validation preparation`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Validation Agent`
- Supporting Roles:
  - `Program Governor`
  - `Anti-Shortcut Auditor`
- Allowed Models: `gpt-5.4`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-VA-01_PHASE_15_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_VALIDATION_REQUEST.md`
- Forbidden Files:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 16 and later artifacts

## Objective

- Goal: validate the final Phase 15 planning package before user review, including the live-turn repair gap and the real desktop demo path
- Expected Outputs:
  - validation checklist
  - later validation-request surface definition
- Non-Goals:
  - plan authoring
  - runtime authoring
  - approval

## Required Reads First

- full Phase 15 draft
- audit output
- Governor verification output
- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`

## Step-by-Step Work Method

1. Confirm the plan is decision-complete.
2. Confirm every closure requirement has a later artifact path.
3. Confirm later demos are inspectable and truthful.
4. Confirm the live-turn repair gap is explicitly owned rather than hand-waved.
5. Confirm the primary final demo path is a real desktop UI chat host rather than a terminal-only shell.
6. Confirm role separation and review-surface completeness.

## Required Cross-Checks

- no author/validator collision
- no missing review surface
- no implied approval
- no fake "real chat" claim without a non-terminal host path

## Exit Criteria

- review request scope is exact and inspectable

## Handoff Target

- `Program Governor`

## Anti-Drift Rule

- Do not author plan content or runtime behavior.

## Explicit Proof That No Approval Is Implied

- Validation asks for review only.
- It does not approve or close Phase 15.
