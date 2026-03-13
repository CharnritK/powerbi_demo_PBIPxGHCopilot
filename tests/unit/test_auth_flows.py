from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from src.auth.delegated_user import acquire_delegated_access_token
from src.auth.service_principal import acquire_service_principal_access_token
from src.common.errors import AuthError
from src.config.loader import load_settings


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "sample_config.yaml"
MISSING_ENV = Path(__file__).resolve().parents[1] / "fixtures" / ".missing.env"


def _settings():
    return load_settings(env_path=MISSING_ENV, settings_path=FIXTURE)


def test_delegated_device_code_flow(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeCache:
        has_state_changed = False

    class FakePublicClient:
        def __init__(self, **_: object) -> None:
            pass

        def get_accounts(self, username: str | None = None) -> list[dict]:
            return []

        def initiate_device_flow(self, scopes: list[str]) -> dict:
            assert scopes
            return {"user_code": "abc", "message": "Use code abc"}

        def acquire_token_by_device_flow(self, flow: dict) -> dict:
            assert flow["user_code"] == "abc"
            return {"access_token": "delegated-token"}

    monkeypatch.setattr("src.auth.delegated_user.load_token_cache", lambda _: FakeCache())
    monkeypatch.setattr("src.auth.delegated_user.persist_token_cache", lambda *_: None)
    monkeypatch.setattr("src.auth.delegated_user.msal.PublicClientApplication", FakePublicClient)

    assert acquire_delegated_access_token(_settings(), use_device_code=True) == "delegated-token"


def test_service_principal_requires_secret() -> None:
    settings = _settings()
    settings = replace(settings, auth=replace(settings.auth, client_secret=None))
    with pytest.raises(AuthError):
        acquire_service_principal_access_token(settings)


def test_service_principal_token_flow(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeConfidentialClient:
        def __init__(self, **_: object) -> None:
            pass

        def acquire_token_for_client(self, scopes: list[str]) -> dict:
            assert scopes
            return {"access_token": "sp-token"}

    monkeypatch.setattr("src.auth.service_principal.msal.ConfidentialClientApplication", FakeConfidentialClient)
    assert acquire_service_principal_access_token(_settings()) == "sp-token"
