"""Exportadores DOT exactos para visualización externa."""

from __future__ import annotations

from bipartite_minsa.domain.clinical_graph import ClinicalDecisionGraph
from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.result import MatchingResult


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def directed_graph_dot(graph: ClinicalDecisionGraph) -> str:
    """Representación DOT del grafo dirigido con aislados."""

    lines = ["digraph clinical {", "  rankdir=LR;", "  node [shape=box];"]
    for node in graph.nodes:
        label = f"{node.node_id}\\n{node.text}"
        style = "dashed" if node.node_id not in graph.reachable_node_ids else "solid"
        lines.append(f"  {_quote(node.node_id)} [label={_quote(label)}, style={_quote(style)}];")
    for transition in graph.transitions:
        lines.append(
            f"  {_quote(transition.source_node_id)} -> {_quote(transition.target_node_id)} "
            f"[label={_quote(transition.label or '')}];"
        )
    lines.append("}")
    return "\n".join(lines) + "\n"


def bipartite_matching_dot(graph: BipartiteGraph, result: MatchingResult) -> str:
    """DOT completo; aristas del matching en azul."""

    matched = set(result.pairs)
    lines = [
        "graph coverage {",
        "  rankdir=LR;",
        '  subgraph cluster_left { label="U: escenarios"; color=lightgrey;',
    ]
    lines.extend(f"    {_quote(left_id)} [shape=circle];" for left_id in graph.left)
    lines.append("  }")
    lines.append('  subgraph cluster_right { label="V: objetivos"; color=lightgrey;')
    lines.extend(f"    {_quote(right_id)} [shape=box];" for right_id in graph.right)
    lines.append("  }")
    for edge in graph.edges:
        attributes = "color=blue, penwidth=3" if edge in matched else "color=grey"
        lines.append(f"  {_quote(edge[0])} -- {_quote(edge[1])} [{attributes}];")
    lines.append("}")
    return "\n".join(lines) + "\n"
