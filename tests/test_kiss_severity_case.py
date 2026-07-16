"""Invariantes del ejemplo KISS previo a la generación sintética."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from bipartite_minsa.kiss_case import (
    BP_ELEVATED,
    EXECUTION_BOTTOM,
    NO_SEVERITY_ROUTE_VARIANT_ID,
    SEVERITY_PREDICATES,
    build_assignment_manifest,
    build_kiss_case_route_problem,
    execute_kiss_decision_graph,
    find_compatibility_witness,
    validate_finite_catalog,
)
from bipartite_minsa.matching.analysis import hall_deficiency_witnesses
from bipartite_minsa.matching.augmenting_path import AugmentingPathMatcher
from bipartite_minsa.matching.hopcroft_karp import HopcroftKarpMatcher
from bipartite_minsa.serialization import to_jsonable


def test_kiss_graph_has_predeclared_counts_and_maximum() -> None:
    problem = build_kiss_case_route_problem()
    graph = problem.graph
    dfs = AugmentingPathMatcher().solve(graph)
    hk = HopcroftKarpMatcher().solve(graph)

    assert (len(graph.left), len(graph.right), graph.m) == (7, 8, 14)
    assert dfs.cardinality == hk.cardinality == 7
    assert len({left for left, _ in hk.pairs}) == 7
    assert len({right for _, right in hk.pairs}) == 7


def test_catalog_is_finite_unit_capacity_and_clone_resistant() -> None:
    structures = build_kiss_case_route_problem().case_structures
    assert {item.unit_capacity for item in structures} == {1}
    assert len({item.catalog_batch_id for item in structures}) == 1
    assert len({item.canonical_signature for item in structures}) == len(structures)
    assert all(len(item.canonical_signature) == 64 for item in structures)

    clone = replace(structures[0], case_structure_id="case_structure:renamed_clone")
    assert clone.canonical_signature == structures[0].canonical_signature
    with pytest.raises(ValueError, match="clon estructural"):
        validate_finite_catalog((structures[0], clone))


def test_each_structure_observes_all_seven_criteria_without_missingness() -> None:
    problem = build_kiss_case_route_problem()
    severity_ids = {predicate_id for predicate_id, _ in SEVERITY_PREDICATES}

    for index, structure in enumerate(problem.case_structures, start=1):
        domains = {
            variable.variable_id: variable.allowed_values for variable in structure.variables
        }
        assert severity_ids <= set(domains)
        assert domains[BP_ELEVATED] == (True,)
        assert domains[f"severity_criterion:{index:02d}"] == (False, True)
        assert all(
            domain == (False,)
            for predicate_id, domain in domains.items()
            if predicate_id in severity_ids and predicate_id != f"severity_criterion:{index:02d}"
        )
        assert structure.allowed_missingness == ()
        assert len(tuple(structure.iter_instantiations())) == 2


def test_partial_xor_execution_returns_bottom_outside_its_domain() -> None:
    severity_ids = tuple(predicate_id for predicate_id, _ in SEVERITY_PREDICATES)
    complete_negative = {BP_ELEVATED: True, **dict.fromkeys(severity_ids, False)}
    incomplete = dict(complete_negative)
    incomplete.pop(severity_ids[-1])
    two_active = dict(complete_negative)
    two_active[severity_ids[0]] = True
    two_active[severity_ids[1]] = True

    assert execute_kiss_decision_graph(incomplete) == EXECUTION_BOTTOM
    assert execute_kiss_decision_graph(two_active) == EXECUTION_BOTTOM
    assert execute_kiss_decision_graph(complete_negative) == NO_SEVERITY_ROUTE_VARIANT_ID


def test_every_edge_has_a_complete_existential_execution_witness() -> None:
    problem = build_kiss_case_route_problem()
    structures = {item.case_structure_id: item for item in problem.case_structures}
    variants = {item.clinical_route_variant_id: item for item in problem.clinical_route_variants}

    assert len(problem.certificates) == problem.graph.m
    for certificate in problem.certificates:
        structure = structures[certificate.case_structure_id]
        variant = variants[certificate.clinical_route_variant_id]
        witness = certificate.witness
        assert structure.allows(witness)
        assert variant.accepts(witness)
        assert execute_kiss_decision_graph(witness) == variant.clinical_route_variant_id
        assert certificate.reexecution_result == variant.clinical_route_variant_id
        assert set(witness) == set(structure.variable_ids)
        assert certificate.source_refs


def test_no_severity_edges_use_explicit_negative_observations() -> None:
    problem = build_kiss_case_route_problem()
    severity_ids = tuple(predicate_id for predicate_id, _ in SEVERITY_PREDICATES)
    certificates = [
        item
        for item in problem.certificates
        if item.clinical_route_variant_id == NO_SEVERITY_ROUTE_VARIANT_ID
    ]

    assert len(certificates) == 7
    for certificate in certificates:
        witness = certificate.witness
        assert set(severity_ids) <= set(witness)
        assert all(witness[predicate_id] is False for predicate_id in severity_ids)


def test_compatibility_is_not_a_predeclared_one_to_one_mapping() -> None:
    problem = build_kiss_case_route_problem()
    graph = problem.graph
    right_degrees = {
        variant_id: sum(edge_variant == variant_id for _, edge_variant in graph.edges)
        for variant_id in graph.right
    }

    assert graph.m < len(graph.left) * len(graph.right)
    assert {len(graph.adjacency[item]) for item in graph.left} == {2}
    assert right_degrees[NO_SEVERITY_ROUTE_VARIANT_ID] == 7
    assert {
        degree
        for variant_id, degree in right_degrees.items()
        if variant_id != NO_SEVERITY_ROUTE_VARIANT_ID
    } == {1}
    first_structure = problem.case_structures[0]
    unrelated_variant = problem.clinical_route_variants[1]
    assert find_compatibility_witness(first_structure, unrelated_variant) is None


def test_route_variant_identity_combines_path_and_predicates() -> None:
    variants = build_kiss_case_route_problem().clinical_route_variants
    severe = tuple(item for item in variants if item.branch == "severity_present")

    assert len({item.variant_identity for item in variants}) == len(variants)
    assert len({item.path_node_ids for item in severe}) == 1
    assert len({item.predicate_signature for item in severe}) == 7
    for variant in variants:
        assert variant.entry_state_id
        assert variant.decision_node_id
        assert variant.branch
        assert variant.terminal_action_id
        assert variant.source_unit_ids
        assert variant.source_refs
        assert set(variant.required_predicates).isdisjoint(variant.forbidden_predicates)


def test_validation_states_remain_separate_and_conservative() -> None:
    problem = build_kiss_case_route_problem()
    profiles = (
        *(item.validation_status for item in problem.case_structures),
        *(item.validation_status for item in problem.clinical_route_variants),
        *(item.validation_status for item in problem.certificates),
    )
    for profile in profiles:
        assert profile.source_traceability
        assert profile.structural_consistency
        assert profile.clinical_content == "pending_expert_review"
        assert "validated" not in {
            profile.source_traceability,
            profile.structural_consistency,
            profile.clinical_content,
        }


def test_hall_witness_explains_the_seven_of_eight_limit() -> None:
    graph = build_kiss_case_route_problem().graph
    result = HopcroftKarpMatcher().solve(graph)
    witnesses = hall_deficiency_witnesses(graph, result)

    assert len(witnesses) == 1
    witness = witnesses[0]
    assert witness.mechanism == "capacity_bottleneck"
    assert witness.clinical_route_variant_ids == graph.right
    assert witness.neighboring_case_structure_ids == graph.left
    assert witness.deficiency == 1


def test_assignment_manifest_is_reexecutable_and_not_synthetic_data() -> None:
    problem = build_kiss_case_route_problem()
    result = HopcroftKarpMatcher().solve(problem.graph)
    manifest = build_assignment_manifest(problem, result)
    assignments = manifest["selected_assignments"]

    assert manifest["generation_status"] == "not_started"
    assert manifest["counts"] == {
        "case_structures": 7,
        "clinical_route_variants": 8,
        "compatibility_edges": 14,
        "selected_assignments": 7,
    }
    assert isinstance(assignments, list)
    assert len(assignments) == 7
    assert len({item["case_structure_id"] for item in assignments}) == 7
    assert len({item["clinical_route_variant_id"] for item in assignments}) == 7
    for item in assignments:
        assert item["unit_capacity"] == 1
        assert item["reexecution_result"] == item["clinical_route_variant_id"]
        assert (
            execute_kiss_decision_graph(item["witness_assignment"])
            == item["clinical_route_variant_id"]
        )


def test_versioned_sample_is_the_same_problem_used_by_the_demo() -> None:
    problem = build_kiss_case_route_problem()
    sample_path = Path(__file__).parents[1] / "data" / "samples" / "kiss_severity_graph.json"
    sample = json.loads(sample_path.read_text(encoding="utf-8"))

    sample_left = tuple(item["case_structure_id"] for item in sample["case_structures"])
    sample_right = tuple(
        item["clinical_route_variant_id"] for item in sample["clinical_route_variants"]
    )
    sample_edges = {
        (item["case_structure_id"], item["clinical_route_variant_id"])
        for item in sample["compatibility_edges"]
    }
    sample_witnesses = {
        (item["case_structure_id"], item["clinical_route_variant_id"]): item["witness_assignment"]
        for item in sample["compatibility_edges"]
    }
    sample_reexecutions = {
        (item["case_structure_id"], item["clinical_route_variant_id"]): item["reexecution_result"]
        for item in sample["compatibility_edges"]
    }

    assert sample_left == problem.graph.left
    assert set(sample_right) == set(problem.graph.right)
    assert [item["unit_capacity"] for item in sample["case_structures"]] == [1] * 7
    assert [item["canonical_signature"] for item in sample["case_structures"]] == [
        item.canonical_signature for item in problem.case_structures
    ]
    assert sample_edges == set(problem.graph.edges)
    assert sample_witnesses == {
        (item.case_structure_id, item.clinical_route_variant_id): item.witness
        for item in problem.certificates
    }
    assert sample_reexecutions == {
        (item.case_structure_id, item.clinical_route_variant_id): item.reexecution_result
        for item in problem.certificates
    }
    assert sample["counts"] == {
        "case_structures": len(problem.graph.left),
        "clinical_route_variants": len(problem.graph.right),
        "compatibility_edges": problem.graph.m,
        "maximum_matching": 7,
    }


def test_versioned_assignment_manifest_matches_the_solver_output() -> None:
    root = Path(__file__).parents[1]
    problem = build_kiss_case_route_problem()
    result = HopcroftKarpMatcher().solve(problem.graph)
    expected = to_jsonable(build_assignment_manifest(problem, result))
    observed = json.loads(
        (root / "data" / "samples" / "assignment_manifest.json").read_text(encoding="utf-8")
    )
    assert observed == expected


def test_kiss_artifacts_do_not_reintroduce_educational_semantics() -> None:
    root = Path(__file__).parents[1]
    paths = (
        root / "src" / "bipartite_minsa" / "kiss_case.py",
        root / "src" / "bipartite_minsa" / "domain" / "pre_generation.py",
        root / "scripts" / "run_kiss_severity_case.py",
        root / "data" / "samples" / "kiss_severity_graph.json",
        root / "notebooks" / "research_var_cases_kiss.ipynb",
    )
    forbidden_terms = ("educativ", "aprendiz", "microobjet", "learning_objective", "blueprint")
    for path in paths:
        normalized = path.read_text(encoding="utf-8").lower()
        assert not any(term in normalized for term in forbidden_terms), path
