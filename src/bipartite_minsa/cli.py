"""Interfaz única del proyecto."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from bipartite_minsa.pipeline.run_matching import full_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bipartite-minsa")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="ejecuta el pipeline completo")
    run.add_argument(
        "--source-root",
        type=Path,
        default=(Path(value) if (value := os.environ.get("BIPARTITE_MINSA_SOURCE_ROOT")) else None),
    )
    run.add_argument("--output-dir", type=Path, default=Path("reports/runtime"))
    run.add_argument("--source-id", default="gpc-05-hipertension-embarazo-2025")
    run.add_argument("--flows", nargs="*", default=("flow_1", "flow_2"))
    run.add_argument("--algorithm", choices=("hopcroft-karp", "dfs", "both"), default="both")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "run":
        if args.source_root is None:
            raise SystemExit("Use --source-root o BIPARTITE_MINSA_SOURCE_ROOT")
        if args.source_id != "gpc-05-hipertension-embarazo-2025":
            raise SystemExit("source_id fuera de alcance")
        if tuple(args.flows) != ("flow_1", "flow_2"):
            raise SystemExit("el demo validado usa exactamente flow_1 y flow_2")
        report = full_run(args.source_root, args.output_dir)
        metrics = report["graph_metrics"]
        print(
            f"|U|={metrics['left_vertices']} |V|={metrics['right_vertices']} "
            f"|E|={metrics['edges']} |M|={metrics['matching_cardinality']}"
        )


if __name__ == "__main__":
    main()
