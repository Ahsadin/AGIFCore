# P13-TC-ASA-01: Phase 13 Plan Audit

- Task card ID: `P13-TC-ASA-01`
- Role owner: `Anti-Shortcut Auditor`
- Model tier: `gpt-5.4-mini`
- Objective: audit the Phase 13 planning package for fake completeness, giant-shell collapse, fake exports, fake fail-closed UX, fake installer flow, and phase-leak drift
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-ASA-01_PHASE_13_PLAN_AUDIT.md`
- Files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- Required reads first:
  - full Phase 13 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `Test & Replay Lead` evidence-plan output
  - relevant approved Phase 2 through 12 plan and runtime surfaces
- Step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one giant app shell is being passed off as design
  4. check that no approval or completion claim is implied
- Required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of any required subsystem
  - no Phase 14 or 16 behavior smuggled in
  - no empty export, fail-closed, or installer proof path
- Exit criteria: all blockers are either cleared or explicitly raised
- Handoff target: `Program Governor`
- Anti-drift rule: do not rewrite the plan instead of auditing it
- Explicit proof that no approval is implied: audit pass is not phase approval
