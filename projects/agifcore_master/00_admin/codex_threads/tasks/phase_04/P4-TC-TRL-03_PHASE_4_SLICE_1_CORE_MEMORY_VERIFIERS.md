# Phase 4 Slice 1 Core Memory Verifiers

- Task card ID: `P4-TC-TRL-03`
- Role owner: `Test & Replay Lead`
- Model tier: `gpt-5.4 mini`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Define and later run the slice-1 verifier surface for the Phase 4 core runtime:

- working memory
- episodic memory
- continuity memory
- memory review
- rollback-safe updates

## Exact Files Allowed To Touch

- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_working_memory.py`
- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_episodic_memory.py`
- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_continuity_memory.py`
- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_memory_review.py`
- `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_rollback_safe_updates.py`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_working_memory_report.json`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_episodic_memory_report.json`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_continuity_memory_report.json`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_memory_review_report.json`
- `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_rollback_safe_updates_report.json`

## Forbidden Files

- runtime files
- semantic, procedural, correction, promotion, compression, forgetting, and retirement verifiers
- demo bundle files
- plan files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- approved Phase 2 verifier patterns
- approved Phase 3 verifier patterns

## Step-By-Step Method

1. Add self-contained runtime import-path handling relative to repo layout.
2. Verify real bounded behavior for working memory.
3. Verify replayable event-history behavior for episodic memory.
4. Verify continuity anchors and supersession markers.
5. Verify that memory review decisions are explicit and enforced.
6. Verify that rollback-safe updates create restore or reject behavior through the Phase 2 rollback and replay substrate.
7. Emit machine-readable evidence only from real runs.

## Required Cross-Checks

- no verifier reports success when runtime imports fail
- no report text stands in for behavior proof
- no evidence file is generated without a real verifier run
- no graph logic or conversation behavior appears in the slice-1 checks

## Exit Criteria

- all five slice-1 verifier files exist and run
- all five slice-1 evidence files are regenerated from real runs
- slice-1 readiness is truthful

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not turn slice-1 verification into full-phase verification before the rest of the runtime exists.

## Proof That No Approval Is Implied

Slice-1 verification is an internal checkpoint only. Phase 4 remains `open` and is not approved.
