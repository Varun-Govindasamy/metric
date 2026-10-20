"""Expense validation and exact monetary conversion."""

from dataclasses import dataclass
from datetime import date as calendar_date
from decimal import Decimal
import re

from expense_tracker.repository import Expense, ExpenseRepository

_AMOUNT_PATTERN = re.compile(r"[0-9]+(?:\.[0-9]{1,2})?\Z")
_DATE_PATTERN = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")


@dataclass(frozen=True)
class ValidationIssue:
    """One field-specific client input problem."""

    field: str
    message: str


class ExpenseValidationError(ValueError):
    """Raised when client values do not satisfy expense rules."""

    def __init__(self, issues: list[ValidationIssue]) -> None:
        self.issues = issues
        super().__init__("Expense input failed validation.")


class ExpenseService:
    """Apply business validation before calling the persistence layer."""

    def __init__(self, repository: ExpenseRepository) -> None:
        self.repository = repository

    def create_expense(self, payload: dict[str, object]) -> Expense:
        """Validate expense fields and save a valid expense."""
        issues: list[ValidationIssue] = []
        amount_minor_units = self._parse_amount(payload.get("amount"), issues)
        category = self._parse_category(payload.get("category"), issues)
        expense_date = self._parse_date(payload.get("date"), issues)
        if issues:
            raise ExpenseValidationError(issues)
        return self.repository.create(amount_minor_units, category, expense_date)

    @staticmethod
    def _parse_amount(value: object, issues: list[ValidationIssue]) -> int:
        if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
            issues.append(
                ValidationIssue("amount", "Provide a positive amount with at most two decimal places.")
            )
            return 0
        amount_text = str(value).strip()
        if not _AMOUNT_PATTERN.fullmatch(amount_text):
            issues.append(
                ValidationIssue("amount", "Provide a positive amount with at most two decimal places.")
            )
            return 0
        amount = Decimal(amount_text)
        if amount <= 0:
            issues.append(ValidationIssue("amount", "Amount must be greater than zero."))
            return 0
        if amount > Decimal("92233720368547758.07"):
            issues.append(ValidationIssue("amount", "Amount exceeds the supported storage range."))
            return 0
        return int(amount * 100)

    @staticmethod
    def _parse_category(value: object, issues: list[ValidationIssue]) -> str:
        if not isinstance(value, str) or not value.strip():
            issues.append(ValidationIssue("category", "Category must be a non-empty string."))
            return ""
        return value.strip()

    @staticmethod
    def _parse_date(value: object, issues: list[ValidationIssue]) -> str:
        if not isinstance(value, str) or not _DATE_PATTERN.fullmatch(value):
            issues.append(ValidationIssue("date", "Date must be a valid YYYY-MM-DD calendar date."))
            return ""
        try:
            calendar_date.fromisoformat(value)
        except ValueError:
            issues.append(ValidationIssue("date", "Date must be a valid YYYY-MM-DD calendar date."))
            return ""
        return value
