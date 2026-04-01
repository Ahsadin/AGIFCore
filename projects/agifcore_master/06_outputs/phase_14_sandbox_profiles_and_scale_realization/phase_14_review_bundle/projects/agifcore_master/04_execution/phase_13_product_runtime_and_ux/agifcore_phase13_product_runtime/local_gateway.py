from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Mapping

from .contracts import (
    BLOCKED_SURFACES,
    GATEWAY_ENVELOPE_SCHEMA,
    GATEWAY_RESPONSE_SCHEMA,
    MAX_GATEWAY_PAYLOAD_BYTES,
    MAX_GATEWAY_REQUESTS_PER_SESSION,
    MAX_LOCAL_GATEWAY_ROUTES,
    ROUTE_TO_SURFACE,
    bounded_unique,
    canonical_size_bytes,
    stable_hash_payload,
    utc_timestamp,
)
from .fail_closed_ux import select_fail_closed_state

GatewayHandler = Callable[[Mapping[str, Any]], dict[str, Any]]


class LocalGateway:
    def __init__(
        self,
        *,
        session_id: str,
        policy_hash: str,
        handlers: Mapping[str, GatewayHandler],
        fail_closed_catalog: Mapping[str, Any],
    ) -> None:
        self._session_id = session_id
        self._policy_hash = policy_hash
        self._handlers = dict(handlers)
        self._fail_closed_catalog = deepcopy(dict(fail_closed_catalog))
        self._request_count = 0
        if len(self._handlers) > MAX_LOCAL_GATEWAY_ROUTES:
            raise ValueError("gateway route count exceeds planning ceiling")

    @property
    def policy_hash(self) -> str:
        return self._policy_hash

    def route_request(
        self,
        *,
        route: str,
        payload: Mapping[str, Any] | None = None,
        session_id: str | None = None,
        policy_hash: str | None = None,
        method: str = "POST",
    ) -> dict[str, Any]:
        payload_map = dict(payload or {})
        payload_size = canonical_size_bytes(payload_map)
        requested_surface = ROUTE_TO_SURFACE.get(route)
        deny_reason: str | None = None
        deny_surface = requested_surface or "gateway_route"
        if payload_size > MAX_GATEWAY_PAYLOAD_BYTES:
            deny_reason = "payload_too_large"
        elif route not in self._handlers:
            deny_reason = "unknown_route"
        elif self._request_count >= MAX_GATEWAY_REQUESTS_PER_SESSION:
            deny_reason = "rate_limited"
            deny_surface = requested_surface or "gateway_policy"
        elif policy_hash and policy_hash != self._policy_hash:
            deny_reason = "policy_hash_mismatch"
            deny_surface = "gateway_policy"
        elif requested_surface != "session_open" and session_id and session_id != self._session_id:
            deny_reason = "session_mismatch"
            deny_surface = "gateway_policy"
        elif requested_surface in BLOCKED_SURFACES:
            deny_reason = "reserved_surface_fail_closed"
        self._request_count += 1
        envelope_payload = {
            "schema": GATEWAY_ENVELOPE_SCHEMA,
            "request_id": stable_hash_payload(
                {
                    "route": route,
                    "payload": payload_map,
                    "request_index": self._request_count,
                    "session_id": session_id or self._session_id,
                }
            )[:16],
            "session_id": session_id or self._session_id,
            "route": route,
            "requested_surface": requested_surface or "unknown_surface",
            "method": method,
            "payload_size_bytes": payload_size,
            "policy_hash": policy_hash or self._policy_hash,
            "request_count": self._request_count,
            "occurred_at": utc_timestamp(),
            "allowed": deny_reason is None,
            "deny_reason": deny_reason,
        }
        envelope = {
            **envelope_payload,
            "allowlisted_routes": list(
                bounded_unique(
                    list(self._handlers.keys()),
                    ceiling=MAX_LOCAL_GATEWAY_ROUTES,
                    field_name="allowlisted_routes",
                )
            ),
            "envelope_hash": stable_hash_payload(envelope_payload),
        }
        if deny_reason is not None:
            return {
                "schema": GATEWAY_RESPONSE_SCHEMA,
                "status": "blocked",
                "surface_name": requested_surface or "unknown_surface",
                "route": route,
                "envelope": envelope,
                "response": select_fail_closed_state(
                    catalog=self._fail_closed_catalog,
                    surface_name=deny_surface,
                    reason_code=deny_reason,
                ),
                "policy_hash": self._policy_hash,
            }
        response = self._handlers[route](payload_map)
        return {
            "schema": GATEWAY_RESPONSE_SCHEMA,
            "status": "pass",
            "surface_name": requested_surface,
            "route": route,
            "envelope": envelope,
            "response": deepcopy(response),
            "policy_hash": self._policy_hash,
        }
