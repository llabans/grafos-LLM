"""Oráculos exactos para pruebas; no forman parte del solver principal."""

from __future__ import annotations

from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.result import MatchingInstrumentation, MatchingResult


def exhaustive_maximum_matching(graph: BipartiteGraph) -> MatchingResult:
    """Busca exhaustivamente un óptimo; usar solo en instancias pequeñas."""

    best: tuple[tuple[str, str], ...] = ()

    def search(index: int, used_right: frozenset[str], pairs: tuple[tuple[str, str], ...]) -> None:
        nonlocal best
        if index == len(graph.left):
            if len(pairs) > len(best) or (len(pairs) == len(best) and pairs < best):
                best = pairs
            return
        if len(pairs) + (len(graph.left) - index) < len(best):
            return

        left_id = graph.left[index]
        search(index + 1, used_right, pairs)
        for right_id in graph.adjacency[left_id]:
            if right_id not in used_right:
                search(
                    index + 1,
                    used_right | frozenset({right_id}),
                    tuple(sorted((*pairs, (left_id, right_id)))),
                )

    search(0, frozenset(), ())
    return MatchingResult(
        pairs=best,
        instrumentation=MatchingInstrumentation(algorithm="exhaustive-oracle"),
    )


def networkx_cardinality(graph: BipartiteGraph) -> int:
    """Cardinalidad de NetworkX, importado únicamente bajo demanda."""

    import networkx as nx  # type: ignore[import-untyped]

    oracle = nx.Graph()
    oracle.add_nodes_from(graph.left, bipartite=0)
    oracle.add_nodes_from(graph.right, bipartite=1)
    oracle.add_edges_from(graph.edges)
    matching = nx.algorithms.bipartite.maximum_matching(oracle, top_nodes=set(graph.left))
    return sum(1 for left_id in graph.left if left_id in matching)
