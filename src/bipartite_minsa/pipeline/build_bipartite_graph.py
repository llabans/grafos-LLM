"""Pipeline de compatibilidad y construcción de B=(U,V,E)."""

from __future__ import annotations

import argparse
from pathlib import Path

from bipartite_minsa.integration.compatibility_builder import (
    build_compatibilities,
    supported_edges,
)
from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.pipeline.ingest import ingest_sources
from bipartite_minsa.pipeline.integrate import integrate_sources
from bipartite_minsa.pipeline.models import GraphBuildBundle, IntegrationBundle
from bipartite_minsa.serialization import write_json
from bipartite_minsa.validation.provenance_validation import validate_source_refs


def build_graph(integration: IntegrationBundle) -> GraphBuildBundle:
    decisions = build_compatibilities(integration.scenarios, integration.targets)
    validate_source_refs(decisions)
    graph = BipartiteGraph(
        left=tuple(item.scenario_template_id for item in integration.scenarios),
        right=tuple(item.coverage_target_id for item in integration.targets),
        edges=supported_edges(decisions),
    )
    return GraphBuildBundle(integration=integration, decisions=decisions, graph=graph)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/processed/bipartite_graph.json"))
    args = parser.parse_args()
    bundle = build_graph(integrate_sources(ingest_sources(args.source_root)))
    write_json(
        args.output,
        {"left": bundle.graph.left, "right": bundle.graph.right, "edges": bundle.graph.edges},
    )
    sizes = f"|U|={len(bundle.graph.left)} |V|={len(bundle.graph.right)} |E|={bundle.graph.m}"
    print(f"PASS graph {sizes}")


if __name__ == "__main__":
    main()
