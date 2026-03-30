# Phase 4 Slice 2 Audit

- Task card ID: `P4-TC-ASA-03`
- Role owner: `Anti-Shortcut Auditor`
- Model tier: `gpt-5.4 mini`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Audit the Phase 4 slice-2 long-term memory and correction package before any slice-2 merge.

## Exact Files Allowed To Touch

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-02_PHASE_4_SLICE_2_AUDIT_REPORT.md`

## Forbidden Files

- runtime files
- verifier files
- evidence files
- plan files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- slice-2 runtime files on the MGPL slice-2 lane
- slice-2 verifier files and evidence on the TRL slice-2 lane
- slice-2 boundary note on the ACL slice-2 lane

## Step-By-Step Method

1. Check slice-2 scope discipline:
   - semantic memory
   - procedural memory
   - promotion pipeline
   - correction handling
2. Confirm no compression, forgetting, or retirement logic is hidden here.
3. Confirm semantic and procedural planes remain distinct.
4. Confirm promotion stays review-gated.
5. Confirm correction stays rollback-safe and continuity-aware.
6. Confirm no graph implementation and no conversation behavior.
7. Write an explicit pass or blocker report.

## Required Cross-Checks

- no Phase 2 rollback replacement
- no Phase 3 structure drift
- no one-store collapse across long-term planes

## Exit Criteria

- audit report exists
- it states `pass` or `blocked_for_repair`

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not repair slice-2 code during audit.

## Proof That No Approval Is Implied

Slice-2 audit readiness does not approve Phase 4. Phase 4 remains `open`.
