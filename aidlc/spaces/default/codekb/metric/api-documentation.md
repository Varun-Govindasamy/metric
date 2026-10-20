# API Documentation

## Discovered API Surface

No HTTP, JSON, command-based business API, or API specification is implemented in the scanned application source. `main.py` is a greeting-only entry point and exposes no endpoint.

## Intent-Level API Contract (Proposed)

The intent requires JSON endpoints but leaves routes and exact schemas open. The following conventional REST paths are assumptions for future design, not discovered implementation:

| Method and path | Purpose | Request | Proposed success response | Authentication |
|---|---|---|---|---|
| `POST /expenses` | Create an expense | JSON object containing positive `amount`, non-empty `category`, and valid `date` (assume `YYYY-MM-DD`) | `201 Created`; JSON representation of the persisted expense | None, per intent |
| `GET /expenses/totals` | Retrieve all-time category totals | No required parameters | `200 OK`; JSON object/list mapping each category to its combined total | None, per intent |

No route version, currency field, date filters, pagination, rate limiting, or authorization behavior is specified. No middleware chain exists. The unauthenticated local service should not be exposed to an untrusted network without a separately authorized security decision.

### Validation and Error Behavior (Proposed)

Reject missing or malformed fields, non-positive amounts, invalid dates, and invalid JSON with a clear client error. A minimal response could identify the field and reason; exact status code and envelope are not yet implemented or specified. Successful writes should not occur for invalid input.

### Example Shape (Illustrative)

Request:

```json
{
  "amount": 12.5,
  "category": "food",
  "date": "2026-10-20"
}
```

Possible category-total response:

```json
{
  "totals": [
    {
      "category": "food",
      "amount": 12.5
    }
  ]
}
```

The example amount shape does not settle currency or precision. Prefer a decimal-safe contract and document the chosen representation before implementation.
