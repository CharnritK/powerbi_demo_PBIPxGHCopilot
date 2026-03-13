"""Raw Power BI REST client wrapper."""

from __future__ import annotations

from typing import Any

import requests

from src.common.errors import PowerBIAPIError

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

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.session.get(f"{BASE_URL}{path}", params=params, timeout=self.timeout_seconds)
        return self._handle_response(response)

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(f"{BASE_URL}{path}", json=payload, timeout=self.timeout_seconds)
        return self._handle_response(response)

    def get_groups(self, top: int | None = None) -> list[dict[str, Any]]:
        payload = self.get("/groups", params={"$top": top} if top else None)
        return _pick_columns(payload.get("value", []), ["id", "name", "type", "isReadOnly", "isOnDedicatedCapacity"])

    def get_datasets_in_group(self, group_id: str) -> list[dict[str, Any]]:
        payload = self.get(f"/groups/{group_id}/datasets")
        return _pick_columns(payload.get("value", []), ["id", "name", "configuredBy", "isRefreshable", "targetStorageMode"])

    def get_reports_in_group(self, group_id: str) -> list[dict[str, Any]]:
        payload = self.get(f"/groups/{group_id}/reports")
        return _pick_columns(payload.get("value", []), ["id", "name", "datasetId", "webUrl", "embedUrl"])

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
        response = self.post(f"/groups/{group_id}/datasets/{dataset_id}/executeQueries", payload)
        results = response.get("results", [])
        if not results:
            return []
        tables = results[0].get("tables", [])
        if not tables:
            return []
        return tables[0].get("rows", [])

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

        detail_lower = detail.lower()
        if "service principal" in detail_lower:
            message = (
                f"{message} The response suggests a service principal restriction. Check tenant admin settings, allowed security groups, and workspace membership."
            )
        if "build" in detail_lower:
            message = f"{message} The response suggests the caller is missing dataset Build permission."
        if "rls" in detail_lower or "sso" in detail_lower:
            message = (
                f"{message} The response suggests an unsupported identity scenario for executeQueries, such as RLS or SSO with service principal auth."
            )
        raise PowerBIAPIError(f"{message} Details: {detail}")


def _pick_columns(rows: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [{column: row.get(column) for column in columns} for row in rows]


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
