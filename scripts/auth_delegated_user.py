from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Optional

import msal

from config_loader import AppConfig

LOGGER = logging.getLogger(__name__)


def _build_public_client(
    config: AppConfig,
) -> tuple[msal.PublicClientApplication, msal.SerializableTokenCache]:
    cache = _load_token_cache(config.token_cache_path)
    authority = f"https://login.microsoftonline.com/{config.tenant_id}"
    return (
        msal.PublicClientApplication(
            client_id=config.client_id,
            authority=authority,
            token_cache=cache,
        ),
        cache,
    )


def get_delegated_user_token(
    config: AppConfig,
    use_interactive_browser: bool = False,
    login_hint: Optional[str] = None,
) -> Dict:
    app, cache = _build_public_client(config)
    scopes = list(config.delegated_scopes)

    accounts = app.get_accounts(username=login_hint)
    if accounts:
        cached = app.acquire_token_silent(scopes=scopes, account=accounts[0])
        if cached and "access_token" in cached:
            LOGGER.info("Delegated token acquired silently from cache.")
            return cached

    if use_interactive_browser:
        if not config.redirect_uri:
            raise ValueError(
                "Interactive delegated auth requires REDIRECT_URI. Use device code or set REDIRECT_URI=http://localhost."
            )
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

    _persist_token_cache(cache, config.token_cache_path)
    LOGGER.info("Delegated user token acquired successfully.")
    return result


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
