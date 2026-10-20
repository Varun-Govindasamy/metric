# Unit Test Instructions

## Scope

This express workflow has no Unit DAG. These instructions cover the single
Code Generation stage and its four planned pytest files.

## Test Framework and Setup

- Python: 3.13 as selected by `.python-version`.
- Framework: pytest, using FastAPI's `TestClient` for API-level tests.
- Add FastAPI and Uvicorn as runtime dependencies, and pytest plus HTTPX in
  the project's `test` optional dependency group.
- Install the project and test dependencies with:
  `python -m pip install -e ".[test]"`
- No Docker, testcontainers, or external database is required.

## Exact Test Command

Run only the tests for this implementation:

```text
python -m pytest tests/test_database.py tests/test_repository.py tests/test_service.py tests/test_api.py -q
```

The command is the required runner/configuration check before the first test
file is written. Run it again after each layer's tests are added and after all
implementation steps are complete.

## Planned Coverage

Target 10 focused tests, adjusted only if implementation details make an
equivalent assertion clearer:

- `tests/test_database.py`: schema initialization is repeatable and the
  expected expense fields are stored.
- `tests/test_repository.py`: create and retrieve expenses; combine amounts
  for a category; keep different categories separate; return no totals for an
  empty database.
- `tests/test_service.py`: accept a valid expense; reject non-positive or
  malformed/over-precision amounts; reject blank categories; reject invalid
  dates.
- `tests/test_api.py`: create an expense successfully; return field-specific
  validation errors; aggregate persisted expenses through the JSON endpoint.

These tests cover FR1, FR2, and FR3 and provide at least one happy path for the
database, repository, business-logic, and API components.

## Data and Isolation

- Use pytest temporary directories/files for SQLite databases.
- Construct each app/repository with a test-specific database path; never use
  the default user database in tests.
- Do not depend on test order or shared mutable database state.
- Use fixed inputs and exact expected integer minor-unit totals / serialized
  decimal values.

## Expected Targets

- No numeric coverage percentage is specified for the express scope.
- Preserve all existing test behavior; no application tests were found during
  reverse engineering.
- Verify rejected requests do not create persisted rows.

## Mocking

Use real temporary SQLite databases for persistence and aggregation tests.
Use FastAPI's in-process test client for endpoint tests; no external network
service or database mock is needed.
