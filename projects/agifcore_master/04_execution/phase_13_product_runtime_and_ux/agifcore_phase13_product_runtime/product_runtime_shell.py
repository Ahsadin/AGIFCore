from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from .contracts import (
    ALL_GATEWAY_SURFACES,
    PRODUCT_RUNTIME_SHELL_SCHEMA,
    PUBLIC_SURFACES,
    ROUTE_TO_SURFACE,
    stable_hash_payload,
)
from .desktop_ui import LocalDesktopUI
from .embeddable_runtime_api import EmbeddableRuntimeAPI
from .fail_closed_ux import build_fail_closed_catalog
from .installer_distribution import build_installer_distribution_snapshot
from .interactive_turn import build_interactive_turn
from .local_gateway import LocalGateway
from .local_runner import LocalRunner
from .memory_review_export import build_memory_review_export
from .safe_shutdown import build_safe_shutdown_receipt
from .state_export import build_state_export
from .trace_export import build_trace_export


class ProductRuntimeShell:
    def __init__(
        self,
        *,
        fixture: Mapping[str, Any],
        phase10_turn_state: Mapping[str, Any],
        phase11_cycle_state: Mapping[str, Any],
        phase12_cycle_state: Mapping[str, Any],
    ) -> None:
        self.runner = LocalRunner(
            fixture=fixture,
            phase10_turn_state=phase10_turn_state,
            phase11_cycle_state=phase11_cycle_state,
            phase12_cycle_state=phase12_cycle_state,
        )
        self._session_open = self.runner.session_open()
        self._conversation_turn = self.runner.conversation_turn()
        self._memory_review_export = build_memory_review_export(
            session_open=self._session_open,
            conversation_turn=self._conversation_turn,
            phase11_cycle_state=self.runner.phase11_cycle,
            phase12_cycle_state=self.runner.phase12_cycle,
        )
        self._trace_export = build_trace_export(
            session_open=self._session_open,
            conversation_turn=self._conversation_turn,
            phase10_turn_state=self.runner.phase10_turn,
            phase11_cycle_state=self.runner.phase11_cycle,
            phase12_cycle_state=self.runner.phase12_cycle,
        )
        self._state_export = build_state_export(
            session_open=self._session_open,
            conversation_turn=self._conversation_turn,
            trace_export=self._trace_export,
            memory_review_export=self._memory_review_export,
            phase11_cycle_state=self.runner.phase11_cycle,
            phase12_cycle_state=self.runner.phase12_cycle,
        )
        self._fail_closed_catalog = build_fail_closed_catalog(
            phase10_turn_state=self.runner.phase10_turn,
            phase11_cycle_state=self.runner.phase11_cycle,
            phase12_cycle_state=self.runner.phase12_cycle,
        )
        self._policy_hash = stable_hash_payload(
            {
                "session_id": self._session_open["session_id"],
                "available_surfaces": self._session_open["available_surfaces"],
                "blocked_surfaces": [
                    item["surface_name"] for item in self._session_open["blocked_surfaces"]
                ],
                "allowlisted_routes": list(ROUTE_TO_SURFACE.keys()),
            }
        )
        self._installer_snapshot = build_installer_distribution_snapshot(
            session_open=self._session_open,
            policy_hash=self._policy_hash,
            shell_snapshot_hash="not_written_yet",
        )
        self.gateway = LocalGateway(
            session_id=self._session_open["session_id"],
            policy_hash=self._policy_hash,
            handlers={
                "/api/session-open": lambda _payload: self.session_open(),
                "/api/conversation-turn": lambda payload: self.conversation_turn(
                    user_text=str(payload.get("user_text", "")).strip() or None
                ),
                "/api/state-export": lambda _payload: self.state_export(),
                "/api/trace-export": lambda _payload: self.trace_export(),
                "/api/memory-review-export": lambda _payload: self.memory_review_export(),
                "/api/safe-shutdown": lambda _payload: self.safe_shutdown(),
                "/api/task-submit": lambda _payload: {},
                "/api/policy-update": lambda _payload: {},
                "/api/fail-closed-help": lambda _payload: self.fail_closed_catalog(),
                "/api/installer-status": lambda _payload: self.installer_distribution(),
            },
            fail_closed_catalog=self._fail_closed_catalog,
        )
        self.api = EmbeddableRuntimeAPI(
            session_id=self._session_open["session_id"],
            gateway=self.gateway,
        )
        self.desktop_ui = LocalDesktopUI()
        self._shutdown_receipt: dict[str, Any] | None = None
        self._interactive_turn_sequence = 0
        self._interactive_turn_history: list[dict[str, Any]] = []
        self._session_open["policy_hash"] = self._policy_hash

    def session_open(self) -> dict[str, Any]:
        return deepcopy(self._session_open)

    def conversation_turn(self, *, user_text: str | None = None) -> dict[str, Any]:
        if user_text:
            return self.runner.conversation_turn(user_text=user_text)
        return deepcopy(self._conversation_turn)

    def interactive_turn(self, *, user_text: str) -> dict[str, Any]:
        self._interactive_turn_sequence += 1
        turn = build_interactive_turn(
            user_text=user_text,
            session_open=self.session_open(),
            shell_snapshot=self.shell_snapshot(),
            state_export=self.state_export(),
            memory_review_export=self.memory_review_export(),
            safe_shutdown=self.safe_shutdown(),
            phase10_turn_state=deepcopy(self.runner.phase10_turn),
            phase11_cycle_state=deepcopy(self.runner.phase11_cycle),
            phase12_cycle_state=deepcopy(self.runner.phase12_cycle),
            turn_sequence=self._interactive_turn_sequence,
            prior_turn=deepcopy(self._interactive_turn_history[-1]) if self._interactive_turn_history else None,
            recent_turns=deepcopy(self._interactive_turn_history[-4:]),
        )
        self._interactive_turn_history.append(deepcopy(turn))
        if len(self._interactive_turn_history) > 24:
            self._interactive_turn_history = self._interactive_turn_history[-24:]
        return turn

    def state_export(self) -> dict[str, Any]:
        return deepcopy(self._state_export)

    def trace_export(self) -> dict[str, Any]:
        return deepcopy(self._trace_export)

    def memory_review_export(self) -> dict[str, Any]:
        return deepcopy(self._memory_review_export)

    def safe_shutdown(self) -> dict[str, Any]:
        if self._shutdown_receipt is None:
            self._shutdown_receipt = build_safe_shutdown_receipt(
                session_open=self._session_open,
                state_export=self._state_export,
                trace_export=self._trace_export,
                memory_review_export=self._memory_review_export,
                phase11_cycle_state=self.runner.phase11_cycle,
            )
        return deepcopy(self._shutdown_receipt)

    def fail_closed_catalog(self) -> dict[str, Any]:
        return deepcopy(self._fail_closed_catalog)

    def installer_distribution(self, *, output_dir: Path | None = None) -> dict[str, Any]:
        shell_hash = self.shell_snapshot()["snapshot_hash"]
        if output_dir is not None or self._installer_snapshot["shell_snapshot_hash"] != shell_hash:
            self._installer_snapshot = build_installer_distribution_snapshot(
                session_open=self._session_open,
                policy_hash=self._policy_hash,
                shell_snapshot_hash=shell_hash,
                output_dir=output_dir,
            )
        return deepcopy(self._installer_snapshot)

    def ui_snapshot(self) -> dict[str, Any]:
        return self.desktop_ui.render(
            shell_snapshot=self.shell_snapshot(),
            session_open=self.session_open(),
            conversation_turn=self.conversation_turn(),
            state_export=self.state_export(),
            trace_export=self.trace_export(),
            memory_review_export=self.memory_review_export(),
            fail_closed_catalog=self.fail_closed_catalog(),
            installer_snapshot=self.installer_distribution(),
        )

    def interactive_ui_snapshot(self) -> dict[str, Any]:
        latest_turn = deepcopy(self._interactive_turn_history[-1]) if self._interactive_turn_history else None
        return self.desktop_ui.render_interactive(
            shell_snapshot=self.shell_snapshot(),
            session_open=self.session_open(),
            state_export=self.state_export(),
            trace_export=self.trace_export(),
            memory_review_export=self.memory_review_export(),
            fail_closed_catalog=self.fail_closed_catalog(),
            interactive_history=deepcopy(self._interactive_turn_history),
            latest_turn=latest_turn,
        )

    def shell_snapshot(self) -> dict[str, Any]:
        payload = {
            "schema": PRODUCT_RUNTIME_SHELL_SCHEMA,
            "session_id": self._session_open["session_id"],
            "conversation_id": self._session_open["conversation_id"],
            "turn_id": self._session_open["turn_id"],
            "support_state": self._session_open["support_state"],
            "phase10_turn_hash": self._conversation_turn["phase10_turn_hash"],
            "phase11_cycle_hash": self._conversation_turn["phase11_cycle_hash"],
            "phase12_cycle_hash": self._conversation_turn["phase12_cycle_hash"],
            "available_surfaces": list(PUBLIC_SURFACES),
            "blocked_surface_names": [
                item["surface_name"] for item in self._session_open["blocked_surfaces"]
            ],
            "allowlisted_routes": list(ROUTE_TO_SURFACE.keys()),
            "gateway_surface_count": len(ALL_GATEWAY_SURFACES),
            "ui_views": list(self.desktop_ui.render(
                shell_snapshot={
                    "session_id": self._session_open["session_id"],
                    "support_state": self._session_open["support_state"],
                },
                session_open=self._session_open,
                conversation_turn=self._conversation_turn,
                state_export=self._state_export,
                trace_export=self._trace_export,
                memory_review_export=self._memory_review_export,
                fail_closed_catalog=self._fail_closed_catalog,
                installer_snapshot=self._installer_snapshot,
            )["views"]),
            "policy_hash": self._policy_hash,
            "state_export_hash": self._state_export["snapshot_hash"],
            "trace_export_hash": self._trace_export["snapshot_hash"],
            "memory_review_export_hash": self._memory_review_export["snapshot_hash"],
            "installer_snapshot_hash": self._installer_snapshot["snapshot_hash"],
        }
        ui_views = payload.pop("ui_views")
        payload["ui_view_ids"] = [item["view_id"] for item in ui_views]
        payload["ui_view_count"] = len(payload["ui_view_ids"])
        return {
            **payload,
            "snapshot_hash": stable_hash_payload(payload),
        }
