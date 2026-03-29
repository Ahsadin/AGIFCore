# AGIFCore Project README

## Goal

Build AGIFCore as the new canonical AGIF system from scratch, using earlier AGIF repos as source material only.

## Source Of Truth

The source-of-truth files for this project are:

- `PROJECT_README.md`
- `DECISIONS.md`
- `CHANGELOG.md`
- `01_plan/MASTER_PLAN.md`
- `02_requirements/ROLE_AUTHORITY_RULES.md`
- `02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`

## Work Start Rule

No work starts until those files are read.

## Verification Rule

No phase is earned until:

1. implementation is complete
2. verifiers pass
3. a demo is built for the user
4. the governor asks for review using the validation-agent package
5. the user approves it

## Operating Model

AGIFCore runs through one fixed chain:

- workers report to manager
- manager reports to governor
- governor independently verifies the code, checks, and demo
- governor asks the user to review the end-of-phase demo
- the next phase starts only after user approval
