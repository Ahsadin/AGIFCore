# P9-TC-VA-01 Phase 9 Validation Plan

- task card ID: `P9-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 9 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-VA-01_PHASE_9_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - full Phase 9 draft
  - audit output
  - governor verification output
  - validation protocol
- step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every closure requirement has a later artifact path
  3. confirm the later demos are inspectable and truthful
  4. prepare the later review request only after audit and governor verification exist
- required cross-checks:
  - no author and validator role collision
  - no missing review surface
  - no implied approval
- exit criteria:
  - review request scope is exact and inspectable
- handoff target: `Program Governor`
- anti-drift rule: do not author plan content or runtime behavior
- explicit proof that no approval is implied: validation asks for review and does not mark the phase earned
