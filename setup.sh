#!/usr/bin/env bash
set -euo pipefail

SKIP_DOCS=false

for arg in "$@"; do
  case "$arg" in
    --skip-docs)
      SKIP_DOCS=true
      ;;
    -h|--help)
      echo "Usage: ./setup.sh [--skip-docs]"
      echo "  --skip-docs   Skip dependency install and Sphinx rebuild"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg"
      echo "Usage: ./setup.sh [--skip-docs]"
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ -f .env ]]; then
  set -a
  source .env
  set +a
fi

DB_SERVICE="db"
POSTGRES_USER="${POSTGRES_USER:-appuser}"
SAMPLE_DB="sample"

echo "Preparing chat logger script permissions..."
chmod +x scripts/log_chat_request.sh 2>/dev/null || true
xattr -d com.apple.quarantine scripts/log_chat_request.sh 2>/dev/null || true

if [[ "$(docker compose exec -T "$DB_SERVICE" psql -U "$POSTGRES_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='${SAMPLE_DB}';")" != "1" ]]; then
  echo "Creating database '${SAMPLE_DB}'..."
  docker compose exec -T "$DB_SERVICE" psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE ${SAMPLE_DB};"
else
  echo "Database '${SAMPLE_DB}' already exists."
fi

echo "Ensuring table 'dg' exists in database '${SAMPLE_DB}'..."
docker compose exec -T "$DB_SERVICE" psql -U "$POSTGRES_USER" -d "$SAMPLE_DB" -c "CREATE TABLE IF NOT EXISTS dg (id BIGSERIAL PRIMARY KEY, name TEXT NOT NULL, member TEXT[] NOT NULL DEFAULT '{}', admin TEXT[] NOT NULL DEFAULT '{}', valid_from TIMESTAMPTZ NOT NULL, valid_to TIMESTAMPTZ, tx_from TIMESTAMPTZ NOT NULL DEFAULT NOW(), tx_to TIMESTAMPTZ, CHECK (valid_to IS NULL OR valid_from < valid_to), CHECK (tx_to IS NULL OR tx_from < tx_to));"

if [[ "$SKIP_DOCS" == "true" ]]; then
  echo "Skipping docs steps (--skip-docs)."
  echo "Setup complete."
  exit 0
fi

if [[ ! -x .venv/bin/python ]]; then
  echo "Error: .venv/bin/python not found. Create the venv first with python3.13 -m venv .venv"
  exit 1
fi

echo "Installing/updating Python dependencies..."
.venv/bin/python -m pip install -r requirements.txt

echo "Rebuilding Sphinx documentation..."
.venv/bin/python -m sphinx -b html docs docs/_build/html

echo "Setup complete. Docs generated at docs/_build/html/index.html"
