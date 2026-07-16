"""Resultado verificable e instrumentación de un solver."""

from __future__ import annotations

from dataclasses import dataclass, field

from bipartite_minsa.errors import GraphValidationError
from bipartite_minsa.matching.graph import BipartiteGraph


@dataclass(frozen=True, slots=True)
class MatchingInstrumentation:
    algorithm: str
    bfs_phases: int = 0
    dfs_calls: int = 0
    augmenting_searches: int = 0
    augmentations: int = 0
    edge_scans: int = 0


@dataclass(frozen=True, slots=True)
class MatchingResult:
    """Pares, cardinalidad e instrumentación."""

    pairs: tuple[tuple[str, str], ...]
    instrumentation: MatchingInstrumentation = field(
        default_factory=lambda: MatchingInstrumentation(algorithm="unknown")
    )

    def __post_init__(self) -> None:
        normalized = tuple(sorted(set(self.pairs)))
        if len(normalized) != len(self.pairs):
            raise GraphValidationError("el resultado contiene aristas duplicadas")
        left_ids = [left_id for left_id, _ in normalized]
        right_ids = [right_id for _, right_id in normalized]
        if len(left_ids) != len(set(left_ids)):
            raise GraphValidationError("un vértice izquierdo aparece más de una vez")
        if len(right_ids) != len(set(right_ids)):
            raise GraphValidationError("un vértice derecho aparece más de una vez")
        object.__setattr__(self, "pairs", normalized)

    @property
    def cardinality(self) -> int:
        return len(self.pairs)

    def validate_against(self, graph: BipartiteGraph) -> None:
        """Comprueba pertenencia y unicidad contra el grafo de entrada."""

        graph_edges = set(graph.edges)
        invalid = [pair for pair in self.pairs if pair not in graph_edges]
        if invalid:
            raise GraphValidationError(f"aristas del resultado ajenas al grafo: {invalid}")


def pairs_from_left_map(pair_left: dict[str, str | None]) -> tuple[tuple[str, str], ...]:
    """Convierte un mapa de emparejamiento a pares ordenados."""

    return tuple(sorted((left_id, right_id) for left_id, right_id in pair_left.items() if right_id))
