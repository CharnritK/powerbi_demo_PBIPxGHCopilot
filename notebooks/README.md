# Notebooks

Notebooks are guided execution surfaces for demos, operator workflows, and exploration.

Rules:

- Keep notebooks numbered and presentation-friendly.
- Import reusable logic from `src/` or compatibility wrappers only.
- Do not duplicate auth, HTTP, or semantic-model parsing logic across notebooks.
- Treat notebooks as consumers of repo code, not the place where core behavior lives.

Canonical notebooks:

- `01_delegated_auth_demo.ipynb`
- `02_service_principal_demo.ipynb`
- `90_legacy_powerbi_rest_api_demo.ipynb`
