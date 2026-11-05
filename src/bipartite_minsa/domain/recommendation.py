"""Modelo canónico de recomendación o BPC."""

from dataclasses import dataclass

from bipartite_minsa.domain.provenance import SourceReference, ValidationStatus


@dataclass(frozen=True, slots=True)
class ClinicalRecommendation:
    recommendation_id: str
    recommendation_type: str
    original_text: str
    population_predicates: tuple[str, ...]
    condition_predicates: tuple[str, ...]
    action_predicates: tuple[str, ...]
    strength: str | None
    certainty: str | None
    status: ValidationStatus
    source_refs: tuple[SourceReference, ...]
