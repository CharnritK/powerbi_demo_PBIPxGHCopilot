"""Delegated user authentication for Power BI REST calls."""

from __future__ import annotations

import logging

import msal

from src.auth.token_cache import load_token_cache, persist_token_cache
from src.common.errors import AuthError
from src.config.models import RuntimeSettings

LOGGER = logging.getLogger(__name__)


def acquire_delegated_access_token(
    settings: RuntimeSettings,
    use_device_code: bool | None = None,
    login_hint: str | None = None,
) -> str:
    result = get_delegated_user_token(
        settings=settings,
        use_interactive_browser=not (settings.use_device_code if use_device_code is None else use_device_code),
        login_hint=login_hint,
    )
    return result["access_token"]


def get_delegated_user_token(
    settings: RuntimeSettings,
    use_interactive_browser: bool = False,
    login_hint: str | None = None,
) -> dict:
    cache = load_token_cache(settings.token_cache_path)
    app = msal.PublicClientApplication(
        client_id=settings.client_id,
        authority=f"https://login.microsoftonline.com/{settings.tenant_id}",
        token_cache=cache,
    )
    scopes = settings.delegated_scopes
    accounts = app.get_accounts(username=login_hint)
    if accounts:
        cached = app.acquire_token_silent(scopes=scopes, account=accounts[0])
        if cached and cached.get("access_token"):
            LOGGER.info("Using cached delegated token.")
            return cached

    if use_interactive_browser:
        if not settings.redirect_uri:
            raise AuthError(
                "Interactive delegated auth requires REDIRECT_URI. Use device code flow or set REDIRECT_URI=http://localhost."
            )
        result = app.acquire_token_interactive(
            scopes=scopes,
            redirect_uri=settings.redirect_uri,
            login_hint=login_hint,
            prompt="select_account",
        )
    else:
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            raise AuthError(
                "Device code flow could not start. Confirm the app supports public client flows and delegated API permissions."
            )
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)

    if not result.get("access_token"):
        raise _build_auth_error(result)

    persist_token_cache(cache, settings.token_cache_path)
    return result


def _build_auth_error(result: dict) -> AuthError:
    error = result.get("error", "unknown_error")
    description = result.get("error_description", "No description returned.")
    correlation_id = result.get("correlation_id")
    detail = f"{error}: {description}"
    if correlation_id:
        detail = f"{detail} Correlation ID: {correlation_id}"
    return AuthError(detail)
