# P7-TC-WCPL-02 Phase 7 Conversation Core Implementation

## Header

- Task Card ID: `P7-TC-WCPL-02`
- Phase: `7`
- Title: `Phase 7 Conversation Core Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `World & Conversation Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`, `Source Cartographer`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `this_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/__init__.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/raw_text_intake.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/question_interpretation.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/support_state_logic.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/self_knowledge_surface.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/clarification.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/utterance_planner.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/surface_realizer.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/answer_contract.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/anti_generic_filler.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/conversation_turn.py`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - any Phase 8 and later artifact
  - any Phase 4, 5, or 6 runtime file
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/`
- Forbidden Folders:
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `codex/tc-p7-tc-wcpl-02-phase-7-conversation-core-implementation`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P7-TC-WCPL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the bounded Phase 7 conversation runtime exactly inside the approved phase boundary.
- Expected Outputs:
  - importable Phase 7 runtime package
  - explicit runtime separation across intake, interpretation, support-state, self-knowledge, clarification, planning, realization, contract, and anti-filler enforcement
- Non-Goals:
  - Phase 8 science or world-awareness behavior
  - Phase 9 rich-expression behavior
  - direct mutation of Phase 4, 5, or 6 state
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 7 verifier family after TRL lands
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_07_conversation_core`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_raw_text_intake.py`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_question_interpretation.py`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_support_state_logic.py`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_self_knowledge_surface.py`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_clarification.py`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_utterance_planner_and_surface_realizer.py`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_answer_contract.py`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_anti_generic_filler.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-AUDIT-01_PHASE_7_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-ACL-02_PHASE_7_BOUNDARY_CHECK.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_USER_VERDICT.md`
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
2. Implement intake and interpretation before support-state routing.
3. Implement self-knowledge, clarification, planning, realization, contract, and anti-filler layers as separate modules.
4. Keep all Phase 4, 5, and 6 dependencies read-only and schema-validated.

## Cross-Checks

- No live search execution.
- No unsupported self-knowledge.
- No answer text generation inside support-state logic.
- No Phase 8 or Phase 9 behavior.
