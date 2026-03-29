# AGIFCore Repo Rules

This repository has one canonical long-term project:

- `projects/agifcore_master/`

Before starting any work in this repo, read these files in order:

1. `projects/agifcore_master/PROJECT_README.md`
2. `projects/agifcore_master/DECISIONS.md`
3. `projects/agifcore_master/CHANGELOG.md`
4. `projects/agifcore_master/01_plan/MASTER_PLAN.md`
5. `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
6. `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
7. `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
8. `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
9. `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
10. `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
11. `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
12. `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
13. `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
14. `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`

Working rules:

- Treat `projects/agifcore_master/` as the only canonical source of truth.
- No implementation work starts until the master plan and the frozen build-machine rules are read.
- No implementation, audit, merge, or validation pass starts without a task card created from the frozen template.
- `01_plan/MASTER_PLAN.md` is frozen. Do not change it unless the user explicitly authorizes a master-plan revision.
- AGIFCore uses a governed build machine, not a copied human org chart.
- Every phase ends only after user review and explicit user approval.
- The user is the only phase approver.
- Program Governor is the highest agent authority below the user.
- Build agents are outside the AGIFCore runtime and may never become part of the runtime truth path.
- No agent may both write and validate the same artifact.
- The same model family does not mean the same agent. Build Pod Lead, Merge Arbiter, and Validation Agent must use separate agents, sessions, or threads.
- One active build pod is the default. More parallel build pods require explicit governor approval backed by evaluation evidence.
- Tool access, branch/worktree isolation, model use, and escalation behavior are controlled by frozen policy files, not by ad hoc judgment.
- Meta & Growth Pod is a danger zone and always gets extra audit and stronger governor review.
- Program Governor must never trust report text alone and must independently verify code, checks, and demos before any phase-review request.
- Program Governor is the only role that may ask the user for end-of-phase review.
- No next phase starts until the Program Governor has completed verification and the user has approved the phase demo.
- Keep AGIFCore local-first, no-LLM, no hidden-model, no cloud-correctness, replayable, reversible, auditable, and fail-closed.
- Keep changes small, organized, and reversible.
