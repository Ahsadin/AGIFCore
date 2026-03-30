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
| D-013 | 2026-03-29 | The same model family does not mean the same agent. Build Pod Lead, Merge Arbiter, and Validation Agent must be separate sessions or threads. | Keeps separation of duties real instead of cosmetic. |
| D-014 | 2026-03-29 | Meta & Growth Pod is a danger zone and always gets extra audit, stronger governor review, and additional human checkpoints when behavior changes land. | Prevents impressive-sounding self-modification claims from escaping proof. |
| D-015 | 2026-03-29 | Source Cartographer is active by default in Phase 0 and Phase 1 and reopens only when inherited lineage is touched again. | Keeps source mapping strict without creating permanent overhead. |
| D-016 | 2026-03-29 | Product & Sandbox Pod stays one pod for restart but may not become a dumping ground for unrelated late-phase work. | Keeps the late-phase product lane scoped and readable. |
| D-017 | 2026-03-29 | The current Phase 1 planning baseline is frozen for execution handoff, and Phase 2 planning stays deferred until Phase 1 execution, validation, and explicit user approval are complete. | Preserves the approved planning baseline and prevents premature next-phase drift. |
| D-018 | 2026-03-30 | Phase 1 is approved after audit, governor verification, validation request, and explicit user verdict, and Phase 2 remains not started. | Records the earned Phase 1 gate state without implying any later-phase start. |
| D-019 | 2026-03-30 | The user approved the Phase 2 planning baseline for execution start, that baseline is now frozen for execution start, Phase 2 remains `open`, and Phase 3 has not started. | Allows governed Phase 2 execution to begin without confusing plan freeze with phase completion. |
| D-020 | 2026-03-30 | Phase 2 is approved after audit, governor verification, validation request, review-bundle repair, and explicit user verdict, and Phase 3 has not started. | Records the earned Phase 2 gate state without implying any later-phase start. |
