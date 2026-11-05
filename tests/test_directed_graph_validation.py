"""Pruebas de estructura dirigida previa a la proyección bipartita."""

from __future__ import annotations

import pytest

from bipartite_minsa.errors import GraphValidationError
from bipartite_minsa.ingestion.raw import RawEdge, RawNode
from bipartite_minsa.validation.graph_validation import audit_directed_graph


def _node(node_id: str) -> RawNode:
    return RawNode(node_id=node_id, label=node_id, node_type="test", description=None)


def test_reachability_terminal_isolate_and_cycle() -> None:
    nodes = tuple(_node(item) for item in ("a", "b", "c", "z"))
    edges = (RawEdge("a", "b", ""), RawEdge("b", "c", ""), RawEdge("c", "b", ""))
    audit = audit_directed_graph(nodes, edges, "a")
    assert audit.reachable_node_ids == frozenset({"a", "b", "c"})
    assert audit.isolated_node_ids == ("z",)
    assert audit.reachable_terminal_ids == ()
    assert audit.has_cycle is True


def test_missing_start_and_invalid_endpoint_are_rejected() -> None:
    nodes = (_node("a"),)
    with pytest.raises(GraphValidationError, match="inicio inexistente"):
        audit_directed_graph(nodes, (), "missing")
    with pytest.raises(GraphValidationError, match="endpoint inválido"):
        audit_directed_graph(nodes, (RawEdge("a", "missing", ""),), "a")
