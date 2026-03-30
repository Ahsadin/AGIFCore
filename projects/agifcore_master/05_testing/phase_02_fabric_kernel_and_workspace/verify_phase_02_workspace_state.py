from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
KERNEL_ROOT = (
    PROJECT_ROOT / "04_execution" / "phase_02_fabric_kernel_and_workspace" / "agifcore_phase2_kernel"
)
EVIDENCE_ROOT = (
    PROJECT_ROOT / "06_outputs" / "phase_02_fabric_kernel_and_workspace" / "phase_02_evidence"
)

REPORT_PATH = EVIDENCE_ROOT / "phase_02_workspace_state_report.json"
MANIFEST_PATH = EVIDENCE_ROOT / "phase_02_evidence_manifest.json"

RUNTIME_FILES = [
    KERNEL_ROOT / "workspace_state.py",
    KERNEL_ROOT / "cell_registry.py",
]

BASELINE_FILES = [
    KERNEL_ROOT / "event_types.py",
    KERNEL_ROOT / "event_bus.py",
    PROJECT_ROOT / "01_plan" / "PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md",
    PROJECT_ROOT / "03_design" / "WORKSPACE_MODEL.md",
]

sys.path.insert(0, str(KERNEL_ROOT))

from cell_registry import CellRegistry  # noqa: E402
from event_bus import EventBus  # noqa: E402
from event_types import (  # noqa: E402
    AbstainOrAnswer,
    DiscourseMode,
    FinalAnswerMode,
    KernelEventType,
    KernelResponseSurface,
    KernelTraceRefs,
    KernelTurnContext,
    KnowledgeGapReason,
    NextAction,
    SupportState,
    new_kernel_event,
)
from workspace_state import SharedWorkspaceState  # noqa: E402


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def load_json(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def build_blocked_report(missing: list[str]) -> dict[str, object]:
    return {
        "phase": "2",
        "slice": "2",
        "verifier": "verify_phase_02_workspace_state",
        "status": "blocked",
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 2 slice 2 runtime files are not on disk yet.",
            "missing_files": missing,
        },
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "workspace-runtime-present", "result": "blocked"},
            {"id": "cell-registry-runtime-present", "result": "blocked"},
            {"id": "memory-hook-boundary-review-ready", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "workspace and registry are the planned slice-2 targets",
            "phase 2 remains open",
            "no approval implied",
        ],
    }


