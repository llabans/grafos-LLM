"""Ejecuta solvers, verifica cardinalidad y exporta artefactos auditables."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from time import perf_counter_ns
from typing import Any

from bipartite_minsa.domain.provenance import DecisionStatus
from bipartite_minsa.matching.analysis import hall_deficiency_witnesses
from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher
from bipartite_minsa.matching.result import MatchingResult
from bipartite_minsa.metrics import graph_metrics
from bipartite_minsa.pipeline.build_bipartite_graph import build_graph
from bipartite_minsa.pipeline.ingest import ingest_sources
from bipartite_minsa.pipeline.integrate import integrate_sources
from bipartite_minsa.pipeline.models import GraphBuildBundle
from bipartite_minsa.serialization import write_json, write_jsonl


def timed_solve(matcher: Any, bundle: GraphBuildBundle) -> tuple[MatchingResult, int]:
    start = perf_counter_ns()
    result = matcher.solve(bundle.graph)
    elapsed = perf_counter_ns() - start
    return result, elapsed


def run_and_verify(bundle: GraphBuildBundle) -> dict[str, Any]:
    dfs_result, dfs_ns = timed_solve(AugmentingPathMatcher(), bundle)
    hk_result, hk_ns = timed_solve(HopcroftKarpMatcher(), bundle)
    if dfs_result.cardinality != hk_result.cardinality:
        raise RuntimeError("gate algorítmico: DFS y Hopcroft-Karp discrepan")

    supported = sum(
        1 for decision in bundle.decisions if decision.status == DecisionStatus.SUPPORTED
    )
    decision_counts = Counter(decision.status.value for decision in bundle.decisions)
    report = {
        "graph_metrics": graph_metrics(bundle.graph, hk_result),
        "hall_deficiency_witnesses": hall_deficiency_witnesses(bundle.graph, hk_result),
        "compatibility_decisions": dict(sorted(decision_counts.items())),
        "supported_edges": supported,
        "dfs": {"result": dfs_result, "elapsed_ns_single_run": dfs_ns},
        "hopcroft_karp": {"result": hk_result, "elapsed_ns_single_run": hk_ns},
        "cardinality_agreement": True,
        "timing_interpretation": (
            "Medición descriptiva de una sola ejecución; no sustenta inferencias de escalabilidad."
        ),
    }
    return report


def export_bundle(bundle: GraphBuildBundle, report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    integration = bundle.integration
    write_json(output_dir / "source_manifest.runtime.json", integration.ingestion.source_manifest)
    write_jsonl(output_dir / "evidence_crosswalk.jsonl", integration.crosswalks)
    write_jsonl(output_dir / "scenario_templates.jsonl", integration.scenarios)
    write_jsonl(output_dir / "coverage_targets.jsonl", integration.targets)
    write_jsonl(output_dir / "compatibility_edges.jsonl", bundle.decisions)
    write_json(
        output_dir / "bipartite_graph.json",
        {"left": bundle.graph.left, "right": bundle.graph.right, "edges": bundle.graph.edges},
    )
    write_json(output_dir / "experiment_results.json", report)


def full_run(source_root: Path, output_dir: Path) -> dict[str, Any]:
    bundle = build_graph(integrate_sources(ingest_sources(source_root)))
    report = run_and_verify(bundle)
    export_bundle(bundle, report, output_dir)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports/runtime"))
    parser.add_argument(
        "--algorithm",
        choices=("hopcroft-karp", "dfs", "both"),
        default="both",
        help="La verificación interna siempre ejecuta ambos para comparar cardinalidad.",
    )
    args = parser.parse_args()
    report = full_run(args.source_root, args.output_dir)
    metrics = report["graph_metrics"]
    print(
        "PASS "
        f"|U|={metrics['left_vertices']} |V|={metrics['right_vertices']} "
        f"|E|={metrics['edges']} |M|={metrics['matching_cardinality']} "
        f"coverage={metrics['target_coverage_percent']:.2f}%"
    )


if __name__ == "__main__":
    main()
