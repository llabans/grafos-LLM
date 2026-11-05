#!/usr/bin/env python3
"""Construye el demo, verifica matching y exporta representaciones DOT."""

from __future__ import annotations

import argparse
from pathlib import Path

from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher
from bipartite_minsa.metrics import graph_metrics
from bipartite_minsa.pipeline.build_bipartite_graph import build_graph
from bipartite_minsa.pipeline.ingest import ingest_sources
from bipartite_minsa.pipeline.integrate import integrate_sources
from bipartite_minsa.serialization import write_json
from bipartite_minsa.visualization import bipartite_matching_dot, directed_graph_dot


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports/visualizations"))
    args = parser.parse_args()

    bundle = build_graph(integrate_sources(ingest_sources(args.source_root)))
    result = HopcroftKarpMatcher().solve(bundle.graph)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for graph in bundle.integration.ingestion.graphs:
        flow_id = graph.graph_id.rsplit("__flow__", 1)[-1]
        if graph.clinical_scope:
            (args.output_dir / f"directed_{flow_id}.dot").write_text(
                directed_graph_dot(graph), encoding="utf-8"
            )
    (args.output_dir / "bipartite_matching.dot").write_text(
        bipartite_matching_dot(bundle.graph, result), encoding="utf-8"
    )
    write_json(args.output_dir / "demo_metrics.json", graph_metrics(bundle.graph, result))
    print(f"PASS demo |M|={result.cardinality} -> {args.output_dir}")


if __name__ == "__main__":
    main()
