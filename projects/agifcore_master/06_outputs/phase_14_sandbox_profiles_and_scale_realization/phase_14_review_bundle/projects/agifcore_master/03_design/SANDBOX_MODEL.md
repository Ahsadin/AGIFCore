# Sandbox Model

## Purpose

This file defines the first-pass sandbox boundary for isolated packaged execution in AGIFCore.

## Frozen sandbox responsibilities

- isolate packaged execution where needed
- enforce fuel, memory, and wall-time limits
- fail closed on policy or integrity failure
- preserve evidence about sandbox decisions and limit hits

## Boundary rules

- The sandbox is an enforcement boundary, not a hidden cognition lane.
- Sandboxed execution must still respect bundle integrity and schema validation.
- Limits must be explicit:
  - fuel
  - memory
  - wall-time
- Any request outside allowed capability boundaries must be rejected, not silently widened.

## Relationship to profiles

- Laptop, mobile, and builder profiles may apply different budgets.
- Different budgets do not change the core truth rules or create correctness privilege.
- Sandboxed execution remains subordinate to runner and governance control surfaces.

## Dependency notes

- The exact engine and runtime wiring are later implementation details.
- This first-pass model freezes the need for explicit limits and fail-closed behavior before Phase 14 implementation.
- Later evidence and demo work must make sandbox enforcement inspectable to the user.

## Cross-References

- `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
