from __future__ import annotations

import argparse
import json
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import _phase_15_verifier_common as vc
from agifcore_phase13_product_runtime.contracts import LOCAL_DESKTOP_CHAT_DEMO_SCHEMA
from agifcore_phase15_proof.contracts import REAL_DESKTOP_CHAT_DEMO_SCHEMA

DEFAULT_SCENARIO = "weak"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_SAMPLE_PROMPTS = (
    "who are you",
    "what can you do",
    "what evidence supports that",
)


def _fresh_phase13_shell(*, scenario: str = DEFAULT_SCENARIO):
    return vc.run_phase15_shells()["proof_shells"][scenario].phase13_shell


def _turn_summary(turn: dict[str, object]) -> dict[str, object]:
    return {
        "question_text": turn["question_text"],
        "question_class": turn["question_class"],
        "answer_mode": turn["answer_mode"],
        "final_answer_mode": turn["final_answer_mode"],
        "support_state": turn["support_state"],
        "response_text": turn["response_text"],
        "phases_exercised": turn["phases_exercised"],
        "phase_chain_completed": turn["phase_chain_completed"],
        "phase_results": turn["phase_results"],
        "local_truth_refs": turn["local_truth_refs"][:4],
    }


def build_demo_payload(
    *,
    scenario: str = DEFAULT_SCENARIO,
    prompts: tuple[str, ...] = DEFAULT_SAMPLE_PROMPTS,
) -> dict[str, object]:
    shell = _fresh_phase13_shell(scenario=scenario)
    turns = [shell.interactive_turn(user_text=prompt) for prompt in prompts]
    ui_snapshot = shell.interactive_ui_snapshot()
    return {
        "schema": REAL_DESKTOP_CHAT_DEMO_SCHEMA,
        "phase": "15",
        "demo_id": "real_desktop_chat_demo",
        "status": "open",
        "host_kind": "local_desktop_ui_browser_host",
        "runtime_host": "approved_phase13_desktop_ui",
        "ui_schema": LOCAL_DESKTOP_CHAT_DEMO_SCHEMA,
        "scenario": scenario,
        "sample_prompts": list(prompts),
        "api_routes": [
            "/api/state",
            "/api/turn",
            "/api/reset",
            "/api/scenario",
        ],
        "turn_summaries": [_turn_summary(turn) for turn in turns],
        "ui_snapshot": ui_snapshot,
        "launch_command": (
            "sh projects/agifcore_master/06_outputs/"
            "phase_15_final_intelligence_proof_and_closure_audit/phase_15_demo_bundle/"
            "launch_phase_15_real_desktop_chat_demo.sh"
        ),
        "notes": [
            "local desktop chat demo only",
            "desktop host presents runtime truth and does not own correctness",
            "Phase 15 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    ui_snapshot = payload["ui_snapshot"]
    return [
        "# Phase 15 Demo: Real Desktop Chat Demo",
        "",
        "Phase 15 remains `open`. This is local review material only.",
        "",
        "## Launch",
        "",
        f"- launcher: `{payload['launch_command']}`",
        f"- host kind: `{payload['host_kind']}`",
        f"- runtime host: `{payload['runtime_host']}`",
        "",
        "## Sample Prompts",
        "",
        *[f"- `{prompt}`" for prompt in payload["sample_prompts"]],
        "",
        "## UI Snapshot",
        "",
        f"- selected view: `{ui_snapshot['selected_view']}`",
        f"- view count: `{ui_snapshot['view_count']}`",
        f"- message count: `{ui_snapshot['message_count']}`",
        "",
        "## Truth Note",
        "",
        "- this is the primary non-terminal Phase 15 chat demo host",
        "- terminal chat remains a secondary debug surface",
        "- no approval or closure is implied",
    ]


HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AGIFCore Phase 15 Desktop Chat Demo</title>
  <style>
    :root {
      --bg: #f3efe6;
      --panel: #fffaf2;
      --ink: #1f1c17;
      --muted: #6a6257;
      --accent: #a54d2d;
      --accent-soft: #f1d7cb;
      --line: #d7cdbf;
      --user: #e2ecff;
      --assistant: #fff2d9;
      --shadow: 0 12px 30px rgba(31, 28, 23, 0.08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(165, 77, 45, 0.12), transparent 30%),
        linear-gradient(180deg, #f7f3ec, var(--bg));
      min-height: 100vh;
    }
    .app {
      max-width: 1280px;
      margin: 0 auto;
      padding: 24px;
      display: grid;
      gap: 20px;
    }
    .hero, .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 20px;
      box-shadow: var(--shadow);
    }
    .hero {
      padding: 24px;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-start;
    }
    .hero h1 {
      margin: 0 0 8px;
      font-size: 28px;
    }
    .hero p {
      margin: 0;
      color: var(--muted);
      line-height: 1.5;
      max-width: 760px;
    }
    .hero-tools {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
      justify-content: flex-end;
    }
    .layout {
      display: grid;
      grid-template-columns: minmax(0, 2fr) minmax(300px, 1fr);
      gap: 20px;
    }
    .chat {
      padding: 20px;
      display: grid;
      gap: 16px;
    }
    .thread {
      min-height: 420px;
      max-height: 620px;
      overflow: auto;
      display: grid;
      gap: 12px;
      padding-right: 4px;
    }
    .bubble {
      padding: 14px 16px;
      border-radius: 16px;
      border: 1px solid var(--line);
      line-height: 1.45;
      white-space: pre-wrap;
    }
    .bubble.user {
      background: var(--user);
      justify-self: end;
      max-width: 80%;
    }
    .bubble.assistant {
      background: var(--assistant);
      justify-self: start;
      max-width: 90%;
    }
    .bubble small {
      display: block;
      color: var(--muted);
      margin-top: 8px;
      font-size: 12px;
    }
    .composer {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
      align-items: center;
    }
    textarea {
      width: 100%;
      min-height: 72px;
      resize: vertical;
      border-radius: 14px;
      border: 1px solid var(--line);
      padding: 12px 14px;
      font: inherit;
      background: #fffdf8;
      color: var(--ink);
    }
    button, select {
      border-radius: 999px;
      border: 1px solid transparent;
      padding: 11px 16px;
      font: inherit;
    }
    button {
      background: var(--accent);
      color: #fff8f1;
      cursor: pointer;
    }
    button.secondary {
      background: transparent;
      color: var(--accent);
      border-color: var(--accent-soft);
    }
    .meta {
      padding: 20px;
      display: grid;
      gap: 16px;
    }
    .metric {
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 14px;
      background: #fffdf9;
    }
    .metric h2 {
      margin: 0 0 8px;
      font-size: 15px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
    }
    .metric p, .metric li {
      margin: 0;
      line-height: 1.45;
    }
    .metric ul {
      margin: 8px 0 0;
      padding-left: 18px;
    }
    .phase-list {
      margin: 8px 0 0;
      padding-left: 18px;
      display: grid;
      gap: 4px;
      max-height: 280px;
      overflow: auto;
    }
    .phase-list li {
      line-height: 1.35;
    }
    .muted { color: var(--muted); }
    .footer-note {
      color: var(--muted);
      font-size: 13px;
    }
    @media (max-width: 920px) {
      .layout { grid-template-columns: 1fr; }
      .hero { flex-direction: column; }
      .hero-tools { justify-content: flex-start; }
    }
  </style>
</head>
<body>
  <div class="app">
    <section class="hero">
      <div>
        <h1>AGIFCore Phase 15 Desktop Chat Demo</h1>
        <p>This is the primary non-terminal local review host for the repaired live-turn path. The UI only presents runtime truth. It does not invent answers or own correctness.</p>
      </div>
      <div class="hero-tools">
        <label class="muted">Scenario
          <select id="scenario">
            <option value="weak">weak</option>
            <option value="contradiction">contradiction</option>
          </select>
        </label>
        <button class="secondary" id="reset">Reset</button>
      </div>
    </section>
    <div class="layout">
      <section class="panel chat">
        <div id="thread" class="thread"></div>
        <div class="composer">
          <textarea id="prompt" placeholder="Ask AGIFCore about the project, runtime, phases, evidence, or local state"></textarea>
          <button id="send">Send</button>
        </div>
        <div class="footer-note">Press Enter to send. Use Shift+Enter for a new line. AGIFCore answers local project/runtime questions and will honestly abstain on unsupported ones.</div>
      </section>
      <aside class="panel meta">
        <div class="metric">
          <h2>Latest Turn</h2>
          <p id="latestClass">question_class=none</p>
          <p id="latestSupport">support_state=none</p>
          <p id="latestAnswerMode">answer_mode=none</p>
          <p id="latestFinalMode">final_answer_mode=none</p>
          <p id="latestChainGate">final_answer_after_full_chain=false</p>
        </div>
        <div class="metric">
          <h2>Full Phase Chain</h2>
          <p id="latestChainSummary">full_chain=none</p>
          <ul id="latestPhaseChain" class="phase-list"></ul>
        </div>
        <div class="metric">
          <h2>Local Truth Refs</h2>
          <ul id="latestRefs"></ul>
        </div>
        <div class="metric">
          <h2>UI State</h2>
          <p id="sessionInfo">session_id=...</p>
          <p id="messageInfo">message_count=0</p>
          <p id="viewInfo">view_count=0</p>
        </div>
      </aside>
    </div>
  </div>
  <script>
    const threadEl = document.getElementById("thread");
    const promptEl = document.getElementById("prompt");
    const sendEl = document.getElementById("send");
    const resetEl = document.getElementById("reset");
    const scenarioEl = document.getElementById("scenario");
    const latestClassEl = document.getElementById("latestClass");
    const latestSupportEl = document.getElementById("latestSupport");
    const latestAnswerModeEl = document.getElementById("latestAnswerMode");
    const latestFinalModeEl = document.getElementById("latestFinalMode");
    const latestChainGateEl = document.getElementById("latestChainGate");
    const latestChainSummaryEl = document.getElementById("latestChainSummary");
    const latestPhaseChainEl = document.getElementById("latestPhaseChain");
    const latestRefsEl = document.getElementById("latestRefs");
    const sessionInfoEl = document.getElementById("sessionInfo");
    const messageInfoEl = document.getElementById("messageInfo");
    const viewInfoEl = document.getElementById("viewInfo");

    async function fetchState() {
      const response = await fetch("/api/state");
      const payload = await response.json();
      render(payload.ui_snapshot);
      scenarioEl.value = payload.scenario;
    }

    function render(ui) {
      const transcript = ui.chat_transcript || [];
      threadEl.innerHTML = "";
      transcript.forEach((message) => {
        const bubble = document.createElement("div");
        bubble.className = `bubble ${message.speaker}`;
        bubble.textContent = message.text;
        if (message.speaker === "assistant") {
          const meta = document.createElement("small");
          meta.textContent = `answer_mode=${message.answer_mode} final_answer_mode=${message.final_answer_mode}`;
          bubble.appendChild(meta);
        }
        threadEl.appendChild(bubble);
      });
      threadEl.scrollTop = threadEl.scrollHeight;
      const latest = ui.latest_turn || {};
      latestClassEl.textContent = `question_class=${latest.question_class || "none"}`;
      latestSupportEl.textContent = `support_state=${latest.support_state || "none"}`;
      latestAnswerModeEl.textContent = `answer_mode=${latest.answer_mode || "none"}`;
      latestFinalModeEl.textContent = `final_answer_mode=${latest.final_answer_mode || "none"}`;
      latestChainGateEl.textContent = `final_answer_after_full_chain=${latest.final_answer_released_after_full_chain || false}`;
      latestChainSummaryEl.textContent =
        `full_chain_complete=${latest.phase_chain_completed || false} ` +
        `used=${latest.phases_used_count || 0} ` +
        `no_op=${latest.phases_no_op_count || 0} ` +
        `blocked=${latest.phases_blocked_count || 0} ` +
        `insufficient_input=${latest.phases_insufficient_input_count || 0}`;
      latestPhaseChainEl.innerHTML = "";
      (latest.phase_results || []).forEach((phase) => {
        const li = document.createElement("li");
        li.textContent = `Phase ${phase.phase_id}: ${phase.status}`;
        if (phase.reason) {
          li.title = phase.reason;
        }
        latestPhaseChainEl.appendChild(li);
      });
      latestRefsEl.innerHTML = "";
      (latest.local_truth_refs || []).slice(0, 6).forEach((ref) => {
        const li = document.createElement("li");
        li.textContent = ref;
        latestRefsEl.appendChild(li);
      });
      sessionInfoEl.textContent = `session_id=${ui.session_id}`;
      messageInfoEl.textContent = `message_count=${ui.message_count}`;
      viewInfoEl.textContent = `view_count=${ui.view_count}`;
    }

    async function postJson(path, payload) {
      const response = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload || {}),
      });
      return await response.json();
    }

    async function sendTurn() {
      const userText = promptEl.value.trim();
      if (!userText) return;
      sendEl.disabled = true;
      const payload = await postJson("/api/turn", { user_text: userText });
      render(payload.ui_snapshot);
      promptEl.value = "";
      sendEl.disabled = false;
      promptEl.focus();
    }

    sendEl.addEventListener("click", async () => {
      await sendTurn();
    });

    promptEl.addEventListener("keydown", async (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        await sendTurn();
      }
    });

    resetEl.addEventListener("click", async () => {
      const payload = await postJson("/api/reset", { scenario: scenarioEl.value });
      render(payload.ui_snapshot);
    });

    scenarioEl.addEventListener("change", async () => {
      const payload = await postJson("/api/scenario", { scenario: scenarioEl.value });
      render(payload.ui_snapshot);
    });

    fetchState();
    promptEl.focus();
  </script>