def build_behavior_report() -> dict[str, object]:
    workspace = SharedWorkspaceState(workspace_id="phase-02-workspace")
    registry = CellRegistry()
    bus = EventBus()
    handled_events: list[str] = []

    def bind(event) -> None:
        workspace.bind_event(event)
        handled_events.append(event.event_type.value)

    bus.subscribe(KernelEventType.TURN_ADMITTED, bind)
    bus.subscribe(KernelEventType.RESPONSE_READY, bind)

    turn = KernelTurnContext(
        conversation_id="conv-phase2-slice2",
        turn_id="turn-0002",
        user_intent="verify slice-2 workspace and registry behavior",
        discourse_mode=DiscourseMode.EXPLAIN,
        support_state=SupportState.GROUNDED,
        knowledge_gap_reason=KnowledgeGapReason.NONE,
        next_action=NextAction.ANSWER,
        active_context_refs=("ctx://phase2/slice2",),
    )
    trace_refs = KernelTraceRefs(
        planner_trace_ref="trace://planner/turn-0002",
        simulation_trace_ref="trace://simulation/turn-0002",
        critic_trace_ref="trace://critic/turn-0002",
        governance_trace_ref="trace://governance/turn-0002",
    )

    registry_record = registry.register_cell(
        cell_id="cell-0001",
        role_family="kernel",
        lifecycle_state="active",
        workspace_ref=workspace.cell_ref("cell-0001"),
        metadata={"source": "slice-2-verifier"},
    )
    workspace.register_cell_anchor(
        cell_id="cell-0001",
        role_family="kernel",
        lifecycle_state="active",
        workspace_ref=workspace.cell_ref("cell-0001"),
    )

    admitted = new_kernel_event(
        event_type=KernelEventType.TURN_ADMITTED,
        turn=turn,
        trace_refs=trace_refs,
        producer="workspace_registry_verifier",
        payload={"channel": "workspace"},
    )
    response = KernelResponseSurface(
        response_text="Workspace and registry anchors remain bounded and replayable.",
        abstain_or_answer=AbstainOrAnswer.ANSWER,
        final_answer_mode=FinalAnswerMode.GROUNDED_FACT,
        memory_review_ref="memory://review/phase2-slice2-turn-0002",
    )
    completed = new_kernel_event(
        event_type=KernelEventType.RESPONSE_READY,
        turn=turn,
        trace_refs=trace_refs,
        producer="workspace_registry_verifier",
        payload={"channel": "workspace"},
        response=response,
    )

    bus.publish(admitted)
    bus.publish(completed)

    workspace.attach_replay_ref("replay://phase2/slice2/0001")
    workspace.attach_rollback_ref("rollback://phase2/slice2/0001")
    workspace.attach_quarantine_ref("quarantine://phase2/slice2/0001")
    workspace.attach_evidence_ref("evidence://phase2/slice2/0001")
    workspace.update_cell_anchor(
        "cell-0001",
        lifecycle_state="active",
        workspace_ref=workspace.cell_ref("cell-0001"),
        quarantine_ref="quarantine://phase2/slice2/0001",
        rollback_ref="rollback://phase2/slice2/0001",
    )

    state_export = workspace.state_export()
    memory_review_export = workspace.memory_review_export()
    registry_export = registry.export_state()

    workspace_clone = SharedWorkspaceState()
    workspace_clone.load_export(state_export)
    registry_clone = CellRegistry()
    registry_clone.load_export(registry_export)

    if handled_events != [KernelEventType.TURN_ADMITTED.value, KernelEventType.RESPONSE_READY.value]:
        raise AssertionError("workspace ingest did not preserve event order")
    if len(state_export["turns"]) != 1:
        raise AssertionError("workspace should export one record per conversation_id + turn_id anchor")
    turn_record = state_export["turns"][0]
    if turn_record["conversation_id"] != "conv-phase2-slice2":
        raise AssertionError("conversation_id anchor was not preserved")
    if turn_record["turn_id"] != "turn-0002":
        raise AssertionError("turn_id anchor was not preserved")
    if turn_record["response_text"] != response.response_text:
        raise AssertionError("response surface was not preserved")
    if turn_record["final_answer_mode"] != response.final_answer_mode.value:
        raise AssertionError("final answer mode was not preserved")
    if turn_record["memory_review_ref"] != response.memory_review_ref:
        raise AssertionError("memory review ref was not preserved on the turn record")
    if state_export["memory_hook_surface"]["memory_review_refs"][0]["memory_review_ref"] != response.memory_review_ref:
        raise AssertionError("memory review ref was not exported")
    forbidden_memory_keys = {
        "long_term_memory",
        "semantic_memory",
        "procedural_memory",
        "graph_persistence",
        "memory_store",
    }
    if forbidden_memory_keys & set(state_export.keys()):
        raise AssertionError("workspace export leaked long-term memory keys")
    if memory_review_export["memory_review_refs"][0]["turn_id"] != "turn-0002":
        raise AssertionError("memory review export did not preserve turn anchor")
    if memory_review_export["retention_candidate_refs"] != []:
        raise AssertionError("retention candidates should be empty for slice 2")
    if workspace_clone.state_export() != state_export:
        raise AssertionError("workspace export did not round-trip cleanly")
    if registry_clone.export_state() != registry_export:
        raise AssertionError("registry export did not round-trip cleanly")
    if registry_record["workspace_ref"] != workspace.cell_ref("cell-0001"):
        raise AssertionError("registry workspace ref mismatch")

    return {
        "phase": "2",
        "slice": "2",
        "verifier": "verify_phase_02_workspace_state",
        "status": "pass",
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "workspace-runtime-importable", "result": "pass"},
            {"id": "cell-registry-runtime-importable", "result": "pass"},
            {"id": "workspace-ingest-preserves-anchors", "result": "pass"},
            {"id": "workspace-memory-review-boundary", "result": "pass"},
            {"id": "registry-export-roundtrip", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "runtime_symbols": {
            "workspace_state": [name for name in dir(SharedWorkspaceState) if not name.startswith("_")],
            "cell_registry": [name for name in dir(CellRegistry) if not name.startswith("_")],
        },
        "trace_event_order": handled_events,
        "notes": [
            "workspace hooks remain bounded",
            "no semantic memory or graph persistence",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(RUNTIME_FILES)
    if missing:
        report = build_blocked_report(missing)
        write_json(REPORT_PATH, report)
        print("phase_02 slice_2 workspace_state verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    try:
        report = build_behavior_report()
    except AssertionError as exc:
        report = {
            "phase": "2",
            "slice": "2",
            "verifier": "verify_phase_02_workspace_state",
            "status": "fail",
            "failure": str(exc),
            "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
            "outputs": {
                "report": rel(REPORT_PATH),
                "manifest": rel(MANIFEST_PATH),
            },
            "notes": ["no approval implied"],
        }
        write_json(REPORT_PATH, report)
        print("phase_02 slice_2 workspace_state verifier: FAIL")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    write_json(REPORT_PATH, report)
    print("phase_02 slice_2 workspace_state verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
