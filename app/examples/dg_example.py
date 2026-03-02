from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys


if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from app.dg import QzDistributionGroup


def print_version(step: int, group: QzDistributionGroup) -> None:
    print(f"\nChange {step}:")
    print(f"Object: {group}")

    db_row = group.to_db_tuple()
    print(f"As DB tuple: {db_row}")

    reconstructed = QzDistributionGroup.from_db_row(db_row)
    print(f"Reconstructed object: {reconstructed}")


def main() -> None:
    base_time = datetime(2026, 3, 1, 0, 0, tzinfo=timezone.utc)

    change_1 = QzDistributionGroup(
        name="Engineering Updates",
        member=["alice@example.com", "bob@example.com"],
        admin=["lead@example.com"],
        valid_from=base_time,
        tx_from=base_time,
    )

    change_2 = QzDistributionGroup(
        name="Engineering Updates",
        member=["alice@example.com", "bob@example.com", "carol@example.com"],
        admin=["lead@example.com"],
        valid_from=base_time + timedelta(days=1),
        tx_from=base_time + timedelta(days=1),
    )

    change_3 = QzDistributionGroup(
        name="Engineering Platform Updates",
        member=["alice@example.com", "carol@example.com"],
        admin=["lead@example.com", "manager@example.com"],
        valid_from=base_time + timedelta(days=2),
        tx_from=base_time + timedelta(days=2),
    )

    print_version(1, change_1)
    print_version(2, change_2)
    print_version(3, change_3)


if __name__ == "__main__":
    main()
