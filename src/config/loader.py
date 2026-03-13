"""Configuration loader with YAML, env, and legacy alias support."""

from __future__ import annotations

from pathlib import Path
import os
from typing import Any

import yaml
from dotenv import load_dotenv

from src.common.errors import ConfigurationError
from src.common.logging import configure_logging
from src.common.paths import (
    default_pbip_root,
    default_sample_data_path,
    default_semantic_model_definition_path,
    default_workspace_root,
    get_repo_root,
)
from src.config.models import (
    AuthSettings,
    DELEGATED_SCOPES,
    PathSettings,
    PowerBISettings,
    RuntimeSettings,
    SERVICE_PRINCIPAL_SCOPE,
)

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

DEFAULT_QUERY = 'EVALUATE ROW("Demo", 1)'


def load_settings(
    env_name: str | None = None,
    env_path: Path | str | None = None,
    settings_path: Path | str | None = None,
) -> RuntimeSettings:
    repo_root = get_repo_root()
    _load_environment(repo_root, env_path)

    base_settings = _load_yaml(Path(settings_path)) if settings_path else _load_yaml(repo_root / "config" / "settings.yaml")
    resolved_env_name = (
        env_name
        or os.getenv("APP_ENV")
        or os.getenv("ENVIRONMENT")
        or _yaml_get(base_settings, "environment")
        or "dev"
    ).strip().lower()
    env_settings = _load_yaml(repo_root / "config" / "environments" / f"{resolved_env_name}.yaml")

    auth_mode = validate_auth_mode(_resolve_value("AUTH_MODE", base_settings, env_settings) or "delegated")
    log_level = (_resolve_value("LOG_LEVEL", base_settings, env_settings) or "INFO").upper()
    runtime = RuntimeSettings(
        environment=resolved_env_name,
        auth_mode=auth_mode,
        log_level=log_level,
        auth=AuthSettings(
            tenant_id=_read_required("TENANT_ID", base_settings, env_settings),
            client_id=_read_required("CLIENT_ID", base_settings, env_settings),
            client_secret=_resolve_value("CLIENT_SECRET", base_settings, env_settings),
            redirect_uri=_resolve_value("REDIRECT_URI", base_settings, env_settings),
            use_device_code=_read_bool("USE_DEVICE_CODE", base_settings, env_settings, default=True),
            token_cache_path=Path(_resolve_value("TOKEN_CACHE_PATH", base_settings, env_settings) or ".local/msal_token_cache.bin"),
        ),
        powerbi=PowerBISettings(
            workspace_id=_resolve_value("WORKSPACE_ID", base_settings, env_settings),
            dataset_id=_resolve_value("DATASET_ID", base_settings, env_settings),
            dax_query=_resolve_value("DAX_QUERY", base_settings, env_settings) or DEFAULT_QUERY,
            impersonated_user_name=_resolve_value("IMPERSONATED_USER_NAME", base_settings, env_settings),
            request_timeout_seconds=_read_int("REQUEST_TIMEOUT_SECONDS", base_settings, env_settings, default=60),
            delegated_scopes=tuple(_read_csv_values(_resolve_value("DELEGATED_SCOPES", base_settings, env_settings)))
            or DELEGATED_SCOPES,
            service_principal_scope=_resolve_value("SERVICE_PRINCIPAL_SCOPE", base_settings, env_settings)
            or SERVICE_PRINCIPAL_SCOPE,
        ),
        paths=PathSettings(
            repo_root=repo_root,
            powerbi_root=repo_root / "demo-enterprise" / "bi-repo" / "powerbi",
            workspace_root=default_workspace_root(),
            pbip_root=Path(_resolve_value("PBIP_ROOT", base_settings, env_settings) or str(default_pbip_root())),
            semantic_model_definition_path=Path(
                _resolve_value("SEMANTIC_MODEL_DEFINITION_PATH", base_settings, env_settings)
                or str(default_semantic_model_definition_path())
            ),
            sample_data_path=Path(_resolve_value("SAMPLE_DATA_PATH", base_settings, env_settings) or str(default_sample_data_path())),
        ),
    )
    configure_logging(runtime.log_level)
    return runtime


def load_config(
    env_path: Path | str | None = None,
    settings_path: Path | str | None = None,
) -> RuntimeSettings:
    return load_settings(env_path=env_path, settings_path=settings_path)


def validate_auth_mode(auth_mode: str) -> str:
    normalized = auth_mode.strip().lower()
    if normalized == "delegated_user":
        normalized = "delegated"
    if normalized not in {"delegated", "service_principal"}:
        raise ConfigurationError("AUTH_MODE must be either 'delegated' or 'service_principal'.")
    return normalized


