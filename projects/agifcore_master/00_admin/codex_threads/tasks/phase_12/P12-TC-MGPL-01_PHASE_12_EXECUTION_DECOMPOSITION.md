# P12-TC-MGPL-01: Phase 12 Execution Decomposition

- Task card ID: `P12-TC-MGPL-01`
- Role owner: `Meta & Growth Pod Lead`
- Model tier: `gpt-5.3-codex`
- Objective: decompose the future Phase 12 runtime family without crossing into Phase 13 or Phase 14
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-MGPL-01_PHASE_12_EXECUTION_DECOMPOSITION.md`
- Files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- Required reads first:
  - approved Phase 2 through 11 plans and execution surfaces
  - the Phase 12 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/03_design/CELL_FAMILIES.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md`
- Step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/`
  2. keep the module set explicit:
     - `contracts.py`
     - `self_model_feedback.py`
     - `reflection_control.py`
     - `curiosity_gap_selection.py`
     - `theory_formation.py`
     - `procedure_tool_invention.py`
     - `self_reorganization.py`
     - `domain_genesis.py`
     - `structural_growth_cycle.py`
  3. order implementation so contracts and interface adapters come first, then self-model feedback and reflection control, then curiosity/gap selection, then theory formation, then procedure/tool invention, then self-reorganization, then domain genesis, and the thin coordinator last
  4. identify where Phase 11 exports must be consumed read-only
- Required cross-checks:
  - no runtime code written now
  - no Phase 13 behavior
  - no Phase 14 behavior
  - no hidden autonomy path
- Exit criteria: future module family, execution order, and stop points are explicit
- Handoff target: `Program Governor`
- Anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- Explicit proof that no approval is implied: execution decomposition does not earn the phase
