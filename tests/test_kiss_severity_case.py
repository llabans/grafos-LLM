"""Pruebas directas del ejemplo que se presenta en la versión KISS."""

from __future__ import annotations

import json
from pathlib import Path

from bipartite_minsa.kiss_case import build_kiss_severity_graph
from bipartite_minsa.matching.analysis import hall_deficiency_witnesses
from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher


def test_kiss_graph_has_predeclared_counts_and_maximum() -> None:
    graph = build_kiss_severity_graph()
    dfs = AugmentingPathMatcher().solve(graph)
    hk = HopcroftKarpMatcher().solve(graph)

    assert (len(graph.left), len(graph.right), graph.m) == (7, 8, 14)
    assert dfs.cardinality == hk.cardinality == 7
    assert len({left for left, _ in hk.pairs}) == 7
    assert len({right for _, right in hk.pairs}) == 7


def test_each_case_links_to_its_criterion_and_the_common_bpc() -> None:
    graph = build_kiss_severity_graph()
    for index, case_id in enumerate(graph.left, start=1):
        assert set(graph.adjacency[case_id]) == {
            "objective:bpc:severe_path",
            f"objective:severity:{index:02d}",
        }


def test_hall_witness_explains_the_seven_of_eight_limit() -> None:
    graph = build_kiss_severity_graph()
    result = HopcroftKarpMatcher().solve(graph)
    witnesses = hall_deficiency_witnesses(graph, result)

    assert len(witnesses) == 1
    witness = witnesses[0]
    assert witness.mechanism == "capacity_bottleneck"
    assert witness.target_ids == graph.right
    assert witness.neighboring_scenario_ids == graph.left
    assert witness.deficiency == 1


def test_versioned_sample_is_the_same_graph_used_by_the_demo() -> None:
    graph = build_kiss_severity_graph()
    sample_path = Path(__file__).parents[1] / "data" / "samples" / "kiss_severity_graph.json"
    sample = json.loads(sample_path.read_text(encoding="utf-8"))

    sample_left = tuple(item["id"] for item in sample["left"])
    sample_right = tuple(item["id"] for item in sample["right"])
    assert len(sample_left) == len(set(sample_left)) == len(graph.left)
    assert len(sample_right) == len(set(sample_right)) == len(graph.right)
    assert set(sample_left) == set(graph.left)
    assert set(sample_right) == set(graph.right)
    assert {tuple(edge) for edge in sample["edges"]} == set(graph.edges)
    assert sample["counts"] == {
        "left": len(graph.left),
        "right": len(graph.right),
        "edges": graph.m,
        "maximum_matching": 7,
    }
