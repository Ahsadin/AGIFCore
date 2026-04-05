# P15-TC-REL-02 Phase 15 Real Desktop Chat Demo Plan

- Task Card ID: `P15-TC-REL-02`
- Phase: `15`
- Title: `Phase 15 real desktop chat demo planning`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles:
  - `Program Governor`
  - `Validation Agent`
  - `Product & Sandbox Pod Lead` consult-only
- Allowed Models: `gpt-5.4-mini`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-REL-02_PHASE_15_REAL_DESKTOP_CHAT_DEMO_PLAN.md`
- Forbidden Files:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 16 and later artifacts

## Objective

- Goal: define the real desktop chat demo plan as the canonical primary final demo host for Phase 15 user review
- Expected Outputs:
  - canonical desktop-host demo plan
  - minimum user-review view list
  - later demo script and bundle shape
- Non-Goals:
  - runtime code
  - public release packaging
  - approval

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-ACL-02_PHASE_15_LIVE_TURN_AND_CHAT_BOUNDARIES.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-TRL-04_PHASE_15_LIVE_TURN_ENGINE_AND_CHAT_VERIFICATION_PLAN.md`

## Step-by-Step Work Method

1. Define the desktop UI as the canonical primary chat host.
2. Define the minimum conversation, trace, evidence, and fail-closed views the user must inspect.
3. Define the terminal shell as secondary debug and proof only.
4. Define the later script, bundle, and review-order shape for the real desktop chat demo.

## Required Cross-Checks

- desktop UI stays presentation-only
- runtime remains the only correctness path
- no browser-first or terminal-first substitution for the primary final demo
- no Phase 16 or public packaging drift

## Exit Criteria

- the real desktop chat demo plan is decision-complete

## Handoff Target

- `Program Governor`
- `Validation Agent`

## Anti-Drift Rule

- Do not quietly turn the demo plan into host-runtime redesign.

## Explicit Proof That No Approval Is Implied

- This is a planning artifact only.
- It does not approve or close Phase 15.
