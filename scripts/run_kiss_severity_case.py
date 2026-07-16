"""Asigna estructuras de caso a variantes de ruta antes de generar datos sintéticos."""

from __future__ import annotations

import argparse
from pathlib import Path

from bipartite_minsa.kiss_case import (
    build_assignment_manifest,
    build_kiss_case_route_problem,
    clinical_route_variant_labels,
)
from bipartite_minsa.matching.analysis import hall_deficiency_witnesses
from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher
from bipartite_minsa.matching.oracles import networkx_cardinality
from bipartite_minsa.serialization import write_json


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/runtime/assignment_manifest.json"),
        help="manifiesto reproducible previo a la generación",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path("reports/kiss_severity_case.json"),
        help="resumen reproducible del cálculo y sus límites",
    )
    return parser.parse_args()


def main() -> None:
    """Resuelve el grafo con dos implementaciones propias y exporta la asignación."""

    args = _parse_args()
    problem = build_kiss_case_route_problem()
    graph = problem.graph
    dfs = AugmentingPathMatcher().solve(graph)
    hk = HopcroftKarpMatcher().solve(graph)
    oracle_cardinality = networkx_cardinality(graph)
    witnesses = hall_deficiency_witnesses(graph, hk)
    unassigned = sorted(set(graph.right) - {right for _, right in hk.pairs})
    labels = clinical_route_variant_labels()
    manifest = build_assignment_manifest(problem, hk)
    write_json(args.output, manifest)
    witness = witnesses[0]
    summary = {
        "status": "PASS",
        "stage": "pre_synthetic_generation_assignment",
        "scope": "algorithmic_and_structural_only",
        "graph": {
            "case_structures": len(graph.left),
            "clinical_route_variants": len(graph.right),
            "compatibility_edges": graph.m,
        },
        "maximum_matching": {
            "cardinality": hk.cardinality,
            "route_variant_assignment_percent": 100.0 * hk.cardinality / len(graph.right),
            "solver_agreement": {
                "augmenting_path_dfs": dfs.cardinality,
                "hopcroft_karp": hk.cardinality,
                "networkx_oracle": oracle_cardinality,
            },
        },
        "hall_witness": {
            "clinical_route_variant_count": len(witness.clinical_route_variant_ids),
            "neighboring_case_structure_count": len(witness.neighboring_case_structure_ids),
            "deficiency": witness.deficiency,
        },
        "certificates": {
            "existential_witnesses": len(problem.certificates),
            "reexecution_status": "PASS",
        },
        "generation_status": "not_started",
        "interpretation": (
            "Siete estructuras distintas pueden reservar como máximo siete de ocho "
            "variantes clínicas bajo asignación uno-a-uno."
        ),
        "clinical_content_validation": "pending_expert_review",
    }
    write_json(args.summary_output, summary)

    print(f"PASS |U|={len(graph.left)} |V|={len(graph.right)} |E|={graph.m} |M*|={hk.cardinality}")
    print(
        "agreement "
        f"dfs={dfs.cardinality} "
        f"hopcroft_karp={hk.cardinality} "
        f"networkx={oracle_cardinality}"
    )
    print(f"unassigned_route_variant={unassigned[0]} :: {labels[unassigned[0]]}")
    print(f"existential_certificates={len(problem.certificates)}")
    print(f"assignment_manifest={args.output}")
    print(f"summary_report={args.summary_output}")
    print(
        "hall_witness "
        f"|S|={len(witness.clinical_route_variant_ids)} "
        f"|N(S)|={len(witness.neighboring_case_structure_ids)} "
        f"deficiency={witness.deficiency}"
    )


if __name__ == "__main__":
    main()
