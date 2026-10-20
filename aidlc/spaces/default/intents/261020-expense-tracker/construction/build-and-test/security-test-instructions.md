# Security Test Instructions

## Scope and Setup

Validate the two local-exposure safeguards in NFR2: the development server
binds to loopback by default, and expense request content is not written to
application logs. The API test client and pytest are already declared in the
project's optional test dependencies. Tests use only a temporary SQLite file.

## Command

Run the focused security-relevant checks together with the API error-handling
coverage:

```text
python -m pytest tests/test_api.py -q
```

The tests assert the server default host is `127.0.0.1` and that a distinctive
expense category sent in a request does not appear in captured application
logs. They require no credentials, deployed service, or external network.

## Expected Result

All checks pass. No numeric coverage target or additional security test
framework is defined for this express workflow.
