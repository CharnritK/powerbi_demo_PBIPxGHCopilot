from __future__ import annotations

import logging
from typing import Dict, Optional

import msal

from config_loader import AppConfig

LOGGER = logging.getLogger(__name__)


def _build_public_client(config: AppConfig) -> msal.PublicClientApplication:
    authority = f"https://login.microsoftonline.com/{config.tenant_id}"
    return msal.PublicClientApplication(
        client_id=config.client_id,
        authority=authority,
    )


def get_delegated_user_token(
    config: AppConfig,
    use_interactive_browser: bool = False,
    login_hint: Optional[str] = None,
) -> Dict:
    app = _build_public_client(config)
    scopes = [config.scope]

    accounts = app.get_accounts(username=login_hint)
    if accounts:
        cached = app.acquire_token_silent(scopes=scopes, account=accounts[0])
        if cached and "access_token" in cached:
            LOGGER.info("Delegated token acquired silently from cache.")
            return cached

    if use_interactive_browser:
        if not config.redirect_uri:
            raise ValueError("PBI_REDIRECT_URI is required for interactive delegated auth.")
        result = app.acquire_token_interactive(
            scopes=scopes,
            redirect_uri=config.redirect_uri,
            login_hint=login_hint,
            prompt="select_account",
        )
    else:
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            raise RuntimeError(f"Failed to start device code flow: {flow}")

        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        error = result.get("error_description", result)
        LOGGER.error("Failed to acquire delegated user token: %s", error)
        raise RuntimeError(f"Could not acquire delegated user token: {error}")

    LOGGER.info("Delegated user token acquired successfully.")
    return result
