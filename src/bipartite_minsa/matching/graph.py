"""Estructura de datos bipartita independiente del dominio."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from functools import cached_property
from types import MappingProxyType

from bipartite_minsa.errors import GraphValidationError


@dataclass(frozen=True)
class BipartiteGraph:
    """Grafo bipartito validado, ordenado y determinista.

    Las aristas duplicadas se colapsan. Los vértices aislados permanecen en sus
    particiones para que el modelo de complejidad pueda distinguir ``n`` de ``m``.
    """

    left: tuple[str, ...]
    right: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        normalized_left = tuple(sorted(set(self.left)))
        normalized_right = tuple(sorted(set(self.right)))
        overlap = set(normalized_left) & set(normalized_right)
        if overlap:
            raise GraphValidationError(f"particiones solapadas: {sorted(overlap)}")

        left_set = set(normalized_left)
        right_set = set(normalized_right)
        normalized_edges = tuple(sorted(set(self.edges)))
        for left_id, right_id in normalized_edges:
            if left_id not in left_set:
                raise GraphValidationError(f"endpoint izquierdo inexistente: {left_id}")
            if right_id not in right_set:
                raise GraphValidationError(f"endpoint derecho inexistente: {right_id}")

        object.__setattr__(self, "left", normalized_left)
        object.__setattr__(self, "right", normalized_right)
        object.__setattr__(self, "edges", normalized_edges)

    @cached_property
    def adjacency(self) -> Mapping[str, tuple[str, ...]]:
        """Lista de adyacencia completa, incluidos vértices aislados."""

        mutable: dict[str, list[str]] = {left_id: [] for left_id in self.left}
        for left_id, right_id in self.edges:
            mutable[left_id].append(right_id)
        frozen = {left_id: tuple(sorted(neighbors)) for left_id, neighbors in mutable.items()}
        return MappingProxyType(frozen)

    @property
    def n(self) -> int:
        """Número total de vértices, ``|L| + |R|``."""

        return len(self.left) + len(self.right)

    @property
    def m(self) -> int:
        """Número de aristas distintas."""

        return len(self.edges)

    @property
    def density(self) -> float:
        """Densidad respecto al bipartito completo."""

        possible = len(self.left) * len(self.right)
        return 0.0 if possible == 0 else self.m / possible
