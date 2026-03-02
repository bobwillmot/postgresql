#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="$PROJECT_ROOT/chat_summary.md"

if [[ $# -lt 1 ]]; then
  echo "Usage: ./scripts/log_chat_request.sh \"<chat request text>\" [\"<recap of what was done>\"]"
  exit 1
fi

REQUEST_TEXT="$1"
shift || true
RECAP_TEXT="${*:-No recap provided yet}"
MODEL_NAME="${CHAT_MODEL_NAME:-GPT-5.3-Codex}"
USER_NAME="${CHAT_USER_NAME:-${USER:-unknown}}"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

if [[ ! -f "$LOG_FILE" ]]; then
  cat > "$LOG_FILE" <<'EOF'
# Chat Summary

This file tracks agent-mode chat requests for this project.

## Entries

EOF
fi

echo "- ${TIMESTAMP} | User: ${USER_NAME} | Model: ${MODEL_NAME} | User request: ${REQUEST_TEXT} | Recap: ${RECAP_TEXT}" >> "$LOG_FILE"
echo "Appended to $LOG_FILE"
