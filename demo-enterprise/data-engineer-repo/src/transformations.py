"""Minimal placeholder transformations for the mock Data Engineering repo."""


def standardize_sales_columns(columns: list[str]) -> list[str]:
    return [column.strip().lower().replace(" ", "_") for column in columns]
