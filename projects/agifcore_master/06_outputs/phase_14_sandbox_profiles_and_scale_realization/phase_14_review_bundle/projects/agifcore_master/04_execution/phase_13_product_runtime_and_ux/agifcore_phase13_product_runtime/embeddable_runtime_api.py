from __future__ import annotations

from typing import Any, Mapping

from .contracts import EMBEDDABLE_RUNTIME_API_SCHEMA, SURFACE_TO_ROUTE, stable_hash_payload


class EmbeddableRuntimeAPI:
    def __init__(self, *, session_id: str, gateway: Any) -> None:
        self._session_id = session_id
        self._gateway = gateway

    def _call(
        self,
        *,
        surface_name: str,
        payload: Mapping[str, Any] | None = None,
        include_session_id: bool = True,
    ) -> dict[str, Any]:
        route = SURFACE_TO_ROUTE[surface_name]
        gateway_response = self._gateway.route_request(
            route=route,
            payload=payload or {},
            session_id=self._session_id if include_session_id else None,
            policy_hash=self._gateway.policy_hash,
        )
        wrapper = {
            "schema": EMBEDDABLE_RUNTIME_API_SCHEMA,
            "api_surface": surface_name,
            "session_id": self._session_id,
            "status": gateway_response["status"],
            "gateway_response": gateway_response,
        }
        return {
            **wrapper,
            "contract_hash": stable_hash_payload(wrapper),
        }

    def session_open(self) -> dict[str, Any]:
        return self._call(surface_name="session_open", include_session_id=False)

    def conversation_turn(self, *, user_text: str | None = None) -> dict[str, Any]:
        payload = {"user_text": user_text or ""}
        return self._call(surface_name="conversation_turn", payload=payload)

    def state_export(self) -> dict[str, Any]:
        return self._call(surface_name="state_export")

    def trace_export(self) -> dict[str, Any]:
        return self._call(surface_name="trace_export")

    def memory_review_export(self) -> dict[str, Any]:
        return self._call(surface_name="memory_review_export")

    def safe_shutdown(self) -> dict[str, Any]:
        return self._call(surface_name="safe_shutdown")

    def task_submit(self, *, task_payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
        return self._call(surface_name="task_submit", payload=task_payload or {})

    def policy_update(self, *, policy_payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
        return self._call(surface_name="policy_update", payload=policy_payload or {})
