# P13-TC-SC-01: Phase 13 Provenance And Reuse

- Task card ID: `P13-TC-SC-01`
- Role owner: `Source Cartographer`
- Model tier: `gpt-5.4-mini`
- Objective: map every major Phase 13 subsystem to source basis, disposition, and reuse limits
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-SC-01_PHASE_13_PROVENANCE_AND_REUSE.md`
- Files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- Required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 2 through 12 plans and execution surfaces
  - inspected donor product-runtime and installer files
- Step-by-step work method:
  1. map all ten Phase 13 subsystems
  2. assign one allowed disposition to each subsystem
  3. flag where exact contract inheritance is stronger than whole-shell portability
  4. pass unresolved seam notes to `Architecture & Contract Lead` and `Program Governor`
- Required cross-checks:
  - no fifth disposition
  - no silent omission
  - no treating donor shells as earned AGIFCore runtime
- Exit criteria: each subsystem has source basis, disposition, and rationale
- Handoff target: `Architecture & Contract Lead` then `Program Governor`
- Anti-drift rule: do not claim inspected donor code is already valid AGIFCore runtime
- Explicit proof that no approval is implied: provenance mapping does not earn the phase
