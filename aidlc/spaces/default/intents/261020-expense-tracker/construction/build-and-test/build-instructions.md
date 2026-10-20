# Build Instructions

## Prerequisites

- Python 3.13 or later.
- Install the project and test dependencies from the repository root:
  `python -m pip install -e ".[test]"`
- No external database, Docker, or network service is needed to build or test.

## Build and Verification

Compile the application modules:

```text
python -m compileall -q expense_tracker main.py
```

Run the implementation's focused pytest suite:

```text
python -m pytest tests/test_database.py tests/test_repository.py tests/test_service.py tests/test_api.py -q
```

The pytest command uses isolated temporary SQLite files. For a local manual
run, `python main.py` starts the API on `127.0.0.1:8000`; set
`EXPENSES_DB_PATH` to choose another SQLite file.

## Troubleshooting

- If a package is missing, install the declared dependencies with the command
  above in the project's Python 3.13 environment.
- If tests cannot create their temporary database, check that the temporary
  directory is writable.
- `compileall` checks Python syntax and bytecode compilation; it does not
  contact external services.
