# Task Card

## Header

- Task Card ID: `P15-TC-PG-03`
- Phase: `15`
- Title: `Bounded intelligence closeout setup`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-04-03`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `architecture_contract`, `test_replay`, `release_evidence`
- Allowed Models: `gpt-5.4`, `gpt-5.4-mini`
- Build Pod Agent Session ID: `governor-main-thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/AGIFCORE_BOUNDED_INTELLIGENCE_CLAIM_BOUNDARY.md`
  - `projects/agifcore_master/01_plan/PHASE_16_BOUNDED_RELEASE_AND_PUBLICATION.md`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/BOUNDED_INTELLIGENCE_GATE_SPEC.md`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/bounded_intelligence_benchmark.json`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/06_outputs/*`
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/06_outputs/`
  - `.codex/`

## Branch And Worktree

- Branch Name: `current-thread`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `not_created`

## Objective

- Goal:
  - materialize the bounded claim-boundary and bounded-intelligence gate scaffolding without running the gate or changing runtime behavior
- Expected Outputs:
  - bounded claim-boundary document
  - bounded Phase 16 release/publication plan
  - bounded gate spec
  - frozen `50`-prompt benchmark
  - executable gate verifier
  - decisions and changelog entries
- Non-Goals:
  - no gate execution
  - no runtime tuning
  - no phase closure
  - no commit
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 -m compileall projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
- Required Build Commands:
  - `none`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_failure_summary.json`
- Required Demo Path:
  - `none in this setup pass`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-AUDIT-01_PHASE_15_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `none`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_VALIDATION_REQUEST.md`
- User Verdict Path:
  - `not applicable in this setup pass`
- Additional Human Demo Checkpoint Path:
  - `not applicable in this setup pass`

## Approval Chain

- Auditor: `anti_shortcut_auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `ahsadin`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was planned
- demo path remains unchanged
- rollback path is defined
