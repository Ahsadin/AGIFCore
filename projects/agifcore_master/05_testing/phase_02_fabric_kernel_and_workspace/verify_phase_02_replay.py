from __future__ import annotations

import sys
from copy import deepcopy
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
KERNEL_ROOT = PROJECT_ROOT / "04_execution" / "phase_02_fabric_kernel_and_workspace" / "agifcore_phase2_kernel"
EVIDENCE_ROOT = PROJECT_ROOT / "06_outputs" / "phase_02_fabric_kernel_and_workspace" / "phase_02_evidence"

if str(KERNEL_ROOT) not in sys.path:
    sys.path.insert(0, str(KERNEL_ROOT))

from cell_registry import CellRegistry
from event_bus import EventBus
from event_types import (
    AbstainOrAnswer,
    DiscourseMode,
    FinalAnswerMode,
    KnowledgeGapReason,
    KernelEventType,
    KernelResponseSurface,
    KernelTraceRefs,
    KernelTurnContext,
    NextAction,
    SupportState,
    new_kernel_event,
)
from lifecycle_engine import LifecycleEngine
from replay_ledger import ReplayLedger
from scheduler import Scheduler
from workspace_state import SharedWorkspaceState

REPORT_PATH = EVIDENCE_ROOT / "phase_02_replay_report.json"
MANIFEST_PATH = EVIDENCE_ROOT / "phase_02_evidence_manifest.json"

RUNTIME_FILES = [
    KERNEL_ROOT / "workspace_state.py",
    KERNEL_ROOT / "cell_registry.py",
    KERNEL_ROOT / "lifecycle_engine.py",
    KERNEL_ROOT / "scheduler.py",
    KERNEL_ROOT / "replay_ledger.py",
]

