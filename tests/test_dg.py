from app.dg import QzDistributionGroup


def test_qz_distribution_group_defaults() -> None:
    group = QzDistributionGroup(name="Engineering")

    assert group.name == "Engineering"
    assert group.member == []
    assert group.admin == []


def test_qz_distribution_group_to_db_tuple() -> None:
    group = QzDistributionGroup(
        name="Engineering Updates",
        member=["alice@example.com", "bob@example.com"],
        admin=["lead@example.com"],
    )

    assert group.to_db_tuple() == (
        "Engineering Updates",
        ["alice@example.com", "bob@example.com"],
        ["lead@example.com"],
    )


def test_qz_distribution_group_from_db_row_copies_lists() -> None:
    row = (
        "Engineering Updates",
        ["alice@example.com", "bob@example.com"],
        ["lead@example.com"],
    )

    group = QzDistributionGroup.from_db_row(row)

    assert group.name == "Engineering Updates"
    assert group.member == ["alice@example.com", "bob@example.com"]
    assert group.admin == ["lead@example.com"]

    row[1].append("carol@example.com")
    row[2].append("manager@example.com")

    assert group.member == ["alice@example.com", "bob@example.com"]
    assert group.admin == ["lead@example.com"]
