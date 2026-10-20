# Intent

Workshop template. Fill in the sections marked (fill in) and leave the
rest as-is. Keep it small --- one service, one or two features.

## How to run

1.  Save this file as
    `aidlc/spaces/default/knowledge/documents/intent.md`

2.  Start the workflow:

    ``` text
    /aidlc express --depth minimal --test-strategy minimal --review advisory --guard-policy off --summary-confirmation off
    ```

3.  Then send:

    ``` text
    Read aidlc/spaces/default/knowledge/documents/intent.md and build what it describes
    ```

4.  When the agent asks a question, "recommended" is almost always the
    right answer. You'll still hit a few approval gates and one Plan
    Approval before any code is written --- read them, then approve.

Prerequisites: Python 3 only. No Docker required --- the app and its
tests run locally with plain pytest.

## Run configuration --- leave as-is

  Setting                 Value
  ----------------------- ----------------------------------------------
  Scope                   express
  Depth                   minimal
  Test strategy           minimal
  Reviews                 advisory
  Guard policy            off
  Summary confirmation    off
  Construction autonomy   automatic
  Architecture            ONE modular monolith (not multiple services)
  Tenancy                 single-tenant

**Standing instruction to the agent:** accept all recommended options by
default; only ask when a decision is genuinely blocking and has no
reasonable default. Record assumptions and keep going --- never stop
just to confirm one.

## What to build

Build a simple Expense Tracker as a single Python application that
allows users to record an expense with an amount, category, and date.
The application must provide a JSON API to add expenses and retrieve the
total amount spent in each category. Use straightforward aggregation
logic to calculate category-wise totals from the stored expenses, with
basic input validation and clear error responses.

## Who uses it

A single user or developer interacting with the Expense Tracker through
its JSON API.

## Must-have behaviors

-   Allow a user to add an expense by providing a positive amount, a
    category, and a valid date; reject invalid input with a clear error
    message.
-   Store valid expenses using a simple SQLite database or an in-memory
    store, following the template's existing stack decisions.
-   Provide an API endpoint that returns the total expense amount
    grouped by category, correctly combining multiple expenses in the
    same category.
-   Include minimal pytest tests covering successful expense creation,
    input validation, and category-wise aggregation.

## Out of scope

-   User authentication, registration, and multi-user support.
-   Frontend UI, dashboards, charts, and graphical reports.
-   Budgets, recurring expenses, expense editing, and deletion.
-   External APIs, cloud deployment, Docker, and separate microservices.
-   Advanced analytics, filtering, and reporting beyond category-wise
    totals.

## Decisions already made --- leave as-is (adjust only if you care)

-   Stack: Python with a file-based SQLite database (or a simple
    in-memory store) --- no Docker, no database server to install. Any
    cloud/Terraform is authored, not applied.
-   Tests: plain pytest, run locally. Do not require Docker,
    testcontainers, or an external database.
-   Auth: none for now (keep it simple).
-   Performance, availability, retention, compliance, other
    non-functional targets: accept recommended defaults.

## Assumptions --- leave as-is

Accept all reasonable assumptions; record them in the artifacts and keep
moving. Do not stop to confirm an assumption.
