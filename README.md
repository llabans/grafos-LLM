# Siete casos, ocho objetivos

Versión KISS del proyecto final de algoritmos. Aplica **matching máximo en grafos
bipartitos** a una pregunta de diseño educativo derivada de una sola guía:

```text
gpc-05-hipertension-embarazo-2025
```

## Pregunta de investigación

> ¿Cómo asignar, uno a uno, escenarios clínico-educativos simulados compatibles
> a microobjetivos de aprendizaje sobre severidad para maximizar el número de
> microobjetivos cubiertos, sin reutilizar casos?

Versión oral: **tenemos siete casos y ocho objetivos; ¿cómo emparejarlos para
cubrir tantos objetivos diferentes como sea posible, usando cada caso una sola
vez?**

## El árbol que presentamos

El subgrafo KISS tiene:

```text
|U| = 7 casos simbólicos
|V| = 8 microobjetivos
|E| = 14 compatibilidades
|M*| = 7 pares
```

Cada caso representa uno de los siete criterios explícitos de severidad. Se
conecta con dos objetivos: reconocer su criterio específico y reconocer la
ruta/BPC común asociada a la presencia de severidad. Como un matching no puede
reutilizar vértices, siete casos solo pueden acreditar siete objetivos.

El testigo de Hall lo resume:

```text
|S| = 8 objetivos > |N(S)| = 7 casos compatibles
```

No es un error del algoritmo. Es una brecha de capacidad bajo la regla uno-a-uno.

## Qué significa “cubrir”

“Cubrir un microobjetivo” significa asignarle un caso compatible como
**representante principal**. No significa que:

- el estudiante haya aprendido;
- el caso sea clínicamente validado;
- un caso real solo pueda enseñar un objetivo;
- la cobertura sea sensibilidad, exactitud o beneficio clínico.

La unicidad es útil para construir un banco de fichas, estaciones o actividades
independientes sin doble conteo. Si un caso pudiera acreditar simultáneamente
varios objetivos, el modelo apropiado sería cobertura, *set cover* o
`b`-matching, no matching uno-a-uno.

## Ejecutar el demo autónomo

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/run_kiss_severity_case.py
```

Salida esperada:

```text
PASS |U|=7 |V|=8 |E|=14 |M*|=7
agreement dfs=7 hopcroft_karp=7
hall_witness |S|=8 |N(S)|=7 deficiency=1
```

El demo no necesita el ZIP privado. El pipeline completo permanece disponible
como anexo técnico y puede reproducirse configurando
`BIPARTITE_MINSA_SOURCE_ROOT`.

## Base algorítmica

La fuente curricular principal es el capítulo 25 de *Introduction to
Algorithms*, 4.ª edición (Cormen, Leiserson, Rivest y Stein, 2022). El proyecto
implementa desde cero:

- búsqueda por caminos aumentantes;
- Hopcroft-Karp con BFS por capas y DFS admisible;
- certificado de déficit de Hall;
- pruebas de invariantes, optimalidad y casos límite.

La cota clásica de Hopcroft-Karp es `O(E√V)`; el almacenamiento es `O(V+E)`.

## Estado científico, expresado sin exageración

El trabajo está:

- **validado algorítmicamente** mediante dos solvers propios, oráculos y pruebas;
- **fundamentado científicamente** por literatura sobre guías computables,
  grafos de guías y simulación clínica educativa;
- **pendiente de validación clínica de contenido y validación educativa** con
  expertos y estudiantes.

La revisión realizada no identificó, dentro de su alcance documentado, un
trabajo que una exactamente: GPC estructurada → escenarios trazables → grafo
bipartito caso-objetivo → matching máximo y testigo de Hall. Por eso la
contribución se presenta como una **combinación potencialmente novedosa**, no
como una prioridad universal demostrada.

## Entregables KISS

- `src/bipartite_minsa/kiss_case.py`: subgrafo autónomo.
- `tests/test_kiss_severity_case.py`: prueba explícita `7-8-14-7`.
- `data/samples/kiss_severity_graph.json`: artefacto pequeño y auditable.
- `notebooks/research_var_cases_kiss.ipynb`: Colab de la exposición.
- `docs/kiss_project_report.md`: informe principal.
- `docs/kiss_student_explanation.md`: explicación conceptual detallada.
- `docs/kiss_academic_validation.md`: validez y límites de las afirmaciones.
- `docs/literature_review.md`: mapa de literatura y brecha.
- `docs/validation_protocol.md`: protocolo para la siguiente fase empírica.
- `output/pdf/material_extra_KISS_research_var_cases.pdf`: ficha visual de una página.
- `scripts/build_kiss_handout.py`: generador reproducible de la ficha PDF.
- `outputs/proyecto_final_KISS_research_var_cases.pptx`: presentación.

El “bosque” técnico original —75 escenarios, 35 objetivos, 267 aristas y matching
33— se conserva en `docs/technical_appendix.md` y en la documentación original.

## GOAL y LOOP

**GOAL:** maximizar microobjetivos distintos representados por casos distintos,
con compatibilidad trazable y cero decisiones clínicas.

```text
DEFINIR → CONSTRUIR → RESOLVER → VERIFICAR → INTERPRETAR → REPETIR
```

## Límite de seguridad

Este repositorio no diagnostica, recomienda tratamientos, prioriza pacientes ni
evalúa resultados clínicos. Los casos son escenarios simbólicos para educación y
algoritmos. Una arista significa “compatibilidad demostrada bajo reglas
declaradas”; no significa “conducta médica correcta”.
