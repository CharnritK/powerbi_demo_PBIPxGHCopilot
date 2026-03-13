from __future__ import annotations

from pathlib import Path

from src.auth.delegated_user import _build_auth_error, get_delegated_user_token
from src.config.models import AuthSettings, PathSettings, PowerBISettings, RuntimeSettings


def _settings(*, client_secret: str | None, redirect_uri: str | None) -> RuntimeSettings:
    return RuntimeSettings(
        environment="test",
        auth_mode="delegated",
        log_level="INFO",
        auth=AuthSettings(
            tenant_id="tenant-id",
            client_id="client-id",
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            use_device_code=True,
            token_cache_path=Path(".local/test-cache.bin"),
        ),
        powerbi=PowerBISettings(
            workspace_id="workspace-id",
            dataset_id="dataset-id",
            dax_query='EVALUATE ROW("Demo", 1)',
            impersonated_user_name=None,
            request_timeout_seconds=60,
        ),
        paths=PathSettings(
            repo_root=Path("."),
            powerbi_root=Path("demo-enterprise/bi-repo/powerbi"),
            workspace_root=Path("demo-enterprise/bi-repo/powerbi/workspaces"),
            pbip_root=Path("demo-enterprise/bi-repo/powerbi/sample"),
            semantic_model_definition_path=Path("demo-enterprise/bi-repo/powerbi/sample/definition"),
            sample_data_path=Path("demo-enterprise/bi-repo/powerbi/sample/data"),
        ),
    )


def test_browser_mode_uses_confidential_flow_when_secret_exists(monkeypatch) -> None:
    settings = _settings(client_secret="secret", redirect_uri="http://localhost")
    confidential_calls: list[tuple[str | None, str]] = []

    class FakePublicClientApplication:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def get_accounts(self, username=None):
            return []

    monkeypatch.setattr("src.auth.delegated_user.load_token_cache", lambda path: object())
    monkeypatch.setattr("src.auth.delegated_user.persist_token_cache", lambda cache, path: None)
    monkeypatch.setattr("src.auth.delegated_user.msal.PublicClientApplication", FakePublicClientApplication)
    monkeypatch.setattr(
        "src.auth.delegated_user._acquire_confidential_browser_token",
        lambda settings, authority, cache, login_hint: confidential_calls.append((login_hint, authority))
        or {"access_token": "token"},
    )

    result = get_delegated_user_token(settings, use_interactive_browser=True, login_hint="user@example.com")

    assert result["access_token"] == "token"
    assert confidential_calls == [("user@example.com", "https://login.microsoftonline.com/tenant-id")]


def test_device_code_invalid_client_falls_back_to_confidential_browser(monkeypatch) -> None:
    settings = _settings(client_secret="secret", redirect_uri="http://localhost")
    confidential_calls: list[str] = []

    class FakePublicClientApplication:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def get_accounts(self, username=None):
            return []

        def initiate_device_flow(self, scopes=None):
            return {"user_code": "abc", "message": "Use code abc"}

        def acquire_token_by_device_flow(self, flow):
            return {
                "error": "invalid_client",
                "error_description": "AADSTS7000218: The request body must contain the following parameter: 'client_assertion' or 'client_secret'.",
            }

    monkeypatch.setattr("src.auth.delegated_user.load_token_cache", lambda path: object())
    monkeypatch.setattr("src.auth.delegated_user.persist_token_cache", lambda cache, path: None)
    monkeypatch.setattr("src.auth.delegated_user.msal.PublicClientApplication", FakePublicClientApplication)
    monkeypatch.setattr(
        "src.auth.delegated_user._acquire_confidential_browser_token",
        lambda settings, authority, cache, login_hint: confidential_calls.append(authority) or {"access_token": "token"},
    )

    result = get_delegated_user_token(settings, use_interactive_browser=False)

    assert result["access_token"] == "token"
    assert confidential_calls == ["https://login.microsoftonline.com/tenant-id"]


def test_invalid_client_error_is_actionable() -> None:
    error = _build_auth_error(
        {
            "error": "invalid_client",
            "error_description": "AADSTS7000218: The request body must contain the following parameter: 'client_assertion' or 'client_secret'.",
            "correlation_id": "corr-id",
        }
    )

    message = str(error)
    assert "Enable device-code/public client flows" in message
    assert "CLIENT_SECRET and REDIRECT_URI" in message
    assert "corr-id" in message
