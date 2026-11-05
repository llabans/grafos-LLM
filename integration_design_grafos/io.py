"""Deterministic, containment-safe filesystem I/O."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any


class PathContainmentError(ValueError):
    """Raised when a requested write escapes its approved output root."""


def ensure_within(path: str | Path, root: str | Path) -> Path:
    """Resolve *path* and require it to be inside (or equal to) *root*."""
    resolved_root = Path(root).resolve()
    resolved_path = Path(path).resolve()
    if resolved_path != resolved_root and resolved_root not in resolved_path.parents:
        raise PathContainmentError(f"Path escapes approved root: {resolved_path} not within {resolved_root}")
    return resolved_path


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 digest of a regular file using bounded-memory reads."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_dumps(value: Any) -> str:
    """Serialize JSON deterministically without ASCII-escaping Spanish text."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _atomic_write_text(path: Path, text: str, *, output_root: str | Path) -> Path:
    destination = ensure_within(path, output_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, destination)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise
    return destination


def atomic_write_json(path: str | Path, value: Any, *, output_root: str | Path) -> Path:
    """Atomically write one canonical JSON document under *output_root*."""
    return _atomic_write_text(Path(path), canonical_json_dumps(value) + "\n", output_root=output_root)


def atomic_write_jsonl(
    path: str | Path, records: Iterable[Mapping[str, Any]], *, output_root: str | Path
) -> Path:
    """Atomically write canonical newline-delimited JSON records."""
    text = "".join(canonical_json_dumps(record) + "\n" for record in records)
    return _atomic_write_text(Path(path), text, output_root=output_root)
