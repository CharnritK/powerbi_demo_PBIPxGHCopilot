from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

from src.utils.logging_utils import configure_logging

DELEGATED_SCOPES = (
    "https://analysis.windows.net/powerbi/api/Workspace.Read.All",
    "https://analysis.windows.net/powerbi/api/Dataset.Read.All",
    "https://analysis.windows.net/powerbi/api/Report.Read.All",
)

SERVICE_PRINCIPAL_SCOPE = "https://analysis.windows.net/powerbi/api/.default"


@dataclass(frozen=True)
class AppConfig:
    tenant_id: str
    client_id: str
    client_secret: str | None
    workspace_id: str | None
    dataset_id: str | None
    dax_query: str
    impersonated_user_name: str | None
    auth_mode: str
    redirect_uri: str | None
    use_device_code: bool
    log_level: str
    token_cache_path: Path
    request_timeout_seconds: int

    @property
    def delegated_scopes(self) -> list[str]:
        return list(DELEGATED_SCOPES)

    @property
    def service_principal_scope(self) -> str:
        return SERVICE_PRINCIPAL_SCOPE

    def redacted_summary(self) -> dict[str, str | bool | int | None]:
        return {
            "tenant_id": _mask_guid(self.tenant_id),
            "client_id": _mask_guid(self.client_id),
            "workspace_id": _mask_guid(self.workspace_id),
            "dataset_id": _mask_guid(self.dataset_id),
            "auth_mode": self.auth_mode,
            "redirect_uri": self.redirect_uri,
            "use_device_code": self.use_device_code,
            "log_level": self.log_level,
            "token_cache_path": str(self.token_cache_path),
            "request_timeout_seconds": self.request_timeout_seconds,
        }


def load_config(env_path: str | os.PathLike[str] | None = None) -> AppConfig:
    load_dotenv(dotenv_path=env_path)

    config = AppConfig(
        tenant_id=_read_required("TENANT_ID"),
        client_id=_read_required("CLIENT_ID"),
        client_secret=_read_optional("CLIENT_SECRET"),
        workspace_id=_read_optional("WORKSPACE_ID"),
        dataset_id=_read_optional("DATASET_ID"),
        dax_query=_read_optional("DAX_QUERY") or 'EVALUATE ROW("Demo", 1)',
        impersonated_user_name=_read_optional("IMPERSONATED_USER_NAME"),
        auth_mode=(_read_optional("AUTH_MODE") or "delegated").strip().lower(),
        redirect_uri=_read_optional("REDIRECT_URI"),
        use_device_code=_read_bool("USE_DEVICE_CODE", default=True),
        log_level=(_read_optional("LOG_LEVEL") or "INFO").upper(),
        token_cache_path=Path(_read_optional("TOKEN_CACHE_PATH") or ".local/msal_token_cache.bin"),
        request_timeout_seconds=int(_read_optional("REQUEST_TIMEOUT_SECONDS") or "60"),
    )
    configure_logging(config.log_level)
    return config


def validate_auth_mode(auth_mode: str) -> str:
    normalized = auth_mode.strip().lower()
    if normalized not in {"delegated", "service_principal"}:
        raise ValueError("AUTH_MODE must be either 'delegated' or 'service_principal'.")
    return normalized


def require_group_id(group_id: str | None, config: AppConfig) -> str:
    value = group_id or config.workspace_id
    if not value:
        raise ValueError("A workspace ID is required. Set WORKSPACE_ID or pass --group-id.")
    return value


def require_dataset_id(dataset_id: str | None, config: AppConfig) -> str:
    value = dataset_id or config.dataset_id
    if not value:
        raise ValueError("A dataset ID is required. Set DATASET_ID or pass --dataset-id.")
    return value


def _read_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _read_optional(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _read_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _mask_guid(value: str | None) -> str | None:
    if not value:
        return None
    if len(value) <= 8:
        return "****"
    return f"{value[:4]}...{value[-4:]}"
