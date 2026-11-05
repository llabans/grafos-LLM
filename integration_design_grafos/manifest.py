"""Recursive source and run manifests for immutability audits."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io import ensure_within, sha256_file


def build_tree_manifest(root: str | Path) -> list[dict[str, Any]]:
    """Hash every regular file recursively and return records sorted by POSIX path."""
    source_root = Path(root).resolve()
    if not source_root.is_dir():
        raise NotADirectoryError(source_root)

    records: list[dict[str, Any]] = []
    for candidate in sorted(source_root.rglob("*"), key=lambda item: item.as_posix()):
        if not candidate.is_file():
            continue
        resolved = ensure_within(candidate, source_root)
        records.append(
            {
                "relative_path": resolved.relative_to(source_root).as_posix(),
                "sha256": sha256_file(resolved),
                "bytes": resolved.stat().st_size,
            }
        )
    return records


def compare_tree_manifests(
    before: Sequence[Mapping[str, Any]], after: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Report added, removed, and content- or size-modified paths."""
    before_by_path = {str(record["relative_path"]): record for record in before}
    after_by_path = {str(record["relative_path"]): record for record in after}
    before_paths = set(before_by_path)
    after_paths = set(after_by_path)
    modified = sorted(
        path
        for path in before_paths & after_paths
        if (
            before_by_path[path].get("sha256"),
            before_by_path[path].get("bytes"),
        )
        != (
            after_by_path[path].get("sha256"),
            after_by_path[path].get("bytes"),
        )
    )
    added = sorted(after_paths - before_paths)
    removed = sorted(before_paths - after_paths)
    return {
        "unchanged": not (added or removed or modified),
        "added": added,
        "removed": removed,
        "modified": modified,
    }


def build_run_manifest(
    *,
    run_id: str,
    pipeline_version: str,
    source_manifests: Mapping[str, Sequence[Mapping[str, Any]]],
    input_counts: Mapping[str, int],
    output_counts: Mapping[str, int],
    dropped_counts: Mapping[str, int],
    validation_failures: Sequence[Mapping[str, Any]],
    warnings: Sequence[str],
    output_paths: Sequence[str],
    started_at: str | None = None,
) -> dict[str, Any]:
    """Build (but do not write) a run record with explicit counts and diagnostics."""
    if any(not isinstance(failure, Mapping) for failure in validation_failures):
        raise TypeError("validation_failures must contain structured mapping diagnostics")
    if validation_failures:
        status = "failed_validation"
    elif warnings:
        status = "completed_with_warnings"
    else:
        status = "completed"
    return {
        "run_id": run_id,
        "pipeline_version": pipeline_version,
        "started_at": started_at or datetime.now(timezone.utc).isoformat(),
        "status": status,
        "source_manifests": {name: list(records) for name, records in source_manifests.items()},
        "input_counts": dict(input_counts),
        "output_counts": dict(output_counts),
        "dropped_counts": dict(dropped_counts),
        "validation_failures": list(validation_failures),
        "warnings": list(warnings),
        "output_paths": list(output_paths),
    }
