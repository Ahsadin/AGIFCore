# P5-TC-PG-02 Phase 5 Execution Control

## Header

- Task Card ID: `P5-TC-PG-02`
- Phase: `5`
- Title: `Phase 5 Execution Control`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Architecture & Contract Lead`, `Test & Replay Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `not_assigned`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-PG-02_PHASE_5_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_EXECUTION_START_BRIEF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_GOVERNOR_VERIFICATION_RECORD.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p5-tc-pg-02-phase-5-execution-startup`
- Worktree Path: `.worktrees/P5-TC-PG-02`
- Rollback Tag Name: `rollback/P5-TC-PG-02/<yyyymmdd-hhmm>`

## Objective

- Goal: control the full Phase 5 execution chain without letting phase truth drift or later-phase scope leak in.
- Expected Outputs:
  - this task card
  - the required Phase 5 handoff records when execution reaches those gates
- Non-Goals:
  - runtime implementation
  - verifier implementation
  - evidence generation
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `only if provenance ambiguity appears`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 5 verifier family after TRL lands
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_descriptor_graph.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_skill_graph.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_concept_graph.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_transfer_graph.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_provenance_links.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_conflict_and_supersession.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_support_selection.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-AUDIT-01_PHASE_5_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_USER_VERDICT.md`
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

1. Keep Phase 5 status truthful as `open` throughout execution.
2. Open and maintain task cards before any runtime code and before any verifier or evidence pass.
3. Require build, verifier, evidence, audit, and verification loops to complete before the final review request.
4. Stop only when the full Phase 5 package is ready for final user review.

## Cross-Checks

- No Phase 6 start.
- No Phase 7 behavior.
- No phase approval implied.
- No report text accepted as proof by itself.
