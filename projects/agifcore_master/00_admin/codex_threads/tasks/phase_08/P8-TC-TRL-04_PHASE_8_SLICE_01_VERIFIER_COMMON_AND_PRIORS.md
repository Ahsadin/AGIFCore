# P8-TC-TRL-04 Phase 8 Slice 01 Verifier Common And Priors

## Header

- Task Card ID: `P8-TC-TRL-04`
- Phase: `8`
- Title: `Phase 8 Slice 01 Verifier Common And Priors`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Release & Evidence Lead`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Required Reads:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-TRL-03_PHASE_8_VERIFIER_IMPLEMENTATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-TRL-02_PHASE_8_VERIFIERS_AND_EVIDENCE.md`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/_phase_07_verifier_common.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/_phase_08_verifier_common.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_scientific_priors.py`
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_scientific_priors_report.json`
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_evidence_manifest.json`
- Forbidden Files:
  - any Phase 8 runtime file
  - any other verifier file
  - any demo bundle file
  - any phase truth file
  - any Phase 9 and later artifact

## Objective

- Goal: land the shared verifier helper and the first real Phase 8 verifier/report pair.
- Expected Outputs:
  - `_phase_08_verifier_common.py`
  - `verify_phase_08_scientific_priors.py`
  - `phase_08_scientific_priors_report.json`
  - a manifest that truthfully reflects the current on-disk reports

## Cross-Checks

- No pass result without runtime import and concrete assertions.
- The manifest must not pretend the rest of the family is complete.
- No demo files in this slice.

## Exit Criteria

- common helper imports cleanly
- priors verifier runs
- priors report exists and is machine-readable
- manifest is truthful about partial vs complete state

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This verifier slice does not approve Phase 8. Phase 8 remains `open`.
