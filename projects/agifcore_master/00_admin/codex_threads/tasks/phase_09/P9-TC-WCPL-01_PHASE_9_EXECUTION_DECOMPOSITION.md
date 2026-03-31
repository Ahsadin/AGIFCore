# P9-TC-WCPL-01 Phase 9 Execution Decomposition

- task card ID: `P9-TC-WCPL-01`
- role owner: `World & Conversation Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 9 runtime family without crossing into Phase 10 or 11
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-WCPL-01_PHASE_9_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - approved Phase 2 to 8 plans and execution surfaces
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-SC-01_PHASE_9_PROVENANCE_AND_REUSE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ACL-01_PHASE_9_BOUNDARIES_AND_CONTRACTS.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/`
  2. keep the module set explicit:
     - `contracts.py`
     - `teaching.py`
     - `comparison.py`
     - `planning.py`
     - `synthesis.py`
     - `analogy.py`
     - `concept_composition.py`
     - `cross_domain_composition.py`
     - `audience_aware_explanation_quality.py`
     - `rich_expression_turn.py`
  3. order module implementation so contracts come first, then teaching/comparison, then planning/synthesis, then analogy/composition, then audience-quality, and the thin coordinator last
  4. identify where Phase 7 and Phase 8 exports must be consumed read-only
- required cross-checks:
  - no runtime code written now
  - no Phase 10 behavior
  - no Phase 11 behavior
  - no live search execution
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase
