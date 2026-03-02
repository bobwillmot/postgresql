"""Distribution group domain models."""

from dataclasses import dataclass, field
from datetime import datetime, timezone

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


def dg_load(cur: psycopg.Cursor, dg_name: str) -> "QzDistributionGroup | None":
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
    return QzDistributionGroup.from_db_row(row)


@dataclass
class QzDistributionGroup:
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
    ) -> "QzDistributionGroup":
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

    def previous(self, cur: psycopg.Cursor) -> "QzDistributionGroup | None":
        """Load the previous version of this group by ``name`` and ``tx_from``."""
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
        return QzDistributionGroup.from_db_row(row)
