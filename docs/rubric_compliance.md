# Cumplimiento de la rúbrica

## Procedencia

Las indicaciones del proyecto final habían sido inspeccionadas y registradas
previamente en **docs/evidence_matrix.csv**, elemento C020. En la sesión actual
el PDF de la rúbrica no volvió a estar disponible en el workspace; por ello no
se reextrae ni se inventa contenido. Se conservan únicamente los requisitos ya
verificados:

- teoría;
- análisis;
- aplicación;
- código;
- notebook Colab;
- material extra;
- presentación de 15 minutos.

## Matriz de trazabilidad

| Criterio | Cómo se satisface | Evidencia principal | Gate |
|---|---|---|---|
| teoría | matching, caminos aumentantes, diferencia simétrica, Hopcroft-Karp y Hall | chapter_25_study_notes.md; chapter_25_project_mapping.md | conceptos y citas alineados con CLRS cap. 25 |
| análisis | formulación binaria, optimalidad, complejidad total, déficit y limitaciones | problem_formulation.md; methodology.md; limitations.md | cota inferior y superior coinciden; complejidad declarada |
| aplicación | capa entre GPC computable y futura síntesis clínica | project_report.md; literature_review.md | semántica U-V-E inequívoca y una sola GPC |
| código | baseline, Hopcroft-Karp, ejecución de compatibilidad y manifiesto | src; scripts; tests | tests, lint, tipado y concordancia |
| Colab | reproducción autónoma del caso \(7-8-14\) | notebooks/research_var_cases_kiss.ipynb | muestra \(|M^*|=7\), Hall y manifiesto |
| material extra | ficha y documentación científica | handout_kiss.md; validation_protocol.md; PDF de apoyo | una página legible y enlaces válidos |
| 15 minutos | nueve diapositivas y reserva de contingencia | presentation_outline.md; PPT | duración planeada 14:30 más 0:30 |

## Evidencia esperada por diapositiva

| Slide | Evidencia de rúbrica |
|---:|---|
| 1 | aplicación y pregunta |
| 2 | dos grafos, delimitación del objeto y testigos |
| 3 | formulación bipartita y restricciones uno-a-uno |
| 4 | caminos aumentantes y certificado de optimalidad |
| 5 | Hopcroft-Karp y complejidad |
| 6 | resultado, cotas y déficit de Hall |
| 7 | código, Colab, manifiesto y pruebas |
| 8 | aplicación, literatura y límites de inferencia |
| 9 | conclusión, límites y siguiente fase |

## Controles de calidad

- El término central es **estructura de caso clínico**.
- \(V\) contiene **variantes clínicas de ruta por representar**.
- Cada arista conserva witness_assignment.
- El resultado termina en assignment_manifest.json.
- El Corolario 25.4 sustenta optimalidad; Hall explica el déficit.
- La presentación no afirma validación clínica o generativa ya completada.
- El notebook y la diapositiva de resultados usan los mismos conteos.
- El tiempo total planeado no excede 15 minutos.

## Estado verificado

- `ruff format --check`: 66 archivos conformes;
- `ruff check`: sin incidencias;
- `mypy`: 66 archivos sin errores;
- `pytest`: 41 pruebas superadas y 7 omitidas porque requieren el snapshot
  clínico privado;
- notebook KISS: cinco celdas ejecutadas secuencialmente;
- PPT: nueve diapositivas sin desbordes y con fidelidad de plantilla;
- PDF: una página A4 renderizada e inspeccionada.

La cobertura de la rúbrica y los productos finales están sincronizados. La
revisión clínica experta y la validación generativa siguen pendientes por
diseño, no por un fallo del gate algorítmico.
