from datetime import datetime, timezone

from app.dg import QzDistributionGroup


def test_qz_distribution_group_defaults() -> None:
    group = QzDistributionGroup(name="Engineering")

    assert group.name == "Engineering"
    assert group.member == []
    assert group.admin == []
    assert group.valid_from.tzinfo is not None
    assert group.valid_to is None
    assert group.tx_from.tzinfo is not None
    assert group.tx_to is None


def test_qz_distribution_group_to_db_tuple() -> None:
    valid_from = datetime(2026, 1, 1, tzinfo=timezone.utc)
    tx_from = datetime(2026, 1, 2, tzinfo=timezone.utc)
    group = QzDistributionGroup(
        name="Engineering Updates",
        member=["alice@example.com", "bob@example.com"],
        admin=["lead@example.com"],
        valid_from=valid_from,
        tx_from=tx_from,
    )

    assert group.to_db_tuple() == (
        "Engineering Updates",
        ["alice@example.com", "bob@example.com"],
        ["lead@example.com"],
        valid_from,
        None,
        tx_from,
        None,
    )


def test_qz_distribution_group_from_db_row_copies_lists() -> None:
    valid_from = datetime(2026, 1, 1, tzinfo=timezone.utc)
    valid_to = datetime(2026, 2, 1, tzinfo=timezone.utc)
    tx_from = datetime(2026, 1, 2, tzinfo=timezone.utc)
    tx_to = datetime(2026, 2, 2, tzinfo=timezone.utc)
    row = (
        "Engineering Updates",
        ["alice@example.com", "bob@example.com"],
        ["lead@example.com"],
        valid_from,
        valid_to,
        tx_from,
        tx_to,
    )

    group = QzDistributionGroup.from_db_row(row)

    assert group.name == "Engineering Updates"
    assert group.member == ["alice@example.com", "bob@example.com"]
    assert group.admin == ["lead@example.com"]
    assert group.valid_from == valid_from
    assert group.valid_to == valid_to
    assert group.tx_from == tx_from
    assert group.tx_to == tx_to

    row[1].append("carol@example.com")
    row[2].append("manager@example.com")

    assert group.member == ["alice@example.com", "bob@example.com"]
    assert group.admin == ["lead@example.com"]
