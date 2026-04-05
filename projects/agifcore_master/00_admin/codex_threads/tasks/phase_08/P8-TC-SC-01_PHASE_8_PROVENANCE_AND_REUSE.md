# Task Card

## Header

- Task Card ID: `P8-TC-SC-01`
- Phase: `8`
- Title: `Phase 8 Provenance And Reuse`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Source Cartographer`
- Supporting Roles:
  - `Program Governor`
  - `Constitution Keeper`
- Allowed Models: `gpt-5.4 mini`, `gpt-5.4 nano` utility helpers only
- Build Pod Agent Session ID: `separate-session-required`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `separate-session-required`
- Required Reads:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 6 and Phase 7 plans
  - inspected legacy Phase 8B, Phase 8C, and Phase 9 source files
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-SC-01_PHASE_8_PROVENANCE_AND_REUSE.md`
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
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P8-TC-SC-01/20260331-0000`

## Objective

- Goal:
  - map every major Phase 8 subsystem to source basis, disposition, and reuse limits
- Expected Outputs:
  - subsystem-to-source mapping
  - one allowed disposition per subsystem
  - explicit reuse limits and unresolved seam notes
- Non-Goals:
  - claiming historical code is already valid AGIFCore runtime
  - implementation work
  - audit or validation work
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `n/a`
- Required Evidence Output Paths:
  - `n/a`
- Required Demo Path:
  - `n/a`

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
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scientific priors are mapped
- entity/request inference is mapped
- world-region selection is mapped
- causal-chain reasoning is mapped
- bounded current-world reasoning is mapped
- visible reasoning summaries are mapped
- science reflection is mapped
- rollback path is defined

## Work Method

1. map scientific priors, entity/request inference, world-region selection, causal-chain reasoning, bounded current-world reasoning, visible reasoning summaries, and science reflection
2. assign one allowed disposition to each subsystem
3. flag where v2 remains a strong substrate and where v1 remains research-only lineage rather than runtime donor
4. pass unresolved seam notes to `Architecture & Contract Lead` and `Program Governor`

## Cross-Checks

- no fifth disposition
- no silent omission
- no treating old packages as earned AGIFCore runtime

## Exit Criteria

- each subsystem has source basis, disposition, and rationale

## Handoff Target

`Architecture & Contract Lead` then `Program Governor`

## No Approval Implied

Provenance mapping does not earn the phase.
