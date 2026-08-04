# grafos-LLM

Conversión de guías de práctica clínica (GPC) en **grafos de conocimiento** con ingeniería contract-first, esquemas auditables y pruebas automatizadas. Proyecto **preliminar, en desarrollo**: parte de un esfuerzo mayor para generar representaciones sintéticas a partir de guías clínicas y, posteriormente, entrenar un chatbot clínico asistido.

> Estado: versión preliminar compartida públicamente. No es un modelo entrenado ni validado clínicamente.

## Qué contiene

- `integration_design_grafos/` — paquete Python (contracts, io, manifest) para la integración contract-first de fuentes de guías clínicas inmutables.
- `schemas/v2_graphs/` — 18 esquemas JSON: átomos semánticos, reglas ejecutables, grafos de decisión normalizados, familias clínicas, paquetes de contraste, cobertura multicapa, viñetas estructuradas, candidatos QA/gold y registro de revisión humana.
- `tests/` — pruebas de contratos e inmutabilidad de fuentes (pytest).
- `configs/` — configuración del piloto (ej. breast_cancer_pilot.yaml).
- `docs/` — metodología de grafos multicapa para fine-tuning y plan de diseño v2.

## Instalación y pruebas

```bash
pip install -e ".[test]"
pytest
```

Requisitos: Python >= 3.11, `jsonschema`, `PyYAML`, `NetworkX`, `SciPy`.

## Objetivo metodológico

1. Convertir GPC (fuentes normativas) en segmentos semánticos y unidades de conocimiento clínico.
2. Normalizar en grafos de decisión con reglas ejecutables y trazabilidad a la fuente.
3. Generar representaciones sintéticas (viñetas estructuradas) como insumo para entrenamiento posterior de un asistente clínico, con gates de revisión humana y control de fuga de información.
