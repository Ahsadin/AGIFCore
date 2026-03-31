# P10-TC-TRL-01 Phase 10 Test And Evidence Plan

- task card ID: `P10-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4-mini`
- objective: define the Phase 10 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-TRL-01_PHASE_10_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 9 verifier and evidence families
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
- step-by-step work method:
  1. define one verifier per major Phase 10 subsystem
  2. define cross-cutting contradiction, weak-answer diagnosis, and honesty checks
  3. define evidence reports and manifest contents
  4. define the extra Meta & Growth danger-zone audit hook surfaces
- required cross-checks:
  - tests must verify separation between all ten Phase 10 subsystems
  - weak-answer diagnosis must preserve support-state honesty
  - contradiction handling must be typed and evidence-linked
  - no verifier may accept prose-only introspection as success
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase
