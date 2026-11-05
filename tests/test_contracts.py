import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from integration_design_grafos.contracts import (
    ContractValidationError,
    load_schema_registry,
    validate_foreign_keys,
    validate_jsonl,
    validate_record,
    validate_unique_primary_key,
)


SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas" / "v2_graphs"
REQUIRED_CONTRACTS = {
    "normalized_assertions",
    "concept_lexicon_v2",
    "variable_dictionary",
    "semantic_atoms",
    "executable_rules",
    "normalized_decision_graphs",
    "graph_normalization_patches",
    "coverage_requirements",
    "clinical_families",
    "contrast_bundles",
    "coverage_edges",
    "multicover_solution",
    "structured_vignettes",
    "qa_gold_candidates",
    "human_review_log",
    "run_manifest_v2",
}


EXAMPLES = {
    "normalized_assertions": {
        "assertion_id": "a1",
        "canonical_gpc_id": "gpc1",
        "source_variant_id": "canonical",
        "source_object_id": "rec_1",
        "source_path": "recommendations.json",
        "source_locator": {
            "section": None,
            "page": 10,
            "table_id": None,
            "flow_id": None,
            "recommendation_id": "rec_1",
        },
        "raw_text": "texto",
        "normalized_text": "texto",
        "version_status": "pending_human",
        "supersedes_assertion_ids": [],
        "resolution_basis": "unresolved",
        "review_status": "pending_human",
    },
    "concept_lexicon_v2": {
        "lexicon_entry_id": "lex1",
        "surface_form": "forma",
        "normalized_surface_form": "forma",
        "language": "es",
        "concept_id": "c1",
        "canonical_label": "concepto",
        "mapping_type": "ambiguous",
        "context_constraints": [],
        "negation_sensitive": True,
        "source_assertion_ids": ["a1"],
        "review_status": "pending_human",
    },
    "variable_dictionary": {
        "variable_id": "v1",
        "canonical_label": "Variable",
        "value_type": "categorical",
        "allowed_domain": ["yes", "no"],
        "allowed_units": [],
        "decision_partitions": [],
        "dependent_predicate_ids": ["p1"],
        "incompatibility_rules": [],
        "requires_human_review": True,
        "source_assertion_ids": ["a1"],
        "review_status": "pending_human",
    },
    "semantic_atoms": {
        "atom_id": "atom1",
        "atom_type": "condition",
        "subject_concept_id": "c1",
        "predicate": "has_state",
        "object": {"value": "yes"},
        "polarity": "positive",
        "modality": "may",
        "logic_expression": None,
        "source_assertion_ids": ["a1"],
        "applies_to_recommendation_ids": ["rec_1"],
        "review_status": "pending_human",
    },
    "executable_rules": {
        "rule_id": "rule1",
        "rule_type": "eligibility",
        "expression": {"operator": "eq", "arguments": ["v1", "yes"]},
        "input_variable_ids": ["v1"],
        "output": {"route_id": "route1"},
        "source_atom_ids": ["atom1"],
        "missing_data_behavior": "request_information",
        "review_status": "pending_human",
    },
    "normalized_decision_graphs": {
        "graph_id": "graph1",
        "flow_id": "flow_1",
        "graph_layer": "normalized",
        "source_path": "flowcharts.json",
        "nodes": [
            {
                "node_id": "n1",
                "node_type": "start",
                "label": "Inicio",
                "source_element_ids": ["n1"],
                "review_status": "pending_human",
            }
        ],
        "edges": [],
        "start_node_ids": ["n1"],
        "terminal_node_ids": [],
        "patch_ids": [],
        "diagnostics": [],
        "review_status": "pending_human",
    },
    "graph_normalization_patches": {
        "patch_id": "patch1",
        "flow_id": "flow_1",
        "operation": "mark_annotation",
        "source_elements": ["n8"],
        "result_elements": [],
        "reason": "annotation candidate",
        "evidence": ["a1"],
        "requires_human_approval": True,
        "approval_status": "pending_human",
    },
    "coverage_requirements": {
        "requirement_id": "req1",
        "requirement_type": "uncertainty",
        "description": "Handle uncertainty",
        "priority": "mandatory",
        "multiplicity": 2,
        "risk_basis": "safety",
        "required_atom_ids": ["atom1"],
        "forbidden_atom_ids": [],
        "independence_rule": "distinct_structural_fingerprint",
        "review_status": "pending_human",
    },
    "clinical_families": {
        "family_id": "fam1",
        "family_type": "anchor",
        "source_recommendation_ids": ["rec_1"],
        "required_facts": [{"variable_id": "v1", "value": "yes"}],
        "unknown_facts": [],
        "forbidden_facts": [],
        "target_route_id": "route1",
        "expected_behavior": {"status": "pending_human"},
        "must_do": [],
        "must_not_do": [],
        "covers_requirement_ids": ["req1"],
        "structural_fingerprint": "f" * 64,
        "estimated_review_minutes": None,
        "review_status": "pending_human",
    },
    "contrast_bundles": {
        "contrast_bundle_id": "cb1",
        "family_ids": ["fam1", "fam2"],
        "decisive_variable_ids": ["v1"],
        "invariant_facts": [{"variable_id": "v2", "value": "same"}],
        "requirement_ids": ["req1"],
        "pair_status": "pending_human",
        "review_status": "pending_human",
    },
    "coverage_edges": {
        "edge_id": "edge1",
        "family_id": "fam1",
        "requirement_id": "req1",
        "coverage_type": "direct",
        "witness_facts": [{"variable_id": "v1", "value": "yes"}],
        "expected_behavior": {"status": "pending_human"},
        "source_atom_ids": ["atom1"],
        "verification_status": "pending_human",
    },
    "multicover_solution": {
        "solution_id": "sol1",
        "mode": "minimum_cost_multicover",
        "solution_status": "pending_human",
        "selected_family_ids": [],
        "requirement_coverage": [{"requirement_id": "req1", "required": 2, "achieved": 0}],
        "gap_requirement_ids": ["req1"],
        "total_cost": None,
        "cost_basis": "pending_human",
        "marginal_costs": [],
        "infeasibility_certificate": None,
        "seed": 17,
        "configuration_sha256": "a" * 64,
        "warnings": ["inputs pending review"],
    },
    "structured_vignettes": {
        "vignette_id": "vig1",
        "family_id": "fam1",
        "structural_fingerprint": "f" * 64,
        "variables": [
            {
                "variable_id": "v1",
                "value": None,
                "value_type": "categorical",
                "unit": None,
                "knowledge_status": "unknown",
                "assertion_status": "not_asserted",
                "source_status": "scenario_defined",
                "source_assertion_ids": [],
            }
        ],
        "rendered_text": None,
        "split": "retired",
        "generation_status": "blocked_pending_human",
        "source_atom_ids": ["atom1"],
        "review_status": "pending_human",
    },
    "qa_gold_candidates": {
        "qa_candidate_id": "qa1",
        "vignette_id": "vig1",
        "question": None,
        "candidate_answer": None,
        "expected_behavior": {"status": "pending_human"},
        "source_atom_ids": ["atom1"],
        "candidate_status": "blocked_pending_human",
        "review_status": "pending_human",
    },
    "human_review_log": {
        "review_id": "review1",
        "object_type": "semantic_atom",
        "object_id": "atom1",
        "reviewer_id": None,
        "decision": "pending_human",
        "comments": [],
        "evidence_refs": ["a1"],
        "reviewed_at": None,
    },
    "run_manifest_v2": {
        "run_id": "run1",
        "pipeline_version": "v2",
        "started_at": "2026-07-17T00:00:00+00:00",
        "status": "completed_with_warnings",
        "source_manifests": {
            "canonical": [
                {"relative_path": "a.json", "sha256": "a" * 64, "bytes": 2}
            ]
        },
        "input_counts": {"files": 1},
        "output_counts": {"records": 0},
        "dropped_counts": {"records": 0},
        "validation_failures": [],
        "warnings": ["material gap"],
        "output_paths": ["outputs/run.json"],
    },
}


