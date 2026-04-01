# P12-TC-VA-01: Phase 12 Validation Plan

- Task card ID: `P12-TC-VA-01`
- Role owner: `Validation Agent`
- Model tier: `gpt-5.4`
- Objective: validate the final Phase 12 planning package before user review
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-VA-01_PHASE_12_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_VALIDATION_REQUEST.md`
- Files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- Required reads first:
  - full Phase 12 draft
  - audit output
  - Governor verification output
  - validation protocol
- Step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every closure requirement has a later artifact path
  3. confirm the later demos are inspectable and truthful
  4. confirm the extra danger-zone audit and additional-human-checkpoint paths exist in the closure chain
- Required cross-checks:
  - no author and validator role collision
  - no missing review surface
  - no implied approval
- Exit criteria: review request scope is exact and inspectable
- Handoff target: `Program Governor`
- Anti-drift rule: do not author plan content or runtime behavior
- Explicit proof that no approval is implied: validation asks for review and does not mark the phase earned
