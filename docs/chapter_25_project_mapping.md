# Mapeo de CLRS, capítulo 25, al proyecto

La fuente algorítmica principal es Cormen, Leiserson, Rivest y Stein,
*Introduction to Algorithms*, cuarta edición, capítulo 25.

| Concepto CLRS | Referencia | Uso en el proyecto | Evidencia |
|---|---|---|---|
| grafo bipartito | apertura del capítulo 25 | \(U\) estructuras y \(V\) variantes | validación de particiones |
| matching | pp. impresas 704-705 | pares del manifiesto sin extremos repetidos | invariantes de salida |
| maximal frente a máximo | §25.1 | evitar detenerse en una solución local | oráculo de cardinalidad |
| camino alternante y aumentante | §25.1 | reasignación de pares | prueba del baseline |
| diferencia simétrica | Lema 25.1 | \(M\leftarrow M\oplus P\) | incremento en uno |
| caminos disjuntos | Corolario 25.2 | múltiples aumentos por fase | implementación HK |
| criterio de optimalidad | Corolario 25.4 | parar sin camino aumentante | certificado principal |
| BFS por capas | algoritmo Hopcroft-Karp | distancias alternantes | pruebas de capas |
| DFS admisible | algoritmo Hopcroft-Karp | caminos mínimos de la fase | pruebas de búsqueda |
| complejidad | Teorema 25.8 | \(O(m\sqrt n)\) | análisis |
| condición de Hall | ejercicio 25.1-5 | explicar déficit \(8>7\) | testigo secundario |

## Fuera del núcleo

- Matrimonio estable (§25.2): requiere rankings bilaterales; no corresponde.
- Matching de peso máximo (§25.3): relevante si se incorporan prioridades, pero
  no se implementa en la versión KISS.
- Set cover: responde a reutilización de estructuras y pertenece a otra familia
  de problemas.

## Correspondencia de notación

\[
L=U,\quad R=V,\quad n=|U|+|V|,\quad m=|E|.
\]

La cota de ingeniería del solver es \(O(n+m\sqrt n)\) al incluir
inicialización y vértices aislados. La cota central de Hopcroft-Karp en CLRS es
\(O(m\sqrt n)\).
