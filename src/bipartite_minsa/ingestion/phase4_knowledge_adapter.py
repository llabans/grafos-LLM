"""Inventario Phase 4 filtrado por guía exacta."""

from pathlib import Path

from bipartite_minsa.domain.provenance import TARGET_SOURCE_ID
from bipartite_minsa.ingestion.raw import Phase4Summary
from bipartite_minsa.ingestion.source_manifest import load_jsonl


class Phase4KnowledgeAdapter:
    def load(self, phase4_dir: Path) -> Phase4Summary:
        segments = [
            row
            for row in load_jsonl(phase4_dir / "semantic_segments.jsonl")
            if row.get("source_id") == TARGET_SOURCE_ID
        ]
        units = [
            row
            for row in load_jsonl(phase4_dir / "clinical_knowledge_units.jsonl")
            if row.get("source_id") == TARGET_SOURCE_ID
        ]
        graphs = [
            row
            for row in load_jsonl(phase4_dir / "decision_graphs.jsonl")
            if row.get("source_id") == TARGET_SOURCE_ID
        ]
        return Phase4Summary(
            semantic_segments=len(segments),
            clinical_knowledge_units=len(units),
            decision_graphs=len(graphs),
            knowledge_unit_ids=tuple(sorted(str(row["knowledge_unit_id"]) for row in units)),
        )
