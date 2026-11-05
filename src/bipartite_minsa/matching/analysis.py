"""Certificados de Hall para rutas clínicas sin estructura asignada."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from bipartite_minsa.errors import GraphValidationError
from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.result import MatchingResult


@dataclass(frozen=True, slots=True)
class HallDeficiencyWitness:
    """Conjunto ``S`` de rutas con ``|S| > |N(S)|``."""

    root_unmatched_route: str
    clinical_route_variant_ids: tuple[str, ...]
    neighboring_case_structure_ids: tuple[str, ...]
    deficiency: int
    mechanism: str


def hall_deficiency_witnesses(
    graph: BipartiteGraph,
    result: MatchingResult,
) -> tuple[HallDeficiencyWitness, ...]:
    """Extrae testigos de Hall mediante alcanzabilidad alternante desde ``V``.

    El procedimiento presupone un matching máximo. Si una ruta libre no
    induce déficit positivo, se rechaza el resultado porque existiría un camino
    aumentante o el matching sería inconsistente.
    """

    result.validate_against(graph)
    matched_left = dict(result.pairs)
    matched_right = {right_id: left_id for left_id, right_id in result.pairs}
    right_adjacency: dict[str, list[str]] = {right_id: [] for right_id in graph.right}
    for left_id, right_id in graph.edges:
        right_adjacency[right_id].append(left_id)

    unmatched_right = sorted(set(graph.right) - set(matched_right))
    witnesses: dict[tuple[tuple[str, ...], tuple[str, ...]], HallDeficiencyWitness] = {}
    for root in unmatched_right:
        seen_right = {root}
        seen_left: set[str] = set()
        queue: deque[tuple[str, str]] = deque([("right", root)])
        while queue:
            side, vertex = queue.popleft()
            if side == "right":
                for left_id in sorted(right_adjacency[vertex]):
                    if matched_right.get(vertex) == left_id or left_id in seen_left:
                        continue
                    seen_left.add(left_id)
                    queue.append(("left", left_id))
            else:
                matched_target = matched_left.get(vertex)
                if matched_target is not None and matched_target not in seen_right:
                    seen_right.add(matched_target)
                    queue.append(("right", matched_target))

        route_ids = tuple(sorted(seen_right))
        case_structure_ids = tuple(sorted(seen_left))
        deficiency = len(route_ids) - len(case_structure_ids)
        if deficiency <= 0:
            raise GraphValidationError(
                "la ruta libre no genera testigo de Hall; verifique maximalidad del matching"
            )
        mechanism = "isolated_evidence_gap" if not case_structure_ids else "capacity_bottleneck"
        key = (route_ids, case_structure_ids)
        witnesses.setdefault(
            key,
            HallDeficiencyWitness(
                root_unmatched_route=root,
                clinical_route_variant_ids=route_ids,
                neighboring_case_structure_ids=case_structure_ids,
                deficiency=deficiency,
                mechanism=mechanism,
            ),
        )
    return tuple(sorted(witnesses.values(), key=lambda item: item.root_unmatched_route))