def test_registry_contains_exact_required_schema_set_and_all_schemas_are_valid():
    registry = load_schema_registry(SCHEMA_DIR)
    assert set(registry) == REQUIRED_CONTRACTS
    for schema in registry.values():
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["type"] == "object"
        assert schema["additionalProperties"] is False
        Draft202012Validator.check_schema(schema)


@pytest.mark.parametrize("contract_name", sorted(REQUIRED_CONTRACTS))
def test_representative_record_validates_and_unexpected_top_level_property_is_rejected(
    contract_name,
):
    registry = load_schema_registry(SCHEMA_DIR)
    validate_record(EXAMPLES[contract_name], registry[contract_name], contract_name=contract_name)

    invalid = {**EXAMPLES[contract_name], "unexpected": True}
    with pytest.raises(ContractValidationError, match="unexpected"):
        validate_record(invalid, registry[contract_name], contract_name=contract_name)


def test_nested_records_are_closed():
    registry = load_schema_registry(SCHEMA_DIR)
    invalid = json.loads(json.dumps(EXAMPLES["normalized_assertions"]))
    invalid["source_locator"]["invented_locator"] = "no"
    with pytest.raises(ContractValidationError, match="invented_locator"):
        validate_record(invalid, registry["normalized_assertions"])


def test_jsonl_diagnostics_include_line_and_instance_path(tmp_path):
    path = tmp_path / "atoms.jsonl"
    valid = EXAMPLES["semantic_atoms"]
    invalid = {**valid, "review_status": "automatically_approved"}
    path.write_text(
        json.dumps(valid) + "\n" + "{not-json}\n" + json.dumps(invalid) + "\n",
        encoding="utf-8",
    )

    diagnostics = validate_jsonl(path, load_schema_registry(SCHEMA_DIR)["semantic_atoms"])
    assert [item["line"] for item in diagnostics] == [2, 3]
    assert diagnostics[0]["code"] == "invalid_json"
    assert diagnostics[1]["instance_path"] == "/review_status"


def test_primary_key_validator_rejects_duplicates_and_missing_values():
    assert validate_unique_primary_key([{"id": "a"}, {"id": "b"}], "id") == []
    diagnostics = validate_unique_primary_key([{"id": "a"}, {"id": "a"}, {}], "id")
    assert {item["code"] for item in diagnostics} == {"duplicate_primary_key", "missing_primary_key"}


def test_foreign_key_validator_supports_scalar_and_array_fields():
    parent_ids = {"a1", "a2"}
    records = [{"id": "x", "assertion_id": "a1", "assertion_ids": ["a2", "missing"]}]
    assert validate_foreign_keys(records, "assertion_id", parent_ids) == []
    diagnostics = validate_foreign_keys(records, "assertion_ids", parent_ids)
    assert diagnostics[0]["code"] == "missing_foreign_key"
    assert diagnostics[0]["value"] == "missing"
