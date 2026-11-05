"""Adaptador de la representación derivada Phase 4."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from bipartite_minsa.domain.provenance import TARGET_SOURCE_ID
from bipartite_minsa.errors import SourceValidationError
from bipartite_minsa.ingestion.raw import RawDecisionGraph, RawEdge, RawNode
from bipartite_minsa.ingestion.source_manifest import load_jsonl


class DecisionGraphAdapter:
    """Filtra por la guía exacta y preserva la normalización derivada."""

    def load(self, path: Path) -> tuple[RawDecisionGraph, ...]:
        rows = [row for row in load_jsonl(path) if row.get("source_id") == TARGET_SOURCE_ID]
        graphs = tuple(self._parse_graph(row) for row in rows)
        ids = [graph.flow_id for graph in graphs]
        if len(ids) != len(set(ids)):
            raise SourceValidationError("flow_id duplicado en Phase 4")
        return tuple(sorted(graphs, key=lambda graph: graph.flow_id))

    def _parse_graph(self, value: dict[str, Any]) -> RawDecisionGraph:
        try:
            trace = value["traceability"]
            return RawDecisionGraph(
                flow_id=str(value["flow_id"]),
                decision_graph_id=str(value["decision_graph_id"]),
                start_node_id=str(value["start_node_id"]),
                terminal_node_ids=tuple(sorted(str(item) for item in value["terminal_node_ids"])),
                nodes=tuple(
                    RawNode(
                        node_id=str(node["id"]),
                        label=str(node["label"]),
                        node_type=str(node["type"]),
                        description=(
                            None if node.get("description") is None else str(node["description"])
                        ),
                    )
                    for node in value["nodes"]
                ),
                edges=tuple(
                    RawEdge(
                        source_node_id=str(edge["from_node"]),
                        target_node_id=str(edge["to_node"]),
                        label=str(edge.get("label") or ""),
                    )
                    for edge in value["edges"]
                ),
                page=int(trace["page"]),
                section_id=str(trace["section_id"]),
                route_templates=tuple(value.get("route_templates", [])),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise SourceValidationError(
                f"contrato decision_graph inválido: {value.get('decision_graph_id')}"
            ) from exc
