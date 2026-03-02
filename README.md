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
- an upserted row in `dg` (stores `QzDistributionGroup` as `name`, `member[]`, `admin[]`)

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

## setup.sh helper

Use `setup.sh` to initialize PostgreSQL objects required by this project.

What it does:
- creates database `sample` if it does not exist
- creates table `dg` in `sample` if it does not exist
- rebuilds Sphinx docs to `docs/_build/html`

Run it:

```bash
chmod +x setup.sh
./setup.sh
```

Run DB/table setup only (skip dependency install + docs rebuild):

```bash
./setup.sh --skip-docs
```

Prerequisites:
- PostgreSQL container is running (`docker compose up -d db`)
- `.venv` exists (`python3.13 -m venv .venv`)

`setup.sh` installs Python dependencies automatically before rebuilding docs.

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

```python
from app.dg import QzDistributionGroup

group = QzDistributionGroup(
	name="Engineering Updates",
	member=["alice@example.com", "bob@example.com"],
	admin=["lead@example.com"],
)

print(f"Original object: {group}")

db_row = group.to_db_tuple()
print(f"As DB tuple: {db_row}")

reconstructed = QzDistributionGroup.from_db_row(db_row)
print(f"Reconstructed object: {reconstructed}")
```

Run the example script:

```bash
.venv/bin/python -m app.examples.dg_example
```

Expected output:

```text
Original object: QzDistributionGroup(name='Engineering Updates', member=['alice@example.com', 'bob@example.com'], admin=['lead@example.com'])
As DB tuple: ('Engineering Updates', ['alice@example.com', 'bob@example.com'], ['lead@example.com'])
Reconstructed object: QzDistributionGroup(name='Engineering Updates', member=['alice@example.com', 'bob@example.com'], admin=['lead@example.com'])
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
