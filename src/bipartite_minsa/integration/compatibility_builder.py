"""Compatibilidad pura, explicable y conservadora."""

from __future__ import annotations

from bipartite_minsa.domain.coverage import CompatibilityDecision, CoverageTarget
from bipartite_minsa.domain.provenance import (
    TARGET_SOURCE_ID,
    DecisionStatus,
    ValidationStatus,
    unique_source_refs,
)
from bipartite_minsa.domain.scenario import ScenarioTemplate

BUILDER_VERSION = "compatibility-v1"


def evaluate_compatibility(
    scenario: ScenarioTemplate,
    target: CoverageTarget,
) -> CompatibilityDecision:
    scenario_predicates = set(scenario.input_predicates)
    required = set(target.required_predicates)
    forbidden = set(target.forbidden_predicates)
    actions = set(scenario.activated_action_ids)
    expected_actions = set(target.expected_action_ids)

    missing_predicates = tuple(sorted(required - scenario_predicates))
    contradictions = tuple(sorted(forbidden & scenario_predicates))
    missing_actions = tuple(sorted(expected_actions - actions))
    exclusion_reasons: list[str] = []
    if scenario.source_id != TARGET_SOURCE_ID:
        exclusion_reasons.append("source_id_out_of_scope")
    if scenario.status != ValidationStatus.VALIDATED:
        exclusion_reasons.append("scenario_not_validated")
    if target.status != ValidationStatus.VALIDATED:
        exclusion_reasons.append("target_not_validated")
    if missing_predicates:
        exclusion_reasons.append("missing_required_predicates")
    if contradictions:
        exclusion_reasons.append("forbidden_predicate_present")
    if missing_actions:
        exclusion_reasons.append("missing_expected_actions")
    refs = unique_source_refs((*scenario.source_refs, *target.source_refs))
    if not refs:
        exclusion_reasons.append("missing_provenance")

    status = DecisionStatus.SUPPORTED if not exclusion_reasons else DecisionStatus.REJECTED
    return CompatibilityDecision(
        scenario_template_id=scenario.scenario_template_id,
        coverage_target_id=target.coverage_target_id,
        status=status,
        satisfied_predicates=tuple(sorted(required & scenario_predicates)),
        missing_predicates=missing_predicates,
        contradictions=tuple(
            sorted((*contradictions, *(f"missing_action:{item}" for item in missing_actions)))
        ),
        rule_ids=(BUILDER_VERSION,),
        exclusion_reasons=tuple(exclusion_reasons),
        builder_version=BUILDER_VERSION,
        source_refs=refs,
    )


def build_compatibilities(
    scenarios: tuple[ScenarioTemplate, ...],
    targets: tuple[CoverageTarget, ...],
) -> tuple[CompatibilityDecision, ...]:
    return tuple(
        evaluate_compatibility(scenario, target) for scenario in scenarios for target in targets
    )


def supported_edges(
    decisions: tuple[CompatibilityDecision, ...],
) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            (decision.scenario_template_id, decision.coverage_target_id)
            for decision in decisions
            if decision.status == DecisionStatus.SUPPORTED
        )
    )
