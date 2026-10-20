# Dependencies

## External Dependencies

| Dependency | Declared version | Usage/status |
|---|---|---|
| None | — | `pyproject.toml` declares `dependencies = []`. |

The intent expects pytest for tests, but it is not currently declared. No HTTP framework or database package is declared. Python's built-in SQLite module can support the selected local storage without an external database server, but the scaffold does not use it.

## Internal Dependencies

| Source | Depends on |
|---|---|
| `main.py` | No internal modules; no imports found. |

No package dependency graph, cycles, or vendored dependencies were found in the application-authored files.

## Dependency and Build Notes

- Project metadata is in `pyproject.toml`; declared project version is `0.1.0`, and Python requirement is `>=3.13`.
- No build backend, lockfile, requirements file, test dependency group, or package-manager-specific dependency manifest was observed in the scanned application-authored files.
- No dependency versions are available to assess for age or advisories.
