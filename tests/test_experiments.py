"""Asegura que los fixtures experimentales sean matemáticos y deterministas."""

from __future__ import annotations

import pytest

from bipartite_minsa.experiments import benchmark_matcher, complete_graph, staircase_graph
from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher


def test_staircase_has_closed_form_and_separates_edge_scans() -> None:
    size = 16
    graph = staircase_graph(size)
    dfs = AugmentingPathMatcher().solve(graph)
    hk = HopcroftKarpMatcher().solve(graph)
    assert (graph.n, graph.m, dfs.cardinality, hk.cardinality) == (32, 31, 16, 16)
    assert dfs.instrumentation.edge_scans == size**2
    assert hk.instrumentation.bfs_phases == 1
    assert hk.instrumentation.edge_scans < dfs.instrumentation.edge_scans


def test_complete_graph_and_invalid_sizes() -> None:
    graph = complete_graph(4)
    assert (graph.n, graph.m) == (8, 16)
    assert HopcroftKarpMatcher().solve(graph).cardinality == 4
    with pytest.raises(ValueError):
        staircase_graph(-1)
    with pytest.raises(ValueError):
        complete_graph(-1)


def test_benchmark_records_raw_samples_and_summary() -> None:
    result = benchmark_matcher(
        HopcroftKarpMatcher(),
        staircase_graph(8),
        fixture="unit_fixture",
        size_parameter=8,
        repeats=3,
    )
    assert len(result.raw_elapsed_ns) == 3
    assert result.min_elapsed_ns <= result.median_elapsed_ns <= result.max_elapsed_ns
    assert result.q1_elapsed_ns <= result.q3_elapsed_ns
    assert result.approximate_peak_traced_bytes > 0
    assert result.instrumentation["algorithm"] == "hopcroft-karp"
    with pytest.raises(ValueError):
        benchmark_matcher(
            HopcroftKarpMatcher(),
            staircase_graph(1),
            fixture="invalid",
            size_parameter=1,
            repeats=2,
        )
