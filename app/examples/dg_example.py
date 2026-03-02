"""Example: three sequential bi-temporal changes for DistributionGroup."""

from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import sys

from dotenv import load_dotenv
import psycopg


if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from app.dg import dg_load, DistributionGroup


def get_connection_string() -> str:
    return (
        f"dbname={os.getenv('POSTGRES_DB')} "
        f"user={os.getenv('POSTGRES_USER')} "
        f"password={os.getenv('POSTGRES_PASSWORD')} "
        f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
        f"port={os.getenv('POSTGRES_PORT', '5432')}"
    )


def ensure_dg_schema(cur: psycopg.Cursor) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS dg (
            id BIGSERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            member TEXT[] NOT NULL DEFAULT '{}',
            admin TEXT[] NOT NULL DEFAULT '{}',
            valid_from TIMESTAMPTZ NOT NULL,
            valid_to TIMESTAMPTZ,
            tx_from TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            tx_to TIMESTAMPTZ,
            CHECK (valid_to IS NULL OR valid_from < valid_to),
            CHECK (tx_to IS NULL OR tx_from < tx_to)
        )
        """
    )
    cur.execute("ALTER TABLE dg ADD COLUMN IF NOT EXISTS id BIGSERIAL")
    cur.execute("ALTER TABLE dg ADD COLUMN IF NOT EXISTS valid_from TIMESTAMPTZ")
    cur.execute("ALTER TABLE dg ADD COLUMN IF NOT EXISTS valid_to TIMESTAMPTZ")
    cur.execute("ALTER TABLE dg ADD COLUMN IF NOT EXISTS tx_from TIMESTAMPTZ")
    cur.execute("ALTER TABLE dg ADD COLUMN IF NOT EXISTS tx_to TIMESTAMPTZ")
    cur.execute("UPDATE dg SET valid_from = NOW() WHERE valid_from IS NULL")
    cur.execute("UPDATE dg SET tx_from = NOW() WHERE tx_from IS NULL")
    cur.execute("ALTER TABLE dg ALTER COLUMN valid_from SET NOT NULL")
    cur.execute("ALTER TABLE dg ALTER COLUMN tx_from SET NOT NULL")
    cur.execute("ALTER TABLE dg ALTER COLUMN tx_from SET DEFAULT NOW()")


def print_version(
    step: int,
    group: DistributionGroup,
    persisted_row: tuple[
        str,
        list[str],
        list[str],
        datetime,
        datetime | None,
        datetime,
        datetime | None,
    ],
) -> None:
    print(f"\nChange {step}:")
    print(f"Object: {group}")

    db_row = group.to_db_tuple()
    print(f"As DB tuple: {db_row}")

    reconstructed = DistributionGroup.from_db_row(db_row)
    print(f"Reconstructed object: {reconstructed}")

    persisted = DistributionGroup.from_db_row(persisted_row)
    print(f"Persisted row from PostgreSQL: {persisted}")


def main() -> None:
    load_dotenv()

    base_time = datetime(2026, 3, 1, 0, 0, tzinfo=timezone.utc)

    print("DistributionGroup bi-temporal change history (with PostgreSQL persistence):")

    change_1 = DistributionGroup(
        name="Engineering Updates",
        member=["alice@example.com", "bob@example.com"],
        admin=["lead@example.com"],
        valid_from=base_time,
        tx_from=base_time,
    )

    change_2 = DistributionGroup(
        name="Engineering Updates",
        member=["alice@example.com", "bob@example.com", "carol@example.com"],
        admin=["lead@example.com"],
        valid_from=base_time + timedelta(days=1),
        tx_from=base_time + timedelta(days=1),
    )

    change_3 = DistributionGroup(
        name="Engineering Platform Updates",
        member=["alice@example.com", "carol@example.com"],
        admin=["lead@example.com", "manager@example.com"],
        valid_from=base_time + timedelta(days=2),
        tx_from=base_time + timedelta(days=2),
    )

    changes = [change_1, change_2, change_3]

    conn_str = get_connection_string()
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            ensure_dg_schema(cur)
            for index, group in enumerate(changes, start=1):
                cur.execute(
                    """
                    INSERT INTO dg (name, member, admin, valid_from, valid_to, tx_from, tx_to)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING name, member, admin, valid_from, valid_to, tx_from, tx_to
                    """,
                    group.to_db_tuple(),
                )
                persisted_row = cur.fetchone()

                if persisted_row is not None:
                    print_version(index, group, persisted_row)

            print("\nRead helpers:")
            latest_engineering = dg_load(cur, "Engineering Updates")
            previous_engineering = (
                latest_engineering.previous(cur) if latest_engineering is not None else None
            )
            latest_platform = dg_load(cur, "Engineering Platform Updates")
            previous_platform = latest_platform.previous(cur) if latest_platform is not None else None

            print(f"Latest 'Engineering Updates': {latest_engineering}")
            print(f"Previous 'Engineering Updates': {previous_engineering}")
            print(f"Latest 'Engineering Platform Updates': {latest_platform}")
            print(f"Previous 'Engineering Platform Updates': {previous_platform}")


if __name__ == "__main__":
    main()
