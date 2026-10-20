"""SQLite-backed expense persistence and category aggregation."""

from dataclasses import dataclass
import sqlite3

from expense_tracker.database import SQLiteDatabase


@dataclass(frozen=True)
class Expense:
    """A persisted expense with an integer minor-unit amount."""

    id: int
    amount_minor_units: int
    category: str
    date: str


@dataclass(frozen=True)
class CategoryTotal:
    """A category and its aggregated integer minor-unit amount."""

    category: str
    total_minor_units: int


class ExpenseRepository:
    """Provide parameterized SQLite operations for expenses."""

    def __init__(self, database: SQLiteDatabase) -> None:
        self.database = database

    def create(self, amount_minor_units: int, category: str, date: str) -> Expense:
        """Persist an expense atomically and return the stored row."""
        with self.database.connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO expenses (amount_minor_units, category, expense_date)
                VALUES (?, ?, ?)
                """,
                (amount_minor_units, category, date),
            )
            row = connection.execute(
                """
                SELECT id, amount_minor_units, category, expense_date
                FROM expenses WHERE id = ?
                """,
                (cursor.lastrowid,),
            ).fetchone()
        return self._to_expense(row)

    def get(self, expense_id: int) -> Expense | None:
        """Find one expense by its ID."""
        with self.database.connection() as connection:
            row = connection.execute(
                """
                SELECT id, amount_minor_units, category, expense_date
                FROM expenses WHERE id = ?
                """,
                (expense_id,),
            ).fetchone()
        return self._to_expense(row) if row is not None else None

    def category_totals(self) -> list[CategoryTotal]:
        """Return category sums in deterministic case-sensitive order."""
        with self.database.connection() as connection:
            rows = connection.execute(
                """
                SELECT category, SUM(amount_minor_units) AS total_minor_units
                FROM expenses
                GROUP BY category
                ORDER BY category COLLATE BINARY
                """
            ).fetchall()
        return [
            CategoryTotal(
                category=row["category"],
                total_minor_units=row["total_minor_units"],
            )
            for row in rows
        ]

    @staticmethod
    def _to_expense(row: sqlite3.Row) -> Expense:
        return Expense(
            id=row["id"],
            amount_minor_units=row["amount_minor_units"],
            category=row["category"],
            date=row["expense_date"],
        )
