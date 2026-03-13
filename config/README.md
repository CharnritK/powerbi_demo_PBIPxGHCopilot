# Configuration

This folder holds non-secret configuration templates for the repository.

The canonical secret template lives at the repo root: `.env.example`.
`config/.env.example` is a compatibility copy for teams that prefer the loader fallback at `config/.env`.

Configuration precedence:

1. Environment variables and the repo-root `.env`
2. `config/.env` if the repo-root `.env` is absent
3. Local YAML files such as `config/settings.yaml` and `config/environments/<env>.yaml`
4. Defaults inside `src/config/loader.py`

Committed files in this folder are examples only. Do not store secrets here.

Canonical environment variable names:

- `APP_ENV`
- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET`
- `WORKSPACE_ID`
- `DATASET_ID`
- `AUTH_MODE`
- `REDIRECT_URI`
- `USE_DEVICE_CODE`
- `DAX_QUERY`
- `IMPERSONATED_USER_NAME`
- `LOG_LEVEL`
- `TOKEN_CACHE_PATH`
- `REQUEST_TIMEOUT_SECONDS`

Legacy `PBI_*` aliases are still supported by the loader for compatibility, but new docs and examples treat them as secondary.
