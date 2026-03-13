# Repo Decisions

Key decisions:

- `pyproject.toml` is the dependency source of truth; `requirements*.txt` remain convenience wrappers.
- `notebooks/` stays top-level because notebooks are a first-class operator surface in this repo.
- Power BI assets live under `powerbi/workspaces/` instead of the repo root.
- Compatibility wrappers remain for existing `scripts/*.py` and `src/demos/*` paths.
- Example YAML is committed; local YAML overrides are ignored.
- Presentation assets remain in the repo but are no longer the root navigation model.
