# P15-TC-SC-01 Phase 15 Provenance And Reuse

- Task Card ID: `P15-TC-SC-01`
- Phase: `15`
- Title: `Phase 15 provenance and reuse mapping`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Source Cartographer`
- Supporting Roles:
  - `Program Governor`
  - `Architecture & Contract Lead`
- Allowed Models: `gpt-5.4-mini`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-SC-01_PHASE_15_PROVENANCE_AND_REUSE.md`
- Forbidden Files:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 16 and later artifacts

## Objective

- Goal: map each Phase 15 subsystem, including live-turn repair and real desktop chat demo lineage, to donor basis, one allowed disposition, reuse limits, and unresolved seams
- Expected Outputs:
  - provenance map for all Phase 15 subsystems
  - explicit donor-basis references
  - unresolved seam notes where portability is partial
- Non-Goals:
  - runtime authoring
  - verifier authoring
  - validation or approval

## Required Reads First

- `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
- `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
- `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
- approved Phase 2 through Phase 14 plans and execution surfaces
- donor blind/live-demo/soak/repro/closure files
- donor open-question runtime and live-demo lineage

## Step-by-Step Work Method

1. Map blind packs, hidden packs, live-demo pack, soak harness, hardening package, reproducibility package, closure audit, live-turn repair, and real desktop chat demo host.
2. Assign exactly one allowed disposition to each subsystem.
3. Flag where inherited contract is stronger than whole-module portability.
4. Pass unresolved seams to `Architecture & Contract Lead` and `Program Governor`.

## Required Cross-Checks

- no fifth disposition
- no silent omission
- no donor proof treated as earned AGIFCore proof
- no donor open-question runtime treated as a direct drop-in replacement

## Exit Criteria

- each Phase 15 subsystem has source basis, disposition, and rationale

## Handoff Target

- `Architecture & Contract Lead`
- `Program Governor`

## Anti-Drift Rule

- Do not claim donor code is already valid AGIFCore completion.

## Explicit Proof That No Approval Is Implied

- Provenance mapping records reuse truth only.
- It does not approve or close Phase 15.
