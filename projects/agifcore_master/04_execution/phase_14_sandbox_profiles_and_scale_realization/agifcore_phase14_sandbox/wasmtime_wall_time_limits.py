from __future__ import annotations

from .contracts import (
    MAX_WASMTIME_LIMIT_CLASSES,
    POLICY_CLASS_IDS,
    WASMTIME_WALL_TIME_LIMITS_SCHEMA,
    require_non_empty_str,
    stable_hash_payload,
)


WALL_TIME_LIMIT_CLASSES = {
    "mobile_constrained": {
        "class_id": "mobile_constrained",
        "wall_time_ms": 250,
        "notes": ["mobile profile uses the smallest bounded wall-time class"],
    },
    "laptop_default": {
        "class_id": "laptop_default",
        "wall_time_ms": 1000,
        "notes": ["laptop profile inherits the donor-side reference Wasmtime wall-time limit"],
    },
    "builder_diagnostic": {
        "class_id": "builder_diagnostic",
        "wall_time_ms": 2000,
        "notes": ["builder may widen diagnostics but must stay explicit and bounded"],
    },
    "strict_fail_closed": {
        "class_id": "strict_fail_closed",
        "wall_time_ms": 100,
        "notes": ["strict fail-closed class stops slow packaged execution earliest"],
    },
}


def build_wasmtime_wall_time_limits() -> dict[str, object]:
    if len(WALL_TIME_LIMIT_CLASSES) > MAX_WASMTIME_LIMIT_CLASSES:
        raise ValueError("wall-time class count exceeds planning ceiling")
    payload = {
        "schema": WASMTIME_WALL_TIME_LIMITS_SCHEMA,
        "class_count": len(WALL_TIME_LIMIT_CLASSES),
        "classes": list(WALL_TIME_LIMIT_CLASSES.values()),
    }
    return {
        **payload,
        "snapshot_hash": stable_hash_payload(payload),
    }


def select_wall_time_class(*, policy_id: str) -> dict[str, object]:
    policy_key = require_non_empty_str(policy_id, "policy_id")
    class_id = POLICY_CLASS_IDS[policy_key]
    return dict(WALL_TIME_LIMIT_CLASSES[class_id])

