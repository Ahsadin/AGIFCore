# P8-TC-TRL-02 Phase 8 Verifiers And Evidence

## Header

- Task Card ID: `P8-TC-TRL-02`
- Phase: `8`
- Title: `Phase 8 Verifiers And Evidence`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Release & Evidence Lead`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-WCPL-02_PHASE_8_SCIENCE_WORLD_AWARENESS_IMPLEMENTATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/_phase_07_verifier_common.py`
  - approved Phase 7 verifier family and demo bundle

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
  - all files under `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Forbidden Files:
  - any Phase 9 and later artifact
  - any Phase 4, 5, 6, or 7 file
  - any Phase 8 runtime file
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/phase_09_*`
  - `projects/agifcore_master/04_execution/phase_10_*`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P8-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: turn the Phase 8 plan into a concrete verifier/evidence checklist that later implementation must satisfy without ambiguity.
- Expected Outputs:
  - verifier common fixture chain
  - seven subsystem verifiers
  - evidence manifest
  - demo bundle checklist
- Non-Goals:
  - runtime behavior changes outside what verifier scaffolding requires
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_scientific_priors.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_entity_request_inference.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_world_region_selection.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_causal_chain_reasoning.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_bounded_current_world_reasoning.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_visible_reasoning_summaries.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_science_reflection.py`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - all files under `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_*.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/`

## Verifier Checklist

- The later verifier family must stay split by subsystem. No single verifier may prove all of Phase 8.
- Every verifier must import real runtime modules and assert against real dataclass fields.
- Every verifier must emit a machine-readable report file under `phase_08_evidence/`.
- Every verifier report must be rebuilt from actual on-disk report files, not from a hand-written manifest.
- Every blocked report must name the missing file or dependency report, not just say `blocked`.
- Every pass report must include exact checked files, concrete assertions, anchors, and notes.
- No report may be empty.
- No report may claim pass without a real runtime import and at least one concrete assertion.
- No visible reasoning summary may leak hidden-thought text into a report.
- No unsupported exact current-fact claim may appear in any test fixture or demo fixture.

## Expected Test Inputs

- Scientific priors verifier:
  - a bounded prior catalog with at least one clearly relevant prior, one clearly irrelevant prior, and one ambiguous prior
  - provenance refs for each selected prior
  - a request that should select no more than the Phase 8 ceiling of 12 priors
  - a request that should fail closed when the evidence is too weak
- Entity/request inference verifier:
  - a messy science question with explicit causal language
  - a self-knowledge question about AGIFCore capabilities
  - a live-current question that requires freshness honesty
  - an ambiguous follow-up that should not over-commit
- World-region selection verifier:
  - a request with a target domain and a matching world-model region
  - a request with multiple plausible region candidates
  - a request with no safe region so the result must stay unresolved
- Causal-chain reasoning verifier:
  - a request that can be broken into typed causal steps
  - a request that requires a missing-variable marker
  - a request that should expose a weak link or fail closed
- Bounded current-world reasoning verifier:
  - a bounded local support case
  - a live-current request that must return `needs_fresh_information` or `live_measurement_required`
  - a current-world request with insufficient local evidence
- Visible reasoning summary verifier:
  - a grounded request with known/inferred/uncertainty fields
  - a live-current request that must keep the summary bounded
  - a request that forces the summary to stay public-summary-only
- Science reflection verifier:
  - a run with a weak-prior choice
  - a run with a missing variable
  - a run with a falsifier and next verification step

## Evidence Shape

- `phase_08_evidence_manifest.json` must be the top-level index of actual report files.
- Each report JSON must include at minimum:
  - `phase`
  - `verifier`
  - `status`
  - `checked_files`
  - `assertions`
  - `outputs`
  - `anchors` for pass reports
  - `blocker` for blocked reports
  - `notes`
- Each report must point to its own file in `outputs.report`.
- The manifest must list every required report exactly once.
- The manifest status must reflect the actual on-disk report statuses.
- The manifest must stay `phase_8_verifier_family_pass` only when all required reports are present and passing.

## Demo Surfaces

- `phase_08_demo_index.md` must point to the concrete demo files and the evidence manifest.
- `phase_08_science_explanation_demo.md` must show:
  - the original prompt
  - inferred entity/request shape
  - selected priors
  - selected region or context
  - typed causal chain
  - public reasoning summary fields
  - science reflection note
  - backing report files
- `phase_08_bounded_live_fact_demo.md` must show:
  - live-current cue detection
  - bounded local evidence set
  - freshness boundary
  - `needs_fresh_information` or `live_measurement_required`
  - public reasoning summary fields
  - proof that no unsupported exact current answer was emitted
- Demo files must be inspectable from files alone.
- Demo files must not imply phase approval.

## Failure Signatures

- Scientific priors:
  - pass without typed prior cells
  - more than 12 selected priors
  - missing provenance refs
  - selection that ignores scope limits or failure cases
- Entity/request inference:
  - request analysis collapses into prose only
  - no explicit ambiguity markers
  - live-current cues are ignored
  - self-knowledge is inferred from generic text only
- World-region selection:
  - one default region is always chosen
  - multiple candidates are not preserved
  - unresolved requests are forced into a false positive
- Causal-chain reasoning:
  - steps are prose only
  - no machine-checkable step ids or step kinds
  - missing variables are hidden
  - weak links are not surfaced
- Bounded current-world reasoning:
  - exact current facts are emitted without fresh evidence
  - external search is implied inside the verifier
  - insufficient evidence still yields a confident answer
- Visible reasoning summaries:
  - summary becomes hidden-thought leakage
  - summary exceeds the character ceiling
  - summary omits `what_is_known`, `what_is_inferred`, `uncertainty`, or `what_would_verify`
- Science reflection:
  - reflection exists only as labels with no effect
  - no falsifier or next verification step is recorded
  - reflection output expands into meta-cognition behavior

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-AUDIT-01_PHASE_8_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `Merge Arbiter`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined

## Work Method

1. Create the common fixture and report helpers first.
2. Build one verifier per major Phase 8 subsystem.
3. Keep the verifier family aligned to the Phase 8 contract dataclasses and budget ceilings.
4. Make every verifier produce machine-readable evidence.
5. Refresh the evidence manifest only from actual report files.
6. Keep the demo bundle and evidence bundle file-backed and inspectable.

## Later Verifier Families To Generate

- `verify_phase_08_scientific_priors.py`
- `verify_phase_08_entity_request_inference.py`
- `verify_phase_08_world_region_selection.py`
- `verify_phase_08_causal_chain_reasoning.py`
- `verify_phase_08_bounded_current_world_reasoning.py`
- `verify_phase_08_visible_reasoning_summaries.py`
- `verify_phase_08_science_reflection.py`
- `_phase_08_verifier_common.py`
- later demo and evidence packagers only after the verifier family is stable

## Cross-Checks

- No empty report files.
- No pass status without a real runtime import and concrete assertions.
- No unsupported exact current-fact output in test fixtures.
- No visible reasoning summary as hidden-thought leakage.
- No verifier may overreach into runtime implementation or Phase 9/10 behavior.
