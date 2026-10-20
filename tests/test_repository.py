from expense_tracker.database import SQLiteDatabase
from expense_tracker.repository import ExpenseRepository


def make_repository(tmp_path):
    database = SQLiteDatabase(tmp_path / "repository.sqlite")
    database.initialize()
    return ExpenseRepository(database)


def test_create_and_get_returns_the_persisted_expense(tmp_path):
    repository = make_repository(tmp_path)

    created = repository.create(2599, "Travel", "2026-10-20")

    assert created.id > 0
    assert created.amount_minor_units == 2599
    assert created.category == "Travel"
    assert created.date == "2026-10-20"
    assert repository.get(created.id) == created


def test_category_totals_combine_same_category_and_separate_others(tmp_path):
    repository = make_repository(tmp_path)
    repository.create(125, "Food", "2026-10-19")
    repository.create(275, "Food", "2026-10-20")
    repository.create(900, "Travel", "2026-10-20")

    totals = repository.category_totals()

    assert [(row.category, row.total_minor_units) for row in totals] == [
        ("Food", 400),
        ("Travel", 900),
    ]


def test_category_totals_are_empty_without_expenses(tmp_path):
    repository = make_repository(tmp_path)

    assert repository.category_totals() == []
