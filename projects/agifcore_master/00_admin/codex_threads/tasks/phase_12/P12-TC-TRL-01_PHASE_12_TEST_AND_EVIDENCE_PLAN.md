# P12-TC-TRL-01: Phase 12 Test And Evidence Plan

- Task card ID: `P12-TC-TRL-01`
- Role owner: `Test & Replay Lead`
- Model tier: `gpt-5.4-mini`
- Objective: define the Phase 12 verifier, evidence, and closure-check family
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-TRL-01_PHASE_12_TEST_AND_EVIDENCE_PLAN.md`
- Files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- Required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 11 verifier and evidence families
  - the Phase 12 draft
- Step-by-step work method:
  1. define one verifier per major Phase 12 subsystem
  2. define cross-cutting reorganization, domain-genesis, theory-growth, procedure-invention, curiosity, rollback, and honesty checks
  3. define evidence reports and manifest contents
  4. define the extra Meta & Growth danger-zone audit hook surfaces and the additional human checkpoint evidence
- Required cross-checks:
  - tests must verify separation between all seven Phase 12 subsystems
  - reorganization must be machine-checkable and rollback-linked
  - domain genesis must stay candidate-bound and non-sprawling
  - theory formation must be falsifiable and evidence-linked
  - curiosity/gap selection must stay bounded and local
- Exit criteria: later test and evidence path is decision-complete
- Handoff target: `Release & Evidence Lead` then `Program Governor`
- Anti-drift rule: do not implement runtime behavior through verifier planning
- Explicit proof that no approval is implied: verification planning does not earn the phase
