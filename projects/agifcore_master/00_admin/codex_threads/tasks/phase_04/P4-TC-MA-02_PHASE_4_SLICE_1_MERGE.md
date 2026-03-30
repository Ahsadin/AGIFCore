# Phase 4 Slice 1 Merge

- Task card ID: `P4-TC-MA-02`
- Role owner: `Merge Arbiter`
- Model tier: `gpt-5.3-codex`
- Phase: `Phase 4`
- Status: `pending_audit`

## Objective

Integrate the cleared Phase 4 slice-1 runtime, verifier, evidence, and boundary-note commits into one clean slice-1 merge lane.

## Exact Files Allowed To Touch

- slice-1 runtime files under `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/`
- slice-1 verifier files under `projects/agifcore_master/05_testing/phase_04_memory_planes/`
- slice-1 evidence files under `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-NOTE-ACL-02_PHASE_4_BOUNDARY_NOTES.md`

## Forbidden Files

- plan files
- demo bundle files
- Phase 5+ files
- any unrelated Phase 4 surfaces beyond slice 1

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-01_PHASE_4_SLICE_1_AUDIT_REPORT.md`
- the cleared slice-1 runtime, verifier, and ACL commits

## Step-By-Step Method

1. Merge only after a slice-1 audit pass exists.
2. Integrate the cleared MGPL, TRL, and ACL commits into the merge lane.
3. Keep the integration limited to slice-1 files only.
4. Do not rewrite content except what is strictly needed to integrate cleanly.
5. Hand the integrated lane back to Program Governor for independent reruns.

## Required Cross-Checks

- merged files match the cleared slice-1 scope
- no extra Phase 4 runtime files appear
- no Phase 5 drift appears

## Exit Criteria

- the merge lane contains the cleared slice-1 package
- the merge lane is ready for Governor reruns

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not fix design or behavior during merge. Merge only the cleared slice-1 package.

## Proof That No Approval Is Implied

Slice-1 merge readiness does not approve Phase 4. Phase 4 remains `open`.
