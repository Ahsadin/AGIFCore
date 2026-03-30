# Demo Protocol

## Purpose

This file defines the first-pass Phase 1 demo protocol for AGIFCore.

It tells the user what must be inspectable before later review, how the evidence should be grouped, and what each demo is supposed to prove at a planning level.

This file does not approve Phase 1 and does not authorize release completion.

## Required user-review demos

### 1. Project structure demo

What the user must inspect:

- `projects/agifcore_master/01_plan/PHASE_INDEX.md`
- `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
- `projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md`

What must exist before this demo is shown:

- the Phase 1 plan exists
- the phase index shows the locked phase order
- the gate checklist shows truthful status for Phase 1
- the project-structure audit shows the current scaffold honestly
- placeholder state is explicitly called out instead of being hidden

What good looks like:

- the project structure matches the frozen plan
- the user can see which files are substantive and which remain placeholders
- no later-phase work is presented as already complete

What failure looks like:

- missing required root or project truth files
- hidden placeholder state
- any claim that Phase 1 structure is already closed

### 2. Archival statement demo

What the user must inspect:

- `projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md`
- `projects/agifcore_master/CHANGELOG.md`
- `projects/agifcore_master/DECISIONS.md`

What must exist before this demo is shown:

- the archival note exists under the canonical Phase 0/Phase 1 support path
- the note clearly states AGIF v2 is historical source material only
- the note blocks shortcut completion claims
- the note is aligned to the frozen master plan and current gate truth

What good looks like:

- the user can read a direct archival boundary with no loophole
- AGIF v2 is treated as source context, not as completed AGIFCore work
- the historical boundary is consistent across project truth files

What failure looks like:

- vague or reversible archival wording
- any text that makes AGIF v2 sound like completed AGIFCore
- any implied shortcut around the Phase 0/Phase 1 boundary

### 3. Source-freeze method demo

What the user must inspect:

- `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
- `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
- `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
- `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
- `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`

What must exist before this demo is shown:

- the frozen source pool list exists
- the source-freeze method exists
- the exact four source pools are named
- the inheritance matrix and runtime rebuild map exist as first-pass rows
- unresolved lineage items are stated explicitly instead of silently omitted

What good looks like:

- the user can see the exact source pools and the exact use method
- later Phase 1 provenance work is clearly constrained by the frozen boundary
- rebuild, port, adapt, and reject dispositions are visible and understandable

What failure looks like:

- a missing source pool
- no explicit source-freeze method
- any claim that the lineage mapping is already final or fully verified

### 4. Architecture and trace demo

What the user must inspect:

- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/03_design/ARCHITECTURE_OVERVIEW.md`
- `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
- `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
- `projects/agifcore_master/03_design/PUBLIC_RELEASE_MODEL.md`
- `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
- `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
- `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`

What must exist before this demo is shown:

- the trace contract exists as a non-placeholder first-pass draft
- the runner/gateway/UI split is explicit
- the workspace, product runtime, governance, sandbox, bundle, deployment, and release boundaries are explicit
- the design pack no longer reads as placeholder-only

What good looks like:

- the user can inspect a coherent first-pass architecture boundary
- the trace contract and design pack agree with the frozen master plan
- later implementation details are still clearly deferred

What failure looks like:

- a 4-line placeholder or equally thin architecture file
- a contract that allows bypassing trace or governance truth
- a design file that claims runtime completion before execution work exists

## Evidence package organization

The evidence package for later Phase 1 review should be grouped in this order:

1. project structure evidence
2. archival statement evidence
3. source-freeze evidence
4. architecture and trace evidence

Each group should include:

- the canonical file paths the user is meant to inspect
- the audit report that checked the claims
- the Governor verification record that reran direct checks
- the validation request that points the user to the review surfaces

The package must remain inspectable from files alone.

Report text is not enough. The evidence package must point to real files that the user can open.

## Demo rules

- Use the canonical Phase 1 file names only.
- Treat older `PHASE_00_*` files as noncanonical draft inputs only.
- Do not present any demo as approval or release completion.
- Do not ask the user to approve a phase until the audit, Governor verification, validation request, and explicit user review are all complete.
- If a prerequisite file is still placeholder-only, the demo must stop and state that gap plainly.

## Cross-References

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
