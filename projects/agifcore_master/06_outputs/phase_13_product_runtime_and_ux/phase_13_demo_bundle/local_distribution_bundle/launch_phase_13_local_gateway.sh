#!/usr/bin/env sh
set -eu
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../../../../../.." && pwd)
cd "$REPO_ROOT"
python3 - <<'PY'
from pathlib import Path
import json
import sys
root = Path.cwd()
sys.path.insert(0, str(root / "projects/agifcore_master/05_testing/phase_12_structural_growth"))
sys.path.insert(0, str(root / "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux"))
import _phase_12_verifier_common as p12c
from agifcore_phase13_product_runtime import ProductRuntimeShell
result = p12c.run_phase12_cycle(scenario="weak")
shell = ProductRuntimeShell(
    fixture=result["fixture"],
    phase10_turn_state=result["phase10_turn"],
    phase11_cycle_state=result["phase11_cycle"],
    phase12_cycle_state=result["cycle"].to_dict(),
)
payload = shell.api.conversation_turn(user_text="installer gateway smoke test")
print(json.dumps(payload, indent=2, sort_keys=True))
PY
