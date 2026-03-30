# Phase 4 Slice 2 Merge

- Task card ID: `P4-TC-MA-03`
- Role owner: `Merge Arbiter`
- Model tier: `gpt-5.3-codex`
- Phase: `Phase 4`
- Status: `pending_audit`

## Objective

Integrate the cleared Phase 4 slice-2 runtime, verifier, evidence, and boundary-note commits into one clean slice-2 merge lane on top of the cleared slice-1 merge baseline.

## Exact Files Allowed To Touch

- slice-2 runtime files under `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/`
- slice-2 verifier files under `projects/agifcore_master/05_testing/phase_04_memory_planes/`
- slice-2 evidence files under `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-NOTE-ACL-03_PHASE_4_SLICE_2_BOUNDARY_NOTES.md`

## Forbidden Files

- slice-3 lifecycle files
- demo files
- plan files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-02_PHASE_4_SLICE_2_AUDIT_REPORT.md`
- the cleared slice-2 runtime, verifier, and ACL commits

## Step-By-Step Method

1. Merge only after a slice-2 audit pass exists.
2. Integrate the cleared slice-2 commits onto the cleared slice-1 merge baseline.
3. Keep the merge limited to slice-2 files.
4. Hand the integrated lane back to Program Governor for independent reruns.

## Required Cross-Checks

- no slice-3 files appear
- no Phase 5 drift appears

## Exit Criteria

- the merge lane contains the cleared slice-2 package
- the merge lane is ready for Governor reruns

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not redesign or repair during merge.

## Proof That No Approval Is Implied

Slice-2 integration does not approve Phase 4. Phase 4 remains `open`.
