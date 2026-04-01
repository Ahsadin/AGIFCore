from __future__ import annotations

from .contracts import (
    MAX_WASMTIME_LIMIT_CLASSES,
    POLICY_CLASS_IDS,
    WASMTIME_FUEL_LIMITS_SCHEMA,
    require_non_empty_str,
    stable_hash_payload,
)


FUEL_LIMIT_CLASSES = {
    "mobile_constrained": {
        "class_id": "mobile_constrained",
        "fuel_limit": 25_000_000,
        "notes": ["mobile profile uses the smallest bounded Wasmtime fuel class"],
    },
    "laptop_default": {
        "class_id": "laptop_default",
        "fuel_limit": 100_000_000,
        "notes": ["laptop profile inherits the donor-side reference Wasmtime fuel limit"],
    },
    "builder_diagnostic": {
        "class_id": "builder_diagnostic",
        "fuel_limit": 200_000_000,
        "notes": ["builder may widen diagnostics but has no correctness privilege"],
    },
    "strict_fail_closed": {
        "class_id": "strict_fail_closed",
        "fuel_limit": 5_000_000_000,
        "notes": ["strict fail-closed class exists for deny-first sandbox checks"],
    },
}


def build_wasmtime_fuel_limits() -> dict[str, object]:
    if len(FUEL_LIMIT_CLASSES) > MAX_WASMTIME_LIMIT_CLASSES:
        raise ValueError("fuel class count exceeds planning ceiling")
    payload = {
        "schema": WASMTIME_FUEL_LIMITS_SCHEMA,
        "class_count": len(FUEL_LIMIT_CLASSES),
        "classes": list(FUEL_LIMIT_CLASSES.values()),
    }
    return {
        **payload,
        "snapshot_hash": stable_hash_payload(payload),
    }


def select_fuel_class(*, policy_id: str) -> dict[str, object]:
    policy_key = require_non_empty_str(policy_id, "policy_id")
    class_id = POLICY_CLASS_IDS[policy_key]
    return dict(FUEL_LIMIT_CLASSES[class_id])
