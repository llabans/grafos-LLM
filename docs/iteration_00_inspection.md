# Iteración 0 - Inspección, evidencia y diseño

## Objetivo

Establecer, antes de programar, qué fuentes son autorizadas, qué transformaciones son defendibles y qué artefactos deben quedar bloqueados por evidencia. Esta iteración cubre la primera acción exigida por el prompt maestro y no declara implementado ningún algoritmo.

## Evidencia inspeccionada

- Repositorio GitHub `llabans/grafos-LLM`: existe, es público, rama por defecto declarada `main`, tamaño reportado 0 y sin contenido inicial.
- ZIP local `integration_design_data(1).zip`, extraído sin modificar el original en un directorio de trabajo separado.
- Snapshot exclusivo de `gpc-05-hipertension-embarazo-2025`.
- `flowcharts.json`, `recommendations.json`, `tables.json`, `structure.json` y `bibliografia.json`.
- `decision_graphs.jsonl`, `semantic_segments.jsonl` y `clinical_knowledge_units.jsonl`, filtrados por `source_id` exacto.
- *Introduction to Algorithms*, 4.ª edición (2022), PDF local, capítulo 25.
- Rúbrica de `proyecto_final(1).pdf`: presentación de 15 minutos con teoría, análisis, aplicaciones, código, Colab y material extra.

## Hallazgos reproducibles

| Control | Observado | Baseline | Estado |
|---|---:|---:|---|
| Recomendaciones/BPC | 5 | 5 | Conforme |
| Tablas | 221 | 221 | Conforme |
| Flujogramas | 3 | 3 | Conforme |
| Segmentos Phase 4 | 30 | 30 | Conforme |
| Unidades de conocimiento Phase 4 | 269 | 269 | Conforme |
| Grafos de decisión Phase 4 | 3 | 3 | Conforme |

No se detectó `SOURCE_DRIFT` en los conteos base. Esto no convierte esos valores en constantes de software.

## Responsabilidad semántica

| Fuente | Rol primario en el proyecto | Regla de uso |
|---|---|---|
| `flowcharts.json` | Topología dirigida, nodos, transiciones y etiquetas | Fuente estructural primaria |
| `decision_graphs.jsonl` | Inicio, terminales derivados y representación normalizada | Fuente derivada; reconciliar, nunca duplicar |
| `recommendations.json` | Recomendaciones y BPC, con texto original y atributos GRADE | Autoridad textual para esos enunciados |
| `tables.json` | Factores, criterios y valores tabulados | Extraer solo estructuras verificables |
| `structure.json` | Secciones, páginas y contexto documental | Contextualización y procedencia |
| Phase 4 | Unidades auxiliares y trazabilidad | Integración auxiliar, siempre filtrada por guía |
| `bibliografia.json` | Metadatos bibliográficos de la guía | No constituye evidencia clínica inspeccionada |

## Inventario de flujogramas

| Flujo | Página GPC | Nodos | Aristas | Alcance | Decisión |
|---|---:|---:|---:|---|---|
| `flow_1` | 13 | 6 | 5 | Clínico-estructural | Incluir; auditar salida paralela `Sí` |
| `flow_2` | 14 | 9 | 7 | Clínico-estructural | Incluir; excluir `n9` de rutas alcanzables |
| `flow_3` | 22 | 8 | 8 | Metodología de evidencia | Excluir del caso clínico; conservar en auditoría |

## Reconciliación preliminar

Para los tres flujos, Phase 4 conserva los mismos identificadores, textos, tipos, nodos y aristas que la fuente primaria. Phase 4 añade `start_node_id`, `terminal_node_ids`, `knowledge_unit_ids`, `traceability` y `route_templates`. Los `route_templates` están vacíos.

La equivalencia estructural no resuelve dos decisiones semánticas:

1. En `flow_1`, las dos aristas `Sí` de `n1` activan ramas paralelas; se modelarán como `AND` por la advertencia explícita de la fuente.
2. En `flow_2`, Phase 4 enumera `n9` como terminal por grado de salida cero, pero la fuente lo marca como nota técnica aislada; no será terminal clínico ni parte de una firma alcanzable.

## Propuesta del modelo canónico

Los adaptadores producirán objetos inmutables y tipados para `SourceReference`, `ClinicalNode`, `ClinicalTransition`, `ClinicalDecisionGraph`, `ClinicalRecommendation`, `ClinicalCriterion`, `ExecutionSignature`, `EvidenceCrosswalk`, `ScenarioTemplate`, `CoverageTarget` y `CompatibilityDecision`.

Los diccionarios JSON no circularán más allá de los adaptadores. Todo objeto conservará `source_id`, ruta relativa, entidad, página/sección y SHA-256.

## Propuesta de crosswalk

El crosswalk inicial se limitará a relaciones por identificadores y estructura explícita:

