# Expense Tracker

A local, single-tenant JSON API for recording expenses and viewing totals by
category. Expenses are stored in SQLite; amounts are saved as integer minor
units and returned as fixed two-decimal strings. No currency is implied.

## Requirements

- Python 3.13 or later

## Install

Create and activate a virtual environment, then install the app and test
dependencies:

```text
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

On macOS or Linux:

```sh
source .venv/bin/activate
python -m pip install -e ".[test]"
```

## Run locally

```text
python main.py
```

The development server listens on `127.0.0.1:8000`. The default SQLite
database is `expenses.db` in the current working directory. Set
`EXPENSES_DB_PATH` to select another database file.

PowerShell:

```powershell
$env:EXPENSES_DB_PATH = ".\data\expenses.sqlite"
python main.py
```

macOS or Linux:

```sh
EXPENSES_DB_PATH=./data/expenses.sqlite python main.py
```

## API

Create an expense with `POST /expenses`:

```json
{
  "amount": "12.34",
  "category": "Food",
  "date": "2026-10-20"
}
```

The successful response has status `201` and returns the persisted expense.
Amounts must be positive, with no more than two fractional digits; dates must
be real calendar dates in `YYYY-MM-DD` form. Categories are trimmed and may
not be empty. Invalid input returns a JSON error with field-specific details.

Fetch category totals with `GET /expenses/totals`. Totals are ordered by
category and returned with fixed two-decimal string amounts. An empty database
returns `{"totals":[]}`.

## Tests

Run the focused test suite with:

```text
python -m pytest tests/test_database.py tests/test_repository.py tests/test_service.py tests/test_api.py -q
```

All tests use temporary SQLite files and do not modify the application's
database.