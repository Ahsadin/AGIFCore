# P8-TC-ACL-02 Phase 8 Boundary Check

## Header

- Task Card ID: `P8-TC-ACL-02`
- Phase: `8`
- Title: `Phase 8 Boundary Check`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Constitution Keeper`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
- Forbidden Files:
  - any runtime, testing, or output file
  - any Phase 9 and later artifact
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P8-TC-ACL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: verify that the implemented Phase 8 package stays inside the approved boundaries.
- Expected Outputs:
  - this boundary check record
- Non-Goals:
  - runtime implementation
  - verifier implementation
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `only if donor ambiguity appears`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 8 verifier family after implementation lands
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-AUDIT-01_PHASE_8_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `Merge Arbiter`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined

## Work Method

1. Verify subsystem boundaries against the approved Phase 8 plan.
2. Confirm only allowed Phase 6 and Phase 7 interfaces are consumed.
3. Check that no Phase 9 or Phase 10 behavior leaked into the runtime.
4. Record concrete drift findings or an explicit no-drift result.

## Cross-Checks

- No one mixed reasoning function.
- No final response generation inside Phase 8.
- No direct mutation of Phase 6 or Phase 7 state.
- No hidden-thought disclosure disguised as visible reasoning.
