# Business Overview

## Purpose and Domain

The intended product is a small, single-tenant Expense Tracker for one user or developer. Its domain is recording dated expenses and understanding spending grouped by category. The source of truth for these requirements is `aidlc/spaces/default/knowledge/documents/intent.md`.

## Intended Capabilities

- Create an expense from a positive amount, a category, and a valid date.
- Reject invalid input with a clear error response.
- Persist expenses in a local file-based SQLite database.
- Return totals grouped by category, combining expenses in each category.
- Include minimal pytest coverage for creation, validation, and category aggregation.

Authentication, multiple users, UI, editing/deletion, budgets, external services, cloud deployment, and advanced reporting are explicitly out of scope.

## Current Implementation

The repository is currently a Python scaffold, not an Expense Tracker: `main.py` only prints a greeting. There is no HTTP/JSON API, expense model, validation, SQLite persistence, aggregation, or test suite in the application source. The intent describes work to be built, not behavior already present.

## Assumptions to Preserve

- Use SQLite on disk as selected by the intent's stack decision; do not substitute ephemeral memory storage.
- A reasonable REST contract is `POST /expenses` for creation and `GET /expenses/totals` for category totals. These paths are assumptions because the intent does not prescribe route names.
- Store amounts as decimal-safe values (for example integer minor units) rather than binary floating-point values; the currency and precision remain unspecified.
- Treat dates as calendar dates in an unambiguous ISO `YYYY-MM-DD` format. The intent does not define currency, timezone, category vocabulary, or date-range filters.
- Keep the service single-tenant and local-first. The deployment/listening interface is not specified; avoid exposing an unauthenticated API beyond a trusted local boundary by default.
- Keep pytest lightweight and runnable locally, with no Docker or external database service.
