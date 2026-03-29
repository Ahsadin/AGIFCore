# Escalation And Freeze Rules

## Purpose

Stop repeated mismatch, misleading completion claims, or unsafe improvisation from turning into long failure loops.

## Trigger Conditions

### Evidence mismatch

If code, tests, evidence, or demo do not support the reported result:

- reopen the task immediately
- block phase closure

### Repeated mismatch

If the same phase is reopened twice for evidence mismatch:

- stop build work on that phase
- require explicit Program Governor review
- require explicit user review before more coding continues

### Misleading completion claim

If a role claims work is done without supporting files, tests, or evidence:

- freeze that role from further phase work until reviewed
- require an audit pass before work resumes

### Forbidden tool, model, or network use

If a role violates the tool matrix or model manifest:

- stop work immediately
- quarantine the affected patch
- require Program Governor review

### Branch or worktree violation

If serious work happened outside the allowed branch or worktree policy:

- reject the patch from integration
- recreate the task on a compliant branch or worktree

## Hard Freeze Outcomes

- `reopen_for_rework`
- `freeze_role`
- `freeze_phase`
- `quarantine_patch`
- `escalate_to_user`

## Rule

When trust breaks, the system freezes first and explains second.
