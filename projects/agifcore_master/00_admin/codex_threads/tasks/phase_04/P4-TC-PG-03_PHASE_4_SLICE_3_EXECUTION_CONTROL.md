# Phase 4 Slice 3 Execution Control

- Task card ID: `P4-TC-PG-03`
- Role owner: `Program Governor`
- Model tier: `gpt-5.4`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Control the final implementation slice of Phase 4:

- compression pipeline
- forgetting and retirement
- integrated full-phase rerun preparation

This card exists to keep the last runtime slice bounded and to keep final closeout separate from final approval.

## Exact Files Allowed To Touch

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-PG-03_PHASE_4_SLICE_3_EXECUTION_CONTROL.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-MGPL-06_PHASE_4_SLICE_3_COMPRESSION_FORGETTING_AND_RETIREMENT.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-TRL-05_PHASE_4_SLICE_3_LIFECYCLE_VERIFIERS.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-ACL-04_PHASE_4_SLICE_3_BOUNDARY_CHECK.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-ASA-04_PHASE_4_SLICE_3_AUDIT.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-MA-04_PHASE_4_SLICE_3_MERGE.md`

## Forbidden Files

- runtime files
- verifier files
- evidence files
- demo files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- slice-2 merge readiness results
- `projects/agifcore_master/03_design/MEMORY_MODEL.md`
- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`

## Step-By-Step Method

1. Confirm slice-2 is cleared before slice-3 runtime begins.
2. Open the slice-3 runtime, verifier, boundary, audit, and merge cards.
3. Keep slice-3 limited to compression plus forgetting and retirement.
4. Reserve final demos, validation, and user review for later closeout work only.

## Required Cross-Checks

- no Phase 5 graph drift
- no conversation behavior drift
- no hidden final approval language

## Exit Criteria

- all slice-3 role cards exist
- slice-3 scope is bounded and explicit

## Handoff Target

`Memory & Graph Pod Lead`

## Anti-Drift Rule

Do not let slice-3 grow into final user-review packaging work.

## Proof That No Approval Is Implied

Slice-3 control is internal execution governance only. Phase 4 remains `open`.
