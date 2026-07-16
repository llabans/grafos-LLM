# Matching bipartito previo a generación sintética

## GOAL

Construir el mayor assignment_manifest.json uno-a-uno entre un catálogo finito
de estructuras de caso y variantes clínicas de una única GPC.

## Pipeline

    GPC → grafo dirigido → variantes
    esquema → estructuras
    estructuras × variantes → testigos → grafo bipartito
    matching → assignment_manifest.json

## Formulación

\[
\max\sum_{(u,v)\in E}x_{uv}
\]

sujeto a:

\[
\sum_vx_{uv}\leq1,\qquad
\sum_ux_{uv}\leq1,\qquad
x_{uv}\in\{0,1\}.
\]

## Demo reproducible

| \(|U|\) | \(|V|\) | \(|E|\) | \(|M^*|\) | déficit |
|---:|---:|---:|---:|---:|
| 7 | 8 | 14 | 7 | 1 |

Optimalidad:

- solución factible de siete;
- cota superior siete;
- Hall \(8>7\).

## Algoritmos

| Método | Idea | Tiempo |
|---|---|---:|
| baseline | un camino aumentante por búsqueda | \(O(|U|m)\) |
| Hopcroft-Karp | BFS por capas y DFS admisible | \(O(m\sqrt n)\) |

Pipeline:

\[
T_{\mathrm{routes}}+T_{\mathrm{structures}}+
O(|U||V|C_{\mathrm{compat}})+O(n+m\sqrt n).
\]

## Interpretación

Siete variantes pueden reservar estructuras independientes. La octava queda sin
entrada bajo capacidad uno. Esto no mide prevalencia ni realismo clínico.

## Validez

| Algorítmica | Estructural | Clínica | Generativa |
|---|---|---|---|
| solver y óptimo | rutas, aristas, testigos | panel y GPC | después de generar |

## Referencias

CLRS, cap. 25; Hopcroft y Karp (1973); Peleg et al. (2003); Boxwala et
al. (2004); Walonoski et al. (2018); Deng et al. (2026).
