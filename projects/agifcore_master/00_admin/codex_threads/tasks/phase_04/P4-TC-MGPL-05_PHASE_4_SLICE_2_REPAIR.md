# Phase 4 Slice 2 Repair

- Task card ID: `P4-TC-MGPL-05`
- Role owner: `Memory & Graph Pod Lead`
- Model tier: `gpt-5.3-codex`
- Phase: `Phase 4`
- Status: `repair_ready`

## Objective

Repair the two concrete slice-2 blockers found by the slice-2 audit:

1. promotion must prove it is using a real approved review candidate from `MemoryReviewQueue`
2. correction handling must apply rollback-safe updated state atomically instead of mutating live stores after the batch

## Exact Files Allowed To Touch

- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/promotion_pipeline.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/correction_handling.py`
- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_corrections_and_promotion.py`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_corrections_and_promotion_report.json`

## Forbidden Files

- slice-3 lifecycle files
- plan files
- demo files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-02_PHASE_4_SLICE_2_AUDIT_REPORT.md`
- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- current slice-2 runtime files
- current slice-2 correction/promotion verifier

## Step-By-Step Method

1. Make promotion require a real review-queue source and approved status from that queue.
2. Make correction handling load the applied rollback-safe batch state back into live stores atomically.
3. If atomic load fails, restore the rollback snapshot and reload the restored state.
4. Rerun the corrections/promotion verifier and refresh its report.

## Required Cross-Checks

- promotion rejects forged approved mappings
- correction leaves no partial live-store writes behind on failure

## Exit Criteria

- the two audit findings are concretely addressed
- the corrections/promotion verifier passes again

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not broaden the repair into slice-3 lifecycle work.

## Proof That No Approval Is Implied

Repair completion does not approve slice 2 or Phase 4. Phase 4 remains `open`.
