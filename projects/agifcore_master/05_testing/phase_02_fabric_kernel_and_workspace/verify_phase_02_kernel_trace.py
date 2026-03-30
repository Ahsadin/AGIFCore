from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
KERNEL_ROOT = (
    PROJECT_ROOT
    / "04_execution"
    / "phase_02_fabric_kernel_and_workspace"
    / "agifcore_phase2_kernel"
)
EVIDENCE_ROOT = (
    PROJECT_ROOT
    / "06_outputs"
    / "phase_02_fabric_kernel_and_workspace"
    / "phase_02_evidence"
)
DEMO_ROOT = (
    PROJECT_ROOT
    / "06_outputs"
    / "phase_02_fabric_kernel_and_workspace"
    / "phase_02_demo_bundle"
)

sys.path.insert(0, str(KERNEL_ROOT))

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


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_demo(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_aggregate_manifest(evidence_manifest_path: Path) -> dict[str, object]:
    report_specs = [
        ("phase_02_kernel_trace_report.json", "slice1-kernel-trace-report"),
        ("phase_02_workspace_state_report.json", "slice2-workspace-state-report"),
        ("phase_02_lifecycle_report.json", "slice3-lifecycle-report"),
        ("phase_02_scheduler_report.json", "slice3-scheduler-report"),
        ("phase_02_replay_report.json", "slice4-replay-report"),
        ("phase_02_rollback_quarantine_report.json", "slice4-rollback-quarantine-report"),
        ("phase_02_fail_closed_report.json", "slice4-fail-closed-report"),
    ]
    checked_files: list[str] = []
    seen_files: set[str] = set()
    assertions: list[dict[str, str]] = []
    missing_reports: list[str] = []
    outputs: dict[str, str] = {
        "evidence_manifest": str(evidence_manifest_path.relative_to(REPO_ROOT)),
        "demo_index": str((DEMO_ROOT / "phase_02_demo_index.md").relative_to(REPO_ROOT)),
    }

    for filename, assertion_id in report_specs:
        report_path = EVIDENCE_ROOT / filename
        outputs[filename.removesuffix(".json")] = str(report_path.relative_to(REPO_ROOT))
        if not report_path.exists():
            assertions.append({"id": assertion_id, "result": "missing"})
            missing_reports.append(filename)
            continue
        payload = read_json(report_path)
        status = str(payload.get("status", "unknown"))
        assertions.append({"id": assertion_id, "result": "pass" if status == "pass" else status})
        for file_path in payload.get("checked_files", []):
            if file_path not in seen_files:
                checked_files.append(file_path)
                seen_files.add(file_path)

    demo_files = [
        "phase_02_kernel_trace_demo.md",
        "phase_02_shared_workspace_demo.md",
        "phase_02_replay_demo.md",
        "phase_02_rollback_quarantine_demo.md",
        "phase_02_demo_index.md",
    ]
    for filename in demo_files:
        demo_path = DEMO_ROOT / filename
        if demo_path.exists():
            outputs[filename.removesuffix(".md")] = str(demo_path.relative_to(REPO_ROOT))

    notes = [
        "aggregate Phase 2 evidence index",
        "phase 2 remains open",
        "no phase approval implied",
    ]
    if missing_reports:
        notes.insert(1, f"missing evidence reports: {', '.join(missing_reports)}")
        status = "incomplete"
    else:
        notes.insert(1, "slice 1 through slice 4 outputs are now referenced")
        status = "pass" if all(item["result"] == "pass" for item in assertions) else "incomplete"

    return {
        "phase": "2",
        "slice": "aggregate",
        "verifier": "phase_02_evidence_manifest",
        "status": status,
        "checked_files": checked_files,
        "assertions": assertions,
        "outputs": outputs,
        "notes": notes,
    }


def run_verifier() -> tuple[dict[str, object], dict[str, object], Path]:
    bus = EventBus()
    handled_events: list[str] = []

    bus.subscribe(KernelEventType.TURN_ADMITTED, lambda event: handled_events.append(event.event_type.value))
    bus.subscribe(KernelEventType.RESPONSE_READY, lambda event: handled_events.append(event.event_type.value))

    turn = KernelTurnContext(
        conversation_id="conv-phase2-slice1",
        turn_id="turn-0001",
        user_intent="verify slice-1 kernel trace substrate",
        discourse_mode=DiscourseMode.EXPLAIN,
        support_state=SupportState.GROUNDED,
        knowledge_gap_reason=KnowledgeGapReason.NONE,
        next_action=NextAction.ANSWER,
        active_context_refs=("ctx://phase2/slice1",),
    )
    trace_refs = KernelTraceRefs(
        planner_trace_ref="trace://planner/turn-0001",
        simulation_trace_ref="trace://simulation/turn-0001",
        critic_trace_ref="trace://critic/turn-0001",
        governance_trace_ref="trace://governance/turn-0001",
    )

    admitted = new_kernel_event(
        event_type=KernelEventType.TURN_ADMITTED,
        turn=turn,
        trace_refs=trace_refs,
        producer="kernel_trace_verifier",
        payload={"admission_source": "slice_1_verifier"},
    )
    response = KernelResponseSurface(
        response_text="Slice 1 event fabric is present and trace-aligned.",
        abstain_or_answer=AbstainOrAnswer.ANSWER,
        final_answer_mode=FinalAnswerMode.GROUNDED_FACT,
        memory_review_ref="memory://review/phase2-slice1-turn-0001",
    )
    completed = new_kernel_event(
        event_type=KernelEventType.RESPONSE_READY,
        turn=turn,
        trace_refs=trace_refs,
        producer="kernel_trace_verifier",
        payload={"render_surface": "local_desktop_ui"},
        response=response,
    )

    bus.publish(admitted)
    bus.publish(completed)

    trace_export = bus.trace_export()
    event_export = bus.event_export()

    runtime_files = [
        KERNEL_ROOT / "event_types.py",
        KERNEL_ROOT / "event_bus.py",
    ]
    for runtime_file in runtime_files:
        ensure(runtime_file.exists(), f"missing runtime file: {runtime_file}")

    ensure(len(event_export) == 2, "slice 1 should emit exactly two verification events")
    ensure(len(trace_export) == 2, "slice 1 trace export should contain two records")
    ensure(
        handled_events == [KernelEventType.TURN_ADMITTED.value, KernelEventType.RESPONSE_READY.value],
        "expected turn_admitted then response_ready handler order",
    )
    ensure(
        trace_export[0]["event_type"] == KernelEventType.TURN_ADMITTED.value
        and trace_export[1]["event_type"] == KernelEventType.RESPONSE_READY.value,
        "slice 1 proof must remain limited to event_types/event_bus behavior",
    )
    ensure(
        all(record["conversation_id"] == "conv-phase2-slice1" for record in trace_export),
        "trace export must preserve stable conversation anchors",
    )
    ensure(
        all(record["turn_id"] == "turn-0001" for record in trace_export),
        "trace export must preserve stable turn anchors",
    )
    ensure(
        trace_export[0]["support_state"] == SupportState.GROUNDED.value,
        "support_state must remain honest and explicit",
    )
    ensure(
        trace_export[1]["final_answer_mode"] == FinalAnswerMode.GROUNDED_FACT.value,
        "response event must preserve final_answer_mode",
    )

    evidence_manifest_path = EVIDENCE_ROOT / "phase_02_evidence_manifest.json"
    trace_report_path = EVIDENCE_ROOT / "phase_02_kernel_trace_report.json"
    demo_path = DEMO_ROOT / "phase_02_kernel_trace_demo.md"

    assertions = [
        {"id": "slice1-event-types-exist", "result": "pass"},
        {"id": "slice1-event-bus-exists", "result": "pass"},
        {"id": "slice1-trace-contract-alignment", "result": "pass"},
        {"id": "slice1-bounded-to-event-layer", "result": "pass"},
    ]

    trace_report = {
        "phase": "2",
        "slice": "1",
        "status": "pass",
        "trace_event_count": len(trace_export),
        "handled_event_order": handled_events,
        "trace_export": trace_export,
        "event_export": event_export,
        "boundary_note": "workspace, registry, lifecycle, scheduler, replay, rollback, quarantine, and fail-closed are not part of slice 1",
    }

    demo_lines = [
        "# Phase 2 Slice 1 Kernel Trace Demo",
        "",
        "## Scope",
        "",
        "- Covers only `event_types.py`, `event_bus.py`, and `verify_phase_02_kernel_trace.py`.",
        "",
        "## What Exists",
        "",
        "- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_types.py`",
        "- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_bus.py`",
        "- `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_kernel_trace.py`",
        "",
        "## What Was Checked",
        "",
        "- Typed slice-1 event structures exist.",
        "- The governed event bus admits and dispatches slice-1 events.",
        "- Stable conversation and turn anchors are preserved in trace export.",
        "- Slice 1 proof is limited to `event_types.py` and `event_bus.py` behavior.",
        "",
        "## Evidence",
        "",
        f"- Evidence manifest: `{evidence_manifest_path.relative_to(REPO_ROOT)}`",
        f"- Trace report: `{trace_report_path.relative_to(REPO_ROOT)}`",
        "",
        "## Result",
        "",
        "- Slice 1 kernel-trace verification passed.",
        "",
        "## Boundary Note",
        "",
        "- Workspace, registry, lifecycle, scheduler, replay, rollback, quarantine, and fail-closed are not part of slice 1.",
        "",
        "## Gate Note",
        "",
        "- Phase 2 remains `open`.",
        "- No phase approval is implied.",
    ]

    write_json(trace_report_path, trace_report)
    write_demo(demo_path, demo_lines)
    evidence_manifest = build_aggregate_manifest(evidence_manifest_path)
    write_json(evidence_manifest_path, evidence_manifest)

    return evidence_manifest, trace_report, demo_path


def main() -> int:
    evidence_manifest, trace_report, demo_path = run_verifier()
    trace_report_output = evidence_manifest["outputs"].get(
        "phase_02_kernel_trace_report",
        evidence_manifest["outputs"].get("trace_report", "unknown"),
    )
    print("phase_02 slice_1 kernel trace verifier: PASS")
    print(
        f"evidence={trace_report_output} demo={demo_path.relative_to(REPO_ROOT)} "
        f"events={trace_report['trace_event_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
