# P10-TC-MGPL-01 Phase 10 Execution Decomposition

- task card ID: `P10-TC-MGPL-01`
- role owner: `Meta & Growth Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 10 runtime family without crossing into Phase 11 or 12
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-MGPL-01_PHASE_10_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - approved Phase 2 through 9 plans and execution surfaces
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-SC-01_PHASE_10_PROVENANCE_AND_REUSE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-ACL-01_PHASE_10_BOUNDARIES_AND_CONTRACTS.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/`
  2. keep the module set explicit:
     - `contracts.py`
     - `self_model.py`
     - `meta_cognition_layer.py`
     - `attention_redirect.py`
     - `meta_cognition_observer.py`
     - `skeptic_counterexample.py`
     - `strategy_journal.py`
     - `thinker_tissue.py`
     - `surprise_engine.py`
     - `theory_fragments.py`
     - `weak_answer_diagnosis.py`
     - `meta_cognition_turn.py`
  3. order implementation so contracts come first, then self-model/layer/observer, then redirect/skeptic, then journal/thinker tissue, then surprise/theory fragments, then diagnosis, and the thin coordinator last
  4. identify where Phase 7, 8, and 9 exports must be consumed read-only
- required cross-checks:
  - no runtime code written now
  - no Phase 11 behavior
  - no Phase 12 behavior
  - no hidden self-improvement path
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase
