"""Fixtures compartidas y separación explícita de la fuente privada."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def source_root() -> Path:
    """Devuelve el snapshot local autorizado o salta las pruebas de fuente."""

    configured = os.environ.get("BIPARTITE_MINSA_SOURCE_ROOT")
    if not configured:
        pytest.skip("BIPARTITE_MINSA_SOURCE_ROOT no está definido")
    root = Path(configured).expanduser().resolve()
    if not root.is_dir():
        pytest.skip(f"snapshot local no disponible: {root}")
    return root
