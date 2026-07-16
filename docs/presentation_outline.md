# Guion de presentación KISS — 15 minutos

## Trabajo de comunicación

Al terminar, los compañeros deben comprender que un grafo bipartito puede
asignar casos distintos a objetivos distintos, demostrar la cobertura máxima y
convertir una brecha curricular en una decisión de diseño.

## Narrativa principal

| # | Tiempo | Título | Trabajo de la diapositiva | Evidencia |
|---:|---:|---|---|---|
| 1 | 0:50 | Siete casos para ocho objetivos: ¿alcanza? | presentar tensión, pregunta, GOAL y límite no clínico | GPC + pregunta |
| 2 | 1:25 | Los casos y los objetivos forman dos grupos | definir `U`, `V` y una arista | subgrafo KISS |
| 3 | 1:25 | Cada caso se asigna una sola vez | matching, máximo vs. maximal y restricciones | CLRS cap. 25 |
| 4 | 1:35 | Reasignar puede aumentar la cobertura | mostrar un camino aumentante de 1 a 2 pares | Berge/CLRS |
| 5 | 1:35 | Hopcroft-Karp encuentra varios aumentos por fase | BFS, DFS admisible y `O(E√V)` | CLRS/HK 1973 |
| 6 | 2:25 | Siete casos no pueden cubrir ocho objetivos uno-a-uno | visualizar `7/8/14`, matching 7 y Hall `8>7` | código + fuente |
| 7 | 2:05 | El Colab reproduce el óptimo: `M*=7` | ejecutar demo autónomo y dos solvers | tests/reporte |
| 8 | 1:50 | El grafo convierte una brecha en una decisión educativa | añadir un caso o cambiar de modelo; conectar literatura | síntesis científica |
| 9 | 1:10 | El resultado es estructural, no clínico | resolver la pregunta, estado de validez y referencias | matriz de validez |
|  | **14:20** |  | 40 segundos de contingencia |  |

## Contenido visible por diapositiva

### 1. Siete casos para ocho objetivos: ¿alcanza?

- Pregunta oral: “Tenemos 7 casos y 8 objetivos. ¿Cómo cubrir tantos como sea
  posible sin reutilizar un caso?”
- GOAL: maximizar objetivos distintos representados por casos distintos.
- Alcance: diseño educativo derivado de una GPC; no decisiones sobre pacientes.

### 2. Los casos y los objetivos forman dos grupos

- Izquierda `U`: casos `C1...C7`.
- Derecha `V`: objetivos `O1...O7` y `O_BPC`.
- Arista: el caso puede ser representante principal del objetivo bajo la regla.
- Frase clave: “compatible” no significa “clínicamente validado”.

### 3. Cada caso se asigna una sola vez

\[
\max\sum_{(u,v)\in E}x_{uv}
\]

con restricciones de grado seleccionadas `≤1` en ambos lados.

- matching: asignación válida;
- maximal: no puede añadirse una arista localmente;
- máximo: tiene cardinalidad global óptima.

### 4. Reasignar puede aumentar la cobertura

Mostrar un ejemplo de dos casos y dos objetivos:

```text
antes:   C1—O1       C2 libre, O2 libre
camino:  C2—O1—C1—O2
después: C2—O1       C1—O2
```

La diferencia simétrica aumenta `|M|` en uno.

### 5. Hopcroft-Karp encuentra varios aumentos por fase

1. BFS construye capas de caminos aumentantes mínimos.
2. DFS usa solo aristas admisibles.
3. Se aplican caminos disjuntos en la misma fase.

Complejidad: `O(E√V)`; espacio `O(V+E)`.

### 6. Siete casos no pueden cubrir ocho objetivos uno-a-uno

Visual central:

- siete casos abreviados: PA, plaquetas, hígado, riñón, pulmón,
  neuro/visual, útero-placentario;
- ocho objetivos: siete criterios + BPC;
- cada caso se conecta con su objetivo y con BPC;
- siete aristas de matching resaltadas;
- un objetivo sin representante.

Prueba:

```text
|U|=7 |V|=8 |E|=14 |M*|=7
Hall: |S|=8 > |N(S)|=7
```

### 7. El Colab reproduce el óptimo: `M*=7`

Código visible máximo de 8 a 10 líneas y salida:

```text
PASS |U|=7 |V|=8 |E|=14 |M*|=7
agreement dfs=7 hopcroft_karp=7
```

LOOP en notas: definir → construir → resolver → verificar → interpretar →
repetir.

### 8. El grafo convierte una brecha en una decisión educativa

- Opción A: añadir un octavo caso independiente.
- Opción B: permitir varios objetivos por caso y usar otro modelo.
- Literatura: las GPC ya se modelan como grafos y las simulaciones escalan la
  práctica; esta propuesta añade una capa de curación óptima y explicable.
- Novedad calibrada: combinación potencialmente poco explorada; validación
  experta pendiente.

### 9. El resultado es estructural, no clínico

Respuesta final:

> Siete casos cubren como máximo siete de ocho microobjetivos bajo unicidad; el
> grafo demuestra la brecha y orienta una acción de diseño.

Estado:

- algoritmo: validado;
- fundamento científico: documentado;
- contenido clínico y efecto educativo: por validar prospectivamente.

Referencias visibles mínimas: CLRS cap. 25; Hopcroft y Karp (1973); Kandula y
Bhattacharyya (2023); Gupta et al. (2025); MedSimAI (2025/2026).

## Demo funcional

```bash
python scripts/run_kiss_severity_case.py
```

El notebook `notebooks/research_var_cases_kiss.ipynb` no requiere subir el ZIP.
El pipeline completo queda en anexo.

## Preguntas probables

- **¿Por qué 7 es máximo?** Hay solución de 7 y solo existen 7 casos; Hall da
  `8>7`.
- **¿Cuál objetivo queda fuera?** El matching no ponderado no prioriza; cualquier
  óptimo puede dejar uno distinto.
- **¿Un caso no puede enseñar dos cosas?** Sí. La unicidad es una política para
  representantes independientes; sin ella usaríamos cobertura o `b`-matching.
- **¿La GPC trae objetivos de aprendizaje?** No. Son microobjetivos diseñados y
  deben validarse por expertos.
- **¿Está clínicamente validado?** No. Está validado como algoritmo y tiene un
  protocolo prospectivo de contenido y utilidad educativa.
- **¿Es novedoso?** La combinación exacta no apareció en la revisión dirigida;
  se presenta como potencialmente novedosa, no como “primera mundial”.

## Corte si falta tiempo

1. En la diapositiva 4, explicar una sola inversión del camino.
2. En la diapositiva 5, decir la cota sin derivarla.
3. En la diapositiva 8, mostrar solo dos antecedentes y remitir al informe.
4. Proteger la diapositiva 6 y la conclusión.
