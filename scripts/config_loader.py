from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

DELEGATED_SCOPES = (
    "https://analysis.windows.net/powerbi/api/Workspace.Read.All",
    "https://analysis.windows.net/powerbi/api/Dataset.Read.All",
    "https://analysis.windows.net/powerbi/api/Report.Read.All",
)

SERVICE_PRINCIPAL_SCOPE = "https://analysis.windows.net/powerbi/api/.default"

LEGACY_ENV_NAMES = {
    "TENANT_ID": "PBI_TENANT_ID",
    "CLIENT_ID": "PBI_CLIENT_ID",
    "CLIENT_SECRET": "PBI_CLIENT_SECRET",
    "WORKSPACE_ID": "PBI_WORKSPACE_ID",
    "DATASET_ID": "PBI_DATASET_ID",
    "AUTH_MODE": "PBI_AUTH_MODE",
    "REDIRECT_URI": "PBI_REDIRECT_URI",
    "LOG_LEVEL": "PBI_LOG_LEVEL",
    "REQUEST_TIMEOUT_SECONDS": "PBI_TIMEOUT_SECONDS",
}

AUTH_MODE_ALIASES = {
    "delegated_user": "delegated",
}


@dataclass
class AppConfig:
    tenant_id: str
    client_id: str
    client_secret: str | None
    redirect_uri: str | None
    auth_mode: str
    delegated_scopes: tuple[str, ...]
    service_principal_scope: str
    workspace_id: str | None
    dataset_id: str | None
    dax_query: str
    impersonated_user_name: str | None
    use_device_code: bool
    timeout_seconds: int
    log_level: str
    token_cache_path: Path


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def load_config(env_path: str | None = None, settings_json_path: str | None = None) -> AppConfig:
    repo_root = Path(__file__).resolve().parent.parent
    _load_environment(repo_root, env_path)
    settings = _load_settings(repo_root, settings_json_path)

    config = AppConfig(
        tenant_id=_read_required(settings, "TENANT_ID"),
        client_id=_read_required(settings, "CLIENT_ID"),
        client_secret=_read_optional(settings, "CLIENT_SECRET"),
        redirect_uri=_read_optional(settings, "REDIRECT_URI"),
        auth_mode=_normalize_auth_mode(_read_optional(settings, "AUTH_MODE") or "delegated"),
        delegated_scopes=_read_scopes(settings),
        service_principal_scope=_read_optional(settings, "SERVICE_PRINCIPAL_SCOPE")
        or _read_optional(settings, "PBI_SCOPE")
        or SERVICE_PRINCIPAL_SCOPE,
        workspace_id=_read_optional(settings, "WORKSPACE_ID"),
        dataset_id=_read_optional(settings, "DATASET_ID"),
        dax_query=_read_optional(settings, "DAX_QUERY") or 'EVALUATE ROW("Demo", 1)',
        impersonated_user_name=_read_optional(settings, "IMPERSONATED_USER_NAME"),
        use_device_code=_read_bool(settings, "USE_DEVICE_CODE", default=True),
        timeout_seconds=_read_int(settings, "REQUEST_TIMEOUT_SECONDS", default=60),
        log_level=(_read_optional(settings, "LOG_LEVEL") or "INFO").upper(),
        token_cache_path=Path(
            _read_optional(settings, "TOKEN_CACHE_PATH") or ".local/msal_token_cache.bin"
        ),
    )

    _export_legacy_aliases(config)
    _setup_logging(config.log_level)
    return config


def _load_environment(repo_root: Path, env_path: str | None) -> None:
    if env_path:
        load_dotenv(env_path, override=False)
        return

    for candidate in (repo_root / ".env", repo_root / "config" / ".env"):
        if candidate.exists():
            load_dotenv(candidate, override=False)
            return

    load_dotenv(override=False)


def _load_settings(repo_root: Path, settings_json_path: str | None) -> dict[str, Any]:
    candidates: list[Path] = []
    if settings_json_path:
        candidates.append(Path(settings_json_path))
    else:
        candidates.append(repo_root / "config" / "settings.json")

    for candidate in candidates:
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return {}


def _read_required(settings: dict[str, Any], name: str) -> str:
    value = _read_optional(settings, name)
    if value:
        return value
    legacy_name = LEGACY_ENV_NAMES.get(name)
    if legacy_name:
        value = _coerce_optional_string(settings.get(legacy_name))
        if value:
            return value
    raise ValueError(f"Missing required configuration: {name}")


def _read_optional(settings: dict[str, Any], name: str) -> str | None:
    raw = os.getenv(name)
    if raw is None and name in LEGACY_ENV_NAMES:
        raw = os.getenv(LEGACY_ENV_NAMES[name])
    if raw is None:
        raw = settings.get(name)
    if raw is None and name in LEGACY_ENV_NAMES:
        raw = settings.get(LEGACY_ENV_NAMES[name])
    return _coerce_optional_string(raw)


def _read_bool(settings: dict[str, Any], name: str, default: bool) -> bool:
    raw = _read_optional(settings, name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _read_int(settings: dict[str, Any], name: str, default: int) -> int:
    raw = _read_optional(settings, name)
    if raw is None:
        return default
    return int(raw)


def _read_scopes(settings: dict[str, Any]) -> tuple[str, ...]:
    raw = _read_optional(settings, "DELEGATED_SCOPES")
    if not raw:
        return DELEGATED_SCOPES
    return tuple(scope.strip() for scope in raw.split(",") if scope.strip())


def _normalize_auth_mode(value: str) -> str:
    normalized = value.strip().lower()
    normalized = AUTH_MODE_ALIASES.get(normalized, normalized)
    if normalized not in {"delegated", "service_principal"}:
        raise ValueError("AUTH_MODE must be either 'delegated' or 'service_principal'.")
    return normalized


def _coerce_optional_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _export_legacy_aliases(config: AppConfig) -> None:
    aliases = {
        "PBI_TENANT_ID": config.tenant_id,
        "PBI_CLIENT_ID": config.client_id,
        "PBI_CLIENT_SECRET": config.client_secret,
        "PBI_WORKSPACE_ID": config.workspace_id,
        "PBI_DATASET_ID": config.dataset_id,
        "PBI_AUTH_MODE": config.auth_mode,
        "PBI_REDIRECT_URI": config.redirect_uri,
        "PBI_SCOPE": config.service_principal_scope,
        "PBI_TIMEOUT_SECONDS": str(config.timeout_seconds),
        "PBI_LOG_LEVEL": config.log_level,
    }
    for key, value in aliases.items():
        if value is not None:
            os.environ[key] = str(value)
