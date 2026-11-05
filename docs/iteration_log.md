# Registro del LOOP

## Iteración 0 — Inspección exclusiva

### Objetivo

Congelar alcance, fuentes, rúbrica y teoría antes de programar.

### Evidencia inspeccionada

- prompt operativo del proyecto;
- `proyecto_final(1).pdf`, una página;
- CLRS cuarta edición, capítulo 25, páginas impresas 704-743 / PDF 911-963;
- snapshot canónico, Phase 4 multiguía y mapa de variantes.

### Cambios

- formulación inicial;
- manifiestos de hashes;
- auditoría de fuente, reconciliación y semántica;
- arquitectura del pipeline.

### Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| extracción y conteo JSON/JSONL | 453 JSON canónicos parseables; baseline reconciliado |
| SHA-256 | 8 archivos fijados |
| inspección PDF | capítulo y rúbrica registrados |

### Validación de afirmaciones

| Claim | Fuente | Estado |
|---|---|---|
| Cap. 25 contiene HK y `O(E√V)` | CLRS §25.1 | verificado |
| Presentación dura 15 min | proyecto final p. 1 | verificado |
| Variante resumida es `draft` | mapa Phase 4 | verificado/excluido |

### Riesgos o bloqueos

- IDs de nodo repetidos entre flujos;
- `n9` aislado;
- doble rama `Sí`;
- Phase 4 multiguía.

### Estado de gates

- [x] Capítulo 25
- [x] Estructura
- [ ] Correctitud algorítmica
- [x] Fuente clínica
- [x] Trazabilidad
- [ ] Pruebas
- [ ] Documentación
- [ ] Reproducibilidad

### Siguiente corte vertical

Modelos, adaptadores y reconciliación ejecutable.

## Iteración 1 — Fuente a modelo canónico

### Objetivo

Construir contratos tipados y rechazar drift, mezcla o conflicto.

### Evidencia inspeccionada

- cinco agregados canónicos;
- tres archivos Phase 4;
- advertencias de `flow_1` y `flow_2`.

### Cambios

- dataclasses de dominio y procedencia;
- adaptadores por artefacto;
- comparación de flujos primario/derivado;
- alcanzabilidad, terminales, ciclos y aislados.

### Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| `scripts/validate_sources.py` | PASS |
| reconciliación 3 flujos | 0 diferencias |

### Validación de afirmaciones

| Claim | Fuente | Estado |
|---|---|---|
| `flow_1` tiene 6/5 | fuente + Phase 4 | verificado |
| `flow_2:n9` es aislado | fuente + alcanzabilidad | verificado |
| `flow_3` es metodológico | contenido y estructura | excluido de demo |

### Riesgos o bloqueos

- `route_templates` vacío exige reglas locales explícitas.

### Estado de gates

- [x] Capítulo 25
- [x] Estructura
- [ ] Correctitud algorítmica
- [x] Fuente clínica
- [x] Trazabilidad
- [x] Pruebas de fuente
- [ ] Documentación final
- [ ] Reproducibilidad final

### Siguiente corte vertical

Firmas, crosswalk, `U`, `V` y `E_B`.

## Iteración 2 — Integración y grafo bipartito

### Objetivo

Transformar evidencia reconciliada en un grafo explicable.

### Evidencia inspeccionada

- `table_003`;
- cinco recomendaciones/BPC;
- nodos y acciones de `flow_1` y `flow_2`.

### Cambios

- cinco firmas de ejecución;
- 22 criterios de riesgo y 7 de severidad;
- cinco crosswalks;
- 75 escenarios y 35 objetivos;
- 2.625 decisiones, 267 aprobadas.

### Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| pipeline de integración | PASS, conteos deterministas |
| procedencia | todas las entidades con fuente objetivo |
| `rec_3` | 75/75 pares rechazados |

### Validación de afirmaciones

| Claim | Fuente | Estado |
|---|---|---|
| `|U|=75` | reglas combinatorias | verificado |
| `|V|=35` | builder deduplicado | verificado |
| `|E_B|=267` | regla de compatibilidad | verificado |

### Riesgos o bloqueos

- un objetivo aislado es resultado válido, no error a completar.

### Estado de gates

- [x] Capítulo 25
- [x] Estructura
- [ ] Correctitud algorítmica final
- [x] Fuente clínica
- [x] Trazabilidad
- [x] Pruebas de integración
- [ ] Documentación final
- [ ] Reproducibilidad final

### Siguiente corte vertical

Solvers, oráculos, certificados y benchmarks.

## Iteración 3 — Correctitud y experimentos

### Objetivo

Demostrar cardinalidad, explicar déficits y medir sin sobreinterpretar.

### Evidencia inspeccionada

- CLRS §25.1;
- artículos de Berge y Hopcroft–Karp;
- resultados instrumentados.

### Cambios

- DFS aumentante y Hopcroft–Karp propios;
- oráculos exhaustivo y NetworkX;
- testigos de Hall;
- fixtures escalera y completo;
- protocolo de 21 repeticiones.

### Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| `pytest -q` | 29 passed |
| universo `≤3×3` | 689/689 concordantes |
| `ruff check` | PASS |
| `mypy` | PASS |
| pipeline demo | `75,35,267,33` |

### Validación de afirmaciones

| Claim | Fuente | Estado |
|---|---|---|
| `|M*|=33` | dos solvers + NetworkX + Hall | verificado |
| déficit `1>0` | grafo derivado | verificado |
| déficit `8>7` | grafo derivado | verificado |
| HK reduce revisitas en escalera | 21 repeticiones + escaneos | verificado localmente |

### Riesgos o bloqueos

- tiempos dependientes de entorno;
- no hacer inferencia clínica ni de hardware.

### Estado de gates

- [x] Capítulo 25
- [x] Estructura
- [x] Correctitud algorítmica
- [x] Fuente clínica
- [x] Trazabilidad
- [x] Pruebas
- [ ] Documentación final
- [ ] Reproducibilidad de entrega

### Siguiente corte vertical

Colab, PPT, material extra y QA completo.

## Iteración 4 — Entrega y revisión

### Objetivo

Cerrar la rúbrica del curso y registrar el estado final verificable.

### Evidencia inspeccionada

- requisitos de 15 minutos;
- matriz teoría–código–prueba–diapositiva;
- checklist de Definition of Done.

### Cambios

- notebook Colab;
- documentación académica y pedagógica;
- presentación de 10 diapositivas con notas;
- material extra de una página;
- paquete reproducible.

### Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| `scripts/validate_project.py` | PASS: formato, lint, tipos, 29 tests y pipeline |
| smoke del notebook | PASS: 15/15 celdas de código |
| `slides_test.py` | PASS: 10 slides, sin overflow |
| inspección visual de slides | 10/10 a tamaño completo |
| `pdfinfo` + render del material extra | PASS: 1 página A4, inspeccionada |

### Validación de afirmaciones

Todas las afirmaciones principales se registran en `evidence_matrix.csv`.

### Riesgos o bloqueos

- publicación remota depende de la política de rama y revisión humana.

### Estado de gates

- [x] Capítulo 25
- [x] Estructura
- [x] Correctitud algorítmica
- [x] Fuente clínica
- [x] Trazabilidad
- [x] Pruebas
- [x] Documentación
- [x] Reproducibilidad de entrega

### Siguiente corte vertical

Revisión humana y Pull Request desde la rama de trabajo.
