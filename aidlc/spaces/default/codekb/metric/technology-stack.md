# Technology Stack

| Area | Observed technology | Evidence and notes |
|---|---|---|
| Language | Python | Root application file is `main.py`. |
| Python constraint | `>=3.13` | `pyproject.toml`. |
| Runtime selector | Python `3.13` | `.python-version`; this is a configured version, not confirmation of the executing interpreter. |
| Project metadata/build configuration | `pyproject.toml` | Project name `metric`, version `0.1.0`; no build backend or tool configuration declared. |
| Runtime libraries | None declared | `dependencies = []`. |
| API framework | None detected | No framework imports or API configuration present. |
| Persistence | None implemented | Intent selects file-based SQLite; no database code or file exists in the application source. SQLite is available through Python's standard library but is not currently used. |
| Tests | None present | Intent calls for local pytest tests; pytest is not declared in project metadata. |
| Packaging/container/cloud | None detected | No Docker, cloud, or deployment configuration found in application-authored scope. |

No installed package versions or actual interpreter version were established; the scan did not run environment probes or project commands.
