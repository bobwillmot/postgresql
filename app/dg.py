"""Distribution group domain models."""

from dataclasses import dataclass, field


@dataclass
class QzDistributionGroup:
    """Represents a distribution group with members and administrators."""

    name: str
    member: list[str] = field(default_factory=list)
    admin: list[str] = field(default_factory=list)

    def to_db_tuple(self) -> tuple[str, list[str], list[str]]:
        """Convert the instance into a tuple matching the ``dg`` table columns."""
        return (self.name, self.member, self.admin)

    @classmethod
    def from_db_row(cls, row: tuple[str, list[str], list[str]]) -> "QzDistributionGroup":
        """Create an instance from a database row.

        Args:
            row: Tuple ordered as ``(name, member, admin)``.
        """
        return cls(name=row[0], member=list(row[1]), admin=list(row[2]))
