# Repo Decisions

Key decisions:

- `pyproject.toml` is the dependency source of truth; `requirements*.txt` remain convenience wrappers.
- `notebooks/` stays top-level because notebooks are a first-class operator surface in this repo.
- Power BI assets live under `demo-enterprise/bi-repo/powerbi/workspaces/` inside the enterprise demo.
- Compatibility wrappers remain for existing `scripts/*.py` and `src/demos/*` paths.
- Example YAML is committed; local YAML overrides are ignored.
- Presentation assets remain in the repo but are no longer the root navigation model.
