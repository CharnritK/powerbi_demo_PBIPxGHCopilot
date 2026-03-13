from __future__ import annotations

from typing import Iterable

import pandas as pd


def as_dataframe(rows: Iterable[dict] | pd.DataFrame) -> pd.DataFrame:
    if isinstance(rows, pd.DataFrame):
        return rows.copy()
    return pd.DataFrame(list(rows))


def dataframe_preview(rows: Iterable[dict] | pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    frame = as_dataframe(rows)
    if frame.empty:
        return frame
    return frame.head(limit)


def markdown_summary(title: str, items: dict[str, object]) -> str:
    lines = [f"### {title}", ""]
    for key, value in items.items():
        lines.append(f"- **{key}**: {value}")
    return "\n".join(lines)


def test_case_preview(frame: pd.DataFrame) -> pd.DataFrame:
    preferred = [
        "test_id",
        "status",
        "review_status",
        "priority",
        "table_name",
        "measure_name",
        "scenario_type",
        "report_name",
        "page_name",
        "visual_name",
    ]
    available = [column for column in preferred if column in frame.columns]
    if not available:
        return frame
    return frame.loc[:, available]
