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
                    name TEXT PRIMARY KEY,
                    member TEXT[] NOT NULL DEFAULT '{}',
                    admin TEXT[] NOT NULL DEFAULT '{}'
                )
                """
            )

            group = QzDistributionGroup(
                name="Engineering Updates",
                member=["alice@example.com", "bob@example.com"],
                admin=["lead@example.com"],
            )
            cur.execute(
                """
                INSERT INTO dg (name, member, admin)
                VALUES (%s, %s, %s)
                ON CONFLICT (name)
                DO UPDATE SET member = EXCLUDED.member, admin = EXCLUDED.admin
                """,
                group.to_db_tuple(),
            )
            cur.execute("SELECT name, member, admin FROM dg WHERE name = %s", (group.name,))
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
