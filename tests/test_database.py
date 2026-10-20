import sqlite3

import pytest

from expense_tracker.database import SQLiteDatabase


def test_schema_initialization_is_repeatable_and_has_expected_fields(tmp_path):
    database_path = tmp_path / "expenses.sqlite"
    database = SQLiteDatabase(database_path)

    database.initialize()
    database.initialize()

    with sqlite3.connect(database_path) as connection:
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(expenses)").fetchall()
        }
    assert columns == {"id", "amount_minor_units", "category", "expense_date"}


def test_database_stores_expense_fields_and_survives_reopening(tmp_path):
    database_path = tmp_path / "expenses.sqlite"
    database = SQLiteDatabase(database_path)
    database.initialize()

    with database.connection() as connection:
        connection.execute(
            """
            INSERT INTO expenses (amount_minor_units, category, expense_date)
            VALUES (?, ?, ?)
            """,
            (1234, "Food", "2026-10-20"),
        )

    reopened_database = SQLiteDatabase(database_path)
    reopened_database.initialize()
    with reopened_database.connection() as connection:
        saved_row = connection.execute(
            """
            SELECT amount_minor_units, category, expense_date
            FROM expenses
            """
        ).fetchone()

    assert tuple(saved_row) == (1234, "Food", "2026-10-20")


@pytest.mark.parametrize(
    ("amount_minor_units", "category"),
    [(0, "Food"), (100, "")],
)
def test_database_rejects_nonpositive_amount_or_empty_category(
    tmp_path, amount_minor_units, category
):
    database = SQLiteDatabase(tmp_path / "expenses.sqlite")
    database.initialize()

    with pytest.raises(sqlite3.IntegrityError):
        with database.connection() as connection:
            connection.execute(
                """
                INSERT INTO expenses (amount_minor_units, category, expense_date)
                VALUES (?, ?, ?)
                """,
                (amount_minor_units, category, "2026-10-20"),
            )

    with database.connection() as connection:
        assert connection.execute("SELECT COUNT(*) FROM expenses").fetchone()[0] == 0
