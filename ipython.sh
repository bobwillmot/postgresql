#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -x .venv/bin/python ]]; then
  echo "Error: .venv/bin/python not found. Create the venv first with python3.13 -m venv .venv"
  exit 1
fi

export PYTHONPATH="$SCRIPT_DIR${PYTHONPATH:+:$PYTHONPATH}"

exec .venv/bin/python -m IPython \
  --InteractiveShellApp.exec_lines="from app.dg import DistributionGroup" \
  --InteractiveShellApp.exec_lines="print('Loaded: DistributionGroup')" \
  "$@"
