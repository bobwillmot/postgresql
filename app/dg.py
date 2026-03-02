"""Distribution group domain models."""

from datetime import datetime, timezone
from dataclasses import dataclass, field


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
        row: tuple[
            str,
            list[str],
            list[str],
            datetime,
            datetime | None,
            datetime,
            datetime | None,
        ],
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
