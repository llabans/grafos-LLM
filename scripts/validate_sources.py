#!/usr/bin/env python3
"""Valida hashes, inventarios, reconciliación y semántica del snapshot."""

from __future__ import annotations

import argparse
from pathlib import Path

from bipartite_minsa.pipeline.ingest import ingest_sources
from bipartite_minsa.serialization import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("reports/source_validation.json"))
    args = parser.parse_args()

    bundle = ingest_sources(args.source_root)
    graph_audits = []
    for graph in bundle.graphs:
        graph_audits.append(
            {
                "graph_id": graph.graph_id,
                "nodes": len(graph.nodes),
                "edges": len(graph.transitions),
                "reachable_nodes": len(graph.reachable_node_ids),
                "unreachable_nodes": sorted(
                    {node.node_id for node in graph.nodes} - graph.reachable_node_ids
                ),
                "clinical_scope": graph.clinical_scope,
                "warnings": graph.warnings,
            }
        )

    write_json(
        args.output,
        {
            "status": "PASS",
            "manifest": bundle.source_manifest,
            "reconciliation": bundle.reconciliations,
            "graph_audits": graph_audits,
            "recommendations": len(bundle.recommendations),
            "risk_criteria": len(bundle.risk_criteria),
            "phase4": bundle.phase4,
        },
    )
    print(f"PASS source validation -> {args.output}")


if __name__ == "__main__":
    main()
