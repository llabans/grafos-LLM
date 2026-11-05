"""Objetivos deduplicados por concepto e identificadores, no por texto."""

from __future__ import annotations

from bipartite_minsa.domain.clinical_graph import ClinicalDecisionGraph
from bipartite_minsa.domain.coverage import CoverageTarget, EvidenceCrosswalk
from bipartite_minsa.domain.criterion import ClinicalCriterion
from bipartite_minsa.domain.provenance import ValidationStatus, unique_source_refs
from bipartite_minsa.domain.recommendation import ClinicalRecommendation


def build_coverage_targets(
    graphs: tuple[ClinicalDecisionGraph, ...],
    recommendations: tuple[ClinicalRecommendation, ...],
    risk_criteria: tuple[ClinicalCriterion, ...],
    severity_criteria: tuple[ClinicalCriterion, ...],
    crosswalks: tuple[EvidenceCrosswalk, ...],
) -> tuple[CoverageTarget, ...]:
    nodes = {node.node_id: node for graph in graphs for node in graph.nodes}
    recs = {item.recommendation_id: item for item in recommendations}
    targets: list[CoverageTarget] = []

    for criterion in (*risk_criteria, *severity_criteria):
        if criterion.category == "low_risk_profile":
            continue
        targets.append(
            CoverageTarget(
                coverage_target_id=f"target:{criterion.criterion_id}",
                category=criterion.category,
                required_predicates=(criterion.normalized_predicate,),
                forbidden_predicates=(),
                expected_action_ids=(),
                crosswalk_ids=(),
                status=ValidationStatus.VALIDATED,
                source_refs=criterion.source_refs,
            )
        )

    recommendation_targets = (
        ("rec_1", "target:recommendation:rec_1", "recommendation", "xw:prevention_aas"),
        ("rec_2", "target:recommendation:rec_2", "recommendation", "xw:prevention_calcium"),
        (
            "rec_3",
            "target:recommendation:rec_3_not_explicit",
            "recommendation_not_explicit_in_flow",
            "xw:rec_3_not_explicit_in_flow",
        ),
        ("bpc_1", "target:bpc:bpc_1", "BPC", "xw:no_severity_referral"),
        ("bpc_2", "target:bpc:bpc_2", "BPC", "xw:severe_referral"),
    )
    for rec_id, target_id, category, crosswalk_id in recommendation_targets:
        rec = recs[rec_id]
        targets.append(
            CoverageTarget(
                coverage_target_id=target_id,
                category=category,
                required_predicates=rec.condition_predicates,
                forbidden_predicates=(),
                expected_action_ids=rec.action_predicates,
                crosswalk_ids=(crosswalk_id,),
                status=ValidationStatus.VALIDATED,
                source_refs=rec.source_refs,
            )
        )

    structural_targets = (
        (
            "target:flow_1:no_risk_branch",
            "decision_outcome",
            ("risk_threshold:not_met",),
            ("flow_1:n2",),
            nodes["flow_1:n2"].source_refs,
        ),
        (
            "target:flow_2:bp_not_elevated",
            "decision_outcome",
            ("bp_elevated:false",),
            ("flow_2:n1",),
            nodes["flow_2:n1"].source_refs,
        ),
    )
    for target_id, category, predicates, actions, refs in structural_targets:
        targets.append(
            CoverageTarget(
                coverage_target_id=target_id,
                category=category,
                required_predicates=predicates,
                forbidden_predicates=(),
                expected_action_ids=actions,
                crosswalk_ids=(),
                status=ValidationStatus.VALIDATED,
                source_refs=unique_source_refs(refs),
            )
        )

    by_id = {target.coverage_target_id: target for target in targets}
    if len(by_id) != len(targets):
        raise ValueError("coverage_target_id duplicado")
    known_crosswalks = {item.crosswalk_id for item in crosswalks}
    referenced = {item for target in targets for item in target.crosswalk_ids}
    if not referenced <= known_crosswalks:
        raise ValueError(f"crosswalk inexistente: {sorted(referenced - known_crosswalks)}")
    return tuple(sorted(targets, key=lambda item: item.coverage_target_id))
