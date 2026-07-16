"""Pruebas de la regla explícita que transforma evidencia en aristas."""

from __future__ import annotations

from bipartite_minsa.domain.coverage import CoverageTarget
from bipartite_minsa.domain.provenance import (
    TARGET_SOURCE_ID,
    DecisionStatus,
    SourceReference,
    ValidationStatus,
)
from bipartite_minsa.domain.scenario import ScenarioTemplate
from bipartite_minsa.integration.compatibility_builder import evaluate_compatibility


def _ref(entity: str) -> SourceReference:
    return SourceReference(
        source_id=TARGET_SOURCE_ID,
        local_path="snapshots/gpc_json/gpc-05-hipertension-embarazo-2025/test.json",
        entity_id=entity,
        page=1,
        section="test",
        sha256="0" * 64,
    )


def _scenario() -> ScenarioTemplate:
    return ScenarioTemplate(
        scenario_template_id="scenario:test",
        source_id=TARGET_SOURCE_ID,
        graph_id="graph:test",
        input_predicates=("p",),
        expected_decision_outcomes=(),
        activated_action_ids=("a",),
        execution_signature_id="sig:test",
        generation_rule_id="rule:test",
        status=ValidationStatus.VALIDATED,
        source_refs=(_ref("scenario"),),
    )


def _target(**overrides: object) -> CoverageTarget:
    values: dict[str, object] = {
        "coverage_target_id": "target:test",
        "category": "test",
        "required_predicates": ("p",),
        "forbidden_predicates": (),
        "expected_action_ids": ("a",),
        "crosswalk_ids": (),
        "status": ValidationStatus.VALIDATED,
        "source_refs": (_ref("target"),),
    }
    values.update(overrides)
    return CoverageTarget(**values)  # type: ignore[arg-type]


def test_supported_decision_requires_predicate_action_and_provenance() -> None:
    decision = evaluate_compatibility(_scenario(), _target())
    assert decision.status == DecisionStatus.SUPPORTED
    assert decision.exclusion_reasons == ()
    assert decision.satisfied_predicates == ("p",)
    assert len(decision.source_refs) == 2


def test_rejected_decision_explains_all_failures() -> None:
    target = _target(
        required_predicates=("missing",),
        forbidden_predicates=("p",),
        expected_action_ids=("missing-action",),
    )
    decision = evaluate_compatibility(_scenario(), target)
    assert decision.status == DecisionStatus.REJECTED
    assert decision.exclusion_reasons == (
        "missing_required_predicates",
        "forbidden_predicate_present",
        "missing_expected_actions",
    )
    assert decision.missing_predicates == ("missing",)
    assert "p" in decision.contradictions
    assert "missing_action:missing-action" in decision.contradictions
