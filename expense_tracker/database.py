"""SQLite connection and schema management for the Expense Tracker."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
import sqlite3


class SQLiteDatabase:
    """Manage schema initialization and short-lived SQLite connections."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def initialize(self) -> None:
        """Create the expense table if it does not exist yet."""
        if self.path != Path(":memory:"):
            self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount_minor_units INTEGER NOT NULL
                        CHECK (amount_minor_units > 0),
                    category TEXT NOT NULL CHECK (length(category) > 0),
                    expense_date TEXT NOT NULL
                )
                """
            )

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        """Yield a transaction-scoped connection and always close it."""
        connection = sqlite3.connect(self.path, timeout=5.0)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()
