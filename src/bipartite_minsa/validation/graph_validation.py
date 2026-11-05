"""Alcanzabilidad, terminales, ciclos y endpoints."""

from __future__ import annotations

from dataclasses import dataclass

from bipartite_minsa.errors import GraphValidationError
from bipartite_minsa.ingestion.raw import RawEdge, RawNode


@dataclass(frozen=True, slots=True)
class DirectedGraphAudit:
    reachable_node_ids: frozenset[str]
    isolated_node_ids: tuple[str, ...]
    reachable_terminal_ids: tuple[str, ...]
    has_cycle: bool


def audit_directed_graph(
    nodes: tuple[RawNode, ...], edges: tuple[RawEdge, ...], start_node_id: str
) -> DirectedGraphAudit:
    node_ids = {node.node_id for node in nodes}
    if start_node_id not in node_ids:
        raise GraphValidationError(f"inicio inexistente: {start_node_id}")
    adjacency: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
    indegree: dict[str, int] = {node_id: 0 for node_id in node_ids}
    for edge in edges:
        if edge.source_node_id not in node_ids or edge.target_node_id not in node_ids:
            raise GraphValidationError(f"endpoint inválido: {edge}")
        adjacency[edge.source_node_id].append(edge.target_node_id)
        indegree[edge.target_node_id] += 1

    reachable: set[str] = set()
    stack = [start_node_id]
    while stack:
        node_id = stack.pop()
        if node_id in reachable:
            continue
        reachable.add(node_id)
        stack.extend(sorted(adjacency[node_id], reverse=True))

    isolated = tuple(
        sorted(node_id for node_id in node_ids if not adjacency[node_id] and indegree[node_id] == 0)
    )
    terminals = tuple(sorted(node_id for node_id in reachable if not adjacency[node_id]))

    color: dict[str, int] = {node_id: 0 for node_id in node_ids}

    def visit(node_id: str) -> bool:
        color[node_id] = 1
        for neighbor in adjacency[node_id]:
            if color[neighbor] == 1 or (color[neighbor] == 0 and visit(neighbor)):
                return True
        color[node_id] = 2
        return False

    has_cycle = any(color[node_id] == 0 and visit(node_id) for node_id in sorted(node_ids))
    return DirectedGraphAudit(frozenset(reachable), isolated, terminals, has_cycle)
