from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests

LOGGER = logging.getLogger(__name__)

BASE_URL = "https://api.powerbi.com/v1.0/myorg"


class PowerBIClient:
    def __init__(self, access_token: str, timeout_seconds: int = 60) -> None:
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{BASE_URL}{path}"
        response = self.session.get(url, params=params, timeout=self.timeout_seconds)
        return self._handle_response(response)

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{BASE_URL}{path}"
        response = self.session.post(url, json=payload, timeout=self.timeout_seconds)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: requests.Response) -> Dict[str, Any]:
        try:
            payload = response.json() if response.text else {}
        except ValueError:
            payload = {"raw_text": response.text}

        if not response.ok:
            LOGGER.error("Power BI API call failed: %s | %s", response.status_code, payload)
            raise RuntimeError(
                f"Power BI API request failed with status {response.status_code}: {payload}"
            )

        return payload