def require_group_id(group_id: str | None, settings: RuntimeSettings) -> str:
    value = group_id or settings.workspace_id
    if not value:
        raise ConfigurationError("A workspace ID is required. Set WORKSPACE_ID or pass --group-id.")
    return value


def require_dataset_id(dataset_id: str | None, settings: RuntimeSettings) -> str:
    value = dataset_id or settings.dataset_id
    if not value:
        raise ConfigurationError("A dataset ID is required. Set DATASET_ID or pass --dataset-id.")
    return value


def _load_environment(repo_root: Path, env_path: Path | str | None) -> None:
    if env_path:
        load_dotenv(dotenv_path=env_path, override=False)
        return
    for candidate in (repo_root / ".env", repo_root / "config" / ".env"):
        if candidate.exists():
            load_dotenv(dotenv_path=candidate, override=False)
            return
    load_dotenv(override=False)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    if content is None:
        return {}
    if not isinstance(content, dict):
        raise ConfigurationError(f"Expected mapping at {path}")
    return content


def _read_required(name: str, base_settings: dict[str, Any], env_settings: dict[str, Any]) -> str:
    value = _resolve_value(name, base_settings, env_settings)
    if not value:
        raise ConfigurationError(f"Missing required configuration: {name}")
    return value


def _read_bool(name: str, base_settings: dict[str, Any], env_settings: dict[str, Any], default: bool) -> bool:
    value = _resolve_value(name, base_settings, env_settings)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _read_int(name: str, base_settings: dict[str, Any], env_settings: dict[str, Any], default: int) -> int:
    value = _resolve_value(name, base_settings, env_settings)
    if value is None:
        return default
    return int(value)


def _resolve_value(name: str, base_settings: dict[str, Any], env_settings: dict[str, Any]) -> str | None:
    raw = os.getenv(name)
    if raw is None and name in LEGACY_ENV_NAMES:
        raw = os.getenv(LEGACY_ENV_NAMES[name])
    if raw is not None:
        return _clean(raw)

    for settings in (env_settings, base_settings):
        if not settings:
            continue
        raw = _yaml_lookup(settings, name)
        if raw is not None:
            return _clean(raw)
        if name in LEGACY_ENV_NAMES:
            raw = _yaml_lookup(settings, LEGACY_ENV_NAMES[name])
            if raw is not None:
                return _clean(raw)
    return None


def _yaml_lookup(settings: dict[str, Any], name: str) -> Any:
    if name in settings:
        return settings[name]
    mapping = {
        "TENANT_ID": ("auth", "tenant_id"),
        "CLIENT_ID": ("auth", "client_id"),
        "CLIENT_SECRET": ("auth", "client_secret"),
        "REDIRECT_URI": ("auth", "redirect_uri"),
        "USE_DEVICE_CODE": ("auth", "use_device_code"),
        "TOKEN_CACHE_PATH": ("auth", "token_cache_path"),
        "AUTH_MODE": ("runtime", "auth_mode"),
        "LOG_LEVEL": ("runtime", "log_level"),
        "WORKSPACE_ID": ("powerbi", "workspace_id"),
        "DATASET_ID": ("powerbi", "dataset_id"),
        "DAX_QUERY": ("powerbi", "dax_query"),
        "IMPERSONATED_USER_NAME": ("powerbi", "impersonated_user_name"),
        "REQUEST_TIMEOUT_SECONDS": ("powerbi", "request_timeout_seconds"),
        "DELEGATED_SCOPES": ("powerbi", "delegated_scopes"),
        "SERVICE_PRINCIPAL_SCOPE": ("powerbi", "service_principal_scope"),
        "PBIP_ROOT": ("paths", "pbip_root"),
        "SEMANTIC_MODEL_DEFINITION_PATH": ("paths", "semantic_model_definition_path"),
        "SAMPLE_DATA_PATH": ("paths", "sample_data_path"),
    }
    path = mapping.get(name)
    if not path:
        return None
    cursor: Any = settings
    for step in path:
        if not isinstance(cursor, dict) or step not in cursor:
            return None
        cursor = cursor[step]
    return cursor


def _yaml_get(settings: dict[str, Any], key: str) -> Any:
    return settings.get(key) if isinstance(settings, dict) else None


def _read_csv_values(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _clean(raw: Any) -> str | None:
    if raw is None:
        return None
    if isinstance(raw, list):
        return ",".join(str(item).strip() for item in raw if str(item).strip())
    text = str(raw).strip()
    return text or None
