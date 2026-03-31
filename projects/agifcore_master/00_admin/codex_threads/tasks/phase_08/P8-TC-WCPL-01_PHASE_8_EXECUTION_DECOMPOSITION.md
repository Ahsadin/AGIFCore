# Task Card

## Header

- Task Card ID: `P8-TC-WCPL-01`
- Phase: `8`
- Title: `Phase 8 Execution Decomposition`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `World & Conversation Pod Lead`
- Supporting Roles:
  - `Architecture & Contract Lead`
  - `Source Cartographer`
  - `Constitution Keeper`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `separate-session-required`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `separate-session-required`
- Required Reads:
  - approved Phase 2 to 7 plans and execution surfaces
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-SC-01_PHASE_8_PROVENANCE_AND_REUSE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-01_PHASE_8_BOUNDARIES_AND_CONTRACTS.md`
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-WCPL-01_PHASE_8_EXECUTION_DECOMPOSITION.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-pg-01-phase-8-plan`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P8-TC-WCPL-01/20260331-0000`

## Objective

- Goal:
  - decompose the future Phase 8 runtime family without crossing into Phase 9 or Phase 10
- Expected Outputs:
  - future runtime family path
  - explicit module set
  - ordered implementation sequence
  - read-only dependency map to Phase 4, Phase 5, Phase 6, and Phase 7 exports
- Non-Goals:
  - writing runtime code
  - broadening into Phase 9 or Phase 10
  - authoring canonical plan truth alone
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none
- Required Build Commands:
  - none
- Required Verifier Paths:
  - later `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
- Required Evidence Output Paths:
  - later `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Required Demo Path:
  - later `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_demo_index.md`

## Handoff Records

- Audit Report Path:
  - later `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ASA-01_PHASE_8_PLAN_AUDIT.md`
- Extra Audit Report Path:
  - `n/a`
- Governor Verification Record Path:
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md`
- User Verdict Path:
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path:
  - later `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_demo_index.md`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- future runtime family is explicit
- module set is explicit
- implementation order is explicit
- read-only Phase 4, 5, 6, and 7 dependency seams are explicit
- no runtime code is written
- rollback path is defined

## Work Method

1. define the future runtime family under `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/`
2. keep the module set explicit: `contracts.py`, `scientific_priors.py`, `entity_request_inference.py`, `world_region_selection.py`, `causal_chain_reasoning.py`, `bounded_current_world_reasoning.py`, `visible_reasoning_summaries.py`, `science_reflection.py`, `science_world_turn.py`
3. order module implementation so contracts and scientific priors come first, then entity/request inference, then world-region selection, then causal-chain reasoning, then bounded current-world reasoning, then visible reasoning summaries, then science reflection, and the thin coordinator last
4. identify where Phase 4, Phase 5, Phase 6, and Phase 7 exports must be consumed read-only

## Cross-Checks

- no runtime code written now
- no Phase 9 rich-expression behavior
- no Phase 10 meta-cognition behavior
- no live search execution

## Exit Criteria

- future module family, execution order, and stop points are explicit

## Handoff Target

`Program Governor`

## No Approval Implied

Execution decomposition does not earn the phase.
