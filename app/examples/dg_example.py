from app.dg import QzDistributionGroup


def main() -> None:
    group = QzDistributionGroup(
        name="Engineering Updates",
        member=["alice@example.com", "bob@example.com"],
        admin=["lead@example.com"],
    )
    print(f"Original object: {group}")

    db_row = group.to_db_tuple()
    print(f"As DB tuple: {db_row}")

    reconstructed = QzDistributionGroup.from_db_row(db_row)
    print(f"Reconstructed object: {reconstructed}")


if __name__ == "__main__":
    main()
