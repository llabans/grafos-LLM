"""Reconciliación exacta y construcción canónica."""

from __future__ import annotations

from dataclasses import dataclass

from bipartite_minsa.domain.clinical_graph import (
    BranchSemantics,
    ClinicalDecisionGraph,
    ClinicalNode,
    ClinicalTransition,
)
from bipartite_minsa.domain.provenance import TARGET_SOURCE_ID, SourceReference
from bipartite_minsa.errors import ReconciliationError
from bipartite_minsa.ingestion.raw import RawDecisionGraph, RawEdge, RawFlowchart
from bipartite_minsa.validation.graph_validation import audit_directed_graph


@dataclass(frozen=True, slots=True)
class GraphReconciliationReport:
    flow_id: str
    missing_nodes: tuple[str, ...]
    added_nodes: tuple[str, ...]
    modified_nodes: tuple[str, ...]
    missing_edges: tuple[tuple[str, str, str], ...]
    added_edges: tuple[tuple[str, str, str], ...]
    page_matches: bool
    section_matches: bool
    start_node_id: str
    route_templates_empty: bool

    @property
    def is_equivalent(self) -> bool:
        return (
            not any(
                (
                    self.missing_nodes,
                    self.added_nodes,
                    self.modified_nodes,
                    self.missing_edges,
                    self.added_edges,
                )
            )
            and self.page_matches
            and self.section_matches
        )


def _edge_key(edge: RawEdge) -> tuple[str, str, str]:
    return (edge.source_node_id, edge.target_node_id, edge.label)


def reconcile_flowchart_representations(
    source_graph: RawFlowchart, derived_graph: RawDecisionGraph
) -> GraphReconciliationReport:
    if source_graph.flow_id != derived_graph.flow_id:
        raise ReconciliationError("flow_id diferentes")
    source_nodes = {node.node_id: node for node in source_graph.nodes}
    derived_nodes = {node.node_id: node for node in derived_graph.nodes}
    common = set(source_nodes) & set(derived_nodes)
    modified = tuple(
        sorted(node_id for node_id in common if source_nodes[node_id] != derived_nodes[node_id])
    )
    source_edges = {_edge_key(edge) for edge in source_graph.edges}
    derived_edges = {_edge_key(edge) for edge in derived_graph.edges}
    report = GraphReconciliationReport(
        flow_id=source_graph.flow_id,
        missing_nodes=tuple(sorted(set(source_nodes) - set(derived_nodes))),
        added_nodes=tuple(sorted(set(derived_nodes) - set(source_nodes))),
        modified_nodes=modified,
        missing_edges=tuple(sorted(source_edges - derived_edges)),
        added_edges=tuple(sorted(derived_edges - source_edges)),
        page_matches=source_graph.page == derived_graph.page,
        section_matches=source_graph.section_id == derived_graph.section_id,
        start_node_id=derived_graph.start_node_id,
        route_templates_empty=not derived_graph.route_templates,
    )
    return report


def _branch_semantics(flow_id: str, edge: RawEdge) -> BranchSemantics:
    label = edge.label.casefold().strip()
    if flow_id == "flow_1" and edge.source_node_id == "n1" and label == "sí":
        return BranchSemantics.AND
    if flow_id == "flow_1" and edge.source_node_id == "n1" and label == "no":
        return BranchSemantics.XOR
    if flow_id == "flow_2" and edge.source_node_id in {"n2", "n4"}:
        return BranchSemantics.XOR
    if label in {"sí", "no"}:
        return BranchSemantics.XOR
    if not label:
        return BranchSemantics.SEQUENTIAL
    return BranchSemantics.UNKNOWN


def build_canonical_graph(
    source_graph: RawFlowchart,
    derived_graph: RawDecisionGraph,
    source_sha256: str,
) -> tuple[ClinicalDecisionGraph, GraphReconciliationReport]:
    report = reconcile_flowchart_representations(source_graph, derived_graph)
    if not report.is_equivalent:
        raise ReconciliationError(f"conflicto estructural en {source_graph.flow_id}: {report}")

    audit = audit_directed_graph(source_graph.nodes, source_graph.edges, report.start_node_id)
    base_path = f"snapshots/gpc_json/{TARGET_SOURCE_ID}/flowcharts.json"
    graph_ref = SourceReference(
        source_id=TARGET_SOURCE_ID,
        local_path=base_path,
        entity_id=source_graph.flow_id,
        page=source_graph.page,
        section=source_graph.section_id,
        sha256=source_sha256,
    )
    nodes = tuple(
        ClinicalNode(
            node_id=f"{source_graph.flow_id}:{node.node_id}",
            node_type=node.node_type,
            text=node.label,
            source_refs=(
                SourceReference(
                    source_id=TARGET_SOURCE_ID,
                    local_path=base_path,
                    entity_id=f"{source_graph.flow_id}:{node.node_id}",
                    page=source_graph.page,
                    section=source_graph.section_id,
                    sha256=source_sha256,
                ),
            ),
        )
        for node in sorted(source_graph.nodes, key=lambda item: item.node_id)
    )
    transitions = tuple(
        ClinicalTransition(
            transition_id=f"{source_graph.flow_id}:edge:{index:02d}",
            source_node_id=f"{source_graph.flow_id}:{edge.source_node_id}",
            target_node_id=f"{source_graph.flow_id}:{edge.target_node_id}",
            label=edge.label or None,
            branch_semantics=_branch_semantics(source_graph.flow_id, edge),
            source_refs=(graph_ref,),
        )
        for index, edge in enumerate(source_graph.edges, start=1)
    )
    graph = ClinicalDecisionGraph(
        graph_id=f"{TARGET_SOURCE_ID}__flow__{source_graph.flow_id}",
        source_id=TARGET_SOURCE_ID,
        title=source_graph.title,
        start_node_id=f"{source_graph.flow_id}:{report.start_node_id}",
        nodes=nodes,
        transitions=transitions,
        reachable_node_ids=frozenset(
            f"{source_graph.flow_id}:{node_id}" for node_id in audit.reachable_node_ids
        ),
        clinical_scope=source_graph.flow_id in {"flow_1", "flow_2"},
        warnings=source_graph.warnings,
        source_refs=(graph_ref,),
    )
    return graph, report
