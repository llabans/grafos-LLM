"""Fixtures matemáticos y medición reproducible separada del dominio clínico."""

from __future__ import annotations

import statistics
import tracemalloc
from dataclasses import asdict, dataclass
from time import perf_counter_ns
from typing import Protocol

from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.result import MatchingResult


class Matcher(Protocol):
    """Contrato mínimo común de los solvers."""

    name: str

    def solve(self, graph: BipartiteGraph) -> MatchingResult: ...


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    fixture: str
    size_parameter: int
    left_vertices: int
    right_vertices: int
    edges: int
    density: float
    algorithm: str
    repeats: int
    raw_elapsed_ns: tuple[int, ...]
    median_elapsed_ns: float
    q1_elapsed_ns: float
    q3_elapsed_ns: float
    min_elapsed_ns: int
    max_elapsed_ns: int
    approximate_peak_traced_bytes: int
    cardinality: int
    instrumentation: dict[str, int | str]


def staircase_graph(size: int) -> BipartiteGraph:
    """Fixture escaso que obliga al DFS basal a revisitar una cadena creciente.

    No contiene conceptos clínicos. Tiene ``2*size`` vértices y ``2*size-1``
    aristas. Con el orden determinista usado aquí, DFS examina ``size**2``
    aristas, mientras Hopcroft--Karp resuelve el matching perfecto en una fase.
    """

    if size < 0:
        raise ValueError("size debe ser no negativo")
    left = tuple(f"u{index:04d}" for index in range(size))
    right = tuple(f"v{index:04d}" for index in range(size))
    edges: list[tuple[str, str]] = []
    for index, left_id in enumerate(left):
        if index:
            edges.append((left_id, right[index - 1]))
        edges.append((left_id, right[index]))
    return BipartiteGraph(left, right, tuple(edges))


def complete_graph(size: int) -> BipartiteGraph:
    """Fixture bipartito completo y balanceado, sin contenido clínico."""

    if size < 0:
        raise ValueError("size debe ser no negativo")
    left = tuple(f"u{index:04d}" for index in range(size))
    right = tuple(f"v{index:04d}" for index in range(size))
    return BipartiteGraph(
        left,
        right,
        tuple((left_id, right_id) for left_id in left for right_id in right),
    )


def benchmark_matcher(
    matcher: Matcher,
    graph: BipartiteGraph,
    *,
    fixture: str,
    size_parameter: int,
    repeats: int = 21,
) -> BenchmarkResult:
    """Mide repeticiones crudas, resumen robusto y memoria trazada aproximada."""

    if repeats < 3:
        raise ValueError("repeats debe ser al menos 3")
    warmup = matcher.solve(graph)
    samples: list[int] = []
    result = warmup
    for _ in range(repeats):
        start = perf_counter_ns()
        result = matcher.solve(graph)
        samples.append(perf_counter_ns() - start)

    tracemalloc.start()
    matcher.solve(graph)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    q1, _, q3 = statistics.quantiles(samples, n=4, method="inclusive")
    instrumentation = {
        key: value
        for key, value in asdict(result.instrumentation).items()
        if isinstance(value, (int, str))
    }
    return BenchmarkResult(
        fixture=fixture,
        size_parameter=size_parameter,
        left_vertices=len(graph.left),
        right_vertices=len(graph.right),
        edges=graph.m,
        density=graph.density,
        algorithm=matcher.name,
        repeats=repeats,
        raw_elapsed_ns=tuple(samples),
        median_elapsed_ns=statistics.median(samples),
        q1_elapsed_ns=q1,
        q3_elapsed_ns=q3,
        min_elapsed_ns=min(samples),
        max_elapsed_ns=max(samples),
        approximate_peak_traced_bytes=peak,
        cardinality=result.cardinality,
        instrumentation=instrumentation,
    )
