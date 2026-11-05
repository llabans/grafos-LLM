"""Validaciones de contratos que no dependen de JSON Schema externo."""

from collections.abc import Iterable

from bipartite_minsa.errors import SourceValidationError


def require_unique(values: Iterable[str], label: str) -> None:
    items = list(values)
    if len(items) != len(set(items)):
        raise SourceValidationError(f"{label} no es único")


def require_exact_source(source_id: str) -> None:
    if source_id != "gpc-05-hipertension-embarazo-2025":
        raise SourceValidationError(f"source_id rechazado: {source_id}")
