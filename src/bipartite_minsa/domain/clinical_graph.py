"""Modelos para el grafo dirigido y sus firmas alcanzables."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from bipartite_minsa.domain.provenance import SourceReference, ValidationStatus


class BranchSemantics(str, Enum):
    """Semántica declarada de una transición o bifurcación."""

    XOR = "XOR"
    AND = "AND"
    SEQUENTIAL = "SEQUENTIAL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class ClinicalNode:
    node_id: str
    node_type: str
    text: str
    source_refs: tuple[SourceReference, ...]


@dataclass(frozen=True, slots=True)
class ClinicalTransition:
    transition_id: str
    source_node_id: str
    target_node_id: str
    label: str | None
    branch_semantics: BranchSemantics
    source_refs: tuple[SourceReference, ...]


@dataclass(frozen=True, slots=True)
class ClinicalDecisionGraph:
    graph_id: str
    source_id: str
    title: str
    start_node_id: str
    nodes: tuple[ClinicalNode, ...]
    transitions: tuple[ClinicalTransition, ...]
    reachable_node_ids: frozenset[str]
    clinical_scope: bool
    warnings: tuple[str, ...]
    source_refs: tuple[SourceReference, ...]


@dataclass(frozen=True, slots=True)
class ExecutionSignature:
    signature_id: str
    graph_id: str
    decision_outcomes: tuple[str, ...]
    required_predicates: tuple[str, ...]
    activated_action_ids: tuple[str, ...]
    reached_node_ids: tuple[str, ...]
    branch_semantics: tuple[BranchSemantics, ...]
    status: ValidationStatus
    source_refs: tuple[SourceReference, ...]
