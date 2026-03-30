# Phase 0 Source Freeze Method

## Purpose

This file records the method for how frozen source material may be used inside AGIFCore.

## Method

1. Start from the frozen source-pool list in `01_plan/PHASE_00_SOURCE_FREEZE_INVENTORY.md`.
2. Treat every frozen source pool as read-only historical input, not as trusted AGIFCore output.
3. Before any inherited logic can count, map it in `01_plan/SOURCE_INHERITANCE_MATRIX.md` with one explicit disposition:
   - `rebuild_clean`
   - `port_with_provenance`
   - `adapt_for_research_only`
   - `reject`
4. Record exact inherited names in `01_plan/COMPONENT_CATALOG.md` and exact runtime modules in `01_plan/RUNTIME_REBUILD_MAP.md`.
5. Reject any attempt to claim completion from old code, old demos, or old benchmark text without AGIFCore rebuild, verification, demo, and explicit user approval.
6. If a new candidate source pool appears, stop and reopen source-freeze governance before using it.
7. Keep the Phase 0 and Phase 1 boundary honest: these source-freeze artifacts only define scope and method; they do not close Phase 0 or Phase 1 by themselves.

## Required follow-through

- Program Governor verifies that later provenance work covers every frozen source pool.
- Source Cartographer performs the row-by-row inheritance mapping during Phase 1 execution.
- Anti-Shortcut Auditor rejects any silent omission or shortcut around this method.

## Boundary note

This method resolves the missing distinct source-freeze method artifact.
Explicit user approval remains separate from artifact existence.
