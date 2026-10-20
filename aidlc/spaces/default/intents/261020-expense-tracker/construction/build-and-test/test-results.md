# Build and Test Results

## Build

- Command: `python -m compileall -q expense_tracker main.py`
- Result: Passed (exit code 0).
- Output: No errors or warnings.

## Unit and API Tests

- Command: `python -m pytest tests/test_database.py tests/test_repository.py tests/test_service.py tests/test_api.py -q`
- Result: **31 passed, 0 failed, 0 skipped** in 1.87 seconds.
- Coverage report: Not generated; no numeric coverage target is defined for
  this express workflow.
- Warning: Starlette emitted a deprecation warning that using HTTPX with
  `starlette.testclient` is deprecated. The warning did not affect test
  results.

The API boundary/security command
`python -m pytest tests/test_api.py -q` was also run: **11 passed** in
1.40 seconds. Those 11 tests overlap the 31-test focused suite and are not
double-counted.

## Target Verification Matrix

| Target ID | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|
| NFR1-PERSISTENCE | Reopened SQLite retains saved expenses; rejected requests create no partial row | Persistence and invalid-input checks passed | `tests/test_database.py`, `tests/test_service.py`, `tests/test_api.py`; focused pytest command | build-and-test | Met |
| NFR2-LOOPBACK | Development server defaults to `127.0.0.1` | Test asserted host `127.0.0.1` and port `8000` | `tests/test_api.py::test_development_server_defaults_to_loopback` | build-and-test | Met |
| NFR2-LOGGING | Full expense request content is absent from application logs | Distinctive submitted marker was absent from captured logs | `tests/test_api.py::test_expense_request_body_is_not_written_to_application_logs` | build-and-test | Met |
| NFR3-ERRORS | Invalid input identifies fields; internal storage details are not returned | Validation and generic storage-error checks passed | `tests/test_api.py`; focused pytest command | build-and-test | Met |
| EXPRESS-CI | No CI execution target is defined for this express plan; CI Pipeline is skipped | Not applicable: the plan runs no CI Pipeline and defines no CI target | `aidlc-state.md`, stage plan | Not applicable | N/A |

## Failures and Follow-Up

No build or test failures occurred. No loop-back was needed.
