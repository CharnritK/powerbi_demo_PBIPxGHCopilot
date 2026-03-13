"""Delegated user authentication for Power BI REST calls."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from queue import Queue
from threading import Thread
from urllib.parse import parse_qs, urlparse
import webbrowser

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
    authority = f"https://login.microsoftonline.com/{settings.tenant_id}"
    app = msal.PublicClientApplication(
        client_id=settings.client_id,
        authority=authority,
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
        result = _acquire_browser_token(
            settings=settings,
            authority=authority,
            cache=cache,
            login_hint=login_hint,
        )
    else:
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            raise AuthError(
                "Device code flow could not start. Confirm the app supports public client flows and delegated API permissions."
            )
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)
        if _should_fallback_to_confidential_browser(result, settings):
            LOGGER.info("Falling back to browser sign-in because device code flow requires a client secret for this app registration.")
            result = _acquire_browser_token(
                settings=settings,
                authority=authority,
                cache=cache,
                login_hint=login_hint,
            )

    if not result.get("access_token"):
        raise _build_auth_error(result)

    persist_token_cache(cache, settings.token_cache_path)
    return result


def _acquire_browser_token(
    settings: RuntimeSettings,
    authority: str,
    cache: msal.SerializableTokenCache,
    login_hint: str | None,
) -> dict:
    if not settings.redirect_uri:
        raise AuthError(
            "Interactive delegated auth requires REDIRECT_URI. Use device code flow or set REDIRECT_URI=http://localhost."
        )
    if settings.client_secret:
        return _acquire_confidential_browser_token(
            settings=settings,
            authority=authority,
            cache=cache,
            login_hint=login_hint,
        )

    app = msal.PublicClientApplication(
        client_id=settings.client_id,
        authority=authority,
        token_cache=cache,
    )
    return app.acquire_token_interactive(
        scopes=settings.delegated_scopes,
        redirect_uri=settings.redirect_uri,
        login_hint=login_hint,
        prompt="select_account",
    )


def _acquire_confidential_browser_token(
    settings: RuntimeSettings,
    authority: str,
    cache: msal.SerializableTokenCache,
    login_hint: str | None,
) -> dict:
    parsed = urlparse(settings.redirect_uri or "")
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"localhost", "127.0.0.1"}:
        raise AuthError("Confidential browser auth requires REDIRECT_URI to use a localhost loopback URL.")

    app = msal.ConfidentialClientApplication(
        client_id=settings.client_id,
        client_credential=settings.client_secret,
        authority=authority,
        token_cache=cache,
    )
    flow = app.initiate_auth_code_flow(
        scopes=settings.delegated_scopes,
        redirect_uri=settings.redirect_uri,
        prompt="select_account",
        login_hint=login_hint,
    )
    auth_uri = flow.get("auth_uri")
    if not auth_uri:
        raise AuthError("Interactive browser auth could not start. The app registration may be missing a valid redirect URI.")

    auth_response = _wait_for_loopback_redirect(settings.redirect_uri, auth_uri)
    return app.acquire_token_by_auth_code_flow(flow, auth_response)


def _wait_for_loopback_redirect(redirect_uri: str, auth_uri: str) -> dict[str, str]:
    parsed = urlparse(redirect_uri)
    host = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    response_queue: Queue[dict[str, str]] = Queue(maxsize=1)

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            request_url = urlparse(self.path)
            if request_url.path != path:
                self.send_error(404)
                return
            payload = {
                key: values[0] if len(values) == 1 else ",".join(values)
                for key, values in parse_qs(request_url.query).items()
            }
            response_queue.put(payload)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authentication completed.</h1>You can return to the notebook.</body></html>")

        def log_message(self, format: str, *args: object) -> None:
            return

    server = HTTPServer((host, port), CallbackHandler)
    server.timeout = 300
    server_thread = Thread(target=server.handle_request, daemon=True)
    server_thread.start()
    webbrowser.open(auth_uri)
    server_thread.join(timeout=305)
    server.server_close()

    if response_queue.empty():
        raise AuthError("Interactive browser auth timed out waiting for the localhost redirect.")
    return response_queue.get_nowait()


def _should_fallback_to_confidential_browser(result: dict, settings: RuntimeSettings) -> bool:
    if not settings.client_secret or not settings.redirect_uri:
        return False
    return result.get("error") == "invalid_client" and "AADSTS7000218" in result.get("error_description", "")


def _build_auth_error(result: dict) -> AuthError:
    error = result.get("error", "unknown_error")
    description = result.get("error_description", "No description returned.")
    correlation_id = result.get("correlation_id")
    detail = f"{error}: {description}"
    if error == "invalid_client" and "AADSTS7000218" in description:
        detail = (
            f"{detail} This app registration is not enabled for public-client delegated auth. "
            "Enable device-code/public client flows in Entra ID, or use browser sign-in with CLIENT_SECRET and REDIRECT_URI configured."
        )
    if correlation_id:
        detail = f"{detail} Correlation ID: {correlation_id}"
    return AuthError(detail)