BASELINE_FILES = [
    KERNEL_ROOT / "event_types.py",
    KERNEL_ROOT / "event_bus.py",
    PROJECT_ROOT / "01_plan" / "PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md",
    PROJECT_ROOT / "01_plan" / "TRACE_CONTRACT.md",
    PROJECT_ROOT / "03_design" / "GOVERNANCE_MODEL.md",
]


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def build_pass_report() -> dict[str, object]:
    workspace = SharedWorkspaceState()
    registry = CellRegistry()
    lifecycle = LifecycleEngine(registry=registry)
    scheduler = Scheduler()
    bus = EventBus()
    ledger = ReplayLedger()

    conversation_id = "conv-phase2-replay"
    turn_id = "turn-0001"
    cell_id = "cell-replay-001"
    workspace_ref = workspace.register_cell_anchor(
        cell_id=cell_id,
        role_family="replay_verifier",
        lifecycle_state="dormant",
    )
    lifecycle.bootstrap_cell(
        cell_id=cell_id,
        role_family="replay_verifier",
        workspace_ref=workspace_ref,
        reason="seed replay verifier cell",
    )
    lifecycle.activate(cell_id, reason="activate replay verifier cell")
    workspace.update_cell_anchor(
        cell_id,
        lifecycle_state="active",
        workspace_ref=workspace_ref,
    )
    registry.update_cell(cell_id, workspace_ref=workspace_ref, lifecycle_state="active")

    scheduler.enqueue_task(
        task_id="task-replay-001",
        cell_id=cell_id,
        priority=5,
        need_score=0.9,
        estimated_cost=1.0,
        payload={"conversation_id": conversation_id, "turn_id": turn_id},
    )
    dispatched_task = scheduler.dispatch_next()
    if dispatched_task is None:
        raise AssertionError("scheduler did not dispatch the replay task")

    turn = KernelTurnContext(
        conversation_id=conversation_id,
        turn_id=turn_id,
        user_intent="verify replay anchors",
        discourse_mode=DiscourseMode.EXPLAIN,
        support_state=SupportState.GROUNDED,
        knowledge_gap_reason=KnowledgeGapReason.NONE,
        next_action=NextAction.ANSWER,
        active_context_refs=("ctx://phase2/replay",),
    )
    trace_refs = KernelTraceRefs(
        planner_trace_ref="trace://planner/turn-0001",
        simulation_trace_ref="trace://simulation/turn-0001",
        critic_trace_ref="trace://critic/turn-0001",
        governance_trace_ref="trace://governance/turn-0001",
    )
    admitted_event = new_kernel_event(
        event_type=KernelEventType.TURN_ADMITTED,
        turn=turn,
        trace_refs=trace_refs,
        producer="replay_verifier",
        payload={"step": "admitted"},
    )
    response_event = new_kernel_event(
        event_type=KernelEventType.RESPONSE_READY,
        turn=turn,
        trace_refs=trace_refs,
        producer="replay_verifier",
        payload={"step": "response"},
        response=KernelResponseSurface(
            response_text="Replay anchors are ready.",
            abstain_or_answer=AbstainOrAnswer.ANSWER,
            final_answer_mode=FinalAnswerMode.GROUNDED_FACT,
            memory_review_ref="memory://review/replay/turn-0001",
        ),
    )
    workspace.bind_event(admitted_event)
    bus.publish(admitted_event)
    workspace.bind_event(response_event)
    bus.publish(response_event)
    workspace.attach_evidence_ref("evidence://phase2/replay")

    trace_export = bus.trace_export()
    state_export = workspace.state_export()
    replay_record = ledger.record_replay(
        replay_id="replay-001",
        conversation_id=conversation_id,
        turn_id=turn_id,
        trace_export=trace_export,
        state_export=state_export,
        event_ids=[admitted_event.event_id, response_event.event_id],
    )
    matched = ledger.verify_replay(
        replay_id=replay_record.replay_id,
        trace_export=trace_export,
        state_export=state_export,
    )

    trace_mismatch_export = deepcopy(trace_export)
    trace_mismatch_export[0]["event_id"] = "evt-tampered-replay"
    trace_mismatch = ledger.verify_replay(
        replay_id=replay_record.replay_id,
        trace_export=trace_mismatch_export,
        state_export=state_export,
    )

    state_mismatch_export = deepcopy(state_export)
    state_mismatch_export["workspace_id"] = "tampered-workspace"
    state_mismatch = ledger.verify_replay(
        replay_id=replay_record.replay_id,
        trace_export=trace_export,
        state_export=state_mismatch_export,
    )

    if not matched["replay_match"]:
        raise AssertionError("replay verification did not match the recorded anchors")
    if trace_mismatch["trace_match"]:
        raise AssertionError("tampered trace export unexpectedly matched")
    if state_mismatch["state_match"]:
        raise AssertionError("tampered state export unexpectedly matched")

    return {
        "phase": "2",
        "slice": "4",
        "verifier": "verify_phase_02_replay",
        "status": "pass",
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "replay-runtime-importable", "result": "pass"},
            {"id": "replay-recorded-deterministic-anchors", "result": "pass"},
            {"id": "replay-match-proved", "result": "pass"},
            {"id": "replay-trace-mismatch-proved", "result": "pass"},
            {"id": "replay-state-mismatch-proved", "result": "pass"},
            {"id": "scheduler-dispatch-used", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "runtime_symbols": {
            "workspace_state": [
                "bind_event",
                "register_cell_anchor",
                "state_export",
                "attach_evidence_ref",
            ],
            "cell_registry": [
                "register_cell",
                "update_cell",
                "export_state",
            ],
            "lifecycle_engine": [
                "bootstrap_cell",
                "activate",
                "export_state",
            ],
            "scheduler": [
                "enqueue_task",
                "dispatch_next",
                "scheduler_metrics",
            ],
            "replay_ledger": [
                "record_replay",
                "verify_replay",
                "replay_export",
            ],
        },
        "anchors": {
            "replay_id": replay_record.replay_id,
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "trace_anchor_hash": replay_record.trace_anchor_hash,
            "state_anchor_hash": replay_record.state_anchor_hash,
            "trace_match": matched["trace_match"],
            "state_match": matched["state_match"],
            "trace_mismatch_match": trace_mismatch["trace_match"],
            "state_mismatch_match": state_mismatch["state_match"],
            "scheduler_dispatch": dispatched_task.to_dict(),
        },
        "notes": [
            "replay must remain deterministic and trace-anchored",
            "no approval implied",
        ],
    }


def build_blocked_report(missing: list[str]) -> dict[str, object]:
    return {
        "phase": "2",
        "slice": "4",
        "verifier": "verify_phase_02_replay",
        "status": "blocked",
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 2 slice 4 replay runtime files are not on disk yet.",
            "missing_files": missing,
        },
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "replay-runtime-present", "result": "blocked"},
            {"id": "replay-ledger-present", "result": "blocked"},
            {"id": "deterministic-replay-anchors-ready", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "replay must remain deterministic and trace-anchored",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(BASELINE_FILES + RUNTIME_FILES)
    if missing:
        report = build_blocked_report(missing)
        write_json(REPORT_PATH, report)
        print("phase_02 slice_4 replay verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    write_json(REPORT_PATH, report)
    print("phase_02 slice_4 replay verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
