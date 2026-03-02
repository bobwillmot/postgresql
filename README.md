# Python + PostgreSQL (Docker) + venv

[![CI](https://github.com/bobwillmot/postgresql/actions/workflows/ci.yml/badge.svg)](https://github.com/bobwillmot/postgresql/actions/workflows/ci.yml)

A minimal starter project for a Python program that connects to PostgreSQL running in Docker.

## Prerequisite

Use Python 3.13 for this project.

```bash
python3.13 --version
```

## 1) Create env file

```bash
cp .env.example .env
```

Default host port is `5433` to avoid conflicts with any local PostgreSQL on `5432`.

## 2) Start PostgreSQL with Docker

```bash
docker compose up -d db
```

Check container health:

```bash
docker compose ps
```

## 3) Create and activate virtual environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

## 4) Install dependencies

```bash
pip install -r requirements.txt
```

## 5) Run the app

```bash
python -m app.main
```

You should see output showing:
- an inserted row in `greetings`
- an inserted row in `dg` (stores bi-temporal `QzDistributionGroup` fields: `name`, `member[]`, `admin[]`, `valid_from/valid_to`, `tx_from/tx_to`)

## Validation

Use this quick smoke-test flow after setup or changes:

```bash
docker compose up -d db
.venv/bin/python -m app.main
docker compose ps db
```

Run unit tests:

```bash
.venv/bin/python -m pytest -q
```

Project IPython shell:

```bash
chmod +x ipython.sh
./ipython.sh
```

This launches IPython with `QzDistributionGroup` pre-imported.

## Sphinx documentation

Build the class catalog documentation:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m sphinx -b html docs docs/_build/html
```

Generated site:

- `docs/_build/html/index.html`

## startup.sh helper

Use `startup.sh` to initialize PostgreSQL objects required by this project.

What it does:
- starts PostgreSQL container `db` if needed
- creates database `sample` if it does not exist
- creates table `dg` in `sample` if it does not exist
- rebuilds Sphinx docs to `docs/_build/html`
- opens `docs/_build/html/index.html` in your default browser

Run it:

```bash
chmod +x startup.sh
./startup.sh
```

Run DB/table setup only (skip dependency install + docs rebuild):

```bash
./startup.sh --skip-docs
```

Prerequisites:
- `.venv` exists (`python3.13 -m venv .venv`)

`startup.sh` installs Python dependencies automatically before rebuilding docs.

## shutdown.sh helper

Use `shutdown.sh` to stop the PostgreSQL Docker container for this project.

```bash
chmod +x shutdown.sh
./shutdown.sh
```

## Chat request logging

Project chat requests are tracked in `chat_summary.md`.

Entry format:

- `YYYY-MM-DDTHH:MM:SSZ | User: <user-name> | Model: <model-name> | User request: <text> | Recap: <what was done>`

Append an entry manually with:

```bash
./scripts/log_chat_request.sh "your request text" "what was done"
```

`startup.sh` auto-prepares this script (execute permission + macOS quarantine clear), so manual "allow" steps are not needed after setup.

## Create an additional database

Create a database named `sample`:

```bash
docker compose exec -T db psql -U appuser -d postgres -c "CREATE DATABASE sample;"
```

Verify it exists:

```bash
docker compose exec -T db psql -U appuser -d postgres -tAc "SELECT datname FROM pg_database WHERE datname='sample';"
```

## Dataclass example

`QzDistributionGroup` is defined in `app/dg.py`.

This example is fully local and does not require PostgreSQL to be running.

The script demonstrates three sequential changes to a bi-temporal `QzDistributionGroup`.

```python
from app.examples.dg_example import main

main()
```

Run the example script:

```bash
.venv/bin/python -m app.examples.dg_example
```

Expected output:

```text
QzDistributionGroup bi-temporal change history:

Change 1:
Object: QzDistributionGroup(...)
As DB tuple: (...)
Reconstructed object: QzDistributionGroup(...)

Change 2:
Object: QzDistributionGroup(...)
As DB tuple: (...)
Reconstructed object: QzDistributionGroup(...)

Change 3:
Object: QzDistributionGroup(...)
As DB tuple: (...)
Reconstructed object: QzDistributionGroup(...)
```

## Troubleshooting

### Python 3.13 not found

If `python3.13` is not available on macOS:

```bash
brew install python@3.13
```

Then verify:

```bash
python3.13 --version
```

### Port already in use

If Docker reports `Bind for 0.0.0.0:<port> failed: port is already allocated`:

1. Open `.env` and set a different `POSTGRES_PORT` (for example `5433`).
2. Recreate services:

```bash
docker compose down
docker compose up -d db
```

3. Check status:

```bash
docker compose ps db
```

## 6) Stop services

```bash
docker compose down
```

To remove DB data too:

```bash
docker compose down -v
```
