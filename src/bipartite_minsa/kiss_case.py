"""Caso KISS: asignación previa de estructuras a variantes de rutas clínicas.

La arista ``(u, v)`` existe solo si se encuentra una instancia completa
``x in Inst(u)`` cuya ejecución parcial determinista recorre exactamente ``v``.
El ejemplo es autónomo y no genera pacientes, prosa ni datos sintéticos.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any

from bipartite_minsa.domain.pre_generation import (
    BooleanVariable,
    CaseStructure,
    ClinicalRouteVariant,
    CompatibilityCertificate,
    ValidationProfile,
)
from bipartite_minsa.matching.graph import BipartiteGraph
from bipartite_minsa.matching.result import MatchingResult

BP_ELEVATED = "bp_elevated"
SEVERITY_PREDICATES: tuple[tuple[str, str], ...] = (
    ("severity_criterion:01", "Presión arterial en rango de severidad"),
    ("severity_criterion:02", "Trombocitopenia"),
    ("severity_criterion:03", "Deterioro de la función hepática"),
    ("severity_criterion:04", "Lesión renal aguda u oliguria"),
    ("severity_criterion:05", "Edema pulmonar"),
    ("severity_criterion:06", "Trastorno cerebral o visual"),
    ("severity_criterion:07", "Disfunción útero-placentaria"),
)

NO_SEVERITY_ROUTE_VARIANT_ID = "clinical_route_variant:flow_2:no_severity"
ENTRY_STATE_ID = "flow_2:bp_elevated"
DECISION_NODE_ID = "flow_2:n4"
COMPATIBILITY_RULE_ID = "existential_execution_witness:v1"
CATALOG_BATCH_ID = "pilot_catalog:severity_flow_2:v1"
EXECUTION_BOTTOM = "⊥"
STRUCTURE_VALIDATION = ValidationProfile(
    source_traceability="fixture_refs_present",
    structural_consistency="verified_by_domain_invariants",
    clinical_content="pending_expert_review",
)
ROUTE_VARIANT_VALIDATION = ValidationProfile(
    source_traceability="fixture_refs_present",
    structural_consistency="verified_by_path_predicate_identity",
    clinical_content="pending_expert_review",
)
EDGE_VALIDATION = ValidationProfile(
    source_traceability="endpoint_refs_present",
    structural_consistency="witness_found_and_reexecuted",
    clinical_content="pending_expert_review",
)


@dataclass(frozen=True, slots=True)
class KissCaseRouteProblem:
    """Catálogo finito, variantes, certificados y grafo reproducible."""

    case_structures: tuple[CaseStructure, ...]
    clinical_route_variants: tuple[ClinicalRouteVariant, ...]
    certificates: tuple[CompatibilityCertificate, ...]
    graph: BipartiteGraph


def _case_structures() -> tuple[CaseStructure, ...]:
    severity_ids = tuple(predicate_id for predicate_id, _ in SEVERITY_PREDICATES)
    forbidden_pairs = tuple(combinations(severity_ids, 2))
    structures: list[CaseStructure] = []
    for index, (focal_id, focal_label) in enumerate(SEVERITY_PREDICATES, start=1):
        variables = (
            BooleanVariable(BP_ELEVATED, (True,)),
            *(
                BooleanVariable(
                    predicate_id,
                    (False, True) if predicate_id == focal_id else (False,),
                )
                for predicate_id in severity_ids
            ),
        )
        structures.append(
            CaseStructure(
                case_structure_id=f"case_structure:severity_focus:{index:02d}",
                catalog_batch_id=CATALOG_BATCH_ID,
                unit_capacity=1,
                label=f"Estructura focal: {focal_label}",
                entry_state_id=ENTRY_STATE_ID,
                variables=variables,
                required_constraints=(
                    "bp_elevated=true",
                    "all_seven_severity_criteria_observed",
                    "at_most_one_severity_criterion=true",
                ),
                forbidden_combinations=forbidden_pairs,
                allowed_missingness=(),
                source_unit_ids=("flow_2:n4", "bpc_1", "bpc_2"),
                source_refs=("GPC:flow_2", "GPC:severity_criteria"),
                validation_status=STRUCTURE_VALIDATION,
            )
        )
    return tuple(structures)


def _clinical_route_variants() -> tuple[ClinicalRouteVariant, ...]:
    severity_ids = tuple(predicate_id for predicate_id, _ in SEVERITY_PREDICATES)
    variants: list[ClinicalRouteVariant] = []
    for index, (predicate_id, label) in enumerate(SEVERITY_PREDICATES, start=1):
        variants.append(
            ClinicalRouteVariant(
                clinical_route_variant_id=(f"clinical_route_variant:flow_2:severity:{index:02d}"),
                label=(
                    f"PA elevada → decisión de severidad → {label} presente → acción por severidad"
                ),
                entry_state_id=ENTRY_STATE_ID,
                required_predicates=(BP_ELEVATED, predicate_id),
                forbidden_predicates=tuple(item for item in severity_ids if item != predicate_id),
                decision_node_id=DECISION_NODE_ID,
                branch="severity_present",
                terminal_action_id="flow_2:n8",
                path_node_ids=(ENTRY_STATE_ID, DECISION_NODE_ID, "flow_2:n8"),
                source_unit_ids=("flow_2:n4", "flow_2:n8", "bpc_2"),
                source_refs=("GPC:flow_2", "GPC:severity_criteria"),
                validation_status=ROUTE_VARIANT_VALIDATION,
            )
        )
    variants.append(
        ClinicalRouteVariant(
            clinical_route_variant_id=NO_SEVERITY_ROUTE_VARIANT_ID,
            label=(
                "PA elevada → decisión de severidad → siete criterios ausentes "
                "→ acción sin severidad"
            ),
            entry_state_id=ENTRY_STATE_ID,
            required_predicates=(BP_ELEVATED,),
            forbidden_predicates=severity_ids,
            decision_node_id=DECISION_NODE_ID,
            branch="no_severity",
            terminal_action_id="flow_2:n7",
            path_node_ids=(ENTRY_STATE_ID, DECISION_NODE_ID, "flow_2:n7"),
            source_unit_ids=("flow_2:n4", "flow_2:n7", "bpc_1"),
            source_refs=("GPC:flow_2", "GPC:severity_criteria"),
            validation_status=ROUTE_VARIANT_VALIDATION,
        )
    )
    return tuple(variants)


def execute_kiss_decision_graph(assignment: dict[str, bool]) -> str:
    """Ejecuta el fragmento XOR; devuelve ``⊥`` fuera de su dominio.

    La función es parcial: exige las ocho variables observadas, entrada positiva
    y como máximo un criterio activo para identificar una variante canónica.
    """

    severity_ids = tuple(predicate_id for predicate_id, _ in SEVERITY_PREDICATES)
    expected_ids = {BP_ELEVATED, *severity_ids}
    if set(assignment) != expected_ids or not assignment[BP_ELEVATED]:
        return EXECUTION_BOTTOM
    active = tuple(predicate_id for predicate_id in severity_ids if assignment[predicate_id])
    if not active:
        return NO_SEVERITY_ROUTE_VARIANT_ID
    if len(active) != 1:
        return EXECUTION_BOTTOM
    index = severity_ids.index(active[0]) + 1
    return f"clinical_route_variant:flow_2:severity:{index:02d}"


def find_compatibility_witness(
    structure: CaseStructure,
    route_variant: ClinicalRouteVariant,
) -> CompatibilityCertificate | None:
    """Busca un testigo exacto para ``exists x in Inst(u): Execute(D,x)=v``."""

    if structure.entry_state_id != route_variant.entry_state_id:
        return None
    for assignment in structure.iter_instantiations():
        if (
            route_variant.accepts(assignment)
            and execute_kiss_decision_graph(assignment) == route_variant.clinical_route_variant_id
        ):
            return CompatibilityCertificate(
                case_structure_id=structure.case_structure_id,
                clinical_route_variant_id=route_variant.clinical_route_variant_id,
                witness_assignment=tuple(sorted(assignment.items())),
                reexecution_result=route_variant.clinical_route_variant_id,
                compatibility_rule_id=COMPATIBILITY_RULE_ID,
                source_refs=tuple(
                    sorted(set((*structure.source_refs, *route_variant.source_refs)))
                ),
                validation_status=EDGE_VALIDATION,
            )
    return None


def validate_finite_catalog(structures: tuple[CaseStructure, ...]) -> None:
    """Bloquea IDs repetidos, clones estructurales y capacidades no unitarias."""

    ids = tuple(item.case_structure_id for item in structures)
    signatures = tuple(item.canonical_signature for item in structures)
    if len(ids) != len(set(ids)):
        raise ValueError("case_structure_id duplicado en el catálogo")
    if len(signatures) != len(set(signatures)):
        raise ValueError("clon estructural detectado por canonical_signature")
    if {item.unit_capacity for item in structures} != {1}:
        raise ValueError("el catálogo piloto debe declarar capacidad unitaria")


def validate_route_variant_identities(
    route_variants: tuple[ClinicalRouteVariant, ...],
) -> None:
    """Impide contar dos veces la misma combinación ruta-predicados."""

    identities = tuple(item.variant_identity for item in route_variants)
    if len(identities) != len(set(identities)):
        raise ValueError("variante clínica duplicada")


def build_kiss_case_route_problem() -> KissCaseRouteProblem:
    """Construye el problema ``7-8-14`` y sus certificados existenciales."""

    structures = _case_structures()
    route_variants = _clinical_route_variants()
    validate_finite_catalog(structures)
    validate_route_variant_identities(route_variants)
    certificates = tuple(
        certificate
        for structure in structures
        for route_variant in route_variants
        if (certificate := find_compatibility_witness(structure, route_variant)) is not None
    )
    graph = BipartiteGraph(
        left=tuple(item.case_structure_id for item in structures),
        right=tuple(item.clinical_route_variant_id for item in route_variants),
        edges=tuple(
            (certificate.case_structure_id, certificate.clinical_route_variant_id)
            for certificate in certificates
        ),
    )
    return KissCaseRouteProblem(
        case_structures=structures,
        clinical_route_variants=route_variants,
        certificates=certificates,
        graph=graph,
    )


def build_kiss_severity_graph() -> BipartiteGraph:
    """Devuelve solo ``B=(U,V,E)`` para los solvers de matching."""

    return build_kiss_case_route_problem().graph


def case_structure_labels() -> dict[str, str]:
    """Etiquetas de ``U`` sin crear instancias ni narrativas."""

    return {
        item.case_structure_id: item.label
        for item in build_kiss_case_route_problem().case_structures
    }


def clinical_route_variant_labels() -> dict[str, str]:
    """Etiquetas de las variantes de ruta que forman ``V``."""

    return {
        item.clinical_route_variant_id: item.label
        for item in build_kiss_case_route_problem().clinical_route_variants
    }


def build_assignment_manifest(
    problem: KissCaseRouteProblem,
    result: MatchingResult,
) -> dict[str, Any]:
    """Materializa la salida previa a instanciación y permite reejecutar cada par."""

    result.validate_against(problem.graph)
    certificates = {
        (item.case_structure_id, item.clinical_route_variant_id): item
        for item in problem.certificates
    }
    structures = {item.case_structure_id: item for item in problem.case_structures}
    variants = {item.clinical_route_variant_id: item for item in problem.clinical_route_variants}
    assignments: list[dict[str, Any]] = []
    for case_structure_id, clinical_route_variant_id in result.pairs:
        certificate = certificates[(case_structure_id, clinical_route_variant_id)]
        structure = structures[case_structure_id]
        variant = variants[clinical_route_variant_id]
        assignments.append(
            {
                "case_structure_id": case_structure_id,
                "canonical_signature": structure.canonical_signature,
                "unit_capacity": structure.unit_capacity,
                "clinical_route_variant_id": clinical_route_variant_id,
                "path_node_ids": variant.path_node_ids,
                "predicate_signature": variant.predicate_signature,
                "witness_assignment": certificate.witness,
                "reexecution_result": certificate.reexecution_result,
                "terminal_action_id": variant.terminal_action_id,
                "source_refs": certificate.source_refs,
                "validation_status": {
                    "source_traceability": certificate.validation_status.source_traceability,
                    "structural_consistency": certificate.validation_status.structural_consistency,
                    "clinical_content": certificate.validation_status.clinical_content,
                },
            }
        )
    matched_variants = {right_id for _, right_id in result.pairs}
    return {
        "schema_version": "1.0",
        "stage": "pre_synthetic_generation_assignment",
        "catalog_batch_id": CATALOG_BATCH_ID,
        "algorithm_reference": "Cormen et al., Introduction to Algorithms, 4e, Chapter 25",
        "counts": {
            "case_structures": len(problem.graph.left),
            "clinical_route_variants": len(problem.graph.right),
            "compatibility_edges": problem.graph.m,
            "selected_assignments": result.cardinality,
        },
        "selected_assignments": assignments,
        "unassigned_clinical_route_variants": sorted(set(problem.graph.right) - matched_variants),
        "generation_status": "not_started",
    }
