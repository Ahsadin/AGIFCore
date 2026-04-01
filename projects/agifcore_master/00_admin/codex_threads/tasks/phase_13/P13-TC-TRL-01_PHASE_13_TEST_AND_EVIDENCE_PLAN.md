# P13-TC-TRL-01: Phase 13 Test And Evidence Plan

- Task card ID: `P13-TC-TRL-01`
- Role owner: `Test & Replay Lead`
- Model tier: `gpt-5.4-mini`
- Objective: define the Phase 13 verifier, evidence, and closure-check family
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-TRL-01_PHASE_13_TEST_AND_EVIDENCE_PLAN.md`
- Files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- Required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 12 verifier and evidence families
  - the Phase 13 draft
- Step-by-step work method:
  1. define one verifier per major Phase 13 subsystem
  2. define cross-cutting gateway no-bypass, fail-closed, export-integrity, shutdown, and installer checks
  3. define evidence reports and manifest contents
  4. define end-to-end, fail-closed UX, and installer/distribution demo verification hooks
- Required cross-checks:
  - tests must verify separation between API, runner, gateway, UI, exports, shutdown, and installer
  - fail-closed paths must be machine-checkable and visible
  - exports must be trace-contract aligned
  - installer flow must prove local installability without public-release claims
- Exit criteria: later test and evidence path is decision-complete
- Handoff target: `Release & Evidence Lead` then `Program Governor`
- Anti-drift rule: do not implement runtime behavior through verifier planning
- Explicit proof that no approval is implied: verification planning does not earn the phase
