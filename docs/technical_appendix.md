# Anexo técnico: el bosque detrás del ejemplo KISS

La presentación principal preespecifica un subgrafo de severidad de
`7 casos × 8 objetivos`. La simplificación es narrativa, no una eliminación del
trabajo técnico. El pipeline completo permanece disponible para auditoría.

## Resultado completo conservado

```text
|U|=75 |V|=35 |E|=267 |M*|=33 cobertura=94,2857 %
```

Dos mecanismos explican los dos objetivos no cubiertos:

1. una brecha aislada de evidencia: `|S|=1>|N(S)|=0`;
2. el cuello de severidad usado en el cuerpo KISS: `|S|=8>|N(S)|=7`.

## Dónde auditar cada componente

| Componente | Documento o módulo |
|---|---|
| formulación matemática | `docs/problem_formulation.md` |
| método completo | `docs/methodology.md` |
| auditoría de fuentes | `docs/source_audit.md` |
| reconciliación Phase 4 | `docs/source_reconciliation.md` |
| semántica de flujogramas | `docs/flowchart_semantics_audit.md` |
| trazabilidad CLRS | `docs/chapter_25_project_mapping.md` |
| validación exhaustiva | `docs/academic_validation.md` |
| explicación extendida | `docs/student_explanation.md` |
| pipeline ejecutable | `src/bipartite_minsa/pipeline/` |
| solvers propios | `src/bipartite_minsa/matching/` |
| pruebas | `tests/` |

## Relación entre el árbol y el bosque

El subgrafo KISS no es un ejemplo inventado después de observar el resultado. Es
la componente inducida por:

- siete escenarios generados por la regla
  `rule:one_explicit_severity_criterion:v1`;
- siete objetivos de criterio de severidad;
- el objetivo `target:bpc:bpc_2` asociado a la ruta con severidad;
- las catorce aristas aprobadas por las reglas del pipeline completo.

Para que el demo sea ejecutable sin el snapshot privado, la rama incluye una
representación mínima con IDs pedagógicos equivalentes en
`data/samples/kiss_severity_graph.json`. Las pruebas verifican directamente
`7-8-14-7`.

## Por qué el anexo no domina la exposición

Los hashes, 689 grafos exhaustivos, benchmarks escalera, gates y reconciliación
son evidencia de rigor. Sin embargo, ninguno es necesario para comprender la
idea central durante quince minutos. Se conservan para preguntas, evaluación y
reproducibilidad.
