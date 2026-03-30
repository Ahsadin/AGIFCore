# Governance Model

## Purpose

This file defines the first-pass governance surfaces that later AGIFCore phases must obey.

## Governance anchors

- the user is the final human approver
- Program Governor is the highest project authority below the user
- no agent may approve its own artifact or phase
- report text alone never counts as proof
- rollback, quarantine, and auditability are first-class system requirements

## Governance surfaces

| Surface | What it governs | What it prevents |
| --- | --- | --- |
| policy pass | whether an action is allowed to proceed | hidden or unsafe continuation |
| critique and error monitoring | whether support is weak, contradictory, or incomplete | confident unsupported output |
| rollback and quarantine | containment when a bad state is detected | silent corruption or unsafe continuation |
| audit and replay | evidence and reproduction of what happened | report-text-only claims |
| phase approval chain | who may move a phase forward | self-approval and fake closure |

## Runtime relationship

- Governance is a system layer, not a UI-only warning system.
- The runner must honor governance outcomes before language realization reaches the user.
- The conversation surface must expose honest weak-support outcomes instead of bypassing governance.
- Workspace and runtime exports must preserve governance-relevant evidence.

## Dependency notes

- This first-pass model freezes the control surfaces, not the final algorithmic implementation.
- Later critique, world-model, and self-improvement phases will deepen governance logic but may not remove these boundaries.
- Any later architecture change that weakens rollback, quarantine, auditability, or user authority should be treated as drift.

## Cross-References

- `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
- `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
- `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
