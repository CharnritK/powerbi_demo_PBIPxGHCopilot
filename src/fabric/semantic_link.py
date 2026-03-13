"""Optional wrapper for Semantic Link style workflows."""

from __future__ import annotations


def load_semantic_link():
    try:
        import sempy.fabric as fabric  # type: ignore
    except ImportError as exc:  # pragma: no cover - optional package
        raise RuntimeError(
            "Semantic Link support is optional. Install `semantic-link-sempy` or the relevant Fabric SDK before using this helper."
        ) from exc
    return fabric
