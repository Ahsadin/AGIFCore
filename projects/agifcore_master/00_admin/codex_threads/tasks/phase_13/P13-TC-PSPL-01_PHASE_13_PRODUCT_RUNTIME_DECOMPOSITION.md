# P13-TC-PSPL-01: Phase 13 Product Runtime Decomposition

- Task card ID: `P13-TC-PSPL-01`
- Role owner: `Product & Sandbox Pod Lead`
- Model tier: `gpt-5.3-codex`
- Objective: decompose the future Phase 13 product-runtime family without crossing into Phase 14 or Phase 16
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-PSPL-01_PHASE_13_PRODUCT_RUNTIME_DECOMPOSITION.md`
- Files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- Required reads first:
  - approved Phase 2 through 12 plans and execution surfaces
  - the Phase 13 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
- Step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/`
  2. keep the module set explicit:
     - `contracts.py`
     - `embeddable_runtime_api.py`
     - `local_runner.py`
     - `local_gateway.py`
     - `desktop_ui.py`
     - `state_export.py`
     - `trace_export.py`
     - `memory_review_export.py`
     - `safe_shutdown.py`
     - `fail_closed_ux.py`
     - `installer_distribution.py`
     - `product_runtime_shell.py`
  3. order implementation so contracts come first, then runner and API, then gateway, then exports, then shutdown, then fail-closed UX, then desktop UI, then installer/distribution, and the thin shell last
  4. identify where lower-phase exports and runner inputs must be consumed without mutation
- Required cross-checks:
  - no runtime code written now
  - no Phase 14 behavior
  - no Phase 16 behavior
  - no hidden autonomy or hidden correctness path
- Exit criteria: future module family, execution order, and stop points are explicit
- Handoff target: `Program Governor`
- Anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- Explicit proof that no approval is implied: execution decomposition does not earn the phase