| Regla | Grafo | Recomendación | Tabla | Estado inicial |
|---|---|---|---|---|
| Prevención AAS | `flow_1:n3,n5` | `rec_1` | `table_003` | Sustentada |
| Prevención calcio | `flow_1:n4,n6` | `rec_2` | `table_003` | Sustentada |
| Ruta sin severidad | `flow_2:n5,n7` | `bpc_1` | - | Sustentada |
| Ruta con severidad | `flow_2:n6,n8` | `bpc_2` | - | Sustentada |
| No brindar antihipertensivos | sin acción gráfica explícita | `rec_3` | `table_003` | Objetivo válido, compatibilidad no demostrada |

No se aprobará ninguna relación por similitud textual.

## Formulación final de U, V y E

Sea `B = (U, V, E)` un grafo bipartito no dirigido:

- `U`: plantillas simbólicas generadas determinísticamente desde firmas alcanzables y criterios explícitos. Incluye un escenario por factor de riesgo alto, combinaciones sin reemplazo de dos factores moderados, la ausencia explícita de factores, la rama de presión no elevada, la rama sin criterios y un escenario por criterio de severidad enumerado.
- `V`: obligaciones atómicas o paquetes de evidencia: factores, resultados de decisión, acciones, recomendaciones y BPC deduplicadas.
- `(u,v) in E`: solo si todos los predicados requeridos por `v` están en `u`, no existe predicado prohibido, las acciones esperadas están activadas, ambos estados son válidos, las entidades pertenecen a la misma guía y la procedencia puede reconstruirse.

El matching maximiza el número de objetivos que reciben representantes distintos. No minimiza el número de escenarios; esa es una pregunta de *set cover*.

## Arquitectura de pipelines

1. **Ingesta:** adaptadores por responsabilidad semántica.
2. **Validación:** contratos, endpoints, alcance, ciclos, terminales y procedencia.
3. **Reconciliación:** fuente primaria frente a Phase 4.
4. **Integración:** firmas, criterios y crosswalk explícito.
5. **Construcción:** `U`, `V`, decisiones de compatibilidad y `E`.
6. **Solver:** DFS aumentante y Hopcroft-Karp, desacoplados del dominio.
7. **Verificación:** búsqueda exhaustiva y NetworkX solo como oráculos.
8. **Reporte:** métricas, visualizaciones, evidencia y limitaciones.

## Riesgos de evidencia

- `table_002` concatena contenido complejo; `table_003` ofrece una estructura más explícita para los factores de riesgo y será la tabla primaria para esa extracción.
- `rec_3` no presenta una acción equivalente explícita en el flujograma: debe permanecer sin arista si el escenario no demuestra esa acción.
- `flow_1` exige semántica paralela; tratarlo como XOR eliminaría una acción sustentada.
- `flow_2:n9` es informativo y aislado; incluirlo como ruta fabricaría alcanzabilidad.
- Los 221 objetos de tabla no son 221 criterios clínicos; se seleccionarán por reglas de inclusión documentadas.
- El PDF del libro fue generado por Calibre y no expone de forma visible la paginación impresa en todas las páginas. Las citas usarán sección y número de página PDF, distinguiéndolo explícitamente.

## Plan por cortes verticales

1. Inventario, hashes y contratos.
2. Modelos canónicos y adaptadores.
3. Reconciliación y semántica dirigida.
4. Firmas de ejecución.
5. Recomendaciones, criterios y crosswalk.
6. Escenarios, objetivos y compatibilidad.
7. Grafo bipartito y baseline DFS.
8. Hopcroft-Karp e instrumentación.
9. Oráculos, propiedades y benchmarks.
10. Colab, visualizaciones, documentación y presentación.

## Preguntas estrictamente bloqueantes

No hay una decisión clínica bloqueante para el corte algorítmico. La publicación en GitHub requiere preservar la prohibición de escribir directamente en `main`; dado que el repositorio está vacío, el paquete puede completarse localmente y la inicialización pública debe tratarse como una decisión de publicación separada.

## Estado de gates

- [x] Capítulo 25 localizado y hash calculado.
- [x] Estructura y conteos inspeccionados.
- [x] Fuente clínica restringida a una guía.
- [x] Riesgos de trazabilidad documentados.
- [ ] Correctitud algorítmica: pendiente de implementación.
- [ ] Pruebas: pendiente de implementación.
- [ ] Documentación final: pendiente de validación cruzada.
- [ ] Reproducibilidad completa: pendiente de pipeline ejecutable.

## Recomendación de cierre de la iteración

Usar `flowcharts.json` como topología primaria; `decision_graphs.jsonl` como derivado reconciliado; recomendaciones, `table_003` y `structure.json` como fuentes complementarias; excluir `flow_3`, `outputs/pilot_30` y toda guía distinta. Enviar `flow_1` a semántica `AND`, bloquear `flow_2:n9` como ruta y comenzar el siguiente corte con modelos canónicos, manifiestos verificables y validadores de procedencia.

