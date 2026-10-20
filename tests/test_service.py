import pytest

from expense_tracker.database import SQLiteDatabase
from expense_tracker.repository import ExpenseRepository
from expense_tracker.service import ExpenseService, ExpenseValidationError


@pytest.fixture
def service_and_repository(tmp_path):
    database = SQLiteDatabase(tmp_path / "service.sqlite")
    database.initialize()
    repository = ExpenseRepository(database)
    return ExpenseService(repository), repository


def test_create_expense_validates_and_converts_amount_without_float_arithmetic(
    service_and_repository,
):
    service, _ = service_and_repository

    expense = service.create_expense(
        {"amount": "12.34", "category": "  Food  ", "date": "2026-10-20"}
    )

    assert expense.amount_minor_units == 1234
    assert expense.category == "Food"
    assert expense.date == "2026-10-20"


@pytest.mark.parametrize("amount", ["0", "0.00", "-1", "not-money", "1.001", "1e2"])
def test_create_expense_rejects_invalid_amounts_without_persisting(
    service_and_repository, amount
):
    service, repository = service_and_repository

    with pytest.raises(ExpenseValidationError) as error:
        service.create_expense(
            {"amount": amount, "category": "Food", "date": "2026-10-20"}
        )

    assert error.value.issues[0].field == "amount"
    assert repository.category_totals() == []


@pytest.mark.parametrize("category", ["", "   ", None])
def test_create_expense_rejects_blank_category(service_and_repository, category):
    service, repository = service_and_repository

    with pytest.raises(ExpenseValidationError) as error:
        service.create_expense(
            {"amount": "1.00", "category": category, "date": "2026-10-20"}
        )

    assert error.value.issues[0].field == "category"
    assert repository.category_totals() == []


@pytest.mark.parametrize("expense_date", ["2026-02-29", "2026-13-01", "20-10-2026"])
def test_create_expense_rejects_invalid_dates(service_and_repository, expense_date):
    service, repository = service_and_repository

    with pytest.raises(ExpenseValidationError) as error:
        service.create_expense(
            {"amount": "1.00", "category": "Food", "date": expense_date}
        )

    assert error.value.issues[0].field == "date"
    assert repository.category_totals() == []
