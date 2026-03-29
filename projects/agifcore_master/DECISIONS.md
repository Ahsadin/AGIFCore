# Decisions

| ID | Date | Decision | Why |
| --- | --- | --- | --- |
| D-001 | 2026-03-29 | `projects/agifcore_master/` is the only canonical AGIFCore project. | Keeps ownership and truth in one place. |
| D-002 | 2026-03-29 | The master plan is frozen at bootstrap. | Ensures all phase plans derive from one fixed source. |
| D-003 | 2026-03-29 | Authority roles are frozen before implementation begins. | Prevents confusion about who can decide, approve, or claim closure. |
| D-004 | 2026-03-29 | AGIFCore uses one fixed chain of command: Worker -> Manager -> Governor -> User. | Keeps reporting, prompts, and closure authority unambiguous. |
| D-005 | 2026-03-29 | Only the governor may ask the user for end-of-phase review, and no next phase starts before user approval. | Prevents silent or assumed phase closure. |
| D-006 | 2026-03-29 | Governor must independently verify code, rerun checks, and verify demos before making a decision. | Prevents trust in report text alone and keeps phase truth evidence-based. |
