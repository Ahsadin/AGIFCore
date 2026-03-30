# Phase 4 Demo: Forgetting And Compression

## What This Demo Shows

This demo shows the final Phase 4 lifecycle effects:

- semantic compression
- rollback-safe episodic forgetting with a retained summary
- explicit procedural retirement

## Evidence Used

- `../phase_04_evidence/phase_04_forgetting_and_compression_report.json`
- `../phase_04_evidence/phase_04_evidence_manifest.json`

## Step 1: Compression Produces A Retained Semantic Summary

From `phase_04_forgetting_and_compression_report.json`:

- `compression_result.compression_id` = `phase4-compression-00000001`
- `compression_result.source_ids` = `[\"semantic-0001\", \"semantic-0002\"]`
- `compression_result.created_id` = `semantic-compression-00000001`
- `semantic_active_entry_ids` = `[\"semantic-compression-00000001\"]`

This shows compression is a real state transition. The two source entries are no longer active, and one retained summary anchor remains active.

## Step 2: The Retained Summary Still Keeps Provenance

From `phase_04_forgetting_and_compression_report.json`:

- `compressed_summary.provenance_refs` keeps both original semantic traces
- `compressed_summary.metadata.compressed_entry_ids` keeps the source ids

This means compression does not erase the ability to inspect where the retained summary came from.

## Step 3: Forgetting Uses A Rollback-Safe Batch And Keeps A Summary Event

From `phase_04_forgetting_and_compression_report.json`:

- `forgetting_result.rollback_ref` = `rollback-00000001`
- `forgetting_result.replay_id` = `phase4-memory-update-00000001`
- `forgetting_result.forgotten_event_ids` = `[\"event-0001\", \"event-0002\"]`
- `forgetting_result.summary_event_id` = `event-summary-0001`

And from `episodic_recent_window`:

- old events `event-0001` and `event-0002` are gone
- summary event `event-summary-0001` remains

This shows forgetting is governed removal, not silent deletion.

## Step 4: Retirement Removes A Procedure From The Active Set

From `phase_04_forgetting_and_compression_report.json`:

- `retirement_result.retirement_id` = `phase4-retirement-00000001`
- `retirement_result.target_id` = `procedure-0001`
- `procedural_state.status` = `retired`
- `procedural_state.retirement_ref` = `retire://phase4/phase4-retirement-00000001`

This shows retirement is explicit and leaves a visible retirement marker.

## Step 5: The Evidence Manifest Lists The Full Report Family

From `phase_04_evidence_manifest.json`:

- the manifest includes all required Phase 4 report files
- the manifest notes that it tracks verifier outputs only and does not imply approval

## Why This Matters

The demo proves:

- compression is real and inspectable
- forgetting is rollback-safe and retains a summary anchor
- retirement is explicit
- the lifecycle behavior is backed by machine-readable evidence

## Approval Note

This is review material only. Phase 4 remains `open`.
