from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT_ENV_EXAMPLE = REPO_ROOT / ".env.example"
CONFIG_ENV_EXAMPLE = REPO_ROOT / "config" / ".env.example"

CANONICAL_KEYS = {
    "APP_ENV",
    "TENANT_ID",
    "CLIENT_ID",
    "CLIENT_SECRET",
    "WORKSPACE_ID",
    "DATASET_ID",
    "DAX_QUERY",
    "IMPERSONATED_USER_NAME",
    "AUTH_MODE",
    "REDIRECT_URI",
    "USE_DEVICE_CODE",
    "LOG_LEVEL",
    "TOKEN_CACHE_PATH",
    "REQUEST_TIMEOUT_SECONDS",
}

LEGACY_KEYS = {
    "PBI_TENANT_ID",
    "PBI_CLIENT_ID",
    "PBI_CLIENT_SECRET",
    "PBI_REDIRECT_URI",
    "PBI_AUTH_MODE",
    "PBI_WORKSPACE_ID",
    "PBI_DATASET_ID",
    "PBI_TIMEOUT_SECONDS",
    "PBI_LOG_LEVEL",
}


def _env_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        keys.add(line.split("=", 1)[0].strip())
    return keys


def test_root_env_example_uses_only_canonical_keys() -> None:
    keys = _env_keys(ROOT_ENV_EXAMPLE)

    assert CANONICAL_KEYS.issubset(keys)
    assert LEGACY_KEYS.isdisjoint(keys)


def test_config_env_example_keeps_canonical_keys_and_legacy_aliases() -> None:
    keys = _env_keys(CONFIG_ENV_EXAMPLE)

    assert CANONICAL_KEYS.issubset(keys)
    assert LEGACY_KEYS.issubset(keys)
