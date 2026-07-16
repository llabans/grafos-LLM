"""Baseline de caminos aumentantes con DFS."""

from __future__ import annotations

from dataclasses import dataclass

from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.result import (
    MatchingInstrumentation,
    MatchingResult,
    pairs_from_left_map,
)


@dataclass(slots=True)
class _Counters:
    searches: int = 0
    dfs_calls: int = 0
    augmentations: int = 0
    edge_scans: int = 0


class AugmentingPathMatcher:
    """Aumenta un camino por búsqueda DFS.

    En el peor caso realiza ``|L|`` búsquedas y examina ``O(m)`` aristas por
    búsqueda: ``O(|L|m)`` tiempo, contenido en ``O(nm)``. El almacenamiento
    auxiliar es ``O(n)`` además de la lista de adyacencia ``O(n+m)``.
    """

    name = "augmenting-path-dfs"

    def solve(self, graph: BipartiteGraph) -> MatchingResult:
        pair_left: dict[str, str | None] = {left_id: None for left_id in graph.left}
        pair_right: dict[str, str | None] = {right_id: None for right_id in graph.right}
        counters = _Counters()

        def augment(left_id: str, seen_right: set[str]) -> bool:
            counters.dfs_calls += 1
            for right_id in graph.adjacency[left_id]:
                counters.edge_scans += 1
                if right_id in seen_right:
                    continue
                seen_right.add(right_id)
                previous_left = pair_right[right_id]
                if previous_left is None or augment(previous_left, seen_right):
                    pair_left[left_id] = right_id
                    pair_right[right_id] = left_id
                    return True
            return False

        for left_id in graph.left:
            counters.searches += 1
            if augment(left_id, set()):
                counters.augmentations += 1

        result = MatchingResult(
            pairs=pairs_from_left_map(pair_left),
            instrumentation=MatchingInstrumentation(
                algorithm=self.name,
                dfs_calls=counters.dfs_calls,
                augmenting_searches=counters.searches,
                augmentations=counters.augmentations,
                edge_scans=counters.edge_scans,
            ),
        )
        result.validate_against(graph)
        return result
