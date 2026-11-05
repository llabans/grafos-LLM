"""Crosswalk explícito por IDs auditados."""

from __future__ import annotations

from bipartite_minsa.domain.clinical_graph import ClinicalDecisionGraph
from bipartite_minsa.domain.coverage import EvidenceCrosswalk
from bipartite_minsa.domain.criterion import ClinicalCriterion
from bipartite_minsa.domain.provenance import DecisionStatus, unique_source_refs
from bipartite_minsa.domain.recommendation import ClinicalRecommendation


def build_crosswalk(
    graphs: tuple[ClinicalDecisionGraph, ...],
    recommendations: tuple[ClinicalRecommendation, ...],
    risk_criteria: tuple[ClinicalCriterion, ...],
) -> tuple[EvidenceCrosswalk, ...]:
    graph_nodes = {node.node_id: node for graph in graphs for node in graph.nodes}
    recs = {item.recommendation_id: item for item in recommendations}
    table_refs = unique_source_refs(
        tuple(ref for criterion in risk_criteria for ref in criterion.source_refs)
    )

    specifications = (
        ("xw:prevention_aas", "prevention_aas", ("flow_1:n3", "flow_1:n5"), "rec_1", True),
        ("xw:prevention_calcium", "prevention_calcium", ("flow_1:n4", "flow_1:n6"), "rec_2", True),
        (
            "xw:no_severity_referral",
            "no_severity_referral",
            ("flow_2:n5", "flow_2:n7"),
            "bpc_1",
            False,
        ),
        ("xw:severe_referral", "severe_referral", ("flow_2:n6", "flow_2:n8"), "bpc_2", False),
    )
    crosswalks: list[EvidenceCrosswalk] = []
    for crosswalk_id, concept_id, node_ids, rec_id, include_table in specifications:
        refs = tuple(ref for node_id in node_ids for ref in graph_nodes[node_id].source_refs)
        refs += recs[rec_id].source_refs
        if include_table:
            refs += table_refs
        crosswalks.append(
            EvidenceCrosswalk(
                crosswalk_id=crosswalk_id,
                concept_id=concept_id,
                graph_refs=node_ids,
                recommendation_refs=(rec_id,),
                criterion_refs=("table_003",) if include_table else (),
                knowledge_unit_refs=(
                    f"gpc-05-hipertension-embarazo-2025__recommendation__{rec_id}",
                ),
                relation_type="explicit_structural_correspondence",
                status=DecisionStatus.SUPPORTED,
                justification="IDs, acción y ubicación concordantes en fuentes autorizadas.",
                source_refs=unique_source_refs(refs),
            )
        )

    rec_3 = recs["rec_3"]
    crosswalks.append(
        EvidenceCrosswalk(
            crosswalk_id="xw:rec_3_not_explicit_in_flow",
            concept_id="withhold_antihypertensive_not_explicit_in_flow",
            graph_refs=("flow_2:n5",),
            recommendation_refs=("rec_3",),
            criterion_refs=(),
            knowledge_unit_refs=("gpc-05-hipertension-embarazo-2025__recommendation__rec_3",),
            relation_type="recommendation_without_explicit_action_node",
            status=DecisionStatus.HUMAN_REVIEW_REQUIRED,
            justification=(
                "La condición aparece en el flujo, pero la acción de la recomendación "
                "no posee nodo explícito; "
                "no se aprueba compatibilidad por similitud."
            ),
            source_refs=unique_source_refs(
                (*graph_nodes["flow_2:n5"].source_refs, *rec_3.source_refs)
            ),
        )
    )
    return tuple(sorted(crosswalks, key=lambda item: item.crosswalk_id))
