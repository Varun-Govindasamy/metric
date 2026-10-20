# Integration Test Instructions

No separate integration suite is required for this express workflow with the
Minimal test strategy. The existing API tests use FastAPI's in-process test
client with the real service, repository, and temporary SQLite database,
covering the local component boundary without external infrastructure.

Run the existing integration-boundary coverage with:

```text
python -m pytest tests/test_api.py -q
```

Test data is isolated in pytest temporary directories. No coverage percentage
or separate integration test target is defined.
