# Formulación matemática

## Problema

La pregunta computacional es: ¿cómo asignar escenarios simbólicos, trazables y distintos al máximo número de obligaciones de cobertura derivadas de una única GPC?

## Dos grafos, dos significados

El grafo dirigido clínico-estructural es `D=(N,A)`. Conserva decisiones, acciones y transiciones. No es automáticamente bipartito.

El grafo de cobertura es `B=(U,V,E)`:

- `U`: escenarios candidatos simbólicos.
- `V`: obligaciones de cobertura atómicas o paquetes deduplicados.
- `E`: compatibilidades demostradas.

## Función de compatibilidad

Para un escenario `u` y un objetivo `v`, sea:

\[
c(u,v)=\mathbf{1}\{R_v\subseteq P_u\}\,
\mathbf{1}\{F_v\cap P_u=\varnothing\}\,
\mathbf{1}\{A_v\subseteq A_u\}\,
\mathbf{1}\{s_u=s_v=\text{validated}\}\,
\mathbf{1}\{g_u=g_v=g^*\}\,
\mathbf{1}\{\rho(u,v)=1\},
\]

donde `P_u` son predicados del escenario, `R_v` los requeridos, `F_v` los prohibidos, `A_u` las acciones activadas, `A_v` las esperadas, `g*` la guía autorizada y `rho` la existencia de procedencia verificable. Entonces:

\[
E=\{(u,v)\in U\times V: c(u,v)=1\}.
\]

## Matching

Un matching `M subseteq E` satisface:

\[
\sum_{v:(u,v)\in E}x_{uv}\le 1 \quad \forall u\in U,
\qquad
\sum_{u:(u,v)\in E}x_{uv}\le 1 \quad \forall v\in V,
\]

con `x_uv in {0,1}` y objetivo:

\[
\max\ |M|=\max\sum_{(u,v)\in E}x_{uv}.
\]

Un matching es **maximal** si no admite otra arista sin violar las restricciones; es **máximo** si su cardinalidad es globalmente óptima; es **perfecto** si cubre todos los vértices. Una asignación ponderada optimiza una suma de pesos y no es el problema básico.

## Camino aumentante y optimalidad

Respecto a `M`, un camino alternante alterna aristas fuera y dentro de `M`. Es aumentante si inicia y termina en vértices libres. La diferencia simétrica con ese camino incrementa la cardinalidad en uno. Por el criterio de Berge presentado en CLRS, `M` es máximo si y solo si no existe camino aumentante.

## Límites

El modelo responde cuántos objetivos reciben representantes distintos. No encuentra el mínimo conjunto de escenarios que cubre todos los objetivos; esa formulación corresponde a *set cover*. El resultado no asigna pacientes ni prescribe acciones.

