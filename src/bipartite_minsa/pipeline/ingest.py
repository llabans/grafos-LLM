"""Pipeline de ingesta, manifiesto y reconciliación."""

from __future__ import annotations

import argparse
from pathlib import Path

from bipartite_minsa.errors import SourceValidationError
from bipartite_minsa.ingestion.decision_graph_adapter import DecisionGraphAdapter
from bipartite_minsa.ingestion.flowchart_adapter import FlowchartAdapter
from bipartite_minsa.ingestion.phase4_knowledge_adapter import Phase4KnowledgeAdapter
from bipartite_minsa.ingestion.recommendation_adapter import RecommendationAdapter
from bipartite_minsa.ingestion.source_manifest import build_source_manifest, source_layout
from bipartite_minsa.ingestion.structure_adapter import StructureAdapter
from bipartite_minsa.ingestion.table_adapter import TableAdapter
from bipartite_minsa.pipeline.models import IngestionBundle
from bipartite_minsa.serialization import write_json
from bipartite_minsa.validation.provenance_validation import validate_source_refs
from bipartite_minsa.validation.source_reconciliation import build_canonical_graph

BASELINE_COUNTS = {
    "recommendations": 5,
    "tables": 221,
    "flowcharts": 3,
    "semantic_segments_phase4": 30,
    "clinical_knowledge_units_phase4": 269,
    "decision_graphs_phase4": 3,
}


def ingest_sources(source_root: Path, *, strict_hashes: bool = True) -> IngestionBundle:
    layout = source_layout(source_root)
    manifest = build_source_manifest(source_root, strict_hashes=strict_hashes)
    hashes = {entry.path: entry.sha256 for entry in manifest["files"]}

    source_flows = FlowchartAdapter().load(layout.snapshot_dir / "flowcharts.json")
    derived_flows = DecisionGraphAdapter().load(layout.phase4_dir / "decision_graphs.jsonl")
    if {item.flow_id for item in source_flows} != {item.flow_id for item in derived_flows}:
        raise SourceValidationError("inventarios de flujos primario y derivado diferentes")
    derived_by_id = {item.flow_id: item for item in derived_flows}
    flow_hash = hashes["snapshots/gpc_json/gpc-05-hipertension-embarazo-2025/flowcharts.json"]
    graph_pairs = tuple(
        build_canonical_graph(flow, derived_by_id[flow.flow_id], flow_hash) for flow in source_flows
    )
    graphs = tuple(pair[0] for pair in graph_pairs)
    reconciliations = tuple(pair[1] for pair in graph_pairs)

    recommendations = RecommendationAdapter().load(
        layout.snapshot_dir / "recommendations.json",
        hashes["snapshots/gpc_json/gpc-05-hipertension-embarazo-2025/recommendations.json"],
    )
    risk_criteria = TableAdapter().load_risk_criteria(
        layout.snapshot_dir / "tables.json",
        hashes["snapshots/gpc_json/gpc-05-hipertension-embarazo-2025/tables.json"],
    )
    structure = StructureAdapter().load(layout.snapshot_dir / "structure.json")
    phase4 = Phase4KnowledgeAdapter().load(layout.phase4_dir)

    observed_counts = {
        "recommendations": len(recommendations),
        "tables": len(
            __import__("json").loads(
                (layout.snapshot_dir / "tables.json").read_text(encoding="utf-8")
            )
        ),
        "flowcharts": len(graphs),
        "semantic_segments_phase4": phase4.semantic_segments,
        "clinical_knowledge_units_phase4": phase4.clinical_knowledge_units,
        "decision_graphs_phase4": phase4.decision_graphs,
    }
    manifest["observed_counts"] = observed_counts
    manifest["baseline_counts"] = BASELINE_COUNTS
    manifest["baseline_match"] = observed_counts == BASELINE_COUNTS
    if not manifest["baseline_match"]:
        manifest["source_drift"] = True
        if strict_hashes:
            raise SourceValidationError(f"SOURCE_DRIFT en conteos: {observed_counts}")

    validate_source_refs(graphs)
    validate_source_refs(recommendations)
    validate_source_refs(risk_criteria)
    return IngestionBundle(
        source_manifest=manifest,
        structure=structure,
        phase4=phase4,
        graphs=graphs,
        reconciliations=reconciliations,
        recommendations=recommendations,
        risk_criteria=risk_criteria,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("reports/runtime/ingestion.json"))
    parser.add_argument("--allow-source-drift", action="store_true")
    args = parser.parse_args()
    bundle = ingest_sources(args.source_root, strict_hashes=not args.allow_source_drift)
    write_json(
        args.output,
        {
            "source_manifest": bundle.source_manifest,
            "structure": bundle.structure,
            "phase4": bundle.phase4,
            "reconciliations": bundle.reconciliations,
            "graphs": bundle.graphs,
            "recommendations": bundle.recommendations,
            "risk_criteria": bundle.risk_criteria,
        },
    )
    print(f"PASS ingestion -> {args.output}")


if __name__ == "__main__":
    main()
