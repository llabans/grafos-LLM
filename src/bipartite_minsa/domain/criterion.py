"""Modelo de criterios estructurados y trazables."""

from dataclasses import dataclass

from bipartite_minsa.domain.provenance import SourceReference, ValidationStatus


@dataclass(frozen=True, slots=True)
class ClinicalCriterion:
    criterion_id: str
    category: str
    original_label: str
    normalized_predicate: str
    value: str | int | float | None
    unit: str | None
    status: ValidationStatus
    source_refs: tuple[SourceReference, ...]
