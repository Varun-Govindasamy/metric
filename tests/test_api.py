import logging
import sqlite3

import pytest
from fastapi.testclient import TestClient

import main
from expense_tracker.api import create_app


@pytest.fixture
def client_and_app(tmp_path):
    app = create_app(tmp_path / "api.sqlite")
    return TestClient(app), app


def test_post_expense_returns_persisted_expense_with_fixed_decimal_amount(
    client_and_app,
):
    client, app = client_and_app

    response = client.post(
        "/expenses",
        json={"amount": 12.3, "category": "  Food ", "date": "2026-10-20"},
    )

    assert response.status_code == 201
    assert response.json()["expense"] == {
        "id": 1,
        "amount": "12.30",
        "category": "Food",
        "date": "2026-10-20",
    }
    assert app.state.repository.get(1).amount_minor_units == 1230


@pytest.mark.parametrize(
    ("payload", "expected_field"),
    [
        ({"amount": 0, "category": "Food", "date": "2026-10-20"}, "amount"),
        ({"amount": "1.00", "category": " ", "date": "2026-10-20"}, "category"),
        ({"amount": "1.00", "category": "Food", "date": "2026-02-29"}, "date"),
        ({"category": "Food", "date": "2026-10-20"}, "amount"),
    ],
)
def test_post_expense_returns_field_specific_errors_without_saving(
    client_and_app, payload, expected_field
):
    client, app = client_and_app

    response = client.post("/expenses", json=payload)

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    assert expected_field in {
        detail["field"] for detail in response.json()["error"]["details"]
    }
    assert app.state.repository.category_totals() == []


@pytest.mark.parametrize("body", [b'{"amount":', b"[]"])
def test_post_expense_rejects_malformed_or_non_object_json(client_and_app, body):
    client, app = client_and_app

    response = client.post(
        "/expenses",
        content=body,
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json()["error"]["details"][0]["field"] == "body"
    assert app.state.repository.category_totals() == []


def test_totals_endpoint_aggregates_saved_expenses_and_empty_state(client_and_app):
    client, _ = client_and_app

    assert client.get("/expenses/totals").json() == {"totals": []}
    for amount, category in [("1.25", "Food"), ("2.75", "Food"), ("9.00", "Travel")]:
        response = client.post(
            "/expenses",
            json={"amount": amount, "category": category, "date": "2026-10-20"},
        )
        assert response.status_code == 201

    totals_response = client.get("/expenses/totals")

    assert totals_response.status_code == 200
    assert totals_response.json() == {
        "totals": [
            {"category": "Food", "amount": "4.00"},
            {"category": "Travel", "amount": "9.00"},
        ]
    }


def test_storage_errors_return_generic_json_without_database_details(
    client_and_app,
):
    client, app = client_and_app
    with app.state.database.connection() as connection:
        connection.execute("DROP TABLE expenses")

    response = client.get("/expenses/totals")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "The request could not be completed because of a storage error.",
        }
    }
    assert "no such table" not in response.text.lower()


def test_expense_request_body_is_not_written_to_application_logs(
    client_and_app, caplog
):
    client, _ = client_and_app
    marker = "private-expense-description"

    with caplog.at_level(logging.DEBUG):
        response = client.post(
            "/expenses",
            json={
                "amount": "12.34",
                "category": marker,
                "date": "2026-10-20",
            },
        )

    assert response.status_code == 201
    assert marker not in caplog.text


def test_development_server_defaults_to_loopback(monkeypatch):
    called = {}

    def capture_run(app, **kwargs):
        called["host"] = kwargs["host"]
        called["port"] = kwargs["port"]

    monkeypatch.setattr(main.uvicorn, "run", capture_run)

    main.main()

    assert called == {"host": "127.0.0.1", "port": 8000}
