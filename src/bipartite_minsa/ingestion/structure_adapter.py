"""Adaptador de contexto y organización documental."""

from pathlib import Path

from bipartite_minsa.domain.provenance import TARGET_SOURCE_ID
from bipartite_minsa.errors import SourceValidationError
from bipartite_minsa.ingestion.raw import StructureContext
from bipartite_minsa.ingestion.source_manifest import load_json


class StructureAdapter:
    def load(self, path: Path) -> StructureContext:
        payload = load_json(path)
        if not isinstance(payload, dict):
            raise SourceValidationError("structure.json debe ser objeto")
        try:
            document = payload["document"]
            if document["id"] != TARGET_SOURCE_ID:
                raise SourceValidationError(f"document.id fuera de alcance: {document['id']}")
            sections = payload["sections"]
            section_ids = tuple(sorted(self._walk_section_ids(sections)))
            return StructureContext(
                source_id=str(document["id"]),
                title=str(document["title"]),
                total_pages=int(document["total_pages"]),
                section_ids=section_ids,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise SourceValidationError("contrato de structure.json inválido") from exc

    def _walk_section_ids(self, sections: object) -> list[str]:
        if not isinstance(sections, list):
            raise SourceValidationError("sections debe ser lista")
        result: list[str] = []
        for section in sections:
            if not isinstance(section, dict) or "id" not in section:
                raise SourceValidationError("sección inválida")
            result.append(str(section["id"]))
            result.extend(self._walk_section_ids(section.get("children", [])))
        return result
