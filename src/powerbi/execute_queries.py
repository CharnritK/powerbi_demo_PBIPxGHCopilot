"""DAX query execution helpers."""

from __future__ import annotations

from src.powerbi.client import PowerBIClient

DEFAULT_QUERY = """EVALUATE
TOPN(
    10,
    SUMMARIZECOLUMNS(
        'Dim Region'[Region],
        "Total Sales", [Total Sales],
        "Gross Margin", [Gross Margin]
    ),
    [Total Sales], DESC
)"""


def execute_dax_query(
    client: PowerBIClient,
    group_id: str,
    dataset_id: str,
    dax_query: str = DEFAULT_QUERY,
    impersonated_user_name: str | None = None,
) -> list[dict]:
    return client.execute_queries_in_group(
        group_id=group_id,
        dataset_id=dataset_id,
        dax_query=dax_query,
        impersonated_user_name=impersonated_user_name,
    )
