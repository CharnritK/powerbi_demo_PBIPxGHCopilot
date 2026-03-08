from __future__ import annotations

import logging
from pathlib import Path

import msal

from src.utils.config import AppConfig

LOGGER = logging.getLogger(__name__)


class DelegatedAuthError(RuntimeError):
    """Raised when delegated authentication cannot complete."""


def acquire_delegated_access_token(
    config: AppConfig,
    use_device_code: bool | None = None,
    login_hint: str | None = None,
) -> str:
    cache = _load_token_cache(config.token_cache_path)
    app = msal.PublicClientApplication(
        client_id=config.client_id,
        authority=f"https://login.microsoftonline.com/{config.tenant_id}",
        token_cache=cache,
    )
    scopes = config.delegated_scopes
    selected_device_code = config.use_device_code if use_device_code is None else use_device_code

    accounts = app.get_accounts(username=login_hint)
    if accounts:
        cached = app.acquire_token_silent(scopes=scopes, account=accounts[0])
        if cached and cached.get("access_token"):
            LOGGER.info("Using cached delegated token for the local demo.")
            return cached["access_token"]

    if selected_device_code:
        result = _acquire_device_code_token(app, scopes)
    else:
        result = _acquire_browser_token(app, scopes, config.redirect_uri, login_hint)

    if not result.get("access_token"):
        _raise_auth_error(result)

    _persist_token_cache(cache, config.token_cache_path)
    return result["access_token"]


def _acquire_device_code_token(app: msal.PublicClientApplication, scopes: list[str]) -> dict:
    flow = app.initiate_device_flow(scopes=scopes)
    if "user_code" not in flow:
        raise DelegatedAuthError(
            "Device code flow could not start. Confirm the app supports public client flows and delegated API permissions."
        )
    print(flow["message"])
    return app.acquire_token_by_device_flow(flow)


def _acquire_browser_token(
    app: msal.PublicClientApplication,
    scopes: list[str],
    redirect_uri: str | None,
    login_hint: str | None,
) -> dict:
    if not redirect_uri:
        raise DelegatedAuthError(
            "Interactive browser auth requires REDIRECT_URI. Use device code flow or set REDIRECT_URI=http://localhost."
        )
    return app.acquire_token_interactive(
        scopes=scopes,
        redirect_uri=redirect_uri,
        login_hint=login_hint,
        prompt="select_account",
    )


def _load_token_cache(cache_path: Path) -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()
    if cache_path.exists():
        cache.deserialize(cache_path.read_text(encoding="utf-8"))
    return cache


def _persist_token_cache(cache: msal.SerializableTokenCache, cache_path: Path) -> None:
    if not cache.has_state_changed:
        return
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(cache.serialize(), encoding="utf-8")


def _raise_auth_error(result: dict) -> None:
    error = result.get("error", "unknown_error")
    description = result.get("error_description", "No description returned.")
    correlation_id = result.get("correlation_id")
    detail = f"{error}: {description}"
    if correlation_id:
        detail = f"{detail} Correlation ID: {correlation_id}"
    raise DelegatedAuthError(detail)
