# Role Authority Rules

## Read-Before-Work Rule

Every single work item must start only after the worker, manager, or governor has read:

1. `PROJECT_README.md`
2. `DECISIONS.md`
3. `CHANGELOG.md`
4. `01_plan/MASTER_PLAN.md`
5. this file

If those files were not read first, the work is not valid.

## User Authority

The user is the final human authority over:

- whether AGIFCore direction changes
- whether the frozen master plan may be revised
- whether a phase demo is accepted
- whether a phase is honestly approved

## Governor Role

Governor is the ultimate project authority below the user.

Governor responsibilities:

- protect the frozen master plan
- decide project truth when worker or manager reports conflict
- accept or reject manager recommendations
- control phase acceptance language
- control claims, closure, release, and public truth
- stop work that violates the constitution, frozen rules, or user direction

Governor may:

- overrule manager and worker conclusions
- reopen invalid work
- reject misleading closure claims

Governor may not:

- overrule the user
- change the frozen master plan without explicit user approval

## Manager Role

Manager reports to Governor.

Manager responsibilities:

- translate the frozen master plan into phase-by-phase execution threads
- assign bounded work to workers
- collect evidence, verifier output, and demos
- report status and blockers to Governor
- keep work aligned to the current phase only

Manager may:

- coordinate workers
- prepare recommendations for Governor
- request corrections when worker output is incomplete

Manager may not:

- declare a phase earned on their own
- override Governor decisions
- change the frozen master plan

## Worker Role

Workers report through the assigned manager path.

Worker responsibilities:

- execute bounded assigned tasks
- keep changes small and scoped
- run required checks
- produce evidence and handoff notes
- report blockers honestly

Workers may:

- implement scoped code and docs
- propose improvements within the assigned task

Workers may not:

- claim a phase earned
- change the frozen master plan
- expand scope across phases without manager approval
- bypass Governor or user authority

## Phase Approval Rule

A phase is not earned until:

1. implementation is complete
2. automated verification passes
3. a demo is built for the user
4. a validation agent asks the user for review
5. the user explicitly approves the phase

## Freeze Rule

`01_plan/MASTER_PLAN.md` is frozen at bootstrap.

No one may change it unless the user explicitly asks for a master-plan revision.

