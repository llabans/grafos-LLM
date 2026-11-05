"""Pipeline de firmas, criterios, crosswalk, escenarios y objetivos."""

from __future__ import annotations

import argparse
from pathlib import Path

from bipartite_minsa.integration.coverage_target_builder import build_coverage_targets
from bipartite_minsa.integration.evidence_crosswalk import build_crosswalk
from bipartite_minsa.integration.execution_signatures import (
    build_execution_signatures,
    build_severity_criteria,
)
from bipartite_minsa.integration.scenario_generator import generate_scenarios
from bipartite_minsa.pipeline.ingest import ingest_sources
from bipartite_minsa.pipeline.models import IngestionBundle, IntegrationBundle
from bipartite_minsa.serialization import write_json
from bipartite_minsa.validation.provenance_validation import validate_source_refs


def integrate_sources(ingestion: IngestionBundle) -> IntegrationBundle:
    severity = build_severity_criteria(ingestion.graphs)
    signatures = build_execution_signatures(ingestion.graphs)
    crosswalks = build_crosswalk(
        ingestion.graphs, ingestion.recommendations, ingestion.risk_criteria
    )
    scenarios = generate_scenarios(signatures, ingestion.risk_criteria, severity)
    targets = build_coverage_targets(
        ingestion.graphs,
        ingestion.recommendations,
        ingestion.risk_criteria,
        severity,
        crosswalks,
    )
    validate_source_refs(severity)
    validate_source_refs(signatures)
    validate_source_refs(crosswalks)
    validate_source_refs(scenarios)
    validate_source_refs(targets)
    return IntegrationBundle(
        ingestion=ingestion,
        severity_criteria=severity,
        signatures=signatures,
        crosswalks=crosswalks,
        scenarios=scenarios,
        targets=targets,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("reports/runtime/integration.json"))
    args = parser.parse_args()
    bundle = integrate_sources(ingest_sources(args.source_root))
    write_json(
        args.output,
        {
            "severity_criteria": bundle.severity_criteria,
            "signatures": bundle.signatures,
            "crosswalks": bundle.crosswalks,
            "scenario_count": len(bundle.scenarios),
            "target_count": len(bundle.targets),
        },
    )
    print(f"PASS integration -> {args.output}")


if __name__ == "__main__":
    main()
