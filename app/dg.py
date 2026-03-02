"""Distribution group domain models."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import os

from dotenv import load_dotenv
import psycopg

DgRow = tuple[
    str,
    list[str],
    list[str],
    datetime,
    datetime | None,
    datetime,
    datetime | None,
]


def _connection_string() -> str:
    return (
        f"dbname={os.getenv('POSTGRES_DB')} "
        f"user={os.getenv('POSTGRES_USER')} "
        f"password={os.getenv('POSTGRES_PASSWORD')} "
        f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
        f"port={os.getenv('POSTGRES_PORT', '5432')}"
    )


def _dg_load_with_cursor(cur: psycopg.Cursor, dg_name: str) -> "DistributionGroup | None":
    """Load the most recent version of a distribution group by name."""
    cur.execute(
        """
        SELECT name, member, admin, valid_from, valid_to, tx_from, tx_to
        FROM dg
        WHERE name = %s
        ORDER BY tx_from DESC, id DESC
        LIMIT 1
        """,
        (dg_name,),
    )
    row = cur.fetchone()
    if row is None:
        return None
    return DistributionGroup.from_db_row(row)


def dg_load(dg_name: str, cur: psycopg.Cursor | None = None) -> "DistributionGroup | None":
    """Load the most recent version of a distribution group by name.

    Args:
        dg_name: Distribution group name.
        cur: Optional active cursor. If omitted, this function opens its own connection.
    """
    if cur is not None:
        return _dg_load_with_cursor(cur, dg_name)

    load_dotenv()
    with psycopg.connect(_connection_string()) as conn:
        with conn.cursor() as local_cur:
            return _dg_load_with_cursor(local_cur, dg_name)


@dataclass
class DistributionGroup:
    """Represents a distribution group with bi-temporal attributes."""

    name: str
    member: list[str] = field(default_factory=list)
    admin: list[str] = field(default_factory=list)
    valid_from: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    valid_to: datetime | None = None
    tx_from: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tx_to: datetime | None = None

    def to_db_tuple(
        self,
    ) -> tuple[
        str,
        list[str],
        list[str],
        datetime,
        datetime | None,
        datetime,
        datetime | None,
    ]:
        """Convert the instance into a tuple matching the ``dg`` table columns."""
        return (
            self.name,
            self.member,
            self.admin,
            self.valid_from,
            self.valid_to,
            self.tx_from,
            self.tx_to,
        )

    @classmethod
    def from_db_row(
        cls,
        row: DgRow,
    ) -> "DistributionGroup":
        """Create an instance from a database row.

        Args:
            row: Tuple ordered as ``(name, member, admin, valid_from, valid_to, tx_from, tx_to)``.
        """
        return cls(
            name=row[0],
            member=list(row[1]),
            admin=list(row[2]),
            valid_from=row[3],
            valid_to=row[4],
            tx_from=row[5],
            tx_to=row[6],
        )

    def _previous_with_cursor(self, cur: psycopg.Cursor) -> "DistributionGroup | None":
        cur.execute(
            """
            SELECT name, member, admin, valid_from, valid_to, tx_from, tx_to
            FROM dg
            WHERE name = %s AND tx_from < %s
            ORDER BY tx_from DESC, id DESC
            LIMIT 1
            """,
            (self.name, self.tx_from),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return DistributionGroup.from_db_row(row)

    def previous(self, cur: psycopg.Cursor | None = None) -> "DistributionGroup | None":
        """Load the previous version of this group by ``name`` and ``tx_from``.

        Args:
            cur: Optional active cursor. If omitted, this function opens its own connection.
        """
        if cur is not None:
            return self._previous_with_cursor(cur)

        load_dotenv()
        with psycopg.connect(_connection_string()) as conn:
            with conn.cursor() as local_cur:
                return self._previous_with_cursor(local_cur)
