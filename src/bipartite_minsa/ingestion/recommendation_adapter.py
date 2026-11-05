"""Adaptador conservador de recomendaciones y BPC."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from bipartite_minsa.domain.provenance import SourceReference, ValidationStatus
from bipartite_minsa.domain.recommendation import ClinicalRecommendation
from bipartite_minsa.errors import SourceValidationError
from bipartite_minsa.ingestion.source_manifest import load_json

_NORMALIZATION_RULES: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "rec_1": (("risk_threshold:met",), ("flow_1:n3",)),
    "rec_2": (("risk_threshold:met",), ("flow_1:n4",)),
    "rec_3": (("severity:none",), ("recommendation:rec_3:withhold_antihypertensive",)),
    "bpc_1": (("bp_elevated:true", "severity:none"), ("flow_2:n7",)),
    "bpc_2": (("bp_elevated:true", "severity:present"), ("flow_2:n8",)),
}


class RecommendationAdapter:
    """Preserva el original y aplica solo reglas explícitas por ID."""

    def load(self, path: Path, sha256: str) -> tuple[ClinicalRecommendation, ...]:
        payload = load_json(path)
        if not isinstance(payload, list):
            raise SourceValidationError("recommendations.json debe ser lista")
        recommendations = tuple(self._parse(value, path, sha256) for value in payload)
        ids = [item.recommendation_id for item in recommendations]
        if len(ids) != len(set(ids)):
            raise SourceValidationError("recommendation_id duplicado")
        if set(ids) != set(_NORMALIZATION_RULES):
            raise SourceValidationError(
                "recomendaciones observadas no coinciden con reglas auditadas"
            )
        return tuple(sorted(recommendations, key=lambda item: item.recommendation_id))

    def _parse(self, value: Any, path: Path, sha256: str) -> ClinicalRecommendation:
        if not isinstance(value, dict):
            raise SourceValidationError("recomendación no objeto")
        try:
            recommendation_id = str(value["id"])
            conditions, actions = _NORMALIZATION_RULES[recommendation_id]
            ref = SourceReference(
                source_id="gpc-05-hipertension-embarazo-2025",
                local_path=f"snapshots/gpc_json/gpc-05-hipertension-embarazo-2025/{path.name}",
                entity_id=recommendation_id,
                page=int(value["page"]),
                section=str(value.get("clinical_context") or "") or None,
                sha256=sha256,
            )
            return ClinicalRecommendation(
                recommendation_id=recommendation_id,
                recommendation_type=str(value["recommendation_type"]),
                original_text=str(value["statement"]),
                population_predicates=(),
                condition_predicates=conditions,
                action_predicates=actions,
                strength=None if value.get("strength") is None else str(value["strength"]),
                certainty=(
                    None
                    if value.get("quality_of_evidence") is None
                    else str(value["quality_of_evidence"])
                ),
                status=ValidationStatus.VALIDATED,
                source_refs=(ref,),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise SourceValidationError(f"recomendación inválida: {value.get('id')}") from exc
