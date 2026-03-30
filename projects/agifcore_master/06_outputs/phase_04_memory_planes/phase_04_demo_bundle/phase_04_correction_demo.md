# Phase 4 Demo: Correction

## What This Demo Shows

This demo shows a semantic correction that:

- preserves the original event trail
- uses rollback-safe updates
- leaves the corrected semantic entry active

## Evidence Used

- `../phase_04_evidence/phase_04_corrections_and_promotion_report.json`

## Step 1: A Promoted Semantic Entry Exists

From `phase_04_corrections_and_promotion_report.json`:

- `semantic_promotion.created_id` = `semantic-entry-00000001`

This is the entry that later receives the correction.

## Step 2: Correction Produces A Real Before-And-After Path

From `phase_04_corrections_and_promotion_report.json`:

- `correction_result.correction_id` = `correction-0001`
- `correction_result.target_id` = `semantic-entry-00000001`
- `correction_result.replacement_id` = `semantic-correction-00000001`
- `correction_result.rollback_ref` = `rollback-00000001`
- `correction_result.replay_id` = `phase4-memory-update-00000001`

This shows correction is not just text in a report. It creates a replacement target plus rollback and replay anchors.

## Step 3: Episodic Memory Preserves The Correction Marker

From `phase_04_corrections_and_promotion_report.json`:

- `episodic_recent_window[0].correction_status` = `corrected`
- `episodic_recent_window[0].correction_markers[0].correction_id` = `correction-0001`
- `episodic_recent_window[0].correction_markers[0].replacement_event_id` = `semantic-correction-00000001`

This keeps the correction visible in replayable history.

## Step 4: The Corrected Semantic Entry Becomes The Active One

From `phase_04_corrections_and_promotion_report.json`:

- `semantic_active_entry_ids` = `[\"semantic-correction-00000001\"]`

This shows the corrected semantic state is now the active state after the governed correction path.

## Why This Matters

The demo proves:

- correction is explicit
- rollback and replay anchors exist
- episodic history is preserved
- semantic state changes are visible and inspectable

## Approval Note

This is review material only. Phase 4 remains `open`.
