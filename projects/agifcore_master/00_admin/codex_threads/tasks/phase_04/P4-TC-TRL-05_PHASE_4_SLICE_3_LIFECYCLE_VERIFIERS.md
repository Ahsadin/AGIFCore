# Phase 4 Slice 3 Lifecycle Verifiers

- Task card ID: `P4-TC-TRL-05`
- Role owner: `Test & Replay Lead`
- Model tier: `gpt-5.4 mini`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Verify the final Phase 4 lifecycle slice:

- compression
- forgetting
- retirement

and regenerate truthful lifecycle evidence from real verifier runs.

## Exact Files Allowed To Touch

- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_forgetting_and_compression.py`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_forgetting_and_compression_report.json`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_evidence_manifest.json`

## Forbidden Files

- runtime files
- slice-1 and slice-2 verifier files except as read-only references
- demo files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- cleared slice-2 evidence bundle
- slice-3 runtime files on the slice-3 runtime lane
- `projects/agifcore_master/03_design/MEMORY_MODEL.md`

## Step-By-Step Method

1. Verify compression creates a real retained-state change.
2. Verify forgetting removes selected retained state only through an explicit governed path.
3. Verify retirement removes a procedure from the active set with a visible retirement marker.
4. Regenerate lifecycle evidence from real runs only.
5. Regenerate the phase-4 evidence manifest so the full report family is truthfully indexed.

## Required Cross-Checks

- compression is not report-only
- forgetting preserves a retained anchor or summary path
- retirement is explicit, not implicit
- evidence manifest references real report files only

## Exit Criteria

- slice-3 lifecycle verifier passes
- slice-3 lifecycle evidence file is regenerated
- evidence manifest is truthful for the integrated report family available at that point

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not turn the evidence manifest into a false full-phase approval artifact.

## Proof That No Approval Is Implied

Slice-3 verification is an internal checkpoint only. Phase 4 remains `open`.
