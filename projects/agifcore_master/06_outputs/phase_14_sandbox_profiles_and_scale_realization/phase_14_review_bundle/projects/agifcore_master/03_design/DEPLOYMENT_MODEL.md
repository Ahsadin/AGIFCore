# Deployment Model

## Purpose

This file defines the first-pass deployment architecture for AGIFCore across the locked machine profiles.

## Frozen deployment profiles

| Profile | Role in the system | Hard boundary |
| --- | --- | --- |
| laptop | primary reference product machine | correctness must reproduce here |
| mobile | constrained product profile | constrained budget is allowed, weaker truth is not |
| builder | diagnostic and instrumentation machine | may inspect deeper, but has no correctness privilege |
| soak | optional endurance machine | may provide endurance evidence only, never replace primary-machine reproducibility |

## Deployment rules

- Correctness may never depend on a separate cloud or hidden service.
- Imported soak artifacts require provenance.
- Builder diagnostics may enrich evidence, not rewrite truth.
- Mobile is a constrained deployment target, not a different product definition.
- Deployment packaging must stay aligned to bundle integrity and sandbox rules.

## First-pass dependency notes

- Exact packaging layout, installer flow, and distribution mechanics are later product-runtime details.
- Profile manifests and budget enforcement are later implementation details, but the profile boundaries are frozen now.
- This deployment model must stay aligned to the machine-role policy and public release lane.

## Cross-References

- `projects/agifcore_master/02_requirements/DEPLOYMENT_PROFILES.md`
- `projects/agifcore_master/02_requirements/MACHINE_ROLE_POLICY.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
