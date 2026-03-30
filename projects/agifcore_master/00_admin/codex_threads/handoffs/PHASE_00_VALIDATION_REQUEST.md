# Validation Request

- Task Card ID: `P0-TC-VA-01`
- Phase: `0`
- Validation Agent: `Validation Agent`
- Date: `2026-03-29`

## What The User Should Review

- Demo Path:
  - `projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md`
  - `projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md`
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Exact Behavior To Check:
  - confirm the `project structure` review surface truthfully shows the current scaffold, planning skeletons, placeholder state, and the canonical versus noncanonical Phase 0 naming state
  - confirm the `archival statement` review surface clearly states that AGIF v2 is historical source only and does not count as AGIFCore progress
  - confirm the `source-freeze method` review surface lists exactly the four frozen source pools, defines the allowed dispositions, and requires reopen governance for any new source pool
- What Good Looks Like:
  - the review uses only the canonical Phase 0 artifact names
  - the archival statement has no loophole that would let AGIF v2 count as completed AGIFCore work
  - the source-freeze inventory and method are concrete enough to constrain later Phase 1 provenance work
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` still shows Phase 0 as `open` pending your explicit verdict
- What Failure Looks Like:
  - the structure audit hides missing files, placeholder state, or the noncanonical draft-input state
  - the archival note is vague, reversible, or allows shortcut completion claims
  - the source-freeze artifacts omit a source pool, omit the disposition rule, or omit the reopen rule
  - the checklist implies approval before your verdict exists

## Supporting Evidence

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-AUDIT-01_PHASE_0_ARTIFACT_AUDIT_REPORT.md`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_GOVERNOR_VERIFICATION_RECORD.md`
- Verifier Output Paths:
  - direct file checks recorded in `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_GOVERNOR_VERIFICATION_RECORD.md`
- Evidence JSON Paths:
  - `none`

## Review Questions

1. Does `projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md` accurately describe the current Phase 0 scaffold and clearly separate canonical Phase 0 artifacts from the older `PHASE_00_*` draft inputs?
2. Does `projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md` clearly state that AGIF v2 is historical source only and blocks shortcut completion claims?
3. Do `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md` and `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md` define a complete and usable source-freeze boundary for later Phase 1 provenance work?

## Requested User Verdict

- `approved`
- `rejected`
- `approved_with_blockers`
