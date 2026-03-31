# P7-TC-REL-02 Phase 7 Demo Bundle

## Header

- Task Card ID: `P7-TC-REL-02`
- Phase: `7`
- Title: `Phase 7 Demo Bundle`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Test & Replay Lead`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `this_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/`

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_demo_bundle/`
- Forbidden Files:
  - any Phase 8 and later artifact
  - any runtime file
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/phase_08_*`

## Branch And Worktree

- Branch Name: `codex/tc-p7-tc-wcpl-02-phase-7-conversation-core-implementation`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P7-TC-REL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: package the Phase 7 messy-question, self-knowledge, and honest abstain/search-needed demos in a directly reviewable form.
- Expected Outputs:
  - runnable demo JSON files
  - matching markdown review surfaces
  - demo index
- Non-Goals:
  - phase approval
  - runtime behavior changes
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/run_phase_07_messy_question_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/run_phase_07_self_knowledge_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_07_conversation_core/run_phase_07_honest_abstain_search_needed_demo.py`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/`
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
