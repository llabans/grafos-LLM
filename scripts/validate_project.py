#!/usr/bin/env python3
"""Ejecuta los gates reproducibles y registra evidencia de cada comando."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from bipartite_minsa.serialization import write_json


def _redact(value: str, source_root: str) -> str:
    return value.replace(source_root, "$BIPARTITE_MINSA_SOURCE_ROOT")


def _run(command: list[str], env: dict[str, str], source_root: str) -> dict[str, Any]:
    completed = subprocess.run(command, capture_output=True, text=True, check=False, env=env)
    return {
        "command": [
            "python" if part == sys.executable else _redact(part, source_root) for part in command
        ],
        "returncode": completed.returncode,
        "stdout": _redact(completed.stdout, source_root),
        "stderr": _redact(completed.stderr, source_root),
        "status": "PASS" if completed.returncode == 0 else "FAIL",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("reports/project_validation.json"))
    args = parser.parse_args()

    env = dict(os.environ)
    resolved_source_root = str(args.source_root.resolve())
    env["BIPARTITE_MINSA_SOURCE_ROOT"] = resolved_source_root
    python = sys.executable
    commands = (
        [python, "-m", "ruff", "format", "--check", "src", "tests", "scripts"],
        [python, "-m", "ruff", "check", "src", "tests", "scripts"],
        [python, "-m", "mypy", "src", "tests", "scripts"],
        [python, "-m", "pytest", "-q"],
        [
            python,
            "-m",
            "bipartite_minsa.pipeline.run_matching",
            "--source-root",
            str(args.source_root.resolve()),
            "--output-dir",
            "reports/runtime",
        ],
    )
    results = [_run(command, env, resolved_source_root) for command in commands]
    passed = all(result["returncode"] == 0 for result in results)
    report = {"status": "PASS" if passed else "FAIL", "gates": results}
    write_json(args.output, report)
    print(f"{report['status']} project validation -> {args.output}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
