#!/usr/bin/env python3
"""Compara DFS y Hopcroft--Karp en fixtures matemáticos y en el demo MINSA."""

from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

from bipartite_minsa.experiments import benchmark_matcher, complete_graph, staircase_graph
from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher
from bipartite_minsa.matching.oracles import networkx_cardinality
from bipartite_minsa.pipeline.build_bipartite_graph import build_graph
from bipartite_minsa.pipeline.ingest import ingest_sources
from bipartite_minsa.pipeline.integrate import integrate_sources
from bipartite_minsa.serialization import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--output", type=Path, default=Path("reports/benchmarks.json"))
    parser.add_argument("--repeats", type=int, default=21)
    args = parser.parse_args()

    solvers = (AugmentingPathMatcher(), HopcroftKarpMatcher())
    fixtures = [
        ("staircase_sparse", size, staircase_graph(size)) for size in (32, 64, 128, 256, 512)
    ]
    fixtures.extend(("complete_balanced", size, complete_graph(size)) for size in (16, 32, 64, 96))
    if args.source_root is not None:
        demo = build_graph(integrate_sources(ingest_sources(args.source_root))).graph
        fixtures.append(("gpc_coverage_graph", len(demo.left) + len(demo.right), demo))

    results = []
    oracle_checks = []
    for fixture_name, size, graph in fixtures:
        oracle = networkx_cardinality(graph)
        oracle_checks.append(
            {
                "fixture": fixture_name,
                "size_parameter": size,
                "networkx_cardinality": oracle,
            }
        )
        for solver in solvers:
            result = benchmark_matcher(
                solver,
                graph,
                fixture=fixture_name,
                size_parameter=size,
                repeats=args.repeats,
            )
            if result.cardinality != oracle:
                raise RuntimeError(
                    f"oráculo discrepa en {fixture_name}/{size}/{solver.name}: "
                    f"{result.cardinality} != {oracle}"
                )
            results.append(result)

    write_json(
        args.output,
        {
            "status": "PASS",
            "protocol": {
                "warmup_runs": 1,
                "timed_repeats": args.repeats,
                "summary": "mediana y cuartiles inclusivos de tiempo de pared",
                "memory": "pico aproximado de asignaciones Python observado con tracemalloc",
                "randomness": "ninguna; fixtures deterministas",
                "interpretation": (
                    "Microbenchmark descriptivo local; no permite inferencia clínica ni "
                    "extrapolación de hardware."
                ),
            },
            "environment": {
                "python": sys.version,
                "platform": platform.platform(),
                "processor": platform.processor(),
            },
            "oracle_checks": oracle_checks,
            "results": results,
        },
    )
    print(f"PASS benchmarks ({len(results)} series) -> {args.output}")


if __name__ == "__main__":
    main()
