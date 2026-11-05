# Validación académica y científica

## Resumen ejecutivo

El producto está validado como **demostración educativa de ingeniería algorítmica reproducible**, no como herramienta clínica. La afirmación central es limitada y verificable: dada una fuente local fijada por hash y una regla explícita de compatibilidad, las implementaciones propias calculan un matching máximo de cardinalidad 33 sobre un grafo bipartito de 75 escenarios, 35 objetivos y 267 aristas.

La validación combina teoría, certificados estructurales, oráculos independientes, pruebas exhaustivas, auditoría de procedencia y medición reproducible. No evalúa la corrección médica de la guía, la efectividad de intervenciones, resultados en pacientes ni validez externa.

## Objeto y alcance de la validación

| Objeto | Pregunta | Evidencia | Alcance del veredicto |
|---|---|---|---|
| Fuente | ¿Se usó el snapshot correcto? | 8 SHA-256, IDs y conteos | Integridad del snapshot local |
| Semántica | ¿Las rutas usadas son alcanzables y respaldadas? | reconciliación, warnings, tests | Modelo estructural declarado |
| Construcción | ¿`U`, `V` y `E_B` siguen reglas explícitas? | reglas versionadas y procedencia | Reproducibilidad del grafo |
| Algoritmo | ¿El resultado es un matching máximo? | teorema de caminos aumentantes, Hall, oráculos | Correctitud para entradas probadas y demo |
| Experimento | ¿Las métricas son regenerables? | protocolo, resultados crudos, ambiente | Descripción local del runtime |
| Comunicación | ¿Se respetan alcance y rúbrica? | notebook, PPT, material extra | Entrega académica de 15 minutos |

## Validez matemática

### Definición correcta del estimando computacional

El “estimando” aquí no es estadístico. Es la función determinista:

\[
\theta(B)=\max_{M\subseteq E_B}\{|M|:M\text{ es matching}\}.
\]

Fijados los bytes de la fuente y la versión de reglas, `B` y `θ(B)` quedan determinados. El resultado `θ(B)=33` no tiene intervalo de confianza porque no proviene de una muestra aleatoria.

### Correctitud del solver

El criterio de Berge, desarrollado en CLRS §25.1, establece que un matching es máximo si y solo si no existe un camino aumentante. El baseline busca aumentos uno por uno. Hopcroft–Karp agrupa caminos aumentantes más cortos por capas BFS y DFS admisible; el Teorema 25.8 de CLRS sustenta la cota clásica `O(m√n)`.

La implementación usa `L=U`, `R=V`, `n=|L|+|R|` y `m=|E_B|`. Los vértices aislados se conservan, por lo que la inicialización explícita añade `O(n)`.

### Certificado específico del demo

El matching de 33 pares es una cota inferior. Dos testigos de Hall aportan una cota superior:

- objetivo `rec_3`: `|S|=1>|N(S)|=0`;
- grupo de severidad/BPC: `|S|=8>|N(S)|=7`.

Los componentes son disjuntos; el déficit total es 2. Por tanto, como `|V|=35`, cualquier matching tiene cardinalidad a lo sumo 33. La solución factible de 33 alcanza esa cota: es máxima.

Este argumento es más fuerte que reportar únicamente concordancia de software, porque explica *por qué* quedan dos objetivos sin cubrir.

## Validez computacional

### Triangulación de oráculos

Se verificaron 689 grafos etiquetados con `|L|,|R|≤3`. Para cada uno se compararon:

1. enumeración exhaustiva propia;
2. DFS aumentante propio;
3. Hopcroft–Karp propio;
4. cardinalidad de NetworkX.

Todas las cardinalidades coincidieron. Se validaron además entradas vacías, aisladas, desconectadas, desbalanceadas, duplicadas o inválidas. Las 29 pruebas actuales pasan junto con `ruff` y `mypy`.

La exhaustividad es sobre ese espacio finito de grafos pequeños; no constituye una prueba formal universal del código, pero reduce el riesgo de fallos de bordes y complementa el argumento algorítmico.

### Separación de responsabilidades

Los solvers reciben únicamente IDs y adyacencia; no importan módulos clínicos. Los adaptadores no ejecutan matching. Las reglas de compatibilidad son puras, versionadas y producen explicación tanto al aprobar como al rechazar. NetworkX solo aparece en `matching/oracles.py` y en pruebas/benchmarks.

## Validez de datos y procedencia

Los cinco agregados primarios y tres archivos Phase 4 se fijan por SHA-256. Los agregados contienen 5 recomendaciones/BPC, 221 tablas y 3 flujos. Tras filtrar Phase 4 por ID exacto se observan 30 segmentos, 269 unidades y 3 grafos.

La reconciliación entre `flowcharts.json` y `decision_graphs.jsonl` no encontró nodos, aristas, textos, páginas o secciones modificados. Los elementos derivados conservan archivo local, entidad, página/sección y hash. La variante resumida y las demás guías se excluyen.

