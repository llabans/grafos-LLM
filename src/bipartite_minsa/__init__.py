"""Asignación bipartita auditable previa a la generación clínica sintética."""

from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher
from bipartite_minsa.matching.result import MatchingResult

__all__ = [
    "AugmentingPathMatcher",
    "BipartiteGraph",
    "HopcroftKarpMatcher",
    "MatchingResult",
]

__version__ = "0.1.0"
