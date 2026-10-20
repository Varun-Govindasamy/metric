# Requirements Analysis

## Intent Analysis

Deliver a small, usable Expense Tracker for a single user or developer. The
application replaces the repository's greeting-only Python scaffold with a
local JSON API that records expenses and reports spending totals by category.
The must-have outcome is correct, durable expense creation and aggregation with
clear validation failures, verified by a lightweight pytest suite.

## Functional Requirements

### Expense recording

#### FR1 — Create an expense

The system shall accept a JSON request containing an amount, category, and
expense date, validate it, persist a valid expense in a local SQLite database,
and return the created expense as JSON.

- **Priority:** Must
- **Source:** [desc] Intent document, “What to build” and “Must-have behaviors.”
- **Acceptance criteria:**
  - Given a positive amount, non-empty category, and valid date, when a user
    submits `POST /expenses`, then the API returns a successful creation
    response containing the saved expense.
  - Given an amount that is zero, negative, malformed, or has unsupported
    precision, when the request is submitted, then the API returns a clear
    client error identifying the amount and does not save an expense.
  - Given a missing or blank category, when the request is submitted, then the
    API returns a clear client error identifying the category and does not
    save an expense.
  - Given a missing or invalid calendar date, when the request is submitted,
    then the API returns a clear client error identifying the date and does
    not save an expense.
  - Given malformed JSON or a request with missing required fields, when the
    request is submitted, then the API returns a clear JSON client error and
    does not save an expense.

#### FR2 — Report expense totals by category

The system shall return the sum of saved expense amounts grouped by category
through `GET /expenses/totals`.

- **Priority:** Must
- **Source:** [desc] Intent document, “What to build” and “Must-have behaviors.”
- **Acceptance criteria:**
  - Given multiple saved expenses in the same category, when a user requests
    category totals, then the returned total for that category equals the sum
    of those expenses.
  - Given expenses in different categories, when totals are requested, then
    each category is represented separately and no expense is counted more
    than once.
  - Given no saved expenses, when totals are requested, then the API returns a
    successful empty JSON result.

#### FR3 — Verify the core behavior with pytest

The project shall include locally runnable pytest tests for successful expense
creation, input validation, and category-wise aggregation without Docker or an
external database service.

- **Priority:** Must
- **Source:** [desc] Intent document, “Must-have behaviors” and “Decisions
  already made.”
- **Acceptance criteria:**
  - Given the test prerequisites are installed, when pytest runs, then tests
    cover expense creation, invalid input, and aggregation of multiple
    expenses in one category.
  - Given test data is created, when the test suite finishes, then test
    storage does not modify the application's persistent user database.

## Non-Functional Requirements

#### NFR1 — Local persistence and data integrity

An expense returned as successfully created shall remain available after the
application is restarted. A rejected request shall not create a partial
expense record.

- **Priority:** Must
- **Verification:** Create an expense, reopen the application against the same
  SQLite file, and confirm the expense is present; verify invalid requests do
  not change the stored expense count.
- **Source:** [desc] File-based SQLite decision; [assumption] successful
  creation means durable persistence.

#### NFR2 — Bound unauthenticated access to the local machine

Because authentication is explicitly out of scope and expense data may be
sensitive, the application shall bind to a loopback interface by default and
shall not log full expense request bodies.

- **Priority:** Must
- **Verification:** Inspect the default bind address and confirm expense
  payloads are absent from application logs.
- **Source:** [desc] Single-user, no-auth scope; [assumption] local-only
  default limits exposure.

#### NFR3 — Clear, non-sensitive error responses

For invalid client input, the API shall return a JSON client-error response
that identifies the invalid field and a corrective message. Unexpected
internal failures shall not return stack traces or database details to the
client.

- **Priority:** Must
- **Verification:** Exercise representative invalid requests and confirm the
  response is JSON, identifies the field, and contains no internal traceback
  or database details.
- **Source:** [desc] Intent requires basic input validation and clear error
  responses; [assumption] internal details are not part of the public API.

## Constraints

- Python application; one modular monolith, not multiple services.
- Use a file-based SQLite database; no database server or Docker.
- Use plain pytest locally; do not require testcontainers or an external
  database.
- Single-tenant and unauthenticated; no registration or multi-user support.
- No frontend, cloud deployment, or external API integration.
- Retain the express scope, minimal depth, minimal test strategy, advisory
  reviews, and summary confirmation off.
- **Source:** [desc] Intent document, “Run configuration,” “Out of scope,” and
  “Decisions already made”; [scope] Workflow-selected scope: express.

## Assumptions

These defaults are explicitly non-blocking and may be revised in a later
stage:

1. **HTTP framework:** Select a small, maintained Python framework appropriate
   for a local JSON API; no framework is mandated by the existing project.
   **Reason:** The repository contains no web framework or API contract.
2. **Routes:** Use `POST /expenses` and `GET /expenses/totals`.
   **Reason:** These concise routes match the requested create and totals
   operations; the intent does not prescribe paths.
3. **Amount format:** Accept positive decimal amounts to at most two fractional
   digits and store/sum them without binary floating-point arithmetic.
   Currency is unspecified and shall not be implied.
   **Reason:** Fixed precision is a practical expense-tracking default and
   avoids rounding errors.
4. **Category:** Treat category as a required, trimmed, non-empty string and
   preserve its case; do not impose a fixed category vocabulary.
   **Reason:** No allowed category list or case-normalization rule is supplied.
5. **Date:** Accept valid calendar dates in ISO `YYYY-MM-DD` form, without
   timezone or time-of-day semantics.
   **Reason:** The intent requests a date rather than a timestamp.
6. **Errors:** Use a consistent JSON error shape with field-specific messages;
   distinguish invalid requests from internal storage failures.
   **Reason:** The intent requires clear error responses but defines no schema.
7. **Local serving:** Bind to `127.0.0.1` by default and make the database file
   location configurable without embedding credentials or secrets.
   **Reason:** No authentication is in scope, and expense data should not be
   exposed on an untrusted network.
8. **Performance and operations:** Do not impose a throughput, availability,
   retention, or compliance target beyond reasonable local-app defaults.
   **Reason:** The intent explicitly accepts recommended defaults and gives
   no workload or regulatory target.

## Out of Scope

- User authentication, registration, and multi-user support.
- Frontend UI, dashboards, charts, or graphical reports.
- Budgets, recurring expenses, expense editing, and deletion.
- External APIs, cloud deployment, Docker, separate microservices, and
  external database services.
- Advanced analytics, filtering, or reporting beyond category totals.
- Currency conversion, exchange rates, and a mandated category taxonomy.
- Date-range filtering or timezone-aware timestamps.

## Open Questions

None block implementation. Currency, amount precision, category normalization,
and the exact public error schema remain assumptions above; the user asked that
reasonable defaults be recorded and carried forward rather than confirmed.

## Sources

- [desc] Initial description: Read aidlc/spaces/default/knowledge/documents/intent.md and build what it describes
- [scope] Workflow-selected scope: express
- User-provided product requirements: `aidlc/spaces/default/knowledge/documents/intent.md`
- Brownfield facts: `aidlc/spaces/default/codekb/metric/business-overview.md`,
  `architecture.md`, and `code-structure.md`

## Assumptions & Open Questions

The assumptions above are planning defaults, not additional user-confirmed
requirements. No unresolved question blocks the minimal implementation.
