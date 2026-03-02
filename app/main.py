import os
from dotenv import load_dotenv
import psycopg
from app.dg import QzDistributionGroup


def get_connection_string() -> str:
    return (
        f"dbname={os.getenv('POSTGRES_DB')} "
        f"user={os.getenv('POSTGRES_USER')} "
        f"password={os.getenv('POSTGRES_PASSWORD')} "
        f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
        f"port={os.getenv('POSTGRES_PORT', '5432')}"
    )


def main() -> None:
    load_dotenv()

    conn_str = get_connection_string()
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS greetings (
                    id SERIAL PRIMARY KEY,
                    message TEXT NOT NULL
                )
                """
            )
            cur.execute("INSERT INTO greetings (message) VALUES (%s)", ("Hello from Python + PostgreSQL!",))
            cur.execute("SELECT id, message FROM greetings ORDER BY id DESC LIMIT 1")
            greeting_row = cur.fetchone()

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
            cur.execute(
                """
                DO $$
                DECLARE
                    pk_col TEXT;
                BEGIN
                    SELECT a.attname
                    INTO pk_col
                    FROM pg_constraint c
                    JOIN pg_class t ON t.oid = c.conrelid
                    JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(c.conkey)
                    WHERE t.relname = 'dg' AND c.contype = 'p'
                    LIMIT 1;

                    IF pk_col = 'name' THEN
                        ALTER TABLE dg DROP CONSTRAINT dg_pkey;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint c
                        JOIN pg_class t ON t.oid = c.conrelid
                        WHERE t.relname = 'dg' AND c.contype = 'p'
                    ) THEN
                        ALTER TABLE dg ADD CONSTRAINT dg_pkey PRIMARY KEY (id);
                    END IF;
                END
                $$;
                """
            )

            group = QzDistributionGroup(
                name="Engineering Updates",
                member=["alice@example.com", "bob@example.com"],
                admin=["lead@example.com"],
            )
            cur.execute(
                """
                INSERT INTO dg (name, member, admin, valid_from, valid_to, tx_from, tx_to)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                group.to_db_tuple(),
            )
            cur.execute(
                """
                SELECT name, member, admin, valid_from, valid_to, tx_from, tx_to
                FROM dg
                WHERE name = %s
                ORDER BY tx_from DESC
                LIMIT 1
                """,
                (group.name,),
            )
            dg_row = cur.fetchone()

    if greeting_row:
        print(f"Inserted row -> id={greeting_row[0]}, message='{greeting_row[1]}'")
    else:
        print("No row returned")

    if dg_row:
        mapped_group = QzDistributionGroup.from_db_row(dg_row)
        print(f"Upserted dg -> {mapped_group}")
    else:
        print("No dg row returned")


if __name__ == "__main__":
    main()