</body>
</html>
"""


class _DesktopChatState:
    def __init__(self, *, scenario: str) -> None:
        self._lock = threading.Lock()
        self._scenario = scenario
        self._shell = _fresh_phase13_shell(scenario=scenario)

    @property
    def scenario(self) -> str:
        return self._scenario

    def ui_snapshot(self) -> dict[str, object]:
        with self._lock:
            return self._shell.interactive_ui_snapshot()

    def run_turn(self, *, user_text: str) -> dict[str, object]:
        with self._lock:
            turn = self._shell.interactive_turn(user_text=user_text)
            return {
                "turn": turn,
                "ui_snapshot": self._shell.interactive_ui_snapshot(),
            }

    def reset(self, *, scenario: str | None = None) -> dict[str, object]:
        with self._lock:
            if scenario:
                self._scenario = scenario
            self._shell = _fresh_phase13_shell(scenario=self._scenario)
            return self._shell.interactive_ui_snapshot()


class RealDesktopChatDemoServer:
    def __init__(self, *, scenario: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
        self._host = host
        self._port = port
        self._state = _DesktopChatState(scenario=scenario)
        self._server = ThreadingHTTPServer((host, port), self._build_handler())
        self._thread: threading.Thread | None = None

    @property
    def scenario(self) -> str:
        return self._state.scenario

    @property
    def port(self) -> int:
        return int(self._server.server_address[1])

    @property
    def url(self) -> str:
        return f"http://{self._host}:{self.port}/"

    def _build_handler(self) -> type[BaseHTTPRequestHandler]:
        state = self._state

        class Handler(BaseHTTPRequestHandler):
            def _send_json(self, payload: dict[str, object], *, status: int = HTTPStatus.OK) -> None:
                body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _read_json(self) -> dict[str, object]:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0:
                    return {}
                raw = self.rfile.read(length)
                return json.loads(raw.decode("utf-8"))

            def do_GET(self) -> None:  # noqa: N802
                if self.path == "/":
                    body = HTML_PAGE.encode("utf-8")
                    self.send_response(HTTPStatus.OK)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                if self.path == "/api/state":
                    self._send_json(
                        {
                            "scenario": state.scenario,
                            "ui_snapshot": state.ui_snapshot(),
                        }
                    )
                    return
                self._send_json({"error": "not_found"}, status=HTTPStatus.NOT_FOUND)

            def do_POST(self) -> None:  # noqa: N802
                payload = self._read_json()
                if self.path == "/api/turn":
                    user_text = " ".join(str(payload.get("user_text", "")).split()).strip()
                    if not user_text:
                        self._send_json({"error": "user_text required"}, status=HTTPStatus.BAD_REQUEST)
                        return
                    result = state.run_turn(user_text=user_text)
                    self._send_json(
                        {
                            "scenario": state.scenario,
                            "turn": result["turn"],
                            "ui_snapshot": result["ui_snapshot"],
                        }
                    )
                    return
                if self.path == "/api/reset":
                    scenario = str(payload.get("scenario", state.scenario)).strip().lower() or state.scenario
                    if scenario not in {"weak", "contradiction"}:
                        self._send_json({"error": "invalid scenario"}, status=HTTPStatus.BAD_REQUEST)
                        return
                    self._send_json({"scenario": scenario, "ui_snapshot": state.reset(scenario=scenario)})
                    return
                if self.path == "/api/scenario":
                    scenario = str(payload.get("scenario", state.scenario)).strip().lower()
                    if scenario not in {"weak", "contradiction"}:
                        self._send_json({"error": "invalid scenario"}, status=HTTPStatus.BAD_REQUEST)
                        return
                    self._send_json({"scenario": scenario, "ui_snapshot": state.reset(scenario=scenario)})
                    return
                self._send_json({"error": "not_found"}, status=HTTPStatus.NOT_FOUND)

            def log_message(self, format: str, *args: object) -> None:  # noqa: A003
                return

        return Handler

    def start(self) -> "RealDesktopChatDemoServer":
        if self._thread is not None:
            return self
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def serve_forever(self) -> None:
        self._server.serve_forever()

    def close(self) -> None:
        if self._thread is not None:
            self._server.shutdown()
        self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None


def serve_demo(*, scenario: str, port: int, open_browser: bool) -> int:
    server = RealDesktopChatDemoServer(scenario=scenario, host=DEFAULT_HOST, port=port)
    print("Phase 15 Real Desktop Chat Demo")
    print("Phase 15 remains open. This is local review material only.")
    print(f"Open: {server.url}")
    print("Use Ctrl+C to stop the local demo server.")
    if open_browser:
        webbrowser.open(server.url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nreal desktop chat demo closed")
    finally:
        server.close()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--scenario", default=DEFAULT_SCENARIO, choices=("weak", "contradiction"))
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--open-browser", action="store_true")
    args = parser.parse_args()

    if args.serve:
        return serve_demo(
            scenario=args.scenario,
            port=args.port,
            open_browser=args.open_browser,
        )

    payload = build_demo_payload(scenario=args.scenario)
    vc.write_demo_payload(filename="phase_15_real_desktop_chat_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_15_real_desktop_chat_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
