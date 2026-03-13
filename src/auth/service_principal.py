"""Service principal authentication for Power BI REST calls."""

from __future__ import annotations

import logging

import msal

from src.common.errors import AuthError
from src.config.models import RuntimeSettings

LOGGER = logging.getLogger(__name__)


def acquire_service_principal_access_token(settings: RuntimeSettings) -> str:
    result = get_service_principal_token(settings)
    return result["access_token"]


def get_service_principal_token(settings: RuntimeSettings) -> dict:
    if not settings.client_secret:
        raise AuthError(
            "CLIENT_SECRET is required for service principal auth. Keep it in .env or a local secret store, never in source control."
        )

    app = msal.ConfidentialClientApplication(
        client_id=settings.client_id,
        client_credential=settings.client_secret,
        authority=f"https://login.microsoftonline.com/{settings.tenant_id}",
    )
    result = app.acquire_token_for_client(scopes=[settings.service_principal_scope])
    if not result.get("access_token"):
        error = result.get("error", "unknown_error")
        description = result.get("error_description", "No description returned.")
        raise AuthError(
            f"{error}: {description} Confirm the tenant admin settings allow service principals to use Power BI APIs and that the app has the required workspace access."
        )

    LOGGER.info("Service principal token acquired successfully.")
    return result
