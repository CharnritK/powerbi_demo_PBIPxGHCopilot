from __future__ import annotations

import pytest

from src.common.errors import PowerBIAPIError
from src.powerbi.client import PowerBIClient


class DummyResponse:
    def __init__(self, payload: dict, ok: bool = True, status_code: int = 200, headers: dict | None = None) -> None:
        self._payload = payload
        self.ok = ok
        self.status_code = status_code
        self.headers = headers or {}
        self.text = "{}"

    def json(self) -> dict:
        return self._payload


def test_get_groups_filters_expected_columns(monkeypatch: pytest.MonkeyPatch) -> None:
    client = PowerBIClient("token")
    payload = {"value": [{"id": "1", "name": "Workspace", "isReadOnly": False, "noise": "x"}]}
    monkeypatch.setattr(client.session, "get", lambda *args, **kwargs: DummyResponse(payload))
    groups = client.get_groups()
    assert groups == [{"id": "1", "name": "Workspace", "type": None, "isReadOnly": False, "isOnDedicatedCapacity": None}]


def test_error_response_raises_powerbi_api_error() -> None:
    client = PowerBIClient("token")
    response = DummyResponse(
        {"error": {"message": "Too many requests"}},
        ok=False,
        status_code=429,
        headers={"Retry-After": "5"},
    )
    with pytest.raises(PowerBIAPIError):
        client._handle_response(response)  # noqa: SLF001
