# Bundle Integrity Model

## Purpose

This file defines the first-pass integrity rules for AGIFCore bundles, contracts, and packaged assets.

## Integrity scope

- schema validation
- bundle manifest validation
- dependency and asset inventory
- fail-closed policy checks before load or execution
- integrity evidence for later audit and release packaging

## Bundle rules

- A bundle may not load if its schema contract is invalid.
- A bundle may not load if required provenance or manifest fields are missing.
- Integrity checks must fail closed instead of silently downgrading trust.
- Runtime packaging must preserve a clear difference between signed or verified structure and mere file presence.
- Evidence export must be able to show what was checked and what failed.

## Relationship to runtime and sandbox

- The product runtime depends on these integrity rules before exposing packaged behavior.
- The sandbox may isolate execution, but sandboxing does not replace integrity checks.
- Release packaging later depends on the same integrity truth, not on a weaker public-facing summary.

## Dependency notes

- Exact hashing, signature, or attestation mechanics are later implementation details.
- This first-pass model freezes the rule that integrity is enforced before execution and before release packaging.
- The final bundle format must stay aligned to schema contracts and later audit evidence.

## Cross-References

- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
- `projects/agifcore_master/03_design/PUBLIC_RELEASE_MODEL.md`
