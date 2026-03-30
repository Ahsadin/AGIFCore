from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
KERNEL_ROOT = PROJECT_ROOT / "04_execution" / "phase_02_fabric_kernel_and_workspace" / "agifcore_phase2_kernel"
EVIDENCE_ROOT = PROJECT_ROOT / "06_outputs" / "phase_02_fabric_kernel_and_workspace" / "phase_02_evidence"

REPORT_PATH = EVIDENCE_ROOT / "phase_02_scheduler_report.json"
MANIFEST_PATH = EVIDENCE_ROOT / "phase_02_evidence_manifest.json"

RUNTIME_FILES = [
    KERNEL_ROOT / "workspace_state.py",
    KERNEL_ROOT / "cell_registry.py",
    KERNEL_ROOT / "lifecycle_engine.py",
    KERNEL_ROOT / "scheduler.py",
]

BASELINE_FILES = [
    KERNEL_ROOT / "event_types.py",
    KERNEL_ROOT / "event_bus.py",
    PROJECT_ROOT / "01_plan" / "PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md",
    PROJECT_ROOT / "03_design" / "GOVERNANCE_MODEL.md",
    PROJECT_ROOT / "03_design" / "FORMAL_MODELS.md",
]

sys.path.insert(0, str(KERNEL_ROOT))

from scheduler import Scheduler, SchedulerCapacityError, SchedulerTaskError  # noqa: E402


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def build_blocked_report(missing: list[str]) -> dict[str, object]:
    return {
        "phase": "2",
        "slice": "3",
        "verifier": "verify_phase_02_scheduler",
        "status": "blocked",
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 2 slice 3 scheduler runtime files are not on disk yet.",
            "missing_files": missing,
        },
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "scheduler-runtime-present", "result": "blocked"},
            {"id": "scheduler-budget-envelope-ready", "result": "blocked"},
            {"id": "scheduler-queue-depth-bounded", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "scheduler is part of slice 3 and follows lifecycle",
            "no approval implied",
        ],
    }


def build_pass_report() -> dict[str, object]:
    scheduler = Scheduler(max_queue_depth=3, latency_target_ms=50)
    task_one = scheduler.enqueue_task(
        task_id="task-1",
        cell_id="cell-scheduler",
        priority=1,
        need_score=0.2,
        estimated_cost=1.0,
        payload={"kind": "alpha"},
    )
    task_two = scheduler.enqueue_task(
        task_id="task-2",
        cell_id="cell-scheduler",
        priority=3,
        need_score=0.1,
        estimated_cost=1.0,
        payload={"kind": "beta"},
    )
    task_three = scheduler.enqueue_task(
        task_id="task-3",
        cell_id="cell-scheduler",
        priority=1,
        need_score=0.9,
        estimated_cost=1.0,
        payload={"kind": "gamma"},
    )

    queue_before_dispatch = scheduler.queue_export()
    if scheduler.queue_depth() != 3:
        raise AssertionError("scheduler queue depth did not track enqueues")
    if [item["task_id"] for item in queue_before_dispatch] != ["task-2", "task-3", "task-1"]:
        raise AssertionError("scheduler queue order did not honor priority and need_score")

    dispatched = [scheduler.dispatch_next(), scheduler.dispatch_next(), scheduler.dispatch_next()]
    if [task.task_id for task in dispatched if task is not None] != ["task-2", "task-3", "task-1"]:
        raise AssertionError("scheduler dispatch order did not match queue order")

    metrics = scheduler.scheduler_metrics()
    if metrics["enqueue_count"] != 3 or metrics["dispatch_count"] != 3:
        raise AssertionError("scheduler metrics did not track enqueue/dispatch counts")
    if metrics["queue_depth"] != 0:
        raise AssertionError("scheduler queue depth did not return to zero")
    if metrics["max_observed_depth"] != 3:
        raise AssertionError("scheduler max observed depth mismatch")
    if metrics["latency_target_ms"] != 50:
        raise AssertionError("scheduler latency target mismatch")
    if metrics["last_dispatch_latency_ms"] is None:
        raise AssertionError("scheduler did not record dispatch latency")

    capacity_scheduler = Scheduler(max_queue_depth=1)
    capacity_scheduler.enqueue_task(
        task_id="capacity-1",
        cell_id="cell-capacity",
        priority=1,
        need_score=0.1,
        estimated_cost=1.0,
        payload={"kind": "capacity"},
    )
    capacity_error = None
    try:
        capacity_scheduler.enqueue_task(
            task_id="capacity-2",
            cell_id="cell-capacity",
            priority=1,
            need_score=0.1,
            estimated_cost=1.0,
            payload={"kind": "capacity"},
        )
    except SchedulerCapacityError as exc:
        capacity_error = str(exc)
    if capacity_error is None:
        raise AssertionError("scheduler capacity bound did not raise an error")

    payload_error = None
    oversized_payload = {"blob": "x" * (256 * 1024 + 1)}
    try:
        scheduler.enqueue_task(
            task_id="task-too-large",
            cell_id="cell-scheduler",
            priority=1,
            need_score=0.1,
            estimated_cost=1.0,
            payload=oversized_payload,
        )
    except SchedulerTaskError as exc:
        payload_error = str(exc)
    if payload_error is None:
        raise AssertionError("scheduler payload size bound did not raise an error")

    return {
        "phase": "2",
        "slice": "3",
        "verifier": "verify_phase_02_scheduler",
        "status": "pass",
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "scheduler-runtime-importable", "result": "pass"},
            {"id": "scheduler-enqueue-order-bounded", "result": "pass"},
            {"id": "scheduler-queue-depth-bound-enforced", "result": "pass"},
            {"id": "scheduler-payload-size-bound-enforced", "result": "pass"},
            {"id": "scheduler-dispatch-metrics-tracked", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "runtime_symbols": {
            "scheduler": [name for name in dir(Scheduler) if not name.startswith("_")],
            "task": [name for name in dir(task_one) if not name.startswith("_")],
        },
        "notes": [
            "scheduler must stay inside the planning ceilings and remain inspectable",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(BASELINE_FILES + RUNTIME_FILES)
    if missing:
        report = build_blocked_report(missing)
        write_json(REPORT_PATH, report)
        print("phase_02 slice_3 scheduler verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    write_json(REPORT_PATH, report)
    print("phase_02 slice_3 scheduler verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
