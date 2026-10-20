import uvicorn

from expense_tracker.api import create_app


def main() -> None:
    """Run the local API, bound to the loopback interface by default."""
    uvicorn.run(create_app(), host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
