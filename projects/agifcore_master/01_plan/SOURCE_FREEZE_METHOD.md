# Source Freeze Method

## Purpose

This is the canonical Phase 0 source-freeze method for AGIFCore.

## Canonical status

- This file is the closure-target source-freeze method for Phase 0.
- The older draft input `projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_METHOD.md` remains a noncanonical draft input only.
- Closure and later review must use this canonical artifact name.

## Method

1. Start from the frozen source-pool list in `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`.
2. Treat every frozen source pool as read-only historical input, not as trusted AGIFCore output.
3. Before any inherited logic can count, represent it explicitly in `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md` with exactly one disposition:
   - `rebuild_clean`
   - `port_with_provenance`
   - `adapt_for_research_only`
   - `reject`
4. Record exact inherited names in `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`.
5. Record exact runtime modules in `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`.
6. Reject any attempt to claim completion from old code, old demos, old benchmark text, or old report text without AGIFCore rebuild or port, verification, demo, and user approval.
7. If a new candidate source pool appears, stop and reopen source-freeze governance before using it.
8. Keep the Phase 0 and Phase 1 boundary explicit: this method defines scope and use rules only; it does not perform Phase 1 provenance work.

## Required follow-through

- Program Governor must later verify that every frozen source pool is covered in Phase 1 provenance artifacts.
- Source Cartographer must later perform the row-by-row mapping work under the frozen Phase 1 baseline.
- Anti-Shortcut Auditor must later reject silent omission or shortcut around this method.

## Blocked shortcuts

- inherited source text does not count as AGIFCore truth
- inherited benchmark text does not count as AGIFCore proof
- inherited demo text does not count as AGIFCore demo evidence
- inherited status text does not count as phase closure

## Phase boundary

This artifact defines the source-freeze method only.
It does not approve Phase 0, Phase 1, or any inherited implementation.
