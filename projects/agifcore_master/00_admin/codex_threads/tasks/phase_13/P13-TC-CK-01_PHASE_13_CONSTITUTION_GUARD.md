# P13-TC-CK-01: Phase 13 Constitution Guard

- Task card ID: `P13-TC-CK-01`
- Role owner: `Constitution Keeper`
- Model tier: `gpt-5.4-mini`
- Objective: guard constitution, fail-closed discipline, and Phase 13 product-shell boundaries
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-CK-01_PHASE_13_CONSTITUTION_GUARD.md`
- Files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- Required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - the Phase 13 draft
- Step-by-step work method:
  1. check that product surfaces stay evidence-bound and fail-closed
  2. check that gateway and UI do not become hidden cognition lanes
  3. check that Phase 13 stays below Phase 14 and Phase 16
  4. report any boundary drift to `Program Governor`
- Required cross-checks:
  - no hidden-model loophole
  - no silent degrade path
  - no unsafe installer magic
  - no Phase 14 or 16 behavior
  - no approval language
- Exit criteria: constitutional objections are resolved or explicitly raised as blockers
- Handoff target: `Program Governor`
- Anti-drift rule: do not author runtime design or implementation
- Explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval
