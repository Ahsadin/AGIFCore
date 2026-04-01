# P12-TC-ACL-01: Phase 12 Boundaries And Contracts

- Task card ID: `P12-TC-ACL-01`
- Role owner: `Architecture & Contract Lead`
- Model tier: `gpt-5.4`
- Objective: own Phase 12 boundaries, allowed interfaces, forbidden leaks, and the Phase 12 overlay-contract strategy
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-ACL-01_PHASE_12_BOUNDARIES_AND_CONTRACTS.md`
- Files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- Required reads first:
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 11 plan and runtime surfaces
  - `Source Cartographer` output
- Step-by-step work method:
  1. define what belongs in each Phase 12 subsystem only
  2. define allowed Phase 11 interfaces
  3. define the supplemental Phase 12 overlay-contract strategy
  4. define forbidden Phase 13 and Phase 14 leaks
  5. pass runtime-family implications to `Program Governor` and `Meta & Growth Pod Lead`
- Required cross-checks:
  - no one mixed structural-growth engine
  - no direct user-facing answer ownership inside Phase 12
  - no direct mutation of Phase 11 state
  - no product-runtime or sandbox/profile semantics
- Exit criteria: boundary rules are explicit enough to verify later
- Handoff target: `Program Governor` then `Meta & Growth Pod Lead`
- Anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, science-world, rich-expression, critique, self-improvement, or the team
- Explicit proof that no approval is implied: boundary framing is planning truth only
