"""Pruebas unitarias y exhaustivas de los algoritmos de matching."""

from __future__ import annotations

from itertools import product

import pytest

from bipartite_minsa.errors import GraphValidationError
from bipartite_minsa.matching.analysis import hall_deficiency_witnesses
from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher
from bipartite_minsa.matching.oracles import exhaustive_maximum_matching, networkx_cardinality
from bipartite_minsa.matching.result import MatchingResult

SOLVERS = (AugmentingPathMatcher(), HopcroftKarpMatcher())


@pytest.mark.parametrize(
    ("graph", "expected"),
    (
        (BipartiteGraph((), (), ()), 0),
        (BipartiteGraph(("u0",), ("v0",), ()), 0),
        (BipartiteGraph(("u0",), ("v0",), (("u0", "v0"),)), 1),
        (
            BipartiteGraph(
                ("u0", "u1", "u2"),
                ("v0", "v1", "v2"),
                (("u0", "v0"), ("u0", "v1"), ("u1", "v0"), ("u2", "v2")),
            ),
            3,
        ),
        (
            BipartiteGraph(
                ("u0", "u1", "u2", "u3"),
                ("v0", "v1"),
                tuple((left, right) for left in ("u0", "u1", "u2", "u3") for right in ("v0", "v1")),
            ),
            2,
        ),
    ),
)
def test_known_instances(graph: BipartiteGraph, expected: int) -> None:
    for solver in SOLVERS:
        result = solver.solve(graph)
        assert result.cardinality == expected
        result.validate_against(graph)


def test_all_labelled_graphs_up_to_three_by_three() -> None:
    """Compara los dos solvers con un oráculo exacto en 689 grafos."""

    checked = 0
    for left_size in range(4):
        for right_size in range(4):
            left = tuple(f"u{index}" for index in range(left_size))
            right = tuple(f"v{index}" for index in range(right_size))
            possible_edges = tuple(product(left, right))
            for mask in range(1 << len(possible_edges)):
                edges = tuple(
                    edge for index, edge in enumerate(possible_edges) if mask & (1 << index)
                )
                graph = BipartiteGraph(left, right, edges)
                expected = exhaustive_maximum_matching(graph).cardinality
                assert AugmentingPathMatcher().solve(graph).cardinality == expected
                assert HopcroftKarpMatcher().solve(graph).cardinality == expected
                assert networkx_cardinality(graph) == expected
                checked += 1
    assert checked == 689


def test_graph_normalizes_order_and_duplicates_but_keeps_isolates() -> None:
    graph = BipartiteGraph(
        ("u1", "u0", "u0"),
        ("v1", "v0", "v1"),
        (("u1", "v1"), ("u1", "v1")),
    )
    assert graph.left == ("u0", "u1")
    assert graph.right == ("v0", "v1")
    assert graph.edges == (("u1", "v1"),)
    assert graph.adjacency["u0"] == ()
    assert graph.n == 4
    assert graph.m == 1
    assert graph.density == pytest.approx(0.25)


@pytest.mark.parametrize(
    "graph",
    (
        lambda: BipartiteGraph(("x",), ("x",), ()),
        lambda: BipartiteGraph(("u",), ("v",), (("missing", "v"),)),
        lambda: BipartiteGraph(("u",), ("v",), (("u", "missing"),)),
    ),
)
def test_invalid_graphs_are_rejected(graph: object) -> None:
    with pytest.raises(GraphValidationError):
        graph()  # type: ignore[operator]


@pytest.mark.parametrize(
    "pairs",
    (
        (("u0", "v0"), ("u0", "v1")),
        (("u0", "v0"), ("u1", "v0")),
        (("u0", "v0"), ("u0", "v0")),
    ),
)
def test_invalid_matching_results_are_rejected(pairs: tuple[tuple[str, str], ...]) -> None:
    with pytest.raises(GraphValidationError):
        MatchingResult(pairs)


def test_instrumentation_is_nontrivial_and_deterministic() -> None:
    graph = BipartiteGraph(
        ("u0", "u1"),
        ("v0", "v1"),
        (("u0", "v0"), ("u0", "v1"), ("u1", "v0")),
    )
    first = HopcroftKarpMatcher().solve(graph)
    second = HopcroftKarpMatcher().solve(graph)
    assert first == second
    assert first.instrumentation.bfs_phases >= 1
    assert first.instrumentation.augmentations == first.cardinality
    assert first.instrumentation.edge_scans > 0


def test_hall_witness_distinguishes_isolate_and_capacity_bottleneck() -> None:
    graph = BipartiteGraph(
        ("u0",),
        ("v0", "v1", "v-isolated"),
        (("u0", "v0"), ("u0", "v1")),
    )
    result = HopcroftKarpMatcher().solve(graph)
    witnesses = hall_deficiency_witnesses(graph, result)
    assert {item.mechanism for item in witnesses} == {
        "capacity_bottleneck",
        "isolated_evidence_gap",
    }
    capacity = next(item for item in witnesses if item.mechanism == "capacity_bottleneck")
    assert capacity.deficiency == 1
    assert capacity.clinical_route_variant_ids == ("v0", "v1")
    assert capacity.neighboring_case_structure_ids == ("u0",)
