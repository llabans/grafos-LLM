"""Escenarios simbólicos, no historias clínicas."""

from dataclasses import dataclass

from bipartite_minsa.domain.provenance import SourceReference, ValidationStatus


@dataclass(frozen=True, slots=True)
class ScenarioTemplate:
    scenario_template_id: str
    source_id: str
    graph_id: str
    input_predicates: tuple[str, ...]
    expected_decision_outcomes: tuple[str, ...]
    activated_action_ids: tuple[str, ...]
    execution_signature_id: str
    generation_rule_id: str
    status: ValidationStatus
    source_refs: tuple[SourceReference, ...]
