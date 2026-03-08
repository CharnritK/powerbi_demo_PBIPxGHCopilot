from __future__ import annotations

import logging

import msal

from src.utils.config import AppConfig

LOGGER = logging.getLogger(__name__)


class ServicePrincipalAuthError(RuntimeError):
    """Raised when service principal auth cannot complete."""


def acquire_service_principal_access_token(config: AppConfig) -> str:
    if not config.client_secret:
        raise ServicePrincipalAuthError(
            "CLIENT_SECRET is required for service principal auth. Keep it in .env or a local secret store, never in source control."
        )

    app = msal.ConfidentialClientApplication(
        client_id=config.client_id,
        client_credential=config.client_secret,
        authority=f"https://login.microsoftonline.com/{config.tenant_id}",
    )
    result = app.acquire_token_for_client(scopes=[config.service_principal_scope])
    if not result.get("access_token"):
        error = result.get("error", "unknown_error")
        description = result.get("error_description", "No description returned.")
        raise ServicePrincipalAuthError(
            f"{error}: {description} Confirm the tenant admin settings allow service principals to use Power BI APIs and that the app has the required workspace access."
        )

    LOGGER.info("Service principal token acquired successfully.")
    return result["access_token"]
