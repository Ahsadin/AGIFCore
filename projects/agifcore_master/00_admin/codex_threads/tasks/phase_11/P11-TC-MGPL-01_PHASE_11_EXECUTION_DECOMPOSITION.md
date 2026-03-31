# P11-TC-MGPL-01: Phase 11 Execution Decomposition

- Task card ID: `P11-TC-MGPL-01`
- Role owner: `Meta & Growth Pod Lead`
- Model tier: `gpt-5.3-codex`
- Objective: decompose the future Phase 11 runtime family without crossing into Phase 12 or Phase 13
- Exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-MGPL-01_PHASE_11_EXECUTION_DECOMPOSITION.md`
- Files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_11_GOVERNED_SELF_IMPROVEMENT.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- Required reads first:
  - approved Phase 2 through 10 plans and execution surfaces
  - the Phase 11 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
- Step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/`
  2. keep the module set explicit:
     - `contracts.py`
     - `offline_reflection_and_consolidation.py`
     - `idle_reflection.py`
     - `proposal_generation.py`
     - `self_experiment_lab.py`
     - `shadow_evaluation.py`
     - `before_after_measurement.py`
     - `adoption_or_rejection_pipeline.py`
     - `post_adoption_monitoring.py`
     - `rollback_proof.py`
     - `thought_episodes.py`
     - `self_initiated_inquiry_engine.py`
     - `self_improvement_cycle.py`
  3. order implementation so contracts and reflection come first, then proposals and experiment lab, then evaluation and measurement, then adoption and monitoring, then rollback proof and thought episodes, and the inquiry engine last
  4. identify where Phase 10 exports must be consumed read-only
- Required cross-checks:
  - no runtime code written now
  - no Phase 12 behavior
  - no Phase 13 behavior
  - no hidden autonomy path
- Exit criteria: future module family, execution order, and stop points are explicit
- Handoff target: `Program Governor`
- Anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- Explicit proof that no approval is implied: execution decomposition does not earn the phase
