"""Generación combinatoria, simbólica y sin reemplazo."""

from __future__ import annotations

from itertools import combinations

from bipartite_minsa.domain.clinical_graph import ExecutionSignature
from bipartite_minsa.domain.criterion import ClinicalCriterion
from bipartite_minsa.domain.provenance import TARGET_SOURCE_ID, ValidationStatus, unique_source_refs
from bipartite_minsa.domain.scenario import ScenarioTemplate


def _scenario(
    scenario_id: str,
    signature: ExecutionSignature,
    predicates: tuple[str, ...],
    rule_id: str,
    criteria: tuple[ClinicalCriterion, ...] = (),
) -> ScenarioTemplate:
    return ScenarioTemplate(
        scenario_template_id=scenario_id,
        source_id=TARGET_SOURCE_ID,
        graph_id=signature.graph_id,
        input_predicates=tuple(sorted(set((*signature.required_predicates, *predicates)))),
        expected_decision_outcomes=signature.decision_outcomes,
        activated_action_ids=signature.activated_action_ids,
        execution_signature_id=signature.signature_id,
        generation_rule_id=rule_id,
        status=ValidationStatus.VALIDATED,
        source_refs=unique_source_refs(
            tuple(
                (
                    *signature.source_refs,
                    *(ref for criterion in criteria for ref in criterion.source_refs),
                )
            )
        ),
    )


def generate_scenarios(
    signatures: tuple[ExecutionSignature, ...],
    risk_criteria: tuple[ClinicalCriterion, ...],
    severity_criteria: tuple[ClinicalCriterion, ...],
) -> tuple[ScenarioTemplate, ...]:
    by_id = {signature.signature_id: signature for signature in signatures}
    high = tuple(item for item in risk_criteria if item.category == "high_risk_factor")
    moderate = tuple(item for item in risk_criteria if item.category == "moderate_risk_factor")
    low = tuple(item for item in risk_criteria if item.category == "low_risk_profile")
    scenarios: list[ScenarioTemplate] = []

    risk_yes = by_id["sig:flow_1:risk_parallel"]
    for criterion in high:
        scenarios.append(
            _scenario(
                f"scenario:{criterion.criterion_id}",
                risk_yes,
                (criterion.normalized_predicate,),
                "rule:risk_high_single:v1",
                (criterion,),
            )
        )
    for first, second in combinations(moderate, 2):
        scenarios.append(
            _scenario(
                f"scenario:{first.criterion_id}+{second.criterion_id}",
                risk_yes,
                (first.normalized_predicate, second.normalized_predicate),
                "rule:risk_moderate_pair_without_replacement:v1",
                (first, second),
            )
        )

    scenarios.append(
        _scenario(
            "scenario:risk_low_explicit",
            by_id["sig:flow_1:no_risk"],
            (low[0].normalized_predicate,),
            "rule:explicit_low_risk_profile:v1",
            low,
        )
    )
    scenarios.append(
        _scenario(
            "scenario:bp_not_elevated",
            by_id["sig:flow_2:bp_not_elevated"],
            (),
            "rule:flow_2_negative_branch:v1",
        )
    )
    scenarios.append(
        _scenario(
            "scenario:bp_elevated_no_severity",
            by_id["sig:flow_2:no_severity"],
            (),
            "rule:flow_2_no_severity:v1",
        )
    )
    for criterion in severity_criteria:
        scenarios.append(
            _scenario(
                f"scenario:{criterion.criterion_id}",
                by_id["sig:flow_2:with_severity"],
                (criterion.normalized_predicate,),
                "rule:one_explicit_severity_criterion:v1",
                (criterion,),
            )
        )
    return tuple(sorted(scenarios, key=lambda item: item.scenario_template_id))
