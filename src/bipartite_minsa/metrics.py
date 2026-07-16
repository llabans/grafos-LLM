"""Métricas descriptivas del grafo; no son métricas clínicas."""

from __future__ import annotations

from collections import Counter, deque
from typing import Any

from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.result import MatchingResult


def graph_metrics(graph: BipartiteGraph, result: MatchingResult | None = None) -> dict[str, Any]:
    right_degree: Counter[str] = Counter()
    for _, right_id in graph.edges:
        right_degree[right_id] += 1
    left_degrees = {left_id: len(graph.adjacency[left_id]) for left_id in graph.left}
    right_degrees = {right_id: right_degree[right_id] for right_id in graph.right}

    neighbors: dict[str, set[str]] = {vertex: set() for vertex in (*graph.left, *graph.right)}
    for left_id, right_id in graph.edges:
        neighbors[left_id].add(right_id)
        neighbors[right_id].add(left_id)
    components = 0
    seen: set[str] = set()
    for vertex in sorted(neighbors):
        if vertex in seen:
            continue
        components += 1
        queue: deque[str] = deque([vertex])
        seen.add(vertex)
        while queue:
            current = queue.popleft()
            for neighbor in sorted(neighbors[current]):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

    metrics: dict[str, Any] = {
        "left_vertices": len(graph.left),
        "right_vertices": len(graph.right),
        "vertices_total": graph.n,
        "edges": graph.m,
        "density": graph.density,
        "connected_components_including_isolates": components,
        "isolated_left": sorted(left_id for left_id, degree in left_degrees.items() if degree == 0),
        "isolated_right": sorted(
            right_id for right_id, degree in right_degrees.items() if degree == 0
        ),
        "left_degree_distribution": dict(sorted(Counter(left_degrees.values()).items())),
        "right_degree_distribution": dict(sorted(Counter(right_degrees.values()).items())),
    }
    if result is not None:
        matched_right = {right_id for _, right_id in result.pairs}
        metrics.update(
            {
                "matching_cardinality": result.cardinality,
                "clinical_route_variant_coverage_percent": (
                    0.0 if not graph.right else 100.0 * result.cardinality / len(graph.right)
                ),
                "unassigned_clinical_route_variants": sorted(set(graph.right) - matched_right),
                "unused_case_structures": sorted(
                    set(graph.left) - {left_id for left_id, _ in result.pairs}
                ),
            }
        )
    return metrics
