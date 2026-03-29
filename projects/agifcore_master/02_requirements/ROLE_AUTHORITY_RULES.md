# Role Authority Rules

## Read-Before-Work Rule

Every single work item must start only after the worker, manager, or governor has read:

1. `PROJECT_README.md`
2. `DECISIONS.md`
3. `CHANGELOG.md`
4. `01_plan/MASTER_PLAN.md`
5. this file

If those files were not read first, the work is not valid.

## Frozen Execution Authority Model

AGIFCore uses one fixed execution chain:

- one `Governor`
- one `Manager`
- `2-5+` `Workers` under the manager when needed

The exact number of workers depends on the task, but the reporting chain does not change.

The chain is always:

`Worker -> Manager -> Governor -> User`

No one may skip around that chain for phase truth, closure, or next-step authority.

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
- decide whether the current worker evidence is good enough to move forward
- decide whether the next prompt or next phase handoff is allowed
- independently inspect actual code and relevant files, not just report text
- independently rerun the required checks, verifiers, and direct sanity paths
- independently verify the demo path before asking the user to review it
- ask the user for end-of-phase review only after the demo and manager report are ready

Governor may:

- overrule manager and worker conclusions
- reopen invalid work
- reject misleading closure claims
- require more worker or manager passes before a user review is requested
- decide the next official prompt after reviewing the manager report

Governor may not:

- overrule the user
- change the frozen master plan without explicit user approval
- mark a phase earned without the required user review and user approval

## Governor Verification Rule

Governor must never trust report text alone.

Governor must verify phase truth by:

- reading the relevant code and files directly
- rerunning the required checks and verifiers directly
- checking that the demo path actually works as claimed

If the code, checks, or demo do not support the report, the report is rejected and the work stays open.

## Manager Role

Manager reports to Governor.

Manager responsibilities:

- translate the frozen master plan into phase-by-phase execution threads
- assign bounded work to workers
- collect evidence, verifier output, and demos
- report status and blockers to Governor
- keep work aligned to the current phase only
- decide how many workers are needed for the current task
- consolidate worker outputs into one clear manager report for Governor
- prepare the demo package and review package for Governor

Manager may:

- coordinate workers
- prepare recommendations for Governor
- request corrections when worker output is incomplete
- split work across `2-5+` workers when the task benefits from parallel bounded scopes

Manager may not:

- declare a phase earned on their own
- override Governor decisions
- change the frozen master plan
- ask the user for final phase approval on their own
- let workers report phase truth directly to the user as if they are the governor

## Worker Role

Workers report through the assigned manager path.

Worker responsibilities:

- execute bounded assigned tasks
- keep changes small and scoped
- run required checks
- produce evidence and handoff notes
- report blockers honestly
- report results back to the manager, not directly as final phase truth
- stay within the exact assigned scope and write set

Workers may:

- implement scoped code and docs
- propose improvements within the assigned task
- work in parallel with other workers when the manager assigns disjoint scopes

Workers may not:

- claim a phase earned
- change the frozen master plan
- expand scope across phases without manager approval
- bypass Governor or user authority
- report directly to the user as the final authority on phase truth
- decide the next official prompt or next phase

## Reporting Flow

The required reporting flow is:

1. Workers finish bounded tasks and report to the manager.
2. The manager consolidates the worker outputs into one manager report.
3. The manager report goes to the governor.
4. The governor reads the relevant code, reruns the required checks, verifies the demo path, and then decides phase truth and the next official prompt.
5. At the end of a phase, the governor asks the user to review a demo.
6. The phase may move forward only after the user approves it.

If this reporting flow is broken, the result is not valid phase truth.

## End-Of-Phase Review Rule

At the end of every phase:

1. workers complete the assigned work
2. manager consolidates the evidence and demo package
3. governor independently verifies the code, checks, and demo package
4. governor asks the user to review the phase demo
5. the user checks the demo and gives a verdict
6. only after user approval may the phase be marked earned and the next phase begin

No next phase may start from assumed acceptance.

## Phase Approval Rule

A phase is not earned until:

1. implementation is complete
2. automated verification passes
3. a demo is built for the user
4. the governor asks the user for review using the validation-agent package
5. the user explicitly approves the phase

## Freeze Rule

`01_plan/MASTER_PLAN.md` is frozen at bootstrap.

No one may change it unless the user explicitly asks for a master-plan revision.

These role and reporting rules are also frozen until the user explicitly approves a revision.
