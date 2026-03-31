# P10-TC-SC-01 Phase 10 Provenance And Reuse

- task card ID: `P10-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4-mini`
- objective: map every major Phase 10 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-SC-01_PHASE_10_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 7, 8, and 9 plans and execution surfaces
  - inspected donor Phase 8C and Phase 9 real-runtime files
- step-by-step work method:
  1. map all ten Phase 10 subsystems
  2. assign one allowed disposition to each subsystem
  3. flag where exact record inheritance is stronger than runtime portability
  4. pass unresolved seam notes to `Architecture & Contract Lead` and `Program Governor`
- required cross-checks:
  - no fifth disposition
  - no silent omission
  - no treating historical packages as earned AGIFCore runtime
- exit criteria:
  - each subsystem has source basis, disposition, and rationale
- handoff target: `Architecture & Contract Lead` then `Program Governor`
- anti-drift rule: do not claim inspected historical code is already valid AGIFCore runtime
- explicit proof that no approval is implied: provenance mapping does not earn the phase
