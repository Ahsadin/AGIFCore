# P14-TC-ACL-02 Phase 14 Manifest Strengthening Boundary

## Header

- Task Card ID: `P14-TC-ACL-02`
- Phase: `14`
- Title: `Phase 14 Manifest Strengthening Boundary`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Product & Sandbox Pod Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `separate_architecture_thread_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/contracts.py`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/cell_manifest.py`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/tissue_manifest.py`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/active_cell_budget.py`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/dormant_cell_survival.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-ACL-02_PHASE_14_MANIFEST_STRENGTHENING_BOUNDARY.md`
- Forbidden Files:
  - `projects/agifcore_master/04_execution/*`
  - `projects/agifcore_master/05_testing/*`
  - `projects/agifcore_master/06_outputs/*`
  - all Phase 15 and later artifacts

## Branch And Worktree

- Branch Name: `codex/tc-p13-tc-pg-03-phase-13-closeout`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P14-TC-ACL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: define the minimum stronger manifest semantics that make family differentiation, tissue specialization, exemplar structure, and constraint diversity real and machine-checkable without broadening Phase 14.
- Expected Outputs:
  - one boundary note with explicit required fields and stop points
- Non-Goals:
  - runtime implementation
  - verifier implementation
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `n/a`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - hand off to `Test & Replay Lead`
- Required Evidence Output Paths:
  - hand off to `Program Governor`
- Required Demo Path:
  - hand off to `Release & Evidence Lead`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-AUDIT-01_PHASE_14_FINAL_PACKAGE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_USER_VERDICT.md`

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

1. Define only fields that affect validation, routing, budget, sandbox, dormancy, continuity, or audit behavior.
2. Keep literal `1024` cells and literal `32` tissues unless a real blocker forces correction.
3. Do not turn Phase 14 into Phase 15 proof work.

## Minimum Strengthening Semantics

- Required cell-level fields:
  - `allowed_actions` and `forbidden_actions`
  - `activation_budget_class` and `activation_priority`
  - `export_visibility_class`
  - `dormancy_behavior_class`
  - `continuity_requirement_class`
  - `evidence_requirement_class`
  - `sandbox_policy_class`
  - `exemplar_class_id`
  - `contract_variant`
- Required tissue-level fields:
  - `specialization_tag`
  - `tissue_focus`
  - `preferred_routing_targets_by_profile`
  - `activation_priority_by_profile`
  - `allowed_family_mix`
  - `continuity_handling_class`
  - `evidence_lane`
  - profile-specific active caps that are allowed to differ by tissue variant
- Required stop points:
  - keep literal `1024` cells
  - keep literal `32` tissues
  - keep existing Phase 14 public/runtime boundaries
  - do not add hand-written bespoke behavior for all `1024` cells
  - do not require lower-phase runtime redesign

## Forbidden Shortcuts

- No decorative metadata that does not affect runtime logic or validation.
- No random tags, lorem-style labels, or fake diversity fields.
- No verifier weakening or removal of existing checks.
- No hiding differentiation only in prose; it must appear in machine-readable evidence.
- No Phase 15 closure-proof, soak, hidden-pack, or publication behavior.
- Stop if the only way forward is to change Phase 14 counts, bypass review evidence, or start Phase 15 work.

## Cross-Checks

- No decorative metadata.
- No Phase 15 leak.
- No approval implied.
