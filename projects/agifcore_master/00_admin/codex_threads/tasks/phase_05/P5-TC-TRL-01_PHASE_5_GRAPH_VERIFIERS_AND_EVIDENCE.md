# P5-TC-TRL-01 Phase 5 Graph Verifiers And Evidence

## Header

- Task Card ID: `P5-TC-TRL-01`
- Phase: `5`
- Title: `Phase 5 Graph Verifiers And Evidence`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4 mini`
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
  - approved Phase 4 verifier and evidence surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_descriptor_graph.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_skill_graph.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_concept_graph.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_transfer_graph.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_provenance_links.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_conflict_and_supersession.py`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/verify_phase_05_support_selection.py`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_descriptor_graph_report.json`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_skill_graph_report.json`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_concept_graph_report.json`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_transfer_graph_report.json`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_provenance_links_report.json`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_conflict_and_supersession_report.json`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_support_selection_report.json`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - demo bundle markdown files until Release & Evidence Lead is activated
  - all Phase 6+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `codex/tc-p5-tc-trl-01-phase-5-graph-verifiers`
- Worktree Path: `.worktrees/P5-TC-TRL-01`
- Rollback Tag Name: `rollback/P5-TC-TRL-01/<yyyymmdd-hhmm>`

## Objective

- Goal: implement and run the full Phase 5 verifier family and produce honest machine-readable evidence for every required graph surface.
- Expected Outputs:
  - full Phase 5 verifier family
  - full Phase 5 evidence family
- Non-Goals:
  - runtime implementation
  - final demo markdown bundle
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - every `verify_phase_05_*` file under `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/`
- Required Build Commands:
  - `python3` verifier runs only
- Required Verifier Paths:
  - full `verify_phase_05_*` family
- Required Evidence Output Paths:
  - full `phase_05_evidence/` family
- Required Demo Path:
  - handoff to Release & Evidence Lead at end of phase

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

1. Build one verifier per required Phase 5 subsystem group.
2. Run real checks against the runtime package.
3. Generate machine-readable evidence only from actual verifier results.
4. Keep evidence honest, phase-local, and inspectable.

## Cross-Checks

- No empty reports.
- No report text alone as proof.
- No runtime implementation in this lane.
- No approval implied.
