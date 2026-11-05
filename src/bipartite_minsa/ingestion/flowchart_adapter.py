"""Adaptador de la fuente primaria de flujogramas."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from bipartite_minsa.errors import SourceValidationError
from bipartite_minsa.ingestion.raw import RawEdge, RawFlowchart, RawNode
from bipartite_minsa.ingestion.source_manifest import load_json


class FlowchartAdapter:
    """Valida estructura mínima y preserva texto/IDs originales."""

    def load(self, path: Path) -> tuple[RawFlowchart, ...]:
        payload = load_json(path)
        if not isinstance(payload, list):
            raise SourceValidationError("flowcharts.json debe ser una lista")
        flows = tuple(self._parse_flow(value) for value in payload)
        ids = [flow.flow_id for flow in flows]
        if len(ids) != len(set(ids)):
            raise SourceValidationError("flow_id duplicado")
        return tuple(sorted(flows, key=lambda flow: flow.flow_id))

    def _parse_flow(self, value: Any) -> RawFlowchart:
        if not isinstance(value, dict):
            raise SourceValidationError("cada flujograma debe ser objeto")
        try:
            nodes = tuple(
                RawNode(
                    node_id=str(node["id"]),
                    label=str(node["label"]),
                    node_type=str(node["type"]),
                    description=(
                        None if node.get("description") is None else str(node["description"])
                    ),
                )
                for node in value["nodes"]
            )
            edges = tuple(
                RawEdge(
                    source_node_id=str(edge["from_node"]),
                    target_node_id=str(edge["to_node"]),
                    label=str(edge.get("label") or ""),
                )
                for edge in value["edges"]
            )
            warnings = tuple(str(item) for item in value.get("metadata", {}).get("warnings", []))
            return RawFlowchart(
                flow_id=str(value["id"]),
                title=str(value["title"]),
                page=int(value["page"]),
                section_id=str(value["section_id"]),
                nodes=nodes,
                edges=edges,
                warnings=warnings,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise SourceValidationError(
                f"contrato de flujograma inválido: {value.get('id')}"
            ) from exc
