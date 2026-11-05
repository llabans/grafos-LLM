"""Objetivos, crosswalk y decisiones de compatibilidad."""

from dataclasses import dataclass

from bipartite_minsa.domain.provenance import DecisionStatus, SourceReference, ValidationStatus


@dataclass(frozen=True, slots=True)
class EvidenceCrosswalk:
    crosswalk_id: str
    concept_id: str
    graph_refs: tuple[str, ...]
    recommendation_refs: tuple[str, ...]
    criterion_refs: tuple[str, ...]
    knowledge_unit_refs: tuple[str, ...]
    relation_type: str
    status: DecisionStatus
    justification: str
    source_refs: tuple[SourceReference, ...]


@dataclass(frozen=True, slots=True)
class CoverageTarget:
    coverage_target_id: str
    category: str
    required_predicates: tuple[str, ...]
    forbidden_predicates: tuple[str, ...]
    expected_action_ids: tuple[str, ...]
    crosswalk_ids: tuple[str, ...]
    status: ValidationStatus
    source_refs: tuple[SourceReference, ...]


@dataclass(frozen=True, slots=True)
class CompatibilityDecision:
    scenario_template_id: str
    coverage_target_id: str
    status: DecisionStatus
    satisfied_predicates: tuple[str, ...]
    missing_predicates: tuple[str, ...]
    contradictions: tuple[str, ...]
    rule_ids: tuple[str, ...]
    exclusion_reasons: tuple[str, ...]
    builder_version: str
    source_refs: tuple[SourceReference, ...]
