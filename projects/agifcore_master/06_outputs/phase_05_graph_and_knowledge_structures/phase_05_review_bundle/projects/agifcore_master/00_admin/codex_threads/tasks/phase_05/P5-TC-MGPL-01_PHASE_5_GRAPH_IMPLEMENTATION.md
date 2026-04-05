# P5-TC-MGPL-01 Phase 5 Graph Implementation

## Header

- Task Card ID: `P5-TC-MGPL-01`
- Phase: `5`
- Title: `Phase 5 Graph Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Memory & Graph Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md`
  - approved Phase 2, 3, and 4 runtime surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/__init__.py`
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/descriptor_graph.py`
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/skill_graph.py`
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/concept_graph.py`
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/transfer_graph.py`
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/provenance_links.py`
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/conflict_rules.py`
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/supersession_rules.py`
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/support_selection.py`
- Forbidden Files:
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/`
- Forbidden Folders:
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`
  - any Phase 6+ execution family

## Branch And Worktree

- Branch Name: `codex/tc-p5-tc-mgpl-01-phase-5-graph-implementation`
- Worktree Path: `.worktrees/P5-TC-MGPL-01`
- Rollback Tag Name: `rollback/P5-TC-MGPL-01/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the full Phase 5 runtime package with real distinct graph layers, real provenance enforcement, and real conflict, supersession, and support-selection behavior.
- Expected Outputs:
  - all required Phase 5 runtime files
- Non-Goals:
  - verifier implementation
  - evidence generation
  - demo markdown authoring
  - Phase 6 or Phase 7 behavior
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - the full Phase 5 verifier family after TRL lands
- Required Build Commands:
  - scoped Python import sanity only if needed
- Required Verifier Paths:
  - full `verify_phase_05_*` family under `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/`
- Required Evidence Output Paths:
  - full `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/` family
- Required Demo Path:
  - full `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/`

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

1. Build four distinct graph layers with clear boundaries even if implementation shares support types.
2. Implement provenance links with machine-checkable enforcement fields, not labels.
3. Implement explicit conflict and supersession behavior with real state transitions.
4. Implement reusable support selection through graph evidence, provenance, trust, and utility bounds.
5. Keep world-model, simulator, and conversation behavior out of the package.

## Cross-Checks

- No one giant undifferentiated graph.
- No fake provenance links.
- No prose-only conflict or supersession rules.
- No support-selection bypass around graph evidence.
- No Phase 6 or Phase 7 drift.
- No approval implied.