Conforme a los principios FAIR, la trazabilidad favorece que los resultados sean encontrables y reutilizables en su contexto; no convierte por sí misma el contenido en clínicamente válido. FAIR se usa aquí como principio de gestión de objetos digitales, no como sello de calidad médica.

## Resultados reproducibles

### Grafo derivado de la GPC

| Métrica | Resultado |
|---|---:|
| `|U|` escenarios | 75 |
| `|V|` objetivos | 35 |
| `|E_B|` compatibilidades | 267 |
| densidad | 0,101714 |
| componentes, incluidos aislados | 6 |
| objetivos aislados | 1 |
| matching máximo | 33 |
| cobertura uno-a-uno de objetivos | 94,2857 % |
| escenarios no usados | 42 |
| objetivos no cubiertos | 2 |

“Cobertura” significa proporción de objetivos con representante único en `M`: no es exactitud, sensibilidad, adherencia clínica ni cobertura poblacional.

### Instrumentación del demo, 21 repeticiones

| Algoritmo | Mediana | Q1–Q3 | Escaneos | Llamadas DFS | Fases BFS | Pico trazado aprox. |
|---|---:|---:|---:|---:|---:|---:|
| DFS aumentante | 154,083 μs | 148,564–171,449 μs | 1.755 | 483 | 0 | 13.712 B |
| Hopcroft–Karp | 150,086 μs | 145,209–154,622 μs | 1.191 | 132 | 2 | 15.592 B |

La diferencia de tiempo es pequeña y no se interpreta inferencialmente. En esta instancia domina el tamaño reducido; la ventaja conceptual de Hopcroft–Karp aparece con mayor claridad en familias escalables.

### Fixture matemático escalera

| Tamaño por lado | DFS mediana | HK mediana | DFS escaneos | HK escaneos |
|---:|---:|---:|---:|---:|
| 32 | 0,125 ms | 0,032 ms | 1.024 | 126 |
| 128 | 2,085 ms | 0,124 ms | 16.384 | 510 |
| 512 | 37,977 ms | 0,545 ms | 262.144 | 2.046 |

Para `k=512`, la reducción observada es aproximadamente 69,6 veces en mediana y 128,1 veces en escaneos. Es un caso determinista construido para mostrar revisitas del DFS; no es una distribución representativa de grafos reales.

## Validez interna, externa y de constructo

### Validez interna

Fortalezas:

- hashes y conteos bloquean drift accidental;
- transformaciones puras y ordenadas;
- reconciliación evita doble ingestión;
- oráculos independientes y testigos de Hall;
- reglas de exclusión explícitas;
- ninguna aleatoriedad oculta.

Amenazas residuales:

- una regla versionada podría ser conceptualmente discutible aun si está bien implementada;
- los contratos se infieren del snapshot porque no todos los agregados traen esquema formal;
- las pruebas exhaustivas cubren grafos pequeños, no todos los tamaños;
- el microbenchmark depende de intérprete, carga y hardware.

### Validez de constructo

El constructo medido es “cobertura uno-a-uno bajo compatibilidad demostrable”. No equivale a importancia, completitud clínica ni utilidad pedagógica subjetiva. La restricción uno-a-uno deliberadamente hace competir objetivos que un mismo escenario podría ilustrar simultáneamente; esa propiedad responde al problema de matching y no a *set cover*.

### Validez externa

No se generaliza a otras GPC, versiones, idiomas, formatos, poblaciones ni sistemas de salud. Una nueva guía requiere nuevos adaptadores, reconciliación y reglas. El desempeño temporal no se extrapola fuera del ambiente registrado.

## Validez científica y responsabilidad

La contribución es metodológica: muestra cómo separar evidencia fuente, modelado y solver; cómo conservar procedencia; y cómo certificar un déficit de cobertura. No produce nuevo conocimiento clínico ni prueba una hipótesis epidemiológica.

Las afirmaciones se clasifican en `docs/evidence_matrix.csv` como teóricas, de fuente, computacionales, experimentales o de alcance. Las afirmaciones experimentales se acompañan de protocolo y archivo de resultados crudos. Las afirmaciones sin soporte explícito se bloquean o quedan en revisión.

## Reproducibilidad y auditabilidad

Un revisor puede:

1. verificar hashes con `validate_sources.py`;
2. ejecutar el pipeline completo;
3. reproducir los 29 tests y los 689 grafos exhaustivos;
4. regenerar benchmarks con 21 repeticiones;
5. inspeccionar las decisiones de compatibilidad y sus referencias;
6. confirmar cardinalidad con NetworkX;
7. revisar los dos testigos de Hall;
8. comparar las salidas JSON deterministas.

La reproducibilidad exige acceso autorizado a la fuente local; el ZIP no se distribuye dentro del repositorio.

## Veredicto

Los gates de teoría, estructura, algoritmo, procedencia y experimento están satisfechos para el alcance educativo declarado. El resultado es defendible en una maestría de ingeniería estadística porque combina formalización, control de datos, pruebas exhaustivas, análisis de complejidad, medición y límites de inferencia. Cualquier uso clínico permanece explícitamente fuera de alcance.
