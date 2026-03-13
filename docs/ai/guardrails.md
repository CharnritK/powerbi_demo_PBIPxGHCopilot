# Guardrails

- Do not commit secrets.
- Do not move Power BI artifacts back under generic source folders.
- Do not create measures that collide with existing column names.
- Re-run semantic-model validation after structural model changes.
- Keep notebooks as consumers of `src/`, not owners of business logic.
