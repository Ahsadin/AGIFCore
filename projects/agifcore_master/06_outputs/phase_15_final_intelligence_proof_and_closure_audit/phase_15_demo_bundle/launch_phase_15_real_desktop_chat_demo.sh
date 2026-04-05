#!/usr/bin/env sh
set -eu
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../../../../.." && pwd)
cd "$REPO_ROOT"
python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/run_phase_15_real_desktop_chat_demo.py --serve --open-browser "$@"
