from __future__ import annotations

import logging
from typing import Dict

import msal

from config_loader import AppConfig

LOGGER = logging.getLogger(__name__)


def get_service_principal_token(config: AppConfig) -> Dict:
    if not config.client_secret:
        raise ValueError(
            "CLIENT_SECRET is required for service principal authentication. The legacy PBI_CLIENT_SECRET alias is still supported."
        )

    authority = f"https://login.microsoftonline.com/{config.tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id=config.client_id,
        client_credential=config.client_secret,
        authority=authority,
    )

    result = app.acquire_token_for_client(scopes=[config.service_principal_scope])

    if "access_token" not in result:
        error = result.get("error_description", result)
        LOGGER.error("Failed to acquire service principal token: %s", error)
        raise RuntimeError(f"Could not acquire service principal token: {error}")

    LOGGER.info("Service principal token acquired successfully.")
    return result
