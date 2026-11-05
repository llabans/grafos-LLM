"""Hopcroft-Karp con BFS por capas y DFS admisible."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import inf

from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.result import (
    MatchingInstrumentation,
    MatchingResult,
    pairs_from_left_map,
)


@dataclass(slots=True)
class _Counters:
    bfs_phases: int = 0
    dfs_calls: int = 0
    augmentations: int = 0
    edge_scans: int = 0


class HopcroftKarpMatcher:
    """Matching máximo determinista por fases de caminos mínimos.

    La implementación mantiene capas implícitas en ``dist`` en lugar de
    materializar ``G_M``, ``H`` y ``H^T``. Es una adaptación computacional
    equivalente al tratamiento de CLRS, capítulo 25.1.

    La cota clásica sobre el grafo activo es ``O(m sqrt(n))``. Como esta clase
    acepta y recorre listas explícitas de vértices aislados, una cota completa
    conservadora es ``O(n + m sqrt(n))``; el almacenamiento es ``O(n+m)``.
    """

    name = "hopcroft-karp"

    def solve(self, graph: BipartiteGraph) -> MatchingResult:
        pair_left: dict[str, str | None] = {left_id: None for left_id in graph.left}
        pair_right: dict[str, str | None] = {right_id: None for right_id in graph.right}
        dist: dict[str, float] = {left_id: inf for left_id in graph.left}
        counters = _Counters()

        def build_layers() -> bool:
            queue: deque[str] = deque()
            shortest = inf
            for left_id in graph.left:
                if pair_left[left_id] is None:
                    dist[left_id] = 0
                    queue.append(left_id)
                else:
                    dist[left_id] = inf

            while queue:
                left_id = queue.popleft()
                if dist[left_id] >= shortest:
                    continue
                for right_id in graph.adjacency[left_id]:
                    counters.edge_scans += 1
                    previous_left = pair_right[right_id]
                    if previous_left is None:
                        shortest = dist[left_id] + 1
                    elif dist[previous_left] == inf:
                        dist[previous_left] = dist[left_id] + 1
                        queue.append(previous_left)
            return shortest != inf

        def augment_layered(left_id: str) -> bool:
            counters.dfs_calls += 1
            for right_id in graph.adjacency[left_id]:
                counters.edge_scans += 1
                previous_left = pair_right[right_id]
                if previous_left is None or (
                    dist[previous_left] == dist[left_id] + 1 and augment_layered(previous_left)
                ):
                    pair_left[left_id] = right_id
                    pair_right[right_id] = left_id
                    return True
            dist[left_id] = inf
            return False

        while build_layers():
            counters.bfs_phases += 1
            for left_id in graph.left:
                if pair_left[left_id] is None and augment_layered(left_id):
                    counters.augmentations += 1

        result = MatchingResult(
            pairs=pairs_from_left_map(pair_left),
            instrumentation=MatchingInstrumentation(
                algorithm=self.name,
                bfs_phases=counters.bfs_phases,
                dfs_calls=counters.dfs_calls,
                augmentations=counters.augmentations,
                edge_scans=counters.edge_scans,
            ),
        )
        result.validate_against(graph)
        return result
