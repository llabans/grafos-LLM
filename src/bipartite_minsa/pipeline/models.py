"""Bundles tipados entre etapas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from bipartite_minsa.domain.clinical_graph import ClinicalDecisionGraph, ExecutionSignature
from bipartite_minsa.domain.coverage import (
    CompatibilityDecision,
    CoverageTarget,
    EvidenceCrosswalk,
)
from bipartite_minsa.domain.criterion import ClinicalCriterion
from bipartite_minsa.domain.recommendation import ClinicalRecommendation
from bipartite_minsa.domain.scenario import ScenarioTemplate
from bipartite_minsa.ingestion.raw import Phase4Summary, StructureContext
from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.validation.source_reconciliation import GraphReconciliationReport


@dataclass(frozen=True, slots=True)
class IngestionBundle:
    source_manifest: dict[str, Any]
    structure: StructureContext
    phase4: Phase4Summary
    graphs: tuple[ClinicalDecisionGraph, ...]
    reconciliations: tuple[GraphReconciliationReport, ...]
    recommendations: tuple[ClinicalRecommendation, ...]
    risk_criteria: tuple[ClinicalCriterion, ...]


@dataclass(frozen=True, slots=True)
class IntegrationBundle:
    ingestion: IngestionBundle
    severity_criteria: tuple[ClinicalCriterion, ...]
    signatures: tuple[ExecutionSignature, ...]
    crosswalks: tuple[EvidenceCrosswalk, ...]
    scenarios: tuple[ScenarioTemplate, ...]
    targets: tuple[CoverageTarget, ...]


@dataclass(frozen=True, slots=True)
class GraphBuildBundle:
    integration: IntegrationBundle
    decisions: tuple[CompatibilityDecision, ...]
    graph: BipartiteGraph
