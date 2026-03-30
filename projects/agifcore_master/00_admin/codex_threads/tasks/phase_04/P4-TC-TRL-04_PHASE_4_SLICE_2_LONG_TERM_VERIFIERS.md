# Phase 4 Slice 2 Long-Term Verifiers

- Task card ID: `P4-TC-TRL-04`
- Role owner: `Test & Replay Lead`
- Model tier: `gpt-5.4 mini`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Verify the Phase 4 slice-2 long-term memory and correction runtime surfaces:

- semantic memory
- procedural memory
- corrections and promotion

## Exact Files Allowed To Touch

- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_semantic_memory.py`
- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_procedural_memory.py`
- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_corrections_and_promotion.py`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_semantic_memory_report.json`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_procedural_memory_report.json`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_corrections_and_promotion_report.json`

## Forbidden Files

- runtime files
- slice-1 verifier files except as read-only references
- compression and forgetting or retirement verifiers
- demo files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- cleared slice-1 verifiers and evidence
- slice-2 runtime files on the slice-2 runtime lane

## Step-By-Step Method

1. Verify semantic memory stores reviewed abstractions only.
2. Verify procedural memory stores reusable procedures with explicit constraints.
3. Verify promotion depends on review-approved candidates.
4. Verify correction handling creates real before or after mutation evidence with rollback-safe updates.
5. Regenerate machine-readable evidence from real runs only.

## Required Cross-Checks

- no raw transcript leaks into semantic memory
- procedural entries remain distinct from semantic entries
- promotion does not bypass review
- correction paths preserve rollback and supersession evidence

## Exit Criteria

- all three slice-2 verifier files exist and pass
- all three slice-2 evidence files are regenerated from real runs

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not expand slice-2 verification into slice-3 lifecycle checks.

## Proof That No Approval Is Implied

Slice-2 verification is an internal checkpoint only. Phase 4 remains `open`.
