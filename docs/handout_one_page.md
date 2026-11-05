# Matching bipartito auditable — ficha de apoyo

## Goal

Asignar escenarios simbólicos, distintos y trazables al máximo número de obligaciones de cobertura derivadas de una única GPC. Uso educativo; **no** diagnóstico, recomendación, priorización ni atención de casos.

## Modelo

- `D=(N,A)`: flujo dirigido; preserva decisiones, ramas, acciones y alcanzabilidad.
- `B=(U,V,E_B)`: `U` escenarios, `V` objetivos, `E_B` compatibilidades demostradas.
- Matching: cada escenario y cada objetivo se usan a lo sumo una vez.

\[
\max\sum x_{uv}\quad
\text{s.a.}\quad
\sum_v x_{uv}\le1,\;
\sum_u x_{uv}\le1,\;
x_{uv}\in\{0,1\}.
\]

## Resultado reproducible

| `|U|` | `|V|` | `|E_B|` | `|M*|` | Cobertura de objetivos |
|---:|---:|---:|---:|---:|
| 75 | 35 | 267 | 33 | 94,3 % |

**Dos déficits:**

1. evidencia: `1` objetivo y `0` vecinos;
2. capacidad: `8` objetivos y `7` escenarios vecinos.

Luego `|M|≤35-2=33`; el algoritmo construye 33. Óptimo certificado.

## Algoritmos

| Método | Idea | Tiempo | Demo: escaneos |
|---|---|---:|---:|
| DFS aumentante | un aumento por búsqueda | `O(nm)` | 1.755 |
| Hopcroft–Karp | BFS por capas + DFS admisible | `O(n+m√n)` con aislados | 1.191 |

Verificación: 29 tests; 689 grafos pequeños exhaustivos; DFS=HK=NetworkX en cardinalidad.

## Interpretación correcta

94,3 % es cobertura uno-a-uno de objetivos estructurados. No es accuracy, validez clínica, cobertura poblacional ni efecto causal. “Sin arista” significa compatibilidad no demostrada bajo la regla y fuente fijadas.

## LOOP

`INSPECT → PLAN → IMPLEMENT → VERIFY → EVIDENCE AUDIT → REVIEW → RECORD → repetir`

## Referencias esenciales

Cormen et al., *Introduction to Algorithms*, 4.ª ed., cap. 25; Hopcroft & Karp (1973), DOI `10.1137/0202019`; Berge (1957), DOI `10.1073/pnas.43.9.842`.
