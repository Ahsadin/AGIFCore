# Phase 4 Plan Freeze Handoff

## Purpose

Freeze the approved Phase 4 planning baseline for execution start without treating Phase 4 as earned.

## Frozen source-of-truth files

- `projects/agifcore_master/PROJECT_README.md`
- `projects/agifcore_master/DECISIONS.md`
- `projects/agifcore_master/CHANGELOG.md`
- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- `projects/agifcore_master/01_plan/PHASE_INDEX.md`
- `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
- `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
- `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
- `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
- all files under `projects/agifcore_master/02_requirements/`
- all files under `projects/agifcore_master/03_design/`
- approved Phase 2 execution, testing, and evidence surfaces
- approved Phase 3 execution, testing, and evidence surfaces

## Approved plan artifact

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`

## Gate truth

- Phase 4 remains `open`.
- This freeze is execution-start approval for the plan baseline only.
- This freeze does not mark Phase 4 complete.
- Phase 5 has not started.

## Roles for execution start

### Active roles

- `Program Governor`
- `Memory & Graph Pod Lead`
- `Architecture & Contract Lead`
- `Test & Replay Lead`

### Consult-only roles

- `Constitution Keeper`
- `Source Cartographer`
- `Kernel Pod Lead`
- `Product & Sandbox Pod Lead`

### Inactive roles

- `World & Conversation Pod Lead`
- `Meta & Growth Pod Lead`
- `Merge Arbiter`
- `Anti-Shortcut Auditor`
- `Validation Agent`
- `Release & Evidence Lead`

## Default build pod

- later Phase 4 execution default build pod = `Memory & Graph Pod Lead`

## Phase scope

- working memory
- episodic memory
- semantic memory
- procedural memory
- continuity memory
- correction handling
- promotion
- compression
- forgetting
- retirement
- memory review
- rollback-safe updates

## Blocked actions

- no Phase 5 graph persistence, graph schemas, graph traversal, or graph conflict logic
- no Phase 6 world-model or simulator work
- no Phase 7 conversation behavior beyond allowed memory interfaces
- no one giant untyped store pretending to be multiple memory planes
- no fake correction, compression, forgetting, retirement, or review claims without verifier-visible behavior
- no phase approval or phase-truth flip to `approved`

## Exact end-of-phase success meaning

- runtime files exist for:
  - `working_memory.py`
  - `episodic_memory.py`
  - `semantic_memory.py`
  - `procedural_memory.py`
  - `continuity_memory.py`
  - `correction_handling.py`
  - `promotion_pipeline.py`
  - `compression_pipeline.py`
  - `forgetting_retirement.py`
  - `memory_review.py`
  - `rollback_safe_updates.py`
- verifiers exist and pass for the full required `verify_phase_04_*` family
- machine-readable evidence exists for the full required `phase_04_*_report.json` family plus `phase_04_evidence_manifest.json`
- demo bundle exists for:
  - `phase_04_memory_carry_forward_demo.md`
  - `phase_04_correction_demo.md`
  - `phase_04_forgetting_compression_demo.md`
  - `phase_04_demo_index.md`
- an end-of-phase audit report exists
- a governor verification record exists
- a validation request draft exists
- the package is ready for final user review
- Phase 5 has not started
