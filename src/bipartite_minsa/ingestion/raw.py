"""Contratos internos para aislar JSON crudo de los modelos de dominio."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class RawNode:
    node_id: str
    label: str
    node_type: str
    description: str | None


@dataclass(frozen=True, slots=True)
class RawEdge:
    source_node_id: str
    target_node_id: str
    label: str


@dataclass(frozen=True, slots=True)
class RawFlowchart:
    flow_id: str
    title: str
    page: int
    section_id: str
    nodes: tuple[RawNode, ...]
    edges: tuple[RawEdge, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RawDecisionGraph:
    flow_id: str
    decision_graph_id: str
    start_node_id: str
    terminal_node_ids: tuple[str, ...]
    nodes: tuple[RawNode, ...]
    edges: tuple[RawEdge, ...]
    page: int
    section_id: str
    route_templates: tuple[Any, ...]


@dataclass(frozen=True, slots=True)
class SourceLayout:
    root: Path
    snapshot_dir: Path
    phase4_dir: Path


@dataclass(frozen=True, slots=True)
class StructureContext:
    source_id: str
    title: str
    total_pages: int
    section_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Phase4Summary:
    semantic_segments: int
    clinical_knowledge_units: int
    decision_graphs: int
    knowledge_unit_ids: tuple[str, ...]
