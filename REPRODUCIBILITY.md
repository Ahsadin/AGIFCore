# AGIFCore Reproducibility

## Purpose

This file explains how to rerun the final bounded-intelligence checks and the publication-safety scan.

These reruns support the bounded claim only.
They do not justify any broad-chat or AGI claim.

## Prerequisites

- Python 3
- the repository checked out locally
- the working directory set to the repo root

## 1. Rerun the frozen bounded gate

```bash
python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py
```

Expected main output:

- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_report.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_failure_summary.json`

Expected bounded result:

- `gate_passed: true`
- `passed_count: 49`
- `prompt_count: 50`
- `hard_fail_count: 0`

## 2. Rerun the shadow benchmark

```bash
python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_shadow_benchmark.py
```

Expected main output:

- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_report.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_summary.json`

Expected shadow result:

- `shadow_passed: true`
- `passed_count: 50`
- `prompt_count: 50`
- `hard_fail_count: 0`

## 3. Run the publication-safety scan

```bash
python3 projects/agifcore_master/05_testing/final_publication/verify_publication_safety.py
```

Expected main output:

- `projects/agifcore_master/06_outputs/final_publication/publication_safety_report.json`
- `projects/agifcore_master/06_outputs/final_publication/publication_safety_summary.md`
- `projects/agifcore_master/06_outputs/final_publication/public_path_redaction_manifest.json`

How to read the result:

- `safe_to_keep` means the file is acceptable as-is
- `redact_for_public_branch` means the file can stay public after local details are removed
- `move_to_local_nonpublic_archive` means the file should not stay on the public branch

## 4. Review the public package

Start with:

- `README.md`
- `CLAIM_BOUNDARY.md`
- `RESULTS.md`
- `projects/agifcore_master/06_outputs/final_publication/final_public_review_bundle/REVIEW_FIRST.md`

## What not to claim from these reruns

Do not claim:

- broad open-ended non-neural chat success
- general AGI
- unrestricted conversational intelligence

The only supported final claim is:

- AGIFCore is closed as a bounded intelligence baseline
