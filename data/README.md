# Política de datos

El repositorio no contiene el ZIP ni los JSON clínico-estructurales originales. La fuente se configura fuera de Git mediante:

```bash
export BIPARTITE_MINSA_SOURCE_ROOT=/ruta/a/integration_design_data
```

## Directorios

- `manifests/`: hashes, tamaños, conteos y metadatos necesarios para detectar drift.
- `interim/`: salidas temporales regenerables; no versionadas.
- `processed/`: artefactos derivados regenerables; no versionados por defecto.
- `samples/`: reservado exclusivamente para fixtures matemáticos sin contenido clínico.

## Fuente autorizada

Solo `gpc-05-hipertension-embarazo-2025`. Se excluyen todas las demás guías y la variante resumida. Phase 4 se filtra por `source_id` exacto antes de contar o adaptar.

## Reproducción

```bash
python scripts/validate_sources.py --source-root "$BIPARTITE_MINSA_SOURCE_ROOT"
python -m bipartite_minsa.pipeline.run_matching \
  --source-root "$BIPARTITE_MINSA_SOURCE_ROOT" \
  --output-dir reports/runtime
```

Las salidas conservan IDs, localización y hash, pero deben revisarse antes de cualquier publicación. No hay datos de pacientes en el proyecto.
