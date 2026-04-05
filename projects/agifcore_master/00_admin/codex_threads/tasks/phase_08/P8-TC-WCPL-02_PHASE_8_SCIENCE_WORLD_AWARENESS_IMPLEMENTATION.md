# P8-TC-WCPL-02 Phase 8 Science World Awareness Implementation

## Header

- Task Card ID: `P8-TC-WCPL-02`
- Phase: `8`
- Title: `Phase 8 Science World Awareness Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `World & Conversation Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`, `Source Cartographer`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/__init__.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/scientific_priors.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/entity_request_inference.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/world_region_selection.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/causal_chain_reasoning.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/bounded_current_world_reasoning.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/visible_reasoning_summaries.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/science_reflection.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/science_world_turn.py`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - any Phase 9 and later artifact
  - any Phase 4, 5, 6, or 7 runtime file
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/`
- Forbidden Folders:
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P8-TC-WCPL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the bounded Phase 8 science and world-awareness runtime exactly inside the approved phase boundary.
- Expected Outputs:
  - importable Phase 8 runtime package
  - explicit runtime separation across priors, inference, region selection, causal reasoning, current-world boundedness, visible reasoning, reflection, and the thin coordinator
- Non-Goals:
  - Phase 9 rich-expression behavior
  - Phase 10 meta-cognition behavior
  - direct mutation of Phase 4, 5, 6, or 7 state
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 8 verifier family after TRL lands
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_08_science_and_world_awareness`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_scientific_priors.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_entity_request_inference.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_world_region_selection.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_causal_chain_reasoning.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_bounded_current_world_reasoning.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_visible_reasoning_summaries.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_science_reflection.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-AUDIT-01_PHASE_8_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
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

1. Build the typed contract surface first.
2. Implement scientific priors and entity/request inference before world-region selection.
3. Implement causal-chain reasoning before bounded current-world reasoning.
4. Implement visible reasoning summaries and science reflection after the reasoning layers exist.
5. Keep all Phase 4, 5, 6, and 7 dependencies read-only and schema-validated.

## Cross-Checks

- No live external search execution.
- No unsupported exact current-fact claims.
- No visible reasoning summary as chain-of-thought theater.
- No prose-only causal chains.
- No Phase 9 or Phase 10 behavior.
