from __future__ import annotations

import logging
from typing import Any

import requests

LOGGER = logging.getLogger(__name__)

BASE_URL = "https://api.powerbi.com/v1.0/myorg"


class PowerBIAPIError(RuntimeError):
    """Raised when the Power BI REST API returns an actionable error."""


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

    def get_groups(self) -> list[dict[str, Any]]:
        payload = self._get("/groups")
        rows = payload.get("value", [])
        return self._pick_columns(rows, ["id", "name", "type", "isReadOnly", "isOnDedicatedCapacity"])

    def get_datasets_in_group(self, group_id: str) -> list[dict[str, Any]]:
        payload = self._get(f"/groups/{group_id}/datasets")
        rows = payload.get("value", [])
        return self._pick_columns(rows, ["id", "name", "configuredBy", "isRefreshable", "targetStorageMode"])

    def get_reports_in_group(self, group_id: str) -> list[dict[str, Any]]:
        payload = self._get(f"/groups/{group_id}/reports")
        rows = payload.get("value", [])
        return self._pick_columns(rows, ["id", "name", "datasetId", "webUrl", "embedUrl"])

    def execute_queries_in_group(
        self,
        group_id: str,
        dataset_id: str,
        dax_query: str,
        impersonated_user_name: str | None = None,
    ) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {
            "queries": [{"query": dax_query}],
            "serializerSettings": {"includeNulls": True},
        }
        if impersonated_user_name:
            payload["impersonatedUserName"] = impersonated_user_name

        response = self._post(f"/groups/{group_id}/datasets/{dataset_id}/executeQueries", payload)
        results = response.get("results", [])
        if not results:
            return []
        tables = results[0].get("tables", [])
        if not tables:
            return []
        return tables[0].get("rows", [])

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.session.get(f"{BASE_URL}{path}", params=params, timeout=self.timeout_seconds)
        return self._handle_response(response)

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(f"{BASE_URL}{path}", json=payload, timeout=self.timeout_seconds)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        try:
            payload = response.json() if response.text else {}
        except ValueError:
            payload = {"raw_text": response.text}

        if response.ok:
            return payload

        status = response.status_code
        retry_after = response.headers.get("Retry-After")
        detail = _extract_error_message(payload)

        if status == 401:
            message = "401 Unauthorized. The token may be expired, the wrong resource may have been requested, or consent is missing."
        elif status == 403:
            message = (
                "403 Forbidden. Confirm the caller has workspace access, dataset permissions, and that tenant admin settings allow this identity path."
            )
        elif status == 404:
            message = "404 Not Found. Confirm the workspace ID, dataset ID, and endpoint path."
        elif status == 429:
            message = f"429 Too Many Requests. Retry later. Retry-After: {retry_after or 'not provided'}."
        else:
            message = f"{status} Power BI API error."

        if "service principal" in detail.lower():
            message = (
                f"{message} The response suggests a service principal restriction. Check tenant admin settings, allowed security groups, and workspace membership."
            )
        if "build" in detail.lower():
            message = f"{message} The response suggests the caller is missing dataset Build permission."
        if "rls" in detail.lower() or "sso" in detail.lower():
            message = (
                f"{message} The response suggests an unsupported identity scenario for executeQueries, such as RLS or SSO with service principal auth."
            )

        raise PowerBIAPIError(f"{message} Details: {detail}")

    @staticmethod
    def _pick_columns(rows: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        for row in rows:
            normalized.append({column: row.get(column) for column in columns})
        return normalized


def _extract_error_message(payload: dict[str, Any]) -> str:
    if not payload:
        return "No payload returned."
    error = payload.get("error")
    if isinstance(error, dict):
        code = error.get("code")
        message = error.get("message")
        if code and message:
            return f"{code}: {message}"
        if message:
            return str(message)
    if isinstance(error, str):
        return error
    return str(payload)
