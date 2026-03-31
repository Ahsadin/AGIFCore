# P9-TC-TRL-01 Phase 9 Test and Evidence Plan

- task card ID: `P9-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4 mini`
- objective: define the Phase 9 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-TRL-01_PHASE_9_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 8 verifier and evidence families
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
- step-by-step work method:
  1. define one verifier per major Phase 9 subsystem
  2. define cross-cutting anti-shortcut and non-generic quality checks
  3. define evidence reports and manifest contents
  4. define failure signatures for each closure requirement
- required cross-checks:
  - tests must verify separation between teaching, comparison, planning, synthesis, analogy, composition, and audience-quality
  - analogy and composition outputs must have machine-checkable trace refs
  - synthesis must preserve support-state honesty
  - audience-aware explanation quality must stay clarity-oriented rather than persuasive
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase
