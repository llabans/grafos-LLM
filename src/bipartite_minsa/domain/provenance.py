"""Procedencia, estados y utilidades de identidad."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

TARGET_SOURCE_ID = "gpc-05-hipertension-embarazo-2025"


class ValidationStatus(str, Enum):
    """Estados conservadores de validación."""

    VALIDATED = "validated"
    PARTIALLY_STRUCTURED = "partially_structured"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    BLOCKED_BY_EVIDENCE = "blocked_by_evidence"


class DecisionStatus(str, Enum):
    """Estados de una correspondencia o compatibilidad."""

    SUPPORTED = "supported"
    REJECTED = "rejected"
    HUMAN_REVIEW_REQUIRED = "human_review_required"


@dataclass(frozen=True, slots=True)
class SourceReference:
    """Referencia verificable a una entidad de la fuente local."""

    source_id: str
    local_path: str
    entity_id: str | None
    page: int | None
    section: str | None
    sha256: str

    def __post_init__(self) -> None:
        if self.source_id != TARGET_SOURCE_ID:
            raise ValueError(f"source_id fuera de alcance: {self.source_id}")
        if len(self.sha256) != 64 or any(c not in "0123456789abcdef" for c in self.sha256):
            raise ValueError("sha256 debe ser hexadecimal en minúsculas y tener 64 caracteres")
        if self.page is not None and self.page < 1:
            raise ValueError("page debe ser positiva")


def unique_source_refs(refs: tuple[SourceReference, ...]) -> tuple[SourceReference, ...]:
    """Deduplica y ordena referencias sin perder granularidad."""

    return tuple(
        sorted(
            set(refs),
            key=lambda ref: (
                ref.local_path,
                ref.entity_id or "",
                ref.page or -1,
                ref.section or "",
                ref.sha256,
            ),
        )
    )
