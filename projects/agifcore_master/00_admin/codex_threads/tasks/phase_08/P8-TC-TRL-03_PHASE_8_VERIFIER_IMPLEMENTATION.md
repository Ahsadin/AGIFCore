# P8-TC-TRL-03 Phase 8 Verifier Implementation

## Header

- Task Card ID: `P8-TC-TRL-03`
- Phase: `8`
- Title: `Phase 8 Verifier Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Release & Evidence Lead`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Required Reads:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-TRL-02_PHASE_8_VERIFIERS_AND_EVIDENCE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/_phase_07_verifier_common.py`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_question_interpretation.py`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_answer_contract.py`

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
  - all files under `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Forbidden Files:
  - any Phase 8 runtime file
  - any demo bundle file
  - any phase-truth or approval file
  - any Phase 9 and later artifact

## Objective

- Goal: implement the full Phase 8 verifier family and machine-readable evidence bundle.
- Expected Outputs:
  - `_phase_08_verifier_common.py`
  - seven subsystem verifiers
  - seven report JSON files
  - `phase_08_evidence_manifest.json`
- Non-Goals:
  - runtime changes
  - demo markdown bundle
  - phase approval

## Work Method

1. Build the common verifier helper first.
2. Create one verifier per Phase 8 subsystem.
3. Make each verifier emit a real report JSON.
4. Build the manifest only from actual on-disk reports.
5. Run the full verifier family and leave all evidence on disk.

## Cross-Checks

- No empty report files.
- No pass result without real runtime imports and assertions.
- No unsupported exact current-fact test fixtures.
- No hidden-thought leakage in visible reasoning summary checks.
- No verifier may write demo bundle files in this slice.

## Exit Criteria

- all required verifier files exist
- all required evidence report files exist
- the manifest reflects the real report statuses
- the full Phase 8 verifier family runs end to end

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- Verifier implementation and passing evidence do not approve Phase 8. Phase 8 remains `open`.
