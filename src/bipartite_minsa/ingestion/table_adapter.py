"""Extracción conservadora de criterios explícitos en `table_003`."""

from __future__ import annotations

from pathlib import Path

from bipartite_minsa.domain.criterion import ClinicalCriterion
from bipartite_minsa.domain.provenance import SourceReference, ValidationStatus
from bipartite_minsa.errors import SourceValidationError
from bipartite_minsa.ingestion.source_manifest import load_json


def _split_list(text: str) -> tuple[str, ...]:
    """Divide guiones principales y conserva viñetas subordinadas."""

    items: list[list[str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            items.append([line[2:].strip()])
        elif items:
            items[-1].append(line)
        else:
            items.append([line])
    return tuple(" ".join(parts).strip() for parts in items if " ".join(parts).strip())


class TableAdapter:
    """Selecciona por ID y estructura, no por similitud semántica."""

    def load_risk_criteria(self, path: Path, sha256: str) -> tuple[ClinicalCriterion, ...]:
        payload = load_json(path)
        if not isinstance(payload, list):
            raise SourceValidationError("tables.json debe ser lista")
        candidates = [
            item for item in payload if isinstance(item, dict) and item.get("id") == "table_003"
        ]
        if len(candidates) != 1:
            raise SourceValidationError("table_003 debe existir una vez")
        table = candidates[0]
        content = table.get("contenido")
        if not isinstance(content, list):
            raise SourceValidationError("table_003 carece de contenido estructurado")

        extracted: list[tuple[str, str]] = []
        for block in content:
            if not isinstance(block, dict) or block.get("tipo") not in {"fila", "fila_encabezado"}:
                continue
            cells = block.get("celdas")
            if not isinstance(cells, list) or len(cells) < 2 or not isinstance(cells[0], dict):
                continue
            level = str(cells[0].get("texto") or "").strip().upper()
            second = cells[1] if isinstance(cells[1], dict) else None
            text = "" if second is None else str(second.get("texto") or "")
            if level == "RIESGO ALTO":
                extracted.extend(("high_risk_factor", item) for item in _split_list(text))
            elif level == "RIESGO MODERADO":
                extracted.extend(("moderate_risk_factor", item) for item in _split_list(text))
            elif level == "RIESGO LEVE":
                extracted.extend(("low_risk_profile", item) for item in _split_list(text))

        observed = {
            category: sum(1 for current, _ in extracted if current == category)
            for category in {c for c, _ in extracted}
        }
        expected = {"high_risk_factor": 10, "moderate_risk_factor": 11, "low_risk_profile": 1}
        if observed != expected:
            raise SourceValidationError(f"estructura inesperada en table_003: {observed}")

        counters: dict[str, int] = {}
        criteria: list[ClinicalCriterion] = []
        for category, original in extracted:
            counters[category] = counters.get(category, 0) + 1
            short = {
                "high_risk_factor": "high",
                "moderate_risk_factor": "moderate",
                "low_risk_profile": "low",
            }[category]
            index = counters[category]
            criterion_id = f"table_003:{short}:{index:02d}"
            predicate = f"risk_{short}:{index:02d}"
            ref = SourceReference(
                source_id="gpc-05-hipertension-embarazo-2025",
                local_path=f"snapshots/gpc_json/gpc-05-hipertension-embarazo-2025/{path.name}",
                entity_id=criterion_id,
                page=9,
                section="sec_4",
                sha256=sha256,
            )
            criteria.append(
                ClinicalCriterion(
                    criterion_id=criterion_id,
                    category=category,
                    original_label=original,
                    normalized_predicate=predicate,
                    value=None,
                    unit=None,
                    status=ValidationStatus.VALIDATED,
                    source_refs=(ref,),
                )
            )
        return tuple(criteria)
