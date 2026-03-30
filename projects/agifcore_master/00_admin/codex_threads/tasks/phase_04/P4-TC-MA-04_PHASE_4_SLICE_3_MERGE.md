# Phase 4 Slice 3 Merge

- Task card ID: `P4-TC-MA-04`
- Role owner: `Merge Arbiter`
- Model tier: `gpt-5.3-codex`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Integrate the cleared slice-3 runtime, verifier, evidence, and boundary-note commits into one clean slice-3 merge lane.

## Exact Files Allowed To Touch

- Phase 4 slice-3 runtime files under `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/`
- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_forgetting_and_compression.py`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_forgetting_and_compression_report.json`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_evidence_manifest.json`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-NOTE-ACL-04_PHASE_4_SLICE_3_BOUNDARY_NOTES.md`

## Forbidden Files

- plan files
- demo bundle files
- validation request files
- Phase 5+ files

## Required Reads First

- slice-3 cleared audit report
- slice-3 runtime lane
- slice-3 verifier lane
- slice-3 boundary note lane
- slice-2 merge lane baseline

## Step-By-Step Method

1. Integrate only the cleared slice-3 role-lane commits.
2. Keep the merge limited to slice-3 lifecycle files and required evidence updates.
3. Do not rewrite content except what is strictly required to integrate the cleared package.
4. Hand the integrated lane back to the Governor for rerun.

## Required Cross-Checks

- no unaudited content is merged
- no slice-3 scope expansion appears in the merge lane
- slice-2 integrated baseline remains intact

## Exit Criteria

- slice-3 merge lane contains the cleared slice-3 package only
- Governor can rerun the lifecycle verifier on the integrated lane

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not add final user-review packaging work in the slice-3 merge step.

## Proof That No Approval Is Implied

Slice-3 merge readiness does not approve Phase 4. Phase 4 remains `open`.
