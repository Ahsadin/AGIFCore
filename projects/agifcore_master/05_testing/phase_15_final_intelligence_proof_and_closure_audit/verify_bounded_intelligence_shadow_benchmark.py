from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import _phase_15_verifier_common as vc
import verify_bounded_intelligence_gate as base

VERIFIER = "verify_bounded_intelligence_shadow_benchmark"
VERIFIER_FILE = (
    "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_shadow_benchmark.py"
)
BENCHMARK_PATH = vc.TEST_ROOT / "bounded_intelligence_shadow_benchmark.json"
REPORT_PATH = vc.EVIDENCE_DIR / "bounded_intelligence_shadow_report.json"
SUMMARY_PATH = vc.EVIDENCE_DIR / "bounded_intelligence_shadow_summary.json"
FAILURE_SUMMARY_PATH = vc.EVIDENCE_DIR / "bounded_intelligence_shadow_failure_summary.json"


def load_benchmark() -> dict[str, Any]:
    return json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))


def build_outputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    benchmark = load_benchmark()
    cases = benchmark["cases"]
    session_shells: dict[tuple[str, str], Any] = {}
    records: list[dict[str, Any]] = []
    failure_counts: Counter[str] = Counter()
    class_totals: Counter[str] = Counter()
    class_passes: Counter[str] = Counter()
    hard_fail_reasons: list[str] = []

    for case in cases:
        session_key = (case["scenario"], case["session_group"])
        if session_key not in session_shells:
            session_shells[session_key] = base.new_phase13_shell(case["scenario"])
        shell = session_shells[session_key]
        result = shell.interactive_turn(user_text=case["prompt"])
        record = base._record_for_case(case, result)
        passed, failure_type, short_reason, all_failures, hard_fail = base.evaluate_case(case, result)
        record["pass_or_fail"] = "pass" if passed else "fail"
        record["primary_failure_type"] = failure_type
        record["short_failure_reason"] = short_reason
        record["all_failure_reasons"] = all_failures
        records.append(record)

        class_group = case["class_group"]
        class_totals[class_group] += 1
        if passed:
            class_passes[class_group] += 1
        failure_counts[failure_type] += 1
        if hard_fail:
            hard_fail_reasons.append(f"{case['id']}: {short_reason}")

    prompt_count = len(records)
    passed_count = sum(1 for item in records if item["pass_or_fail"] == "pass")
    failed_count = prompt_count - passed_count
    overall_pass_rate = passed_count / prompt_count if prompt_count else 0.0

    class_results: dict[str, dict[str, Any]] = {}
    for class_group, total in sorted(class_totals.items()):
        passed = class_passes[class_group]
        class_results[class_group] = {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total else 0.0,
        }

    shadow_passed = overall_pass_rate >= base.CLASS_THRESHOLDS["overall"] and not hard_fail_reasons

    report = {
        "benchmark_id": benchmark["benchmark_id"],
        "benchmark_version": benchmark["version"],
        "prompt_count": prompt_count,
        "status": "bounded_intelligence_shadow_pass" if shadow_passed else "bounded_intelligence_shadow_fail",
        "shadow_passed": shadow_passed,
        "records": records,
        "notes": [
            "shadow benchmark for anti-shortcut integrity only",
            "frozen bounded gate remains the canonical closeout gate",
            "no approval implied",
        ],
    }

    summary = {
        "benchmark_id": benchmark["benchmark_id"],
        "prompt_count": prompt_count,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "overall_pass_rate": overall_pass_rate,
        "class_results": class_results,
        "hard_fail_count": len(hard_fail_reasons),
        "hard_fail_reasons": hard_fail_reasons,
        "failure_counts_by_primary_failure_type": dict(sorted(failure_counts.items())),
        "shadow_passed": shadow_passed,
    }

    ranked_failures = sorted(
        (
            {
                "case_id": item["case_id"],
                "class_group": item["class_group"],
                "primary_failure_type": item["primary_failure_type"],
                "short_failure_reason": item["short_failure_reason"],
            }
            for item in records
            if item["pass_or_fail"] == "fail"
        ),
        key=lambda item: (item["primary_failure_type"], item["case_id"]),
    )

    failure_summary = {
        "benchmark_id": benchmark["benchmark_id"],
        "shadow_passed": shadow_passed,
        "failure_counts_by_primary_failure_type": dict(sorted(failure_counts.items())),
        "hard_fail_reasons": hard_fail_reasons,
        "ranked_failures": ranked_failures,
        "next_step": (
            "shadow benchmark supports the frozen gate integrity review"
            if shadow_passed
            else "runtime still shows wording-sensitive behavior beyond the frozen benchmark"
        ),
    }
    return report, summary, failure_summary


def main() -> int:
    missing = vc.missing_files([VERIFIER_FILE, str(BENCHMARK_PATH.relative_to(vc.REPO_ROOT))])
    if missing:
        raise SystemExit(f"missing shadow benchmark inputs: {missing}")
    if not vc.runtime_modules_available(base.REQUIRED_MODULES):
        raise SystemExit("required runtime modules for bounded-intelligence shadow benchmark are unavailable")

    report, summary, failure_summary = build_outputs()
    vc.dump_json(REPORT_PATH, report)
    vc.dump_json(SUMMARY_PATH, summary)
    vc.dump_json(FAILURE_SUMMARY_PATH, failure_summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
