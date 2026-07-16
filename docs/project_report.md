# Informe del proyecto final

## Título

**Emparejamiento bipartito máximo para cobertura auditable de datos estructurados de una GPC MINSA**

## Resumen

Se desarrolló una aplicación reproducible de matching máximo bipartito orientada a la curación y auditoría educativa de escenarios derivados de la GPC `gpc-05-hipertension-embarazo-2025`. El diseño separa el grafo dirigido de flujogramas del grafo bipartito de cobertura, reconcilia fuente primaria y Phase 4, conserva procedencia por entidad y construye compatibilidades únicamente mediante reglas explícitas.

El grafo final contiene 75 escenarios, 35 objetivos y 267 aristas. Dos implementaciones propias —DFS por caminos aumentantes y Hopcroft–Karp— obtienen cardinalidad 33 y coinciden con NetworkX. Dos testigos de Hall explican la imposibilidad de cubrir 35 objetivos: un objetivo aislado y un cuello de ocho objetivos con siete escenarios vecinos. La cobertura combinatoria es 94,3 %. El software supera lint, tipado y 29 pruebas, incluido el universo de 689 grafos etiquetados con particiones de hasta tres vértices.

## Introducción

Los pipelines de integración pueden producir grandes inventarios de elementos estructurados sin una garantía automática de diversidad o cobertura. Seleccionar manualmente ejemplos es difícil de auditar; usar similitud semántica sin controles puede introducir relaciones no sustentadas. El matching bipartito permite formalizar una asignación uno-a-uno entre escenarios candidatos y obligaciones de cobertura.

La aplicación es deliberadamente no clínica. Los términos de la guía se tratan como datos estructurados para estudiar algoritmos, trazabilidad y reproducibilidad.

## Objetivo

Maximizar el número de objetivos de cobertura que reciben un escenario distinto y compatible, preservando fuente, reglas y explicación para cada arista.

## Métodos

### Datos

Se auditaron cinco agregados canónicos y tres archivos Phase 4. Los hashes y conteos coinciden con el baseline. `flowcharts.json` es autoridad topológica; Phase 4 se usa como derivado reconciliado y se filtra por `source_id` exacto.

### Modelado

El grafo `D` conserva decisiones y alcanzabilidad. De él y de criterios explícitos se obtienen cinco firmas. Las reglas combinatorias generan `U`; los criterios, recomendaciones/BPC y resultados de decisión generan `V`. La compatibilidad exige predicados, acciones, estado, guía y procedencia.

### Algoritmos

Se implementaron desde cero un baseline DFS y Hopcroft–Karp. La teoría principal procede de CLRS, capítulo 25. NetworkX se reserva como oráculo.

### Validación

Se usaron pruebas unitarias, exhaustivas, de procedencia e integración; reconciliación de fuente; cardinalidad de oráculo; testigos de Hall; y microbenchmarks deterministas con 21 repeticiones.

## Resultados

| Etapa | Resultado |
|---|---:|
| flujos reconciliados | 3/3 |
| firmas de ejecución | 5 |
| criterios de riesgo | 22 |
| criterios de severidad | 7 |
| escenarios | 75 |
| objetivos | 35 |
| decisiones de pares | 2.625 |
| compatibilidades aprobadas | 267 |
| compatibilidades rechazadas | 2.358 |
| matching máximo | 33 |

El objetivo `rec_3` está aislado por ausencia de acción explícita compatible. El segundo déficit proviene de ocho objetivos con solo siete escenarios vecinos. La optimalidad se certifica por solución factible de 33 y cota superior de 33.

En el demo, las medianas de tiempo son aproximadamente 154 μs para DFS y 150 μs para Hopcroft–Karp. En el fixture escalera `k=512`, las medianas son aproximadamente 38,0 ms y 0,55 ms, respectivamente. La instrumentación confirma el mecanismo: 262.144 frente a 2.046 escaneos.

## Discusión

El hallazgo principal no es una cifra clínica, sino una distinción algorítmica: alta conectividad local no garantiza cobertura perfecta bajo unicidad. El grupo de severidad tiene aristas, pero posee déficit colectivo. Esto muestra por qué los grados individuales y la inspección visual no sustituyen un matching máximo ni un análisis de Hall.

La ausencia de arista de `rec_3` muestra el valor de la política conservadora: una afirmación no se completa por conocimiento externo. El pipeline conserva la brecha como resultado auditable.

La comparación experimental concuerda con la teoría sin sobreinterpretarla. En instancias pequeñas, la complejidad asintótica no necesariamente produce una diferencia temporal observable. Un fixture controlado permite aislar el patrón de revisitas del baseline.

## Conclusión

El proyecto cumple el objetivo de convertir una fuente estructurada fijada por hash en un problema de matching bien definido, resolverlo con algoritmos propios, certificar su óptimo y explicar las brechas. La arquitectura separa semántica, integración y solver; los resultados son reproducibles y su interpretación está limitada a cobertura educativa.

## Disponibilidad

El repositorio contiene código, pruebas, notebook Colab, documentación, matriz de evidencia, benchmarks y presentación. La fuente local no se incluye; debe configurarse mediante `BIPARTITE_MINSA_SOURCE_ROOT` y superar la validación de hashes.
