# Copilot Instructions for This Project

## Project Overview
- Stack: Python 3.13, PostgreSQL (Docker Compose), local virtual environment (`.venv`).
- Python source lives in `app/`.
- Entry point is `python -m app.main`.

## Environment and Tooling
- Use **Python 3.13** for all code and examples.
- Create/use virtual environment at `.venv`.
- Install dependencies from `requirements.txt`.
- Prefer commands that use the venv interpreter explicitly, e.g. `.venv/bin/python -m ...`.

## Database and Docker
- PostgreSQL runs via `docker compose` service name `db`.
- Environment variables are loaded from `.env`.
- Keep `.env.example` updated when adding/changing required env vars.
- Do not commit secrets or real credentials.

## Code Style
- Keep changes minimal and focused on the requested task.
- Follow existing project style and naming.
- Follow PEP 8 for Python code style.
- Avoid unnecessary abstractions for this small starter project.
- Add type hints for new Python functions when practical.

## Dependency Management
- Pin dependency versions in `requirements.txt`.
- Prefer stable, compatible versions with Python 3.13.
- Do not introduce new dependencies unless necessary.

## Documentation
- When behavior or setup changes, update `README.md` in the same change.
- Keep setup steps copy-paste friendly for macOS.

## Agent Chat Logging
- For every new user request handled in agent mode, append a one-line entry to `chat_summary.md`.
- Use format: `YYYY-MM-DDTHH:MM:SSZ | Model: <model-name> | User request: <text> | Recap: <what was done>`.
- Keep `chat_summary.md` append-only; do not rewrite or remove past entries unless explicitly asked.

## Testing and Verification
- Prefer quick, local verification before broader checks.
- Standard smoke-test flow:
	1. Ensure database is up: `docker compose up -d db`
	2. Run app via venv: `.venv/bin/python -m app.main`
	3. Confirm expected insert/read output from PostgreSQL.
- If setup/config changes are made, also verify Docker service status with `docker compose ps db`.

## What to Avoid
- Do not change project defaults (Python 3.13, Docker Compose Postgres setup) unless explicitly requested.
- Do not add unrelated refactors or features.
