from __future__ import annotations

from .contracts import (
    MAX_WASMTIME_LIMIT_CLASSES,
    POLICY_CLASS_IDS,
    WASMTIME_MEMORY_LIMITS_SCHEMA,
    require_non_empty_str,
    stable_hash_payload,
)


MEMORY_LIMIT_CLASSES = {
    "mobile_constrained": {
        "class_id": "mobile_constrained",
        "memory_limit_mb": 64,
        "notes": ["mobile profile keeps the smallest explicit memory cap"],
    },
    "laptop_default": {
        "class_id": "laptop_default",
        "memory_limit_mb": 256,
        "notes": ["laptop profile inherits the donor-side reference Wasmtime memory cap"],
    },
    "builder_diagnostic": {
        "class_id": "builder_diagnostic",
        "memory_limit_mb": 512,
        "notes": ["builder may widen diagnostics but may not rewrite correctness"],
    },
    "strict_fail_closed": {
        "class_id": "strict_fail_closed",
        "memory_limit_mb": 32,
        "notes": ["strict fail-closed class keeps admission limits smallest"],
    },
}


def build_wasmtime_memory_limits() -> dict[str, object]:
    if len(MEMORY_LIMIT_CLASSES) > MAX_WASMTIME_LIMIT_CLASSES:
        raise ValueError("memory class count exceeds planning ceiling")
    payload = {
        "schema": WASMTIME_MEMORY_LIMITS_SCHEMA,
        "class_count": len(MEMORY_LIMIT_CLASSES),
        "classes": list(MEMORY_LIMIT_CLASSES.values()),
    }
    return {
        **payload,
        "snapshot_hash": stable_hash_payload(payload),
    }


def select_memory_class(*, policy_id: str) -> dict[str, object]:
    policy_key = require_non_empty_str(policy_id, "policy_id")
    class_id = POLICY_CLASS_IDS[policy_key]
    return dict(MEMORY_LIMIT_CLASSES[class_id])

