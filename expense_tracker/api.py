"""FastAPI application factory and JSON endpoints."""

import json
import logging
import os
from decimal import Decimal
from pathlib import Path
import sqlite3

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from expense_tracker.database import SQLiteDatabase
from expense_tracker.repository import ExpenseRepository
from expense_tracker.service import (
    ExpenseService,
    ExpenseValidationError,
    ValidationIssue,
)

logger = logging.getLogger(__name__)
DEFAULT_DATABASE_PATH = "expenses.db"


def create_app(db_path: str | Path | None = None) -> FastAPI:
    """Build an API app using a dedicated local SQLite file."""
    selected_path = (
        db_path or os.environ.get("EXPENSES_DB_PATH", DEFAULT_DATABASE_PATH)
    )
    database = SQLiteDatabase(selected_path)
    database.initialize()
    repository = ExpenseRepository(database)
    service = ExpenseService(repository)
    app = FastAPI(title="Expense Tracker API")
    app.state.database = database
    app.state.repository = repository

    @app.exception_handler(sqlite3.Error)
    @app.exception_handler(OSError)
    async def storage_error_handler(request: Request, error: Exception) -> JSONResponse:
        logger.error("Expense storage operation failed")
        return _error_response(
            500,
            "INTERNAL_ERROR",
            "The request could not be completed because of a storage error.",
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, error: Exception) -> JSONResponse:
        logger.error("Unexpected API failure")
        return _error_response(
            500,
            "INTERNAL_ERROR",
            "The request could not be completed.",
        )

    @app.post("/expenses", status_code=201)
    async def create_expense(request: Request) -> JSONResponse:
        payload = await _read_json_object(request)
        expense = service.create_expense(payload)
        return JSONResponse(
            status_code=201,
            content={
                "expense": {
                    "id": expense.id,
                    "amount": _format_amount(expense.amount_minor_units),
                    "category": expense.category,
                    "date": expense.date,
                }
            },
        )

    @app.get("/expenses/totals")
    async def get_expense_totals() -> dict[str, list[dict[str, str]]]:
        return {
            "totals": [
                {
                    "category": total.category,
                    "amount": _format_amount(total.total_minor_units),
                }
                for total in repository.category_totals()
            ]
        }

    @app.exception_handler(ExpenseValidationError)
    async def validation_error_handler(
        request: Request, error: ExpenseValidationError
    ) -> JSONResponse:
        return _error_response(
            400,
            "VALIDATION_ERROR",
            "One or more fields are invalid.",
            [
                {"field": issue.field, "message": issue.message}
                for issue in error.issues
            ],
        )

    return app


async def _read_json_object(request: Request) -> dict[str, object]:
    try:
        body = await request.body()
        payload = json.loads(
            body.decode("utf-8"),
            parse_float=Decimal,
            parse_constant=_reject_nonstandard_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        raise ExpenseValidationError(
            [
                # A malformed body is a request-level issue rather than a field issue.
                _body_validation_issue()
            ]
        ) from None
    if not isinstance(payload, dict):
        raise ExpenseValidationError([_body_validation_issue()])
    return payload


def _body_validation_issue() -> ValidationIssue:
    return ValidationIssue("body", "Request body must be a JSON object.")


def _reject_nonstandard_constant(value: str) -> None:
    raise ValueError(f"Invalid JSON constant: {value}")


def _format_amount(amount_minor_units: int) -> str:
    return f"{amount_minor_units // 100}.{amount_minor_units % 100:02d}"


def _error_response(
    status_code: int,
    code: str,
    message: str,
    details: list[dict[str, str]] | None = None,
) -> JSONResponse:
    error: dict[str, object] = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return JSONResponse(status_code=status_code, content={"error": error})
