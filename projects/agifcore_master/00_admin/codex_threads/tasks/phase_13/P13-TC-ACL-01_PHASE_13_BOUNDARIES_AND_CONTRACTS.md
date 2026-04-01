# P13-TC-ACL-01: Phase 13 Boundaries And Contracts

- Task card ID: `P13-TC-ACL-01`
- Role owner: `Architecture & Contract Lead`
- Model tier: `gpt-5.4`
- Objective: own Phase 13 boundaries, allowed interfaces, forbidden leaks, and the Phase 13 shell-contract strategy
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-ACL-01_PHASE_13_BOUNDARIES_AND_CONTRACTS.md`
- Files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- Required reads first:
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/03_design/ARCHITECTURE_OVERVIEW.md`
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
  - `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
  - `projects/agifcore_master/03_design/PUBLIC_RELEASE_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 12 plan and runtime surfaces
  - `Source Cartographer` output
- Step-by-step work method:
  1. define what belongs in each Phase 13 subsystem only
  2. define allowed lower-phase interfaces
  3. define the supplemental Phase 13 shell-contract strategy
  4. define forbidden Phase 14 and Phase 16 leaks
  5. pass runtime-family implications to `Program Governor` and `Product & Sandbox Pod Lead`
- Required cross-checks:
  - no one mixed app shell
  - no direct UI ownership of correctness
  - no gateway bypass path
  - no Phase 14 or 16 semantics
- Exit criteria: boundary rules are explicit enough to verify later
- Handoff target: `Program Governor` then `Product & Sandbox Pod Lead`
- Anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, meta-runtime, or the team
- Explicit proof that no approval is implied: boundary framing is planning truth only
