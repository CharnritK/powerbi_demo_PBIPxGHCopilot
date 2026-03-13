# Naming Conventions

Semantic model:

- Fact tables start with `Fact `
- Dimension tables start with `Dim `
- Security bridge tables start with `Security `
- Additive measures prefer `Total <noun>`
- Percent measures use `%`

Repository:

- Notebooks are numbered with a two-digit prefix
- CLI scripts use verb-first names such as `list_workspaces.py`
- Architecture and contract docs use business-readable names, not tool-specific abbreviations where possible
