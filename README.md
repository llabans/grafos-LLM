# Emparejamiento bipartito MINSA

Proyecto final de algoritmos sobre **matching máximo en grafos bipartitos**, aplicado a la cobertura y auditoría educativa de datos estructurados derivados de una única GPC:

```text
gpc-05-hipertension-embarazo-2025
```

El proyecto no diagnostica, recomienda tratamientos ni asigna pacientes. Los términos de la guía se procesan como evidencia estructurada para estudiar algoritmos.

## Idea central

Se distinguen dos capas:

1. `D=(N,A)`: grafo dirigido que conserva decisiones, ramas y acciones de los flujogramas.
2. `B=(U,V,E)`: grafo bipartito donde `U` son escenarios simbólicos, `V` obligaciones de cobertura y `E` compatibilidades demostrables.

El solver maximiza `|M|` con la restricción de que cada escenario y objetivo aparecen, como máximo, una vez. No resuelve *set cover* ni matching causal/epidemiológico.

## Resultado principal

```text
PASS |U|=75 |V|=35 |E|=267 |M|=33 coverage=94.29%
```

Los dos objetivos no cubiertos obedecen a mecanismos distintos:

- un objetivo aislado, sin compatibilidad demostrable (`|S|=1>|N(S)|=0`);
- un cuello de capacidad: ocho objetivos compiten por siete escenarios (`8>7`).

Los testigos de Hall dan la cota `|M|≤33`; el solver construye 33 pares. Por tanto, la optimalidad del demo queda certificada además de verificada con dos implementaciones propias y NetworkX.

## Goal y LOOP

**Goal:** máxima cobertura educativa uno-a-uno con evidencia reconstruible y cero decisiones clínicas.

```text
INSPECT → PLAN → IMPLEMENT → VERIFY → EVIDENCE AUDIT → REVIEW → RECORD
```

Cada ciclo cierra un corte vertical y solo avanza si sus gates están verdes.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

Solo la biblioteca estándar es necesaria en ejecución. `pytest`, `ruff`, `mypy` y `networkx` son dependencias de desarrollo; NetworkX se usa exclusivamente como oráculo de pruebas.

## Configuración de la fuente local

No copie el ZIP clínico al repositorio. Descomprímalo fuera del árbol Git y exporte la raíz:

```bash
export BIPARTITE_MINSA_SOURCE_ROOT=/ruta/a/integration_design_data
```

La ruta debe contener:

```text
snapshots/gpc_json/gpc-05-hipertension-embarazo-2025/
outputs/phase4/
```

Verifique el manifiesto antes de ejecutar:

```bash
python scripts/validate_sources.py --source-root "$BIPARTITE_MINSA_SOURCE_ROOT"
```

## Ejecución reproducible

```bash
python -m bipartite_minsa.cli run \
  --source-root "$BIPARTITE_MINSA_SOURCE_ROOT" \
  --output-dir reports/runtime \
  --algorithm hopcroft-karp
```

Etapas equivalentes:

```bash
python -m bipartite_minsa.pipeline.ingest --source-root "$BIPARTITE_MINSA_SOURCE_ROOT"
python -m bipartite_minsa.pipeline.integrate --source-root "$BIPARTITE_MINSA_SOURCE_ROOT"
python -m bipartite_minsa.pipeline.build_bipartite_graph --source-root "$BIPARTITE_MINSA_SOURCE_ROOT"
python -m bipartite_minsa.pipeline.run_matching --source-root "$BIPARTITE_MINSA_SOURCE_ROOT"
```

Las salidas son deterministas y ordenadas. Cada entidad conserva archivo, ID, página/sección y SHA-256.

## Calidad y pruebas

```bash
ruff format --check .
ruff check .
mypy src tests scripts
pytest -q
python scripts/validate_project.py --source-root "$BIPARTITE_MINSA_SOURCE_ROOT"
```

Las 29 pruebas cubren grafos vacíos, perfectos, no perfectos, desconectados, desbalanceados, con aislados, múltiples óptimos, endpoints inválidos, particiones solapadas y los 689 grafos etiquetados con particiones de tamaño 0 a 3. DFS y Hopcroft--Karp concuerdan con enumeración exhaustiva y NetworkX en cardinalidad; el oráculo no exige los mismos pares cuando existen óptimos múltiples.

Benchmarks reproducibles:

```bash
python scripts/run_benchmarks.py \
  --source-root "$BIPARTITE_MINSA_SOURCE_ROOT" \
  --output reports/benchmarks.json --repeats 21
```

## Material del curso

- `notebooks/emparejamiento_bipartito_minsa.ipynb`: notebook compatible con Colab.
- `docs/chapter_25_study_notes.md`: lectura técnica del capítulo 25 de CLRS.
- `docs/academic_validation.md`: validación académica y científica.
- `docs/student_explanation.md`: explicación para ingeniería estadística con base médica/epidemiológica.
- `docs/project_report.md`: informe integral del proyecto.
- `docs/evidence_matrix.csv`: afirmación → fuente → estado → limitación.
- `outputs/proyecto_final_emparejamiento_bipartito_minsa.pptx`: presentación final.
- `outputs/material_extra_emparejamiento_bipartito.pdf`: ficha de una página.

## Limitaciones

El resultado mide cobertura estructural dentro de una fuente local y un conjunto de reglas explícitas. No mide validez clínica, efectividad, causalidad, importancia médica ni generalización a otras guías. Una ausencia de arista significa “compatibilidad no demostrada bajo estas reglas”, no “conducta incorrecta”.
