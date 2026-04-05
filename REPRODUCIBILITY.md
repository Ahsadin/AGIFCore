# AGIFCore Reproducibility

## Purpose

This file explains how to rerun the final bounded-intelligence checks and the publication-safety scan.

These reruns support the bounded claim only.
They do not justify any broad-chat or AGI claim.

## Prerequisites

- Python 3
- a local checkout of this repository
- the working directory set to the repo root

## Recommended Order

1. compile-check the publication-safety verifier
2. rerun the frozen bounded gate
3. rerun the shadow benchmark
4. rerun the publication-safety scan
5. review the canonical public package

## 1. Compile-Check The Publication-Safety Verifier

```bash
python3 -m py_compile projects/agifcore_master/05_testing/final_publication/verify_publication_safety.py
```

Expected result:

- no error output

## 2. Rerun The Frozen Bounded Gate

```bash
python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py
```

Expected outputs:

- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_report.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_failure_summary.json`

Expected bounded result:

- `gate_passed: true`
- `passed_count: 49`
- `prompt_count: 50`
- `hard_fail_count: 0`

## 3. Rerun The Shadow Benchmark

```bash
python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_shadow_benchmark.py
```

Expected outputs:

- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_report.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_summary.json`

Expected shadow result:

- `shadow_passed: true`
- `passed_count: 50`
- `prompt_count: 50`
- `hard_fail_count: 0`

## 4. Rerun The Publication-Safety Scan

```bash
python3 projects/agifcore_master/05_testing/final_publication/verify_publication_safety.py
```

Expected outputs:

- `projects/agifcore_master/06_outputs/final_publication/publication_safety_report.json`
- `projects/agifcore_master/06_outputs/final_publication/publication_safety_summary.md`
- `projects/agifcore_master/06_outputs/final_publication/public_path_redaction_manifest.json`

Expected public-safety result:

- `flagged files: 0`
- `total findings: 0`

## 5. Review The Canonical Public Package

Start with:

1. `README.md`
2. `CLAIM_BOUNDARY.md`
3. `RESULTS.md`
4. `paper/AGIFCore_Bounded_Intelligence_Final_Report.md`
5. `projects/agifcore_master/06_outputs/final_publication/final_public_review_bundle/REVIEW_FIRST.md`

## Audit And Closeout Notes

The anti-shortcut audit is recorded as an audited result rather than a public rerun script in this package.
Review it here:

- `projects/agifcore_master/06_outputs/final_publication/PUBLICATION_AUDIT_REPORT.md`
- `projects/agifcore_master/06_outputs/final_publication/closeout_records/PHASE_15_AUDIT_PUBLIC.md`

## What A Successful Rerun Means

A successful rerun means:

- the bounded gate still passes
- the shadow benchmark still passes
- the publication-safety scan is clean
- the bounded claim remains supported by the recorded evidence

## What Not To Claim

Do not claim:

- broad open-ended non-neural chat success
- general AGI
- unrestricted conversational intelligence

The only supported final claim is:

- AGIFCore is closed as a bounded intelligence baseline
