# Phase 4 Slice 1 Audit

- Task card ID: `P4-TC-ASA-02`
- Role owner: `Anti-Shortcut Auditor`
- Model tier: `gpt-5.4 mini`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Audit the Phase 4 slice-1 package across the runtime, verifier, evidence, and boundary-note lanes before any slice-1 merge occurs.

## Exact Files Allowed To Touch

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-01_PHASE_4_SLICE_1_AUDIT_REPORT.md`

## Forbidden Files

- all runtime files
- all verifier files
- all evidence JSON files
- all plan files
- all Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-MGPL-03_PHASE_4_SLICE_1_CORE_MEMORY_AND_ROLLBACK.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-TRL-03_PHASE_4_SLICE_1_CORE_MEMORY_VERIFIERS.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-NOTE-ACL-02_PHASE_4_BOUNDARY_NOTES.md`
- slice-1 runtime files in `04_execution/phase_04_memory_planes/agifcore_phase4_memory/`
- slice-1 verifier files in `05_testing/phase_04_memory_planes/`
- slice-1 evidence files in `06_outputs/phase_04_memory_planes/phase_04_evidence/`

## Step-By-Step Method

1. Check scope discipline:
   - working memory
   - episodic memory
   - continuity memory
   - memory review
   - rollback-safe updates
2. Confirm slice 1 does not silently implement semantic, procedural, correction, promotion, compression, forgetting, retirement, graph, or conversation behavior.
3. Check runtime separation:
   - no one giant catch-all store
   - each slice-1 surface has distinct behavior
4. Check evidence honesty:
   - reports match real verifier behavior
   - no empty or decorative outputs
5. Check boundary-note relevance against the actual slice-1 package.
6. Write an explicit pass or blocker report.

## Required Cross-Checks

- no Phase 2 kernel reimplementation
- no Phase 3 structure drift
- rollback-safe updates use the Phase 2 rollback and replay substrate
- review decisions have real enforcement meaning

## Exit Criteria

- audit report exists
- report states `pass` or `blocked_for_repair`
- no approval language appears

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not rewrite the slice-1 package while auditing it.

## Proof That No Approval Is Implied

An audit pass clears slice 1 for merge review only. Phase 4 remains `open`.
