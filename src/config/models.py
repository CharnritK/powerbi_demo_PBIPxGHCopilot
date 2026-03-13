"""Typed runtime settings models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DELEGATED_SCOPES = (
    "https://analysis.windows.net/powerbi/api/Workspace.Read.All",
    "https://analysis.windows.net/powerbi/api/Dataset.Read.All",
    "https://analysis.windows.net/powerbi/api/Report.Read.All",
)
SERVICE_PRINCIPAL_SCOPE = "https://analysis.windows.net/powerbi/api/.default"


@dataclass(frozen=True)
class AuthSettings:
    tenant_id: str
    client_id: str
    client_secret: str | None
    redirect_uri: str | None
    use_device_code: bool
    token_cache_path: Path


@dataclass(frozen=True)
class PowerBISettings:
    workspace_id: str | None
    dataset_id: str | None
    dax_query: str
    impersonated_user_name: str | None
    request_timeout_seconds: int
    delegated_scopes: tuple[str, ...] = DELEGATED_SCOPES
    service_principal_scope: str = SERVICE_PRINCIPAL_SCOPE


@dataclass(frozen=True)
class PathSettings:
    repo_root: Path
    powerbi_root: Path
    workspace_root: Path
    pbip_root: Path
    semantic_model_definition_path: Path
    sample_data_path: Path


@dataclass(frozen=True)
class RuntimeSettings:
    environment: str
    auth_mode: str
    log_level: str
    auth: AuthSettings
    powerbi: PowerBISettings
    paths: PathSettings

    @property
    def tenant_id(self) -> str:
        return self.auth.tenant_id

    @property
    def client_id(self) -> str:
        return self.auth.client_id

    @property
    def client_secret(self) -> str | None:
        return self.auth.client_secret

    @property
    def redirect_uri(self) -> str | None:
        return self.auth.redirect_uri

    @property
    def use_device_code(self) -> bool:
        return self.auth.use_device_code

    @property
    def token_cache_path(self) -> Path:
        return self.auth.token_cache_path

    @property
    def workspace_id(self) -> str | None:
        return self.powerbi.workspace_id

    @property
    def dataset_id(self) -> str | None:
        return self.powerbi.dataset_id

    @property
    def dax_query(self) -> str:
        return self.powerbi.dax_query

    @property
    def impersonated_user_name(self) -> str | None:
        return self.powerbi.impersonated_user_name

    @property
    def request_timeout_seconds(self) -> int:
        return self.powerbi.request_timeout_seconds

    @property
    def timeout_seconds(self) -> int:
        return self.powerbi.request_timeout_seconds

    @property
    def environment_name(self) -> str:
        return self.environment

    @property
    def delegated_scopes(self) -> list[str]:
        return list(self.powerbi.delegated_scopes)

    @property
    def service_principal_scope(self) -> str:
        return self.powerbi.service_principal_scope

    def redacted_summary(self) -> dict[str, str | bool | int | None]:
        return {
            "environment": self.environment,
            "auth_mode": self.auth_mode,
            "tenant_id": _mask_value(self.tenant_id),
            "client_id": _mask_value(self.client_id),
            "workspace_id": _mask_value(self.workspace_id),
            "dataset_id": _mask_value(self.dataset_id),
            "redirect_uri": self.redirect_uri,
            "use_device_code": self.use_device_code,
            "token_cache_path": str(self.token_cache_path),
            "request_timeout_seconds": self.request_timeout_seconds,
            "sample_data_path": str(self.paths.sample_data_path),
        }


def _mask_value(value: str | None) -> str | None:
    if not value:
        return None
    if len(value) <= 8:
        return "****"
    return f"{value[:4]}...{value[-4:]}"
