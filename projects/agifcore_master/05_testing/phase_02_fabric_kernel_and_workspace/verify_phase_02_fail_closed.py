from __future__ import annotations

import sys
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
KERNEL_ROOT = PROJECT_ROOT / "04_execution" / "phase_02_fabric_kernel_and_workspace" / "agifcore_phase2_kernel"
EVIDENCE_ROOT = PROJECT_ROOT / "06_outputs" / "phase_02_fabric_kernel_and_workspace" / "phase_02_evidence"

if str(KERNEL_ROOT) not in sys.path:
    sys.path.insert(0, str(KERNEL_ROOT))

from event_types import KnowledgeGapReason, NextAction, SupportState
from kernel_fail_closed import FailClosedAction, FailClosedReasonCode, KernelFailClosed

REPORT_PATH = EVIDENCE_ROOT / "phase_02_fail_closed_report.json"
MANIFEST_PATH = EVIDENCE_ROOT / "phase_02_evidence_manifest.json"

RUNTIME_FILES = [
    KERNEL_ROOT / "workspace_state.py",
    KERNEL_ROOT / "cell_registry.py",
    KERNEL_ROOT / "lifecycle_engine.py",
    KERNEL_ROOT / "scheduler.py",
    KERNEL_ROOT / "replay_ledger.py",
    KERNEL_ROOT / "rollback_controller.py",
    KERNEL_ROOT / "quarantine_controller.py",
    KERNEL_ROOT / "kernel_fail_closed.py",
]

BASELINE_FILES = [
    KERNEL_ROOT / "event_types.py",
    KERNEL_ROOT / "event_bus.py",
    PROJECT_ROOT / "01_plan" / "PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md",
    PROJECT_ROOT / "01_plan" / "TRACE_CONTRACT.md",
    PROJECT_ROOT / "03_design" / "GOVERNANCE_MODEL.md",
    PROJECT_ROOT / "03_design" / "SANDBOX_MODEL.md",
]


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def build_pass_report() -> dict[str, object]:
    kernel = KernelFailClosed()

    unsafe_answer = kernel.evaluate_support_state(
        support_state=SupportState.UNKNOWN,
        knowledge_gap_reason=KnowledgeGapReason.NONE,
        next_action=NextAction.ANSWER,
        context={"case": "unsafe-answer"},
    )
    policy_blocked = kernel.evaluate_support_state(
        support_state=SupportState.GROUNDED,
        knowledge_gap_reason=KnowledgeGapReason.BLOCKED_BY_POLICY,
        next_action=NextAction.CLARIFY,
        context={"case": "policy-blocked"},
    )
    safe_allowed = kernel.evaluate_support_state(
        support_state=SupportState.GROUNDED,
        knowledge_gap_reason=KnowledgeGapReason.NONE,
        next_action=NextAction.ANSWER,
        context={"case": "safe-answer"},
    )
    explicit_allow = kernel.allow(message="safe answer allowed", context={"case": "explicit-allow"})

    if not unsafe_answer.blocked:
        raise AssertionError("unsafe answer was not blocked")
    if unsafe_answer.reason_code != FailClosedReasonCode.SUPPORT_STATE_BLOCK.value:
        raise AssertionError("unsafe answer did not carry the support-state reason code")
    if unsafe_answer.action != FailClosedAction.HALT_TURN.value:
        raise AssertionError("unsafe answer did not halt the turn")
    if not policy_blocked.blocked:
        raise AssertionError("policy-blocked case was not blocked")
    if policy_blocked.reason_code != FailClosedReasonCode.POLICY_BLOCKED.value:
        raise AssertionError("policy-blocked case did not carry the policy reason code")
    if policy_blocked.action != FailClosedAction.ESCALATE_GOVERNOR.value:
        raise AssertionError("policy-blocked case did not escalate to governor")
    if safe_allowed.blocked:
        raise AssertionError("safe allowed case was unexpectedly blocked")
    if safe_allowed.reason_code is not None:
        raise AssertionError("safe allowed case should not carry a reason code")
    if safe_allowed.action != FailClosedAction.HALT_TURN.value:
        raise AssertionError("safe allowed case did not retain the allow action field")
    if explicit_allow.blocked:
        raise AssertionError("explicit allow decision was unexpectedly blocked")

    return {
        "phase": "2",
        "slice": "4",
        "verifier": "verify_phase_02_fail_closed",
        "status": "pass",
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "unsafe-answer-blocked", "result": "pass"},
            {"id": "policy-blocked-case-escalated", "result": "pass"},
            {"id": "safe-allowed-case-remains-allowed", "result": "pass"},
            {"id": "explicit-reason-action-fields-present", "result": "pass"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "runtime_symbols": {
            "kernel_fail_closed": [
                "allow",
                "block",
                "enforce_condition",
                "evaluate_support_state",
                "decisions_export",
            ],
            "reason_codes": [
                FailClosedReasonCode.SUPPORT_STATE_BLOCK.value,
                FailClosedReasonCode.POLICY_BLOCKED.value,
                FailClosedReasonCode.QUARANTINE_REQUIRED.value,
            ],
            "actions": [
                FailClosedAction.HALT_TURN.value,
                FailClosedAction.ESCALATE_GOVERNOR.value,
            ],
        },
        "decision_results": {
            "unsafe_answer": unsafe_answer.to_dict(),
            "policy_blocked": policy_blocked.to_dict(),
            "safe_allowed": safe_allowed.to_dict(),
            "explicit_allow": explicit_allow.to_dict(),
        },
        "notes": [
            "fail-closed must stop unsafe continuation explicitly",
            "no approval implied",
        ],
    }


def build_blocked_report(missing: list[str]) -> dict[str, object]:
    return {
        "phase": "2",
        "slice": "4",
        "verifier": "verify_phase_02_fail_closed",
        "status": "blocked",
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 2 slice 4 fail-closed runtime files are not on disk yet.",
            "missing_files": missing,
        },
        "checked_files": [rel(path) for path in BASELINE_FILES + RUNTIME_FILES],
        "assertions": [
            {"id": "fail-closed-runtime-present", "result": "blocked"},
            {"id": "fail-closed-refusal-path-ready", "result": "blocked"},
            {"id": "safe-stop-path-explicit", "result": "blocked"},
        ],
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "fail-closed is part of slice 4",
            "no approval implied",
        ],
    }


def main() -> int:
    missing = missing_files(BASELINE_FILES + RUNTIME_FILES)
    if missing:
        report = build_blocked_report(missing)
        write_json(REPORT_PATH, report)
        print("phase_02 slice_4 fail_closed verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_pass_report()
    write_json(REPORT_PATH, report)
    print("phase_02 slice_4 fail_closed verifier: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
