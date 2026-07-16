"""Modelos de la capa combinatoria previa a la generación sintética."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from itertools import product


@dataclass(frozen=True, slots=True)
class BooleanVariable:
    """Variable clínica booleana y su dominio permitido en una estructura."""

    variable_id: str
    allowed_values: tuple[bool, ...]

    def __post_init__(self) -> None:
        if not self.variable_id:
            raise ValueError("variable_id no puede estar vacío")
        if not self.allowed_values:
            raise ValueError("allowed_values no puede estar vacío")
        if len(set(self.allowed_values)) != len(self.allowed_values):
            raise ValueError("allowed_values no puede contener duplicados")


@dataclass(frozen=True, slots=True)
class ValidationProfile:
    """Estados separados para no confundir pruebas estructurales con revisión clínica."""

    source_traceability: str
    structural_consistency: str
    clinical_content: str

    def __post_init__(self) -> None:
        values = (self.source_traceability, self.structural_consistency, self.clinical_content)
        if not all(values):
            raise ValueError("los tres estados de validación deben declararse")
        if "validated" in values:
            raise ValueError("el estado genérico 'validated' no está permitido")


@dataclass(frozen=True, slots=True)
class CaseStructure:
    """Unidad finita de un catálogo piloto, todavía sin instancia ni narración."""

    case_structure_id: str
    catalog_batch_id: str
    unit_capacity: int
    label: str
    entry_state_id: str
    variables: tuple[BooleanVariable, ...]
    required_constraints: tuple[str, ...]
    forbidden_combinations: tuple[tuple[str, ...], ...]
    allowed_missingness: tuple[str, ...]
    source_unit_ids: tuple[str, ...]
    source_refs: tuple[str, ...]
    validation_status: ValidationProfile
    canonical_signature: str = field(init=False)

    def __post_init__(self) -> None:
        variable_ids = tuple(variable.variable_id for variable in self.variables)
        if len(variable_ids) != len(set(variable_ids)):
            raise ValueError("variable_id duplicado en la estructura")
        if set(self.allowed_missingness) - set(variable_ids):
            raise ValueError("allowed_missingness contiene variables desconocidas")
        if not self.source_unit_ids or not self.source_refs:
            raise ValueError("una estructura debe conservar trazabilidad")
        if self.unit_capacity != 1:
            raise ValueError("el matching simple requiere capacidad unitaria declarada")
        payload = {
            "entry_state_id": self.entry_state_id,
            "variables": [
                (variable.variable_id, variable.allowed_values) for variable in self.variables
            ],
            "required_constraints": sorted(self.required_constraints),
            "forbidden_combinations": sorted(
                tuple(sorted(item)) for item in self.forbidden_combinations
            ),
            "allowed_missingness": sorted(self.allowed_missingness),
        }
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        object.__setattr__(
            self,
            "canonical_signature",
            hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        )

    @property
    def variable_ids(self) -> tuple[str, ...]:
        """Identificadores en orden canónico."""

        return tuple(variable.variable_id for variable in self.variables)

    def allows(self, assignment: dict[str, bool]) -> bool:
        """Verifica que una asignación sea completa y pertenezca a ``Inst(u)``."""

        if set(assignment) != set(self.variable_ids):
            return False
        domains = {
            variable.variable_id: set(variable.allowed_values) for variable in self.variables
        }
        if any(value not in domains[variable_id] for variable_id, value in assignment.items()):
            return False
        return not any(
            all(assignment[predicate] for predicate in combination)
            for combination in self.forbidden_combinations
        )

    def iter_instantiations(self) -> Iterator[dict[str, bool]]:
        """Enumera ``Inst(u)``; es exacto para el pequeño ejemplo KISS."""

        variable_ids = self.variable_ids
        domains = tuple(variable.allowed_values for variable in self.variables)
        for values in product(*domains):
            assignment = dict(zip(variable_ids, values, strict=True))
            if self.allows(assignment):
                yield assignment


@dataclass(frozen=True, slots=True)
class ClinicalRouteVariant:
    """Variante canónica: topología de ruta más firma de predicados."""

    clinical_route_variant_id: str
    label: str
    entry_state_id: str
    required_predicates: tuple[str, ...]
    forbidden_predicates: tuple[str, ...]
    decision_node_id: str
    branch: str
    terminal_action_id: str
    path_node_ids: tuple[str, ...]
    source_unit_ids: tuple[str, ...]
    source_refs: tuple[str, ...]
    validation_status: ValidationProfile

    def __post_init__(self) -> None:
        if set(self.required_predicates) & set(self.forbidden_predicates):
            raise ValueError("un predicado no puede ser requerido y prohibido en la misma ruta")
        if not self.path_node_ids or not self.source_unit_ids or not self.source_refs:
            raise ValueError("una variante de ruta debe conservar topología y trazabilidad")

    def accepts(self, assignment: dict[str, bool]) -> bool:
        """Evalúa los predicados explícitos de la variante sobre una instancia."""

        referenced = set((*self.required_predicates, *self.forbidden_predicates))
        if not referenced <= set(assignment):
            return False
        return all(assignment[item] for item in self.required_predicates) and all(
            not assignment[item] for item in self.forbidden_predicates
        )

    @property
    def predicate_signature(self) -> tuple[str, ...]:
        """Firma que distingue variantes con la misma topología clínica."""

        signed = tuple(f"+{item}" for item in self.required_predicates) + tuple(
            f"-{item}" for item in self.forbidden_predicates
        )
        return tuple(sorted(signed))

    @property
    def variant_identity(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Identidad formal ``(path signature, predicate signature)``."""

        return (self.path_node_ids, self.predicate_signature)


@dataclass(frozen=True, slots=True)
class CompatibilityCertificate:
    """Certificado de que existe ``x in Inst(u)`` cuya ejecución produce ``v``."""

    case_structure_id: str
    clinical_route_variant_id: str
    witness_assignment: tuple[tuple[str, bool], ...]
    reexecution_result: str
    compatibility_rule_id: str
    source_refs: tuple[str, ...]
    validation_status: ValidationProfile

    @property
    def witness(self) -> dict[str, bool]:
        """Copia mutable de la asignación testigo."""

        return dict(self.witness_assignment)
