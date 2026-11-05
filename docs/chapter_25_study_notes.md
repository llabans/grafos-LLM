# Notas verificadas del Capítulo 25

## Identificación

- Libro: Cormen, Leiserson, Rivest y Stein, *Introduction to Algorithms*.
- Edición: cuarta, 2022.
- Capítulo: 25, “Matchings in Bipartite Graphs”.
- Editorial: MIT Press. ISBN impreso `9780262046305`; ISBN electrónico `9780262367509`.
- Rango del capítulo: páginas impresas 704-743; páginas físicas PDF 911-963.
- Sección central: §25.1, páginas impresas 705-716; páginas PDF 912-927.
- El archivo es una remaquetación Calibre. Para que la cita sea reconstruible se informa siempre la pareja **página impresa / página PDF** cuando está disponible.

## Conceptos centrales

En las páginas impresas 704-705 / PDF 911-913 se define matching como un subconjunto de aristas sin vértices incidentes repetidos y se introduce el matching máximo por cardinalidad. La sección 25.1 distingue matching maximal de máximo y define caminos alternantes y aumentantes.

Las páginas impresas 706-708 / PDF 914-917 desarrollan la diferencia simétrica, el incremento de cardinalidad (Lema 25.1), el aumento mediante caminos disjuntos (Corolario 25.2), la estructura de la diferencia entre dos matchings (Lema 25.3) y el criterio de ausencia de caminos aumentantes (Corolario 25.4).

Las páginas impresas 708-715 / PDF 917-926 presentan Hopcroft--Karp: conjuntos maximales de caminos aumentantes más cortos y disjuntos, orientación del grafo, capas BFS, búsqueda DFS restringida, invariantes de longitud y el análisis que culmina en el Teorema 25.8 con tiempo `O(E sqrt(V))` bajo la notación del libro.

En la notación del proyecto, `L=U`, `R=V`, `X=L∪R`, `n=|X|` y `m=|E_B|`. La cota clásica se escribe `O(m√n)` sobre el grafo activo. Como la implementación admite listas explícitas de vértices aislados, se informa además una cota completa conservadora `O(n + m√n)` y espacio `O(n+m)`. Esta última precisión es análisis de ingeniería del proyecto, no una cita textual del libro.

## Adaptación del proyecto

El baseline DFS que aumenta un camino por iteración sigue la estrategia general descrita al final de la prueba del Corolario 25.4, pero su pseudocódigo concreto es una decisión de ingeniería del proyecto. La implementación Hopcroft-Karp usa la variante estándar con emparejamientos `pair_left`, `pair_right` y distancias por BFS; no reproduce literalmente la construcción material de `G_M`, `H` y `H^T`, pero mantiene el mismo principio de capas y DFS admisible.

## Secciones no centrales

- §25.2 (impresas 716-723 / PDF 927-936): matrimonio estable; se menciona solo para distinguir objetivos.
- §25.3 (impresas 723-739 / PDF 936-958, con ejercicios y problemas hasta PDF 962): asignación ponderada y algoritmo húngaro; se usa como contraste, no como solver.
- Notas (impresa 743 / PDF 962-963): atribución histórica a Hopcroft--Karp, Berge, Kuhn y otros.

## Política de cita

El archivo completo tiene SHA-256 `76c37e38a15e938dcff6a027aed03f09418423074b1a9ccdda027ba71a5d61a4`. Todas las paráfrasis indican sección y paginación dual; no se reproducen pasajes extensos.
