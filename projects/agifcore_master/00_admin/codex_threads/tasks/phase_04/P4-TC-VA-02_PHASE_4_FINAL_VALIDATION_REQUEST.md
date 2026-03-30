# Phase 4 Final Validation Request

- Task card ID: `P4-TC-VA-02`
- Role owner: `Validation Agent`
- Model tier: `gpt-5.4`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Prepare the final Phase 4 validation request that sends the completed package to the user for review.

## Exact Files Allowed To Touch

- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_VALIDATION_REQUEST.md`

## Forbidden Files

- runtime files
- verifier files
- user verdict files
- approval files
- Phase 5+ files

## Required Reads First

- final package audit report
- Governor verification record
- final demo bundle
- final evidence package
- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`

## Step-By-Step Method

1. Identify the exact files the user must review.
2. State the allowed verdicts clearly.
3. State what passed and what remains unapproved.
4. Keep the request truthful and concise.

## Required Cross-Checks

- no self-validation by an authoring lane
- no approval language before user verdict
- no missing review surface

## Exit Criteria

- validation request exists
- it is sufficient for final user review

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not change the package while writing the validation request.

## Proof That No Approval Is Implied

The validation request asks for review only. Phase 4 remains `open`.
