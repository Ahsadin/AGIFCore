# Phase 4 Demo: Memory Carry-Forward

## What This Demo Shows

This demo shows the governed carry-forward path from bounded working memory into reviewed long-term memory.

## Evidence Used

- `../phase_04_evidence/phase_04_working_memory_report.json`
- `../phase_04_evidence/phase_04_memory_review_report.json`
- `../phase_04_evidence/phase_04_corrections_and_promotion_report.json`

## Step 1: Working Memory Holds A Bounded Candidate

From `phase_04_working_memory_report.json`:

- `turn_ref` = `turn://conv-phase4-slice1-working/turn-0001`
- `consumed_candidate.candidate_id` = `candidate-001`
- `consumed_candidate.target_plane` = `semantic`
- `memory_pressure.current_state_bytes` = `1095`

This shows the memory starts inside bounded working memory and is still explicit as a candidate, not silently promoted.

## Step 2: Review Gate Decides Whether Promotion Is Allowed

From `phase_04_memory_review_report.json`:

- `approval.review_ref` = `memory-review-00000001`
- `approval.status` = `approved`
- `approval.assigned_tier` = `hot`

This shows the review layer changes state explicitly before long-term promotion is allowed.

## Step 3: Approved Candidates Move Into Long-Term Planes

From `phase_04_corrections_and_promotion_report.json`:

- semantic promotion:
  - `semantic_promotion.created_id` = `semantic-entry-00000001`
  - `semantic_promotion.target_plane` = `semantic`
- procedural promotion:
  - `procedural_promotion.created_id` = `procedure-entry-00000002`
  - `procedural_promotion.target_plane` = `procedural`

This shows carry-forward is not one generic long-term store. Semantic and procedural results land in different planes with different entry types.

## Step 4: Episodic Memory Keeps The History Anchor

From `phase_04_corrections_and_promotion_report.json`:

- `episodic_recent_window[0].event_id` = `event-0001`
- `episodic_recent_window[0].event_type` = `semantic_candidate_promoted`

This keeps a replayable event anchor for the promotion path instead of hiding the promotion inside a silent mutation.

## Why This Matters

The demo proves:

- working memory stays bounded
- review changes state explicitly
- semantic and procedural memory stay separate
- episodic memory keeps the replayable history anchor

## Approval Note

This is review material only. Phase 4 remains `open`.
