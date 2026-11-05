"""Invariantes de procedencia para artefactos derivados."""

from collections.abc import Iterable
from typing import Protocol

from bipartite_minsa.domain.provenance import TARGET_SOURCE_ID, SourceReference
from bipartite_minsa.errors import EvidenceBlockedError


class HasSourceRefs(Protocol):
    @property
    def source_refs(self) -> tuple[SourceReference, ...]: ...


def validate_source_refs(items: Iterable[HasSourceRefs]) -> None:
    for item in items:
        if not item.source_refs:
            raise EvidenceBlockedError(f"entidad sin procedencia: {item}")
        if any(ref.source_id != TARGET_SOURCE_ID for ref in item.source_refs):
            raise EvidenceBlockedError(f"mezcla de GPC detectada: {item}")
