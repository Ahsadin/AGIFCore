# Product Runtime Model

## Purpose

This file freezes the first-pass product runtime split that later Phase 13 work must implement.

## Frozen runtime split

| Surface | First-pass responsibility | Must never do |
| --- | --- | --- |
| runner core | execute governed turns, produce traces, coordinate memory-review handoff, drive runtime lifecycle | present itself directly as the user-facing product |
| local gateway/API | validate requests, expose local control endpoints, mediate contract-safe access to the runner | become a hidden second runtime |
| local desktop UI | present interaction, status, traces, and evidence surfaces to the user | own correctness or rewrite trace truth |

## Required runtime exports

- `state_export`
- `trace_export`
- `memory_review_export`
- safe shutdown surface

## Runtime rules

- The product runtime remains local-first.
- The runner, gateway, and UI must all honor the trace contract.
- Fail-closed UX is required when policy, support state, or integrity checks fail.
- Installer and distribution flow are product-runtime concerns, but correctness cannot depend on installer magic.
- Later mobile and builder variants may differ in profile, not in core truth rules.

## First-pass dependency notes

- This first-pass model uses the frozen runner/gateway/UI split from the master plan.
- Exact gateway endpoint layout and exact UI composition remain later design details.
- The schema contract and bundle integrity checks referenced here depend on the bundle and sandbox models staying aligned.

## Cross-References

- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
- `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
- `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
