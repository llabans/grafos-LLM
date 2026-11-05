# Notas verificadas del capítulo 25

## Identificación

- Cormen, Leiserson, Rivest y Stein.
- *Introduction to Algorithms*, cuarta edición, 2022.
- Capítulo 25: “Matchings in Bipartite Graphs”.
- Rango aproximado: páginas impresas 704-743; PDF local 911-963.
- Sección central: §25.1, matching bipartito máximo.

## Definiciones

Para un grafo no dirigido \(G=(V,E)\), un matching \(M\subseteq E\) contiene a
lo sumo una arista incidente por vértice. Un matching **maximal** no admite una
arista adicional de manera local. Un matching **máximo** tiene la mayor
cardinalidad entre todos los matchings. Todo máximo es maximal, pero no al
revés.

En el proyecto, una arista seleccionada reserva una entrada del catálogo de
estructuras para una variante de ruta. La unicidad no es una propiedad médica:
es la capacidad unitaria del problema de asignación.

## Caminos aumentantes

Un camino \(M\)-alternante alterna aristas dentro y fuera de \(M\). Es
\(M\)-aumentante si sus extremos están libres. Por tener una arista no
emparejada adicional:

\[
M'=M\oplus P,\qquad |M'|=|M|+1.
\]

Este es el Lema 25.1. El Corolario 25.2 extiende el resultado a caminos
aumentantes disjuntos por vértices.

## Criterio principal de optimalidad

El Corolario 25.4 establece:

> \(M\) es máximo si y solo si no existe un camino \(M\)-aumentante.

Este es el certificado teórico principal del solver. La condición de Hall se
usa adicionalmente para explicar por qué no existe matching que sature todas
las variantes.

## Hopcroft-Karp

El algoritmo repite:

1. formar el digrafo alternante;
2. usar BFS para encontrar la longitud mínima de aumento;
3. obtener un conjunto maximal de caminos mínimos disjuntos mediante DFS
   admisible;
4. aplicar diferencia simétrica a todos;
5. terminar cuando el conjunto esté vacío.

CLRS demuestra que las longitudes mínimas aumentan entre fases y que el número
de fases es \(O(\sqrt n)\). Cada fase cuesta \(O(m)\), por lo que:

\[
T_{\mathrm{HK}}=O(m\sqrt n).
\]

La implementación práctica con arreglos de pares y distancias mantiene el
principio de capas aunque no materialice literalmente todos los grafos
intermedios de la exposición.

## Hall

El ejercicio 25.1-5 formula la condición:

\[
|A|\leq|N(A)|\quad\text{para todo }A\subseteq L
\]

como condición necesaria y suficiente de matching perfecto cuando las
particiones tienen el mismo tamaño. En la demo, se aplica al lado de las
variantes: ocho variantes comparten siete estructuras vecinas. El déficit uno
explica la imposibilidad de saturarlas.

## Complejidad del pipeline completo

CLRS analiza el solver, no la construcción clínica del grafo. En este proyecto:

\[
T_{\mathrm{total}}=
T_{\mathrm{routes}}+
T_{\mathrm{structures}}+
O(|U||V|C_{\mathrm{compat}})+
O(n+m\sqrt n).
\]

La evaluación de compatibilidad puede dominar el costo aun cuando el matching
sea eficiente.

## Secciones no utilizadas

- §25.2, matrimonio estable: no hay preferencias.
- §25.3, matching de peso máximo: no hay pesos en KISS.

## Política de cita

Se parafrasea la teoría y se cita capítulo, sección y resultado. No se
reproducen pasajes extensos del libro.
