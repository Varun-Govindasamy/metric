# Code Generation Plan

## Summary

- Builds: A local Expense Tracker JSON API with SQLite-backed expense creation and category totals.
- Touches: `main.py`, `expense_tracker/`, `tests/`, `pyproject.toml`, and `README.md`.
- Tests: 10 focused pytest tests for storage, validation, expense creation, and aggregation.

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "org",
  "ordering": "implement each applicable testable layer, then write and run that layer's tests.",
  "scope": "express",
  "test_strategy": "minimal",
  "project_type": "brownfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    }
  ],
  "obligations": {
    "strategy": "minimal",
    "strategy_volume": [
      "One verifiable test per requirement at the narrowest effective level.",
      "At least one happy-path unit test per component.",
      "Unit tests are the default; a bugfix/security scope floor may require an integration or E2E regression when that is the narrowest level that reproduces the defect."
    ],
    "scope_floor": [
      "Keep the existing test suite green.",
      "This scope adds no extra new-test floor beyond the selected test strategy."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Verify the existing test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Verify the existing test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:c8f84e35190e007d9863fad236154d0269ab9bf633fc2a3ff106ed965ba4a9b9",
  "contract_sha256": "sha256:bb76c1b22f8307be6e5780d50cabab891684449d5b164bd0e825e9e4e5c61e5b"
}
```

## Implementation Steps

- [x] **Runner and application skeleton:** Replace the greeting-only entry point with a runnable FastAPI application factory and a `127.0.0.1` development entry point. Keep the application as one Python modular monolith.
- [x] **Test runner configuration:** Add the API runtime dependencies and a `test` optional dependency group for pytest and the FastAPI test client. Verify the exact command `python -m pytest tests/test_database.py tests/test_repository.py tests/test_service.py tests/test_api.py -q` is runnable before the first tests are written.
- [x] **Database behavior:** Add SQLite schema initialization and storage of date, category, and integer minor-unit amount. Use transactions and parameterized SQL. Then add and run `tests/test_database.py`.
- [x] **Repository:** Add create and category-total data access using the SQLite database. Then add and run `tests/test_repository.py`.
- [x] **Business logic:** Validate positive decimal amounts with at most two fractional digits, non-empty trimmed categories, and real ISO `YYYY-MM-DD` dates. Convert amounts to integer minor units without binary floating-point arithmetic. Then add and run `tests/test_service.py`.
- [x] **JSON API:** Implement `POST /expenses` and `GET /expenses/totals`, return consistent JSON errors for malformed or invalid requests, and avoid exposing internal exception details. Keep request logging free of expense payloads. Then add and run `tests/test_api.py`.
- [x] **Documentation and traceability:** Update `README.md` with local install, run, database-path, and test instructions; write `code-summary.md` and `traceability.json`.

## Proposed Structure

```text
expense_tracker/
  __init__.py
  api.py
  database.py
  repository.py
  service.py
tests/
  test_database.py
  test_repository.py
  test_service.py
  test_api.py
```

`main.py` remains the command-line development entry point and starts the API
on loopback. `EXPENSES_DB_PATH` selects the SQLite file; use a local default
and a temporary file for tests. No frontend, cloud, Docker, external database,
authentication, edit/delete operations, or date filters are included.

## API and Data Decisions

- `POST /expenses` accepts `amount`, `category`, and `date`; successful creation returns the persisted expense and a created status.
- `GET /expenses/totals` returns category totals in a deterministic category order; an empty database returns an empty totals collection.
- Store amounts as integer minor units in SQLite and serialize monetary values as fixed two-decimal strings. Currency remains unspecified; this does not imply a particular currency.
- Trim surrounding category whitespace, preserve case, and reject a category that is empty after trimming.
- Return field-specific JSON client errors for invalid input; keep internal database details out of responses.
- Create a separate temporary SQLite database for each test so tests cannot mutate the application database.

## Requirement-to-Plan Traceability

| Requirement | Plan steps | Verification |
|---|---|---|
| FR1 — Create and validate expenses | Database behavior, Repository, Business logic, JSON API | Database, repository, service, and API pytest cases |
| FR2 — Return totals grouped by category | Repository, Business logic, JSON API | Repeated-category and multi-category aggregation tests |
| FR3 — Maintain runnable local pytest coverage | Test runner configuration, all test layers | Unit-scoped pytest command in `unit-test-instructions.md` |
| NFR1 — Durable, atomic local persistence | Database behavior, Repository | Reopen the same database; confirm invalid input creates no row |
| NFR2 — Bound unauthenticated API to loopback | Runner and application skeleton, JSON API | Confirm default bind and no full request-body logging |
| NFR3 — Clear errors without internals | Business logic, JSON API | Invalid request responses contain field guidance and no traceback |

## Plan Notes

- Framework choice: FastAPI with Uvicorn, because the repository has no API framework and this provides a small JSON API with a local test client.
- Keep runtime persistence on the standard-library `sqlite3`; do not add an ORM or database server.
- No numeric line-coverage floor is defined for the express scope; tests must meet the Testing Contract and the requirements above.
- The API paths, fixed two-decimal representation, environment-variable name, and error structure are implementation defaults based on the recorded requirements assumptions.
