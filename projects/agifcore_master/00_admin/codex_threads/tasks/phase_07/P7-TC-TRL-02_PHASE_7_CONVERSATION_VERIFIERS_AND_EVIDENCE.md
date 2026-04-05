# P7-TC-TRL-02 Phase 7 Conversation Verifiers And Evidence

## Header

- Task Card ID: `P7-TC-TRL-02`
- Phase: `7`
- Title: `Phase 7 Conversation Verifiers And Evidence`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Release & Evidence Lead`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `this_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/`
  - approved Phase 6 verifier family and demo bundle

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/05_testing/phase_07_conversation_core/`
  - all files under `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_evidence/`
- Forbidden Files:
  - any Phase 8 and later artifact
  - any Phase 4, 5, or 6 file
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/`
  - `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/phase_08_*`
  - `projects/agifcore_master/04_execution/phase_09_*`

## Branch And Worktree

- Branch Name: `codex/tc-p7-tc-wcpl-02-phase-7-conversation-core-implementation`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P7-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: produce the full machine-checkable Phase 7 verifier family and evidence bundle.
- Expected Outputs:
  - verifier common fixture chain
  - eight subsystem verifiers
  - evidence manifest
- Non-Goals:
  - runtime behavior changes outside what verifier scaffolding requires
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_raw_text_intake.py`
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_question_interpretation.py`
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_support_state_logic.py`
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_self_knowledge_surface.py`
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_clarification.py`
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_utterance_planner_and_surface_realizer.py`
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_answer_contract.py`
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_anti_generic_filler.py`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - all files under `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_*.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-AUDIT-01_PHASE_7_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
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
