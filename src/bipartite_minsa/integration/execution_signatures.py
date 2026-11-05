"""Firmas alcanzables versionadas para los dos flujos incluidos."""

from __future__ import annotations

import re

from bipartite_minsa.domain.clinical_graph import (
    BranchSemantics,
    ClinicalDecisionGraph,
    ExecutionSignature,
)
from bipartite_minsa.domain.criterion import ClinicalCriterion
from bipartite_minsa.domain.provenance import ValidationStatus, unique_source_refs
from bipartite_minsa.errors import EvidenceBlockedError


def _refs_for_nodes(graph: ClinicalDecisionGraph, node_ids: tuple[str, ...]) -> tuple:
    by_id = {node.node_id: node for node in graph.nodes}
    return unique_source_refs(
        tuple(ref for node_id in node_ids for ref in by_id[node_id].source_refs)
    )


def build_execution_signatures(
    graphs: tuple[ClinicalDecisionGraph, ...],
) -> tuple[ExecutionSignature, ...]:
    by_flow = {graph.graph_id.rsplit("__flow__", 1)[-1]: graph for graph in graphs}
    if set(by_flow) != {"flow_1", "flow_2", "flow_3"}:
        raise EvidenceBlockedError(f"inventario de flujos inesperado: {sorted(by_flow)}")

    specifications = (
        (
            "sig:flow_1:no_risk",
            "flow_1",
            ("flow_1:n1=No",),
            ("risk_threshold:not_met",),
            ("flow_1:n2",),
            ("flow_1:n1", "flow_1:n2"),
            (BranchSemantics.XOR,),
        ),
        (
            "sig:flow_1:risk_parallel",
            "flow_1",
            ("flow_1:n1=Sí",),
            ("risk_threshold:met",),
            ("flow_1:n3", "flow_1:n4", "flow_1:n5", "flow_1:n6"),
            ("flow_1:n1", "flow_1:n3", "flow_1:n4", "flow_1:n5", "flow_1:n6"),
            (BranchSemantics.AND, BranchSemantics.SEQUENTIAL),
        ),
        (
            "sig:flow_2:bp_not_elevated",
            "flow_2",
            ("flow_2:n2=No",),
            ("bp_elevated:false",),
            ("flow_2:n1",),
            ("flow_2:n2", "flow_2:n1"),
            (BranchSemantics.XOR,),
        ),
        (
            "sig:flow_2:no_severity",
            "flow_2",
            ("flow_2:n2=Sí", "flow_2:n4=Sin criterios"),
            ("bp_elevated:true", "severity:none"),
            ("flow_2:n5", "flow_2:n7"),
            ("flow_2:n2", "flow_2:n3", "flow_2:n4", "flow_2:n5", "flow_2:n7"),
            (BranchSemantics.XOR, BranchSemantics.SEQUENTIAL),
        ),
        (
            "sig:flow_2:with_severity",
            "flow_2",
            ("flow_2:n2=Sí", "flow_2:n4=Con criterios"),
            ("bp_elevated:true", "severity:present"),
            ("flow_2:n6", "flow_2:n8"),
            ("flow_2:n2", "flow_2:n3", "flow_2:n4", "flow_2:n6", "flow_2:n8"),
            (BranchSemantics.XOR, BranchSemantics.SEQUENTIAL),
        ),
    )
    signatures: list[ExecutionSignature] = []
    for signature_id, flow_id, outcomes, predicates, actions, reached, semantics in specifications:
        graph = by_flow[flow_id]
        if not set(reached) <= graph.reachable_node_ids:
            raise EvidenceBlockedError(f"firma con nodo inalcanzable: {signature_id}")
        signatures.append(
            ExecutionSignature(
                signature_id=signature_id,
                graph_id=graph.graph_id,
                decision_outcomes=outcomes,
                required_predicates=predicates,
                activated_action_ids=actions,
                reached_node_ids=reached,
                branch_semantics=semantics,
                status=ValidationStatus.VALIDATED,
                source_refs=_refs_for_nodes(graph, reached),
            )
        )
    return tuple(signatures)


def build_severity_criteria(
    graphs: tuple[ClinicalDecisionGraph, ...],
) -> tuple[ClinicalCriterion, ...]:
    """Extrae la lista numerada explícita de `flow_2:n4`."""

    flow_2 = next(graph for graph in graphs if graph.graph_id.endswith("__flow__flow_2"))
    node = next(node for node in flow_2.nodes if node.node_id == "flow_2:n4")
    matches = list(re.finditer(r"(?:^|\s)(\d+)\.\s", node.text))
    if len(matches) != 7:
        raise EvidenceBlockedError(
            f"se esperaban 7 criterios de severidad, se observaron {len(matches)}"
        )
    criteria: list[ClinicalCriterion] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(node.text)
        original = node.text[start:end].strip().rstrip(".")
        number = int(match.group(1))
        criteria.append(
            ClinicalCriterion(
                criterion_id=f"flow_2:n4:severity:{number:02d}",
                category="severity_criterion",
                original_label=original,
                normalized_predicate=f"severity_criterion:{number:02d}",
                value=None,
                unit=None,
                status=ValidationStatus.VALIDATED,
                source_refs=node.source_refs,
            )
        )
    return tuple(criteria)
