# P10-TC-ACL-01 Phase 10 Boundaries And Contracts

- task card ID: `P10-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 10 boundaries, allowed interfaces, forbidden leaks, and the Phase 10 overlay-contract strategy
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-ACL-01_PHASE_10_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 7, 8, and 9 plans
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-SC-01_PHASE_10_PROVENANCE_AND_REUSE.md`
- step-by-step work method:
  1. define what belongs in each Phase 10 subsystem only
  2. define allowed Phase 7, 8, and 9 interfaces
  3. define the supplemental Phase 10 overlay-contract strategy
  4. define forbidden Phase 11 and 12 leaks
  5. pass runtime-family implications to `Program Governor` and `Meta & Growth Pod Lead`
- required cross-checks:
  - no one mixed introspection engine
  - no final response-envelope ownership inside Phase 10
  - no direct mutation of Phase 7, 8, or 9 state
  - no self-improvement or structural-growth semantics
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `Meta & Growth Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, science-world, rich-expression, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only
