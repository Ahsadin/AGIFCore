# Deployment Profiles

## Purpose

This file freezes the deployment profile labels that later AGIFCore phases must respect.

## Frozen Profiles

### Laptop

- Default local-use profile
- Used for ordinary authoring and review
- Must stay local-first and fail-closed

### Mobile

- Constrained user-facing profile
- Must keep the surface small and inspectable
- May not assume builder-level resources

### Builder

- Governed build-machine profile
- Used for controlled authoring, tests, and evidence work
- May write only inside task-card scope

### Soak

- Long-running validation profile
- Used for durable checks, evidence capture, and repeatability
- Must not become a hidden execution shortcut

## Phase 1 Rule

These profiles are planning-level boundaries in Phase 1. They are not runtime claims and they do not authorize implementation outside the frozen work order.

## Cross-References

- `projects/agifcore_master/02_requirements/MACHINE_ROLE_POLICY.md`
- `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
