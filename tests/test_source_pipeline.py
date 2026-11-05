"""Gates integrales sobre el snapshot canónico autorizado."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from bipartite_minsa.domain.clinical_graph import BranchSemantics
from bipartite_minsa.domain.provenance import TARGET_SOURCE_ID, DecisionStatus
from bipartite_minsa.matching.analysis import hall_deficiency_witnesses
from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher
from bipartite_minsa.matching.oracles import networkx_cardinality
from bipartite_minsa.pipeline.build_bipartite_graph import build_graph
from bipartite_minsa.pipeline.ingest import BASELINE_COUNTS, ingest_sources
from bipartite_minsa.pipeline.integrate import integrate_sources
from bipartite_minsa.validation.provenance_validation import validate_source_refs

pytestmark = pytest.mark.source


def test_manifest_counts_and_reconciliation(source_root: Path) -> None:
    ingestion = ingest_sources(source_root)
    assert ingestion.source_manifest["source_drift"] is False
    assert ingestion.source_manifest["baseline_match"] is True
    assert ingestion.source_manifest["observed_counts"] == BASELINE_COUNTS
    assert len(ingestion.source_manifest["files"]) == 8
    assert all(item.matches_expected for item in ingestion.source_manifest["files"])
    assert all(report.is_equivalent for report in ingestion.reconciliations)
    assert all(report.route_templates_empty for report in ingestion.reconciliations)


def test_clinical_graph_semantics_and_scope(source_root: Path) -> None:
    graphs = ingest_sources(source_root).graphs
    by_flow = {graph.graph_id.rsplit("__flow__", 1)[-1]: graph for graph in graphs}

    flow_1 = by_flow["flow_1"]
    yes_edges = [
        edge
        for edge in flow_1.transitions
        if edge.source_node_id == "flow_1:n1" and edge.label == "Sí"
    ]
    assert len(flow_1.nodes) == 6
    assert len(flow_1.transitions) == 5
    assert len(yes_edges) == 2
    assert {edge.branch_semantics for edge in yes_edges} == {BranchSemantics.AND}

    flow_2 = by_flow["flow_2"]
    assert len(flow_2.nodes) == 9
    assert len(flow_2.transitions) == 7
    assert "flow_2:n9" not in flow_2.reachable_node_ids

    flow_3 = by_flow["flow_3"]
    assert len(flow_3.nodes) == 8
    assert len(flow_3.transitions) == 8
    assert flow_3.clinical_scope is False
    assert flow_1.clinical_scope is True and flow_2.clinical_scope is True


def test_integration_inventory_and_combinatorics(source_root: Path) -> None:
    bundle = integrate_sources(ingest_sources(source_root))
    assert len(bundle.severity_criteria) == 7
    assert len(bundle.signatures) == 5
    assert len(bundle.crosswalks) == 5
    assert len(bundle.scenarios) == 75
    assert len(bundle.targets) == 35

    scenario_rules = Counter(item.generation_rule_id for item in bundle.scenarios)
    assert scenario_rules["rule:risk_high_single:v1"] == 10
    assert scenario_rules["rule:risk_moderate_pair_without_replacement:v1"] == 55
    assert scenario_rules["rule:one_explicit_severity_criterion:v1"] == 7
    assert all(len(item.source_refs) > 0 for item in bundle.scenarios)
    assert all(len(item.source_refs) > 0 for item in bundle.targets)
    validate_source_refs(bundle.scenarios)
    validate_source_refs(bundle.targets)


def test_bipartite_graph_maximum_and_two_gap_mechanisms(source_root: Path) -> None:
    bundle = build_graph(integrate_sources(ingest_sources(source_root)))
    graph = bundle.graph
    assert (len(graph.left), len(graph.right), graph.m) == (75, 35, 267)

    dfs = AugmentingPathMatcher().solve(graph)
    hk = HopcroftKarpMatcher().solve(graph)
    assert dfs.cardinality == hk.cardinality == networkx_cardinality(graph) == 33

    matched_right = {right for _, right in hk.pairs}
    uncovered = set(graph.right) - matched_right
    isolated = {
        right
        for right in graph.right
        if not any(edge_right == right for _, edge_right in graph.edges)
    }
    assert isolated == {"target:recommendation:rec_3_not_explicit"}
    assert len(uncovered) == 2
    assert isolated < uncovered
    contested = uncovered - isolated
    assert len(contested) == 1
    assert next(iter(contested)).startswith("target:flow_2:n4:severity:")

    witnesses = hall_deficiency_witnesses(graph, hk)
    assert len(witnesses) == 2
    by_mechanism = {item.mechanism: item for item in witnesses}
    assert by_mechanism["isolated_evidence_gap"].deficiency == 1
    assert by_mechanism["capacity_bottleneck"].deficiency == 1
    assert len(by_mechanism["capacity_bottleneck"].target_ids) == 8
    assert len(by_mechanism["capacity_bottleneck"].neighboring_scenario_ids) == 7


def test_unsupported_recommendation_never_becomes_an_edge(source_root: Path) -> None:
    bundle = build_graph(integrate_sources(ingest_sources(source_root)))
    target_id = "target:recommendation:rec_3_not_explicit"
    decisions = [item for item in bundle.decisions if item.coverage_target_id == target_id]
    assert len(decisions) == 75
    assert {item.status for item in decisions} == {DecisionStatus.REJECTED}
    assert not any(right == target_id for _, right in bundle.graph.edges)
    crosswalk = next(
        item
        for item in bundle.integration.crosswalks
        if item.crosswalk_id == "xw:rec_3_not_explicit_in_flow"
    )
    assert crosswalk.status == DecisionStatus.HUMAN_REVIEW_REQUIRED


def test_all_derived_entities_remain_in_source_scope(source_root: Path) -> None:
    bundle = build_graph(integrate_sources(ingest_sources(source_root)))
    collections = (
        bundle.integration.ingestion.graphs,
        bundle.integration.ingestion.recommendations,
        bundle.integration.ingestion.risk_criteria,
        bundle.integration.severity_criteria,
        bundle.integration.signatures,
        bundle.integration.crosswalks,
        bundle.integration.scenarios,
        bundle.integration.targets,
        bundle.decisions,
    )
    refs = [ref for items in collections for item in items for ref in item.source_refs]
    assert refs
    assert {ref.source_id for ref in refs} == {TARGET_SOURCE_ID}
    assert all(len(ref.sha256) == 64 for ref in refs)


def test_pipeline_is_deterministic(source_root: Path) -> None:
    first = build_graph(integrate_sources(ingest_sources(source_root)))
    second = build_graph(integrate_sources(ingest_sources(source_root)))
    assert first.graph == second.graph
    assert first.decisions == second.decisions
