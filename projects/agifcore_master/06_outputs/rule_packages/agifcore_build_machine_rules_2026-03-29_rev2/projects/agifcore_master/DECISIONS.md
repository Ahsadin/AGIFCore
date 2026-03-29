# Decisions

| ID | Date | Decision | Why |
| --- | --- | --- | --- |
| D-001 | 2026-03-29 | `projects/agifcore_master/` is the only canonical AGIFCore project. | Keeps ownership and truth in one place. |
| D-002 | 2026-03-29 | The master plan is frozen at bootstrap. | Ensures all phase plans derive from one fixed source. |
| D-003 | 2026-03-29 | AGIFCore uses a governed build machine, not a generic manager/worker hierarchy. | Keeps planning, coding, testing, auditing, validation, and approval separated. |
| D-004 | 2026-03-29 | Build agents are outside the AGIFCore runtime and may never become part of the runtime truth path. | Protects the shipped system from hidden build-time model dependence. |
| D-005 | 2026-03-29 | The user is the only phase approver. No agent may self-approve a phase. | Prevents silent or assumed closure. |
| D-006 | 2026-03-29 | Program Governor must independently verify code, rerun checks, and verify demos before any review request. | Prevents trust in report text alone and keeps phase truth evidence-based. |
| D-007 | 2026-03-29 | No agent may both write and validate the same artifact. | Enforces separation of duties and reduces false completion claims. |
| D-008 | 2026-03-29 | One active build pod is the default unless evaluation evidence justifies more parallel build work. | Keeps coordination complexity controlled. |
| D-009 | 2026-03-29 | Live build work requires frozen task-card, audit, governor-verification, validation-request, and user-verdict templates. | Turns policy into repeatable operating law. |
| D-010 | 2026-03-29 | Tool permissions and branch/worktree isolation are mandatory controls, not optional conventions. | Prevents silent drift in commands, file access, and integration behavior. |
| D-011 | 2026-03-29 | Exact role-to-model mappings and downgrade rules are frozen in a model manifest before live build work. | Prevents model drift and improvised downgrades. |
| D-012 | 2026-03-29 | Repeated evidence mismatch or misleading completion claims trigger escalation and freeze rules. | Stops endless reopen loops and forces human review when trust breaks. |
