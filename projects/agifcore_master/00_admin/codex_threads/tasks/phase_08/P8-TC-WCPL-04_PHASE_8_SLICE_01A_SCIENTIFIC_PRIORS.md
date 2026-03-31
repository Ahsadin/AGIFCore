# P8-TC-WCPL-04 Phase 8 Slice 01A Scientific Priors

## Header

- Task Card ID: `P8-TC-WCPL-04`
- Phase: `8`
- Title: `Phase 8 Slice 01A Scientific Priors`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `World & Conversation Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-WCPL-03_PHASE_8_SLICE_01_RUNTIME_FOUNDATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/__init__.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/scientific_priors.py`
- Forbidden Files:
  - every other Phase 8 runtime file
  - all test, output, handoff, and truth files
  - any Phase 9 and later artifact

## Objective

- Goal: implement the bounded scientific-prior catalog and selection engine for Phase 8.
- Expected Outputs:
  - importable `scientific_priors.py`
  - optional package export in `__init__.py`
- Non-Goals:
  - inference
  - region selection
  - causal chains
  - current-world reasoning
  - visible reasoning
  - reflection

## Work Method

1. Reuse the typed prior-cell structure already present in `contracts.py`.
2. Port the bounded seed-prior idea from donor lineage without importing donor runtime directly.
3. Keep catalog size and selection bounded by the Phase 8 ceilings.
4. Preserve provenance refs, scope limits, failure cases, and hidden-variable hints.

## Cross-Checks

- No more than `12` priors selected in one run.
- No empty provenance refs.
- No hidden donor runtime import.
- No final answer text.
- No Phase 9 or Phase 10 behavior.

## Exit Criteria

- file imports cleanly
- engine can build a prior snapshot from Phase 7 inference-style inputs
- output uses `ScientificPriorCell`, `SelectedScientificPrior`, and `ScientificPriorsSnapshot`

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This micro-slice is only a build step. Phase 8 remains `open`.
