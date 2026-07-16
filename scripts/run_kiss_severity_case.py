"""Ejecuta el caso KISS autónomo y muestra su certificado estructural."""

from __future__ import annotations

from bipartite_minsa.kiss_case import build_kiss_severity_graph, objective_labels
from bipartite_minsa.matching.analysis import hall_deficiency_witnesses
from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher


def main() -> None:
    """Resuelve el subgrafo con dos implementaciones propias."""

    graph = build_kiss_severity_graph()
    dfs = AugmentingPathMatcher().solve(graph)
    hk = HopcroftKarpMatcher().solve(graph)
    witnesses = hall_deficiency_witnesses(graph, hk)
    uncovered = sorted(set(graph.right) - {right for _, right in hk.pairs})
    labels = objective_labels()

    print(f"PASS |U|={len(graph.left)} |V|={len(graph.right)} |E|={graph.m} |M*|={hk.cardinality}")
    print(f"agreement dfs={dfs.cardinality} hopcroft_karp={hk.cardinality}")
    print(f"uncovered={uncovered[0]} :: {labels[uncovered[0]]}")
    witness = witnesses[0]
    print(
        "hall_witness "
        f"|S|={len(witness.target_ids)} "
        f"|N(S)|={len(witness.neighboring_scenario_ids)} "
        f"deficiency={witness.deficiency}"
    )


if __name__ == "__main__":
    main()
