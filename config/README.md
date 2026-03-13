# Configuration

This folder holds non-secret configuration templates for the repository.

Configuration precedence:

1. Environment variables and the local `.env`
2. Local YAML files such as `config/settings.yaml` and `config/environments/<env>.yaml`
3. Defaults inside `src/config/loader.py`

Committed files in this folder are examples only. Do not store secrets here.

Canonical environment variable names:

- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET`
- `WORKSPACE_ID`
- `DATASET_ID`
- `AUTH_MODE`
- `REDIRECT_URI`
- `USE_DEVICE_CODE`
- `TOKEN_CACHE_PATH`
- `REQUEST_TIMEOUT_SECONDS`

Legacy `PBI_*` aliases are still supported by the loader for compatibility.
