from __future__ import annotations

import json

import _phase_09_verifier_common as vc
from agifcore_phase9_rich_expression.planning import PlanningEngine

VERIFIER = "verify_phase_09_planning"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_09_planning_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase9_rich_expression.contracts",
    "agifcore_phase9_rich_expression.planning",
)


def _case(*, request_id: str, live_measurement_required: bool) -> dict[str, object]:
    raw_text = "Plan the next checks carefully and stop if evidence is missing."
    intake = vc.build_phase7_intake_state(
        conversation_id="conv-p9-plan",
        turn_id=request_id,
        raw_text=raw_text,
    )
    support = vc.build_phase7_support_resolution_state(
        conversation_id="conv-p9-plan",
        turn_id=request_id,
        support_state="search_needed" if live_measurement_required else "grounded",
        knowledge_gap_reason="needs_fresh_information" if live_measurement_required else "none",
        next_action="search_external" if live_measurement_required else "answer",
        evidence_refs=("phase7.support.ref.020",),
        selected_domain_ids=("weather_climate",),
        reason_codes=("bounded_local_support",),
    )
    bounded = vc.build_phase8_bounded_current_world_reasoning_state(
        request_id=request_id,
        decision="needs_fresh_information" if live_measurement_required else "bounded_local_support",
        live_current_requested=live_measurement_required,
        needs_fresh_information=live_measurement_required,
        live_measurement_required=live_measurement_required,
        exact_current_fact_allowed=False,
        bounded_local_support_refs=("phase8.boundary.ref.020",),
        evidence_refs=("phase8.boundary.ref.020", "phase8.boundary.ref.021"),
        reason_codes=("fresh_measurement_required",) if live_measurement_required else ("bounded_local_support",),
    )
    summary = vc.build_phase8_visible_reasoning_summary_state(
        request_id=request_id,
        what_is_known=("A bounded answer exists only if evidence remains local.",),
        what_is_inferred=("The next step should preserve stop points.",),
        uncertainty=("Fresh data is required before stronger claims.",),
        what_would_verify=("Obtain a new measurement before answering.", "List any missing variables.",),
        principle_refs=("measurement_uncertainty",),
        causal_chain_ref="chain::plan::001",
        uncertainty_band="high" if live_measurement_required else "moderate",
        live_measurement_required=live_measurement_required,
        evidence_refs=("phase8.summary.ref.020",),
    )
    reflection = vc.build_phase8_science_reflection_state(
        request_id=request_id,
        records=(
            vc.build_science_reflection_record(
                record_id=f"reflect::{request_id}::01",
                kind="falsifier",
                note="Missing variable could change the next step.",
                source_ref="phase8.summary.ref.020",
                next_verification_step="List the missing variable explicitly.",
                increases_uncertainty=True,
            ),
        ),
        uncertainty_should_increase=live_measurement_required,
    )
    return {
        "intake": intake,
        "support": support,
        "bounded": bounded,
        "summary": summary,
        "reflection": reflection,
    }


def build_pass_report() -> dict[str, object]:
    engine = PlanningEngine()
    fixture = _case(request_id="turn-p9-plan-01", live_measurement_required=True)
    before = vc.deep_copy(fixture)
    snapshot = engine.build_snapshot(
        support_state_resolution_state=fixture["support"],
        bounded_current_world_reasoning_state=fixture["bounded"],
        visible_reasoning_summary_state=fixture["summary"],
        science_reflection_state=fixture["reflection"],
    )
    vc.assert_inputs_unchanged(before, fixture, "planning inputs")

    assert snapshot.step_count <= 10
    assert snapshot.step_count >= 3
    assert all(step.stop_if_unsure for step in snapshot.steps)
    assert any("fresh" in step.action.lower() for step in snapshot.steps)
    assert any("missing variable" in step.verification_hint.lower() or "reflection" in step.verification_hint.lower() for step in snapshot.steps)

    checked_files = vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_planning.py")
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "planning-steps-bounded", "result": "pass"},
            {"id": "stop-if-unsure-preserved", "result": "pass"},
            {"id": "fresh-measurement-step-added", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "fixture": fixture,
            "snapshot": snapshot.to_dict(),
        },
        notes=["planning lane outputs bounded steps only; it does not execute actions"],
    )


def main() -> int:
    missing = vc.missing_files(vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_planning.py"))
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_planning.py"),
            assertion_ids=["runtime-imports-available", "planning-steps-bounded", "stop-if-unsure-preserved"],
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="planning lane verifier could not import its runtime modules or found missing files",
            missing=missing,
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    try:
        report = build_pass_report()
    except Exception as exc:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=vc.checked_files_for("projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_planning.py"),
            assertion_ids=["runtime-imports-available", "planning-steps-bounded", "stop-if-unsure-preserved"],
            blocker_kind="verification_failed",
            blocker_message=str(exc),
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    vc.write_report(REPORT_PATH, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
