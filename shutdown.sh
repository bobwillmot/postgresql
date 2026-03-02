#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Stopping PostgreSQL container (service: db)..."
docker compose stop db

echo "Current db service status:"
docker compose ps db

echo "Shutdown complete."
