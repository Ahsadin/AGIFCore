# P8-TC-TRL-05 Phase 8 Slice 02 Inference And Region Verifiers

## Header

- Task Card ID: `P8-TC-TRL-05`
- Phase: `8`
- Title: `Phase 8 Slice 02 Inference And Region Verifiers`
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
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/_phase_08_verifier_common.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_scientific_priors.py`
  - the full Phase 8 runtime package

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_entity_request_inference.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_world_region_selection.py`
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_entity_request_inference_report.json`
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_world_region_selection_report.json`
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_evidence_manifest.json`
- Forbidden Files:
  - any Phase 8 runtime file
  - any other verifier file
  - any demo bundle file
  - any phase truth file
  - any Phase 9 and later artifact

## Objective

- Goal: land the inference and region-selection verifier/report pairs and refresh the manifest truthfully.
- Expected Outputs:
  - `verify_phase_08_entity_request_inference.py`
  - `verify_phase_08_world_region_selection.py`
  - matching report JSON files
  - updated truthful manifest

## Cross-Checks

- No pass result without runtime import and concrete assertions.
- Inference must check ambiguity, live-current, and self-knowledge cues.
- Region selection must check bounded candidate counts and unresolved preservation.
- Manifest must still be honest about missing later reports.

## Exit Criteria

- both verifiers run
- both reports exist
- manifest reflects the new on-disk report set

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This verifier slice does not approve Phase 8. Phase 8 remains `open`.
