# Phase 4 Slice 3 Audit

- Task card ID: `P4-TC-ASA-04`
- Role owner: `Anti-Shortcut Auditor`
- Model tier: `gpt-5.4 mini`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Audit the final Phase 4 lifecycle slice before any slice-3 merge.

## Exact Files Allowed To Touch

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-04_PHASE_4_SLICE_3_AUDIT_REPORT.md`

## Forbidden Files

- runtime files
- verifier files
- evidence files
- plan files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- slice-3 runtime files on the MGPL slice-3 lane
- slice-3 verifier and evidence files on the TRL slice-3 lane
- slice-3 boundary note on the ACL slice-3 lane

## Step-By-Step Method

1. Check slice-3 scope discipline:
   - compression
   - forgetting
   - retirement
2. Confirm lifecycle transitions are real state transitions, not labels.
3. Confirm forgetting preserves a governed retained anchor.
4. Confirm no graph logic and no conversation behavior appears.
5. Write an explicit pass or blocker report.

## Required Cross-Checks

- no Phase 2 rollback replacement
- no Phase 3 structure drift
- no fake lifecycle completeness

## Exit Criteria

- audit report exists
- it states `pass` or `blocked_for_repair`

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not repair slice-3 code during audit.

## Proof That No Approval Is Implied

Slice-3 audit readiness does not approve Phase 4. Phase 4 remains `open`.
