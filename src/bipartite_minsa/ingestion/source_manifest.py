"""Localización, hashes y conteos de la fuente autorizada."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bipartite_minsa.domain.provenance import TARGET_SOURCE_ID
from bipartite_minsa.errors import SourceValidationError
from bipartite_minsa.ingestion.raw import SourceLayout

EXPECTED_HASHES = {
    f"snapshots/gpc_json/{TARGET_SOURCE_ID}/bibliografia.json": (
        "72d53f3a0024c69f0384282abe5e1efb8789d2de094b85f6567bbf4826c14a44"
    ),
    f"snapshots/gpc_json/{TARGET_SOURCE_ID}/flowcharts.json": (
        "1319d7aa0313dbb409933456dbccb0fa48f94efbb393b2ba7a5308f7aec50391"
    ),
    f"snapshots/gpc_json/{TARGET_SOURCE_ID}/recommendations.json": (
        "469efa9ad85df87ec4b683b2f07a19a0eaba88ee5820ac8783d5ea930d9a1138"
    ),
    f"snapshots/gpc_json/{TARGET_SOURCE_ID}/structure.json": (
        "07c13e216bae5813e5b35d90f876e12ed1b331c2e719e5b99db380d6001e3062"
    ),
    f"snapshots/gpc_json/{TARGET_SOURCE_ID}/tables.json": (
        "3fb3a830d7c2eed4276743212f997f380928a16d976b3fa30acba475f0e2abf5"
    ),
    "outputs/phase4/clinical_knowledge_units.jsonl": (
        "dedb5a0fdec29b61bfeae53dec4100b668adbf7c9b5546844a7ad8da3130c9b0"
    ),
    "outputs/phase4/decision_graphs.jsonl": (
        "a3aee2ddf642cd20786eca59f1d685ea2cbf0c8e2ace4c8b56152c2e21860201"
    ),
    "outputs/phase4/semantic_segments.jsonl": (
        "463cdc490e88f879a17086225bebfba1a22695bbd62d1fc3f4c9bbb4621f93a7"
    ),
}


@dataclass(frozen=True, slots=True)
class FileManifestEntry:
    path: str
    size_bytes: int
    sha256: str
    expected_sha256: str
    matches_expected: bool


def sha256_file(path: Path) -> str:
    """Calcula SHA-256 en bloques."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_layout(source_root: Path) -> SourceLayout:
    """Resuelve y valida directorios mínimos."""

    root = source_root.expanduser().resolve()
    snapshot = root / "snapshots" / "gpc_json" / TARGET_SOURCE_ID
    phase4 = root / "outputs" / "phase4"
    if not snapshot.is_dir():
        raise SourceValidationError(f"snapshot canónico ausente: {snapshot}")
    if not phase4.is_dir():
        raise SourceValidationError(f"Phase 4 ausente: {phase4}")
    return SourceLayout(root=root, snapshot_dir=snapshot, phase4_dir=phase4)


def build_source_manifest(source_root: Path, *, strict_hashes: bool = True) -> dict[str, Any]:
    """Construye manifiesto y detecta drift sin forzar el baseline."""

    layout = source_layout(source_root)
    entries: list[FileManifestEntry] = []
    for relative_path, expected in sorted(EXPECTED_HASHES.items()):
        absolute = layout.root / relative_path
        if not absolute.is_file():
            raise SourceValidationError(f"archivo obligatorio ausente: {relative_path}")
        observed = sha256_file(absolute)
        entries.append(
            FileManifestEntry(
                path=relative_path,
                size_bytes=absolute.stat().st_size,
                sha256=observed,
                expected_sha256=expected,
                matches_expected=observed == expected,
            )
        )

    drift = [entry.path for entry in entries if not entry.matches_expected]
    if strict_hashes and drift:
        raise SourceValidationError(f"SOURCE_DRIFT en: {drift}")

    return {
        "source_id": TARGET_SOURCE_ID,
        "source_drift": bool(drift),
        "drift_files": drift,
        "files": entries,
    }


def load_json(path: Path) -> Any:
    """Carga JSON y convierte errores a errores de fuente."""

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SourceValidationError(f"JSON inválido o ilegible: {path}") from exc


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Carga JSONL como registros de objetos."""

    rows: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise SourceValidationError(f"fila JSONL no objeto: {path}:{line_number}")
                rows.append(value)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SourceValidationError(f"JSONL inválido o ilegible: {path}") from exc
    return rows
