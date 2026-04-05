# P15-TC-TRL-04 Phase 15 Live Turn Engine And Chat Verification Plan

- Task Card ID: `P15-TC-TRL-04`
- Phase: `15`
- Title: `Phase 15 live-turn engine and chat verification planning`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles:
  - `Program Governor`
  - `Release & Evidence Lead`
  - `Anti-Shortcut Auditor`
- Allowed Models: `gpt-5.4-mini`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-TRL-04_PHASE_15_LIVE_TURN_ENGINE_AND_CHAT_VERIFICATION_PLAN.md`
- Forbidden Files:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 16 and later artifacts

## Objective

- Goal: define the live-turn engine, broad question-class proof, follow-up continuity proof, selective phase-usage proof, and real desktop chat demo verification plan
- Expected Outputs:
  - broad prompt matrix
  - per-turn evidence field list
  - live-turn and desktop-demo verifier plan
- Non-Goals:
  - runtime code
  - fabricated reports
  - approval

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
- donor Phase 9 open-question runtime proof files
- `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`

## Step-by-Step Work Method

1. Define the broad prompt matrix across all required question classes.
2. Define per-turn evidence fields, including target grounding and actual phases exercised.
3. Define follow-up continuity proof requirements.
4. Define current-world target-grounding and bounded-estimate proof requirements.
5. Define the real desktop chat demo verifier and failure signatures.

## Required Cross-Checks

- no generic fallback dominating the prompt matrix
- no over-reported phase usage
- no exact-prompt-only success criteria
- no terminal-only demo acceptance path

## Exit Criteria

- live-turn and chat verification plan is decision-complete

## Handoff Target

- `Release & Evidence Lead`
- `Program Governor`

## Anti-Drift Rule

- Do not hide runtime design decisions inside a test plan.

## Explicit Proof That No Approval Is Implied

- This is proof planning only.
- It does not approve or close Phase 15.
