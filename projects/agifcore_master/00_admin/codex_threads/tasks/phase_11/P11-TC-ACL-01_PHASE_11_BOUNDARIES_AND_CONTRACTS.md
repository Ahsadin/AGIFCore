# P11-TC-ACL-01: Phase 11 Boundaries And Contracts

- Task card ID: `P11-TC-ACL-01`
- Role owner: `Architecture & Contract Lead`
- Model tier: `gpt-5.4`
- Objective: own Phase 11 boundaries, allowed interfaces, forbidden leaks, and the Phase 11 overlay-contract strategy
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-ACL-01_PHASE_11_BOUNDARIES_AND_CONTRACTS.md`
- Files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_11_GOVERNED_SELF_IMPROVEMENT.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- Required reads first:
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 10 plan and runtime surfaces
  - `Source Cartographer` output
- Step-by-step work method:
  1. define what belongs in each Phase 11 subsystem only
  2. define allowed Phase 10 interfaces
  3. define the supplemental Phase 11 overlay-contract strategy
  4. define forbidden Phase 12 and Phase 13 leaks
  5. pass runtime-family implications to `Program Governor` and `Meta & Growth Pod Lead`
- Required cross-checks:
  - no one mixed self-improvement engine
  - no direct user-facing answer ownership inside Phase 11
  - no direct mutation of Phase 10 state
  - no structural-growth or product-runtime semantics
- Exit criteria: boundary rules are explicit enough to verify later
- Handoff target: `Program Governor` then `Meta & Growth Pod Lead`
- Anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, science-world, rich-expression, critique, or the team
- Explicit proof that no approval is implied: boundary framing is planning truth only
