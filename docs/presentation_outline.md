# Guion de presentación — 15 minutos

La presentación principal tiene 10 diapositivas y 14:30 de contenido, con 0:30 de contingencia. El notebook y el material extra quedan disponibles para preguntas.

| # | Tiempo | Título | Mensaje defendible | Visual | Evidencia |
|---:|---:|---|---|---|---|
| 1 | 0:45 | Cobertura máxima, evidencia intacta | Goal y alcance no clínico | título + dos particiones | rúbrica, formulación |
| 2 | 1:00 | Del Capítulo 25 al software verificable | teoría→código→prueba | matriz de trazabilidad | CLRS §25.1 |
| 3 | 1:15 | Una fuente, ocho hashes, cero mezclas | control de fuente y conteos | embudo de auditoría | manifiesto, reconciliación |
| 4 | 1:20 | Dos grafos; dos preguntas | `D` no es `B` | flujo dirigido + bipartito | auditoría semántica |
| 5 | 1:15 | Pipeline con LOOP y gates | cada transformación puede bloquear | pipeline + rail LOOP | arquitectura |
| 6 | 1:30 | El problema matemático | maximizar asignación uno-a-uno | fórmula + conteos 75/35/267 | metodología |
| 7 | 1:45 | La reasignación que aumenta `|M|` | camino aumentante | antes/camino/después | CLRS, Berge |
| 8 | 1:45 | Hopcroft–Karp: caminos por capas | BFS+DFS y complejidad | capas + comparación | CLRS, código |
| 9 | 2:45 | Resultado: 33 y dos brechas explicadas | óptimo certificado, benchmark local | KPI, Hall, gráfico | resultados, tests |
| 10 | 1:10 | Máxima cobertura auditable | contribución y límites | síntesis | DoD |
|  | **14:30** |  |  |  |  |

## Apertura sugerida

> “El problema no es decidir qué hacer con una paciente. Es construir el máximo conjunto de pruebas distintas cuya cobertura pueda reconstruirse hasta la fuente.”

## Transiciones

- 1→2: “Para que ‘máximo’ sea una afirmación demostrable, llevé el Capítulo 25 hasta código y pruebas.”
- 2→3: “Pero un algoritmo correcto no compensa una fuente mezclada.”
- 3→4: “La primera decisión de modelado fue no confundir el flujo con el matching.”
- 4→5: “Esa separación organiza todo el pipeline.”
- 5→6: “Con los gates cerrados, el problema queda reducido a tres conjuntos.”
- 6→7: “La pieza local que permite mejorar una asignación es el camino aumentante.”
- 7→8: “Hopcroft–Karp acelera la idea agrupando aumentos mínimos por fases.”
- 8→9: “Ahora podemos interpretar el resultado con óptimo, no solo con una cifra.”
- 9→10: “La conclusión combina cobertura, explicación y límites.”

## Demo funcional

En la diapositiva 9 se ejecuta o muestra la salida ya preparada:

```text
PASS |U|=75 |V|=35 |E|=267 |M|=33 coverage=94.29%
```

Si hay conexión y tiempo, abrir el Colab en la celda “Pipeline completo”. Si no, usar la salida de la diapositiva y reservar el notebook para preguntas. No improvisar edición de fuente durante la exposición.

## Preguntas probables

- **¿Por qué 33 es máximo?** Solución factible 33 + dos testigos disjuntos de Hall con déficit total 2.
- **¿Por qué no 34?** Siete escenarios de severidad compiten por ocho objetivos relacionados.
- **¿Por qué no completar la recomendación aislada?** El gate de evidencia prohíbe inferir una acción no explícita.
- **¿NetworkX hizo el trabajo?** No; solo verifica cardinalidad. El demo usa dos implementaciones propias.
- **¿Es propensity-score matching?** No; no hay pacientes, covariables ni estimando causal.
- **¿94,3 % es una métrica clínica?** No; es cobertura combinatoria de objetivos construidos.

## Control de tiempo

Ensayar tres veces. Puntos de corte si se excede el tiempo:

1. En diapositiva 3, omitir el detalle de tamaños de archivo.
2. En diapositiva 7, explicar una sola inversión del camino.
3. En diapositiva 8, decir la cota sin desarrollar la prueba completa.
4. Proteger al menos 2:15 para resultados y conclusión.
