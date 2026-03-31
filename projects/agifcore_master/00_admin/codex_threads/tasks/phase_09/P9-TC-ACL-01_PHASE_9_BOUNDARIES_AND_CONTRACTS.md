# P9-TC-ACL-01 Phase 9 Boundaries and Contracts

- task card ID: `P9-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 9 boundaries, allowed interfaces, forbidden leaks, and the Phase 9 overlay-contract strategy
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ACL-01_PHASE_9_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 7 and Phase 8 plans
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-SC-01_PHASE_9_PROVENANCE_AND_REUSE.md`
- step-by-step work method:
  1. define what belongs in each Phase 9 subsystem only
  2. define allowed Phase 7 and Phase 8 interfaces
  3. define the supplemental Phase 9 overlay-contract strategy for inherited trace refs
  4. define forbidden Phase 10 and 11 leaks
  5. pass runtime-family implications to `Program Governor` and `World & Conversation Pod Lead`
- required cross-checks:
  - no one mixed style engine
  - no final response-envelope ownership inside Phase 9
  - no direct mutation of Phase 7 or Phase 8 state
  - no persuasion theater disguised as audience adaptation
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `World & Conversation Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only
